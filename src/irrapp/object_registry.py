from graphql import GraphQLField, GraphQLObjectType, GraphQLList, GraphQLSchema, \
                    GraphQLInputObjectType, GraphQLArgument, GraphQLInt, GraphQLString, GraphQLInputField
from irrapp.utils import get_catalog, generate_output_type, get_requested_fields, load_sql, generate_fields

class ObjectRegistry:
    """
    A registry for managing DuckDB relationships as GraphQL objects with traversable edges.
    
    This class allows you to:
    1. Register multiple DuckDB relationships as GraphQL objects
    2. Define edges between objects to enable traversal from one relationship to another
    3. Generate a complete GraphQL schema with proper type definitions
    
    The registry maintains separate collections for output types (for queries), input types 
    (for filtering), and edges (for defining relationships between objects).
    
    Example usage:
        conn = duckdb.connect(":memory:")
        catalog = get_catalog("/path/to/catalog")
        
        registry = ObjectRegistry(conn, catalog)
        
        # Register DuckDB relationships as GraphQL objects
        registry.register_type("Customer", "Customer")
        registry.register_type("Invoice", "Invoice")
        registry.register_type("InvoiceItem", "InvoiceItem")
        
        # Add edges to define how to traverse between objects
        registry.add_edge("Query", "customers", "Customer")
        registry.add_edge("Customer", "invoices", "Invoice")
        registry.add_edge("Invoice", "items", "InvoiceItem")
        
        # Generate the final GraphQL schema
        schema = registry.generate_schema()
    """
    
    def __init__(self, conn, catalog):
        """
        Initialize the ObjectRegistry.
        
        Args:
            conn: DuckDB connection object
            catalog: Data catalog containing table definitions
        """
        self.output_types = {
            "Query": {},
        }
        self.input_types = set()
        self.count_types = set()

        self.edges = {}
        self.conn = conn
        self.catalog = catalog
        self.graphql_types = {}

    def add_edge(self, input_type, name, output_type, join_on=None):
        """
        Add an edge between two types to enable traversal in the GraphQL schema.
        
        This method defines how you can navigate from one DuckDB relationship to another.
        For example, you can traverse from a Customer to their Invoices, or from an 
        Invoice to its Items.
        
        Args:
            input_type (str): The source type name (e.g., "Customer", "Query")
            name (str): The field name for the edge (e.g., "invoices", "customers")
            output_type (str): The target type name (e.g., "Invoice", "Customer")
            join_on (dict, optional): Column mapping for joining. Keys are source columns, 
                                    values are target columns. If None, uses common column names.
            
        Example:
            # Allow querying customers from the root Query type
            registry.add_edge("Query", "customers", "Customer")
            
            # Allow traversing from Customer to their invoices with explicit join columns
            registry.add_edge("Customer", "invoices", "Invoice", {"customer_id": "customer_id"})
            
            # Allow traversing using common column names (auto-detected)
            registry.add_edge("Customer", "invoices", "Invoice")
        """
        if input_type not in self.edges:
            self.edges[input_type] = []
        if join_on == None:
            join_on = self.get_common_columns(input_type, output_type)

        self.edges[input_type].append({
            "name": name,
            "output_type": output_type,
            "join_on": join_on
        })

    def get_common_columns(self, source_type, target_type):
        """Find common column names between two types."""
        source_fields = set(self.output_types.get(source_type, {}).keys())
        target_fields = set(self.output_types.get(target_type, {}).keys())
        common = source_fields & target_fields
        return {col: col for col in common}

    def generate_edge_resolver(self, edge):
        def _resolver(obj, info, filter={}, offset=0, limit=100):
            target_type = edge["output_type"]
            
            # Load the target relation
            relation = load_sql(self.conn, self.catalog, target_type)
            
            # apply join conditions
            for (source_col, target_col) in edge.get("join_on", {}).items():
                relation = relation.filter(f"{target_col} = '{obj[source_col]}'")

            # Apply filtering logic based on filter arguments
            for field_name, field_value in filter.items():
                if field_value is not None:
                    relation = relation.filter(f"{field_name} = '{field_value}'")

            # Get requested fields and return matching records
            requested_fields = get_requested_fields(info)
            raw_fields = list(set(requested_fields) & set(relation.columns))   
            
            if "_distinct_" in requested_fields:
                # Get the distinct count fields from the _distinct_ selection
                distinct_fields = []
                for field_node in info.field_nodes:
                    for selection in field_node.selection_set.selections:
                        if selection.name.value == "_distinct_":
                            distinct_fields = [sub_selection.name.value for sub_selection in selection.selection_set.selections]
                            break
                
                distinct_fields = list(set(distinct_fields) & set(relation.columns))   

                # Build count distinct query for each requested field
                count_queries = []
                for field in distinct_fields:
                    count_queries.append(f"COUNT(DISTINCT {field}) as _distinct___{field}")
                # Execute count distinct aggregation
                relation = relation.aggregate(", ".join(raw_fields + count_queries), ", ".join(raw_fields))
            else:
                relation = relation.select(*raw_fields)

            # Apply limit if provided
            if limit>0:
                relation = relation.limit(limit, offset)

            results = relation.to_df().to_dict(orient="records")
            
            # Restructure results to move _distinct___ fields into nested _distinct_ dictionary
            for record in results:
                distinct_data = {}
                keys_to_remove = []
                
                for key, value in record.items():
                    if key.startswith("_distinct___"):
                        field_name = key[len("_distinct___"):]
                        distinct_data[field_name] = value
                        keys_to_remove.append(key)
                
                # Remove the original _distinct___ keys and add nested _distinct_ dict
                for key in keys_to_remove:
                    del record[key]
                
                if distinct_data:
                    record["_distinct_"] = distinct_data
            
            return results
        
        return _resolver

    def register_type(self, type_name, table):
        """
        Register a DuckDB relationship as a GraphQL object type.
        
        This method takes a table/relationship from your DuckDB catalog and creates
        both output and input types for the GraphQL schema. The output type is used
        for query results, while the input type (with "Filter" suffix) is used for
        filtering operations.
        
        Args:
            type_name (str): The name to use for the GraphQL type (e.g., "Customer")
            table (str): The table name in the catalog (e.g., "Customer")
            
        Example:
            # Register the Customer table as a Customer GraphQL type
            registry.register_type("Customer", "Customer")
            
            # Register with mutations enabled
            registry.register_type("Customer", "Customer", mutable=True)
            
            # This creates:
            # - Customer type for query results
            # - CustomerFilter type for filtering
        """
        relation = load_sql(self.conn, self.catalog, table)
        table_fields = generate_fields(relation)
        self.output_types[type_name] = table_fields.copy()
        
        self.input_types.add(f"{type_name}Filter") 
        self.graphql_types[f"{type_name}Filter"] = GraphQLInputObjectType(
                name=f"{type_name}Filter",
                fields=table_fields
            )
        
        self.count_types.add(f"{type_name}Counts")
        self.graphql_types[f"{type_name}Counts"] = GraphQLObjectType(
                name=f"{type_name}Counts",
                fields=dict([(fld, GraphQLInt) for fld in table_fields.keys()])
            )
            
    def lazy_generate(self, type_name):
        def _generate():
            fields = self.output_types[type_name].copy()
            if type_name != "Query":
                fields["_distinct_"] = GraphQLField(type_=self.graphql_types[f"{type_name}Counts"])
            # Add edge fields
            for edge in self.edges.get(type_name, []):
                field_name = edge["name"]
                target_type = edge.get("output_type")
                fields[field_name] = GraphQLField(
                    type_=GraphQLList(self.graphql_types[target_type]),
                    args={
                        "filter": GraphQLArgument(self.graphql_types[f"{target_type}Filter"]),
                        "limit": GraphQLArgument(GraphQLInt),
                        "offset": GraphQLArgument(GraphQLInt),
                    },
                    resolve=self.generate_edge_resolver(edge)
                )
            return fields

        return _generate 

    def generate_schema(self):
        """
        Generate the complete GraphQL schema from registered types and edges.
        
        This method builds the final GraphQL schema by combining all registered
        types and their defined edges. It creates the necessary GraphQL object
        types and wires them together according to the edge definitions.
        
        Returns:
            GraphQLSchema: The complete GraphQL schema ready for use
            
        Example:
            schema = registry.generate_schema()
            app = GraphQL(schema=schema)
        """    

        for type_name, fields in self.output_types.items():
            self.graphql_types[type_name] = GraphQLObjectType(
                name=type_name,
                fields=self.lazy_generate(type_name)  # Use lambda for lazy evaluation
            )

        return GraphQLSchema(query=self.graphql_types["Query"])

