# %%
from irrapp.utils import get_catalog, load_sql, generate_output_type, generate_input_type
import duckdb
import pandas as pd
# %%
catalog = get_catalog("/home/juko/irrapp")

# %%
catalog.load("Invoice")
catalog.load("Customer")

# %%
conn = duckdb.connect(":memory:")
# %%
df = load_sql(conn, catalog, "processors")
# %%
pfields = generate_input_type(df, "ProcessorsFilter")

