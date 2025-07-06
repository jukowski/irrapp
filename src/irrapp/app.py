from ariadne.asgi import GraphQL
from irrapp.utils import get_catalog
from irrapp.object_registry import ObjectRegistry
import duckdb


conn = duckdb.connect(":memory:")
catalog = get_catalog("/home/juko/irrapp")

reg = ObjectRegistry(conn, catalog)
reg.register_type("Customer", "Customer", mutable=True)
reg.register_type("Invoice", "Invoice")

reg.add_edge("Query", "customer", "Customer")
reg.add_edge("Query", "invoice", "Invoice")

reg.add_edge("Invoice", "customer", "Customer")
reg.add_edge("Customer", "invoices", "Invoice")

app = GraphQL(schema=reg.generate_schema())
