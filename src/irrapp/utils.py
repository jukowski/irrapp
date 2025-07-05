from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from graphql import (
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLInputObjectType,
    GraphQLField,
    GraphQLList,
    GraphQLString,
    GraphQLInt,
    GraphQLFloat,
    GraphQLBoolean,
)

def get_catalog(project_path):
    bootstrap_project(project_path)
    return KedroSession.create(project_path).load_context().catalog

def load_sql(conn, catalog, name):
    return conn.read_parquet(str(catalog._datasets[name]._filepath))

def map_dtype_to_graphql(dtype) -> GraphQLField:
    dtype_str = str(dtype).lower()
    if "int" in dtype_str:
        return GraphQLInt
    elif "float" in dtype_str:
        return GraphQLFloat
    elif "bool" in dtype_str:
        return GraphQLBoolean
    elif "object" in dtype_str or "string" in dtype_str:
        return GraphQLString
    else:
        return GraphQLString  # fallback
    
def generate_fields(duck_relation):
    return {
        col: map_dtype_to_graphql(dtype)
        for col, dtype in zip(duck_relation.columns, duck_relation.dtypes)
    }

def generate_output_type(df, name):
    return GraphQLObjectType(
        name=name,
        fields=lambda: generate_fields(df),
    )

def get_requested_fields(info):
    field_nodes = info.field_nodes
    selection = field_nodes[0].selection_set.selections
    return [field.name.value for field in selection]


def generate_input_type(df, name):
    return GraphQLInputObjectType(
        name=name,
        fields=lambda: generate_fields(df),
    )