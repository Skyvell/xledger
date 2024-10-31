# Flexlink pointing to the Excel file containing the cost categories.
FLEX_LINK = "https://demo.xledger.net/Flex/112706068541888.xlsx?t=Ag9kybBKVZTLglyW4gzgmoIyryUcn76Oz5ieCO1o_gnYnGLIVOtkmB8bVSqKrULd-Hhd4rITYFAKWu6p7QUbfa6_GKWsZZsNSbtuEUoLLf0weijEe2UfCadAVFEcEZJOL5oWbnR0fwQAeuTM6igS2AIApYf6amezdOFaeA_SUR3l4ZEtMmG_Agse-4AGUx-d7HODI4g8A6rIrmiKx_QOjgAJEMBCO3TMvuvO1CwIMRYpWvEmZDRbmlePV5za1OziDHT10rBcfAxZQOIMCCpXz6tBB0JtDUjj1hT4dBKKnp2ndQq2Wo_QMoZwo2y3XVexsDLA4w9V3Oj84Fq92fSd"

# Only include these columns in the Parquet file.
COLUMNS = [
    "Owner",
    "Code",
    "Level No",
    "Description",
    "Level Parent",
    "Allow Posting",
    "Created",
    "Modified",
    "Leaf Node"
]

# Define the pandas data types for each column.
COLUMN_DATA_TYPES = [
    "string",
    "string",
    "int64",
    "string",
    "string",
    "bool",
    "string",
    "string",
    "bool"
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))