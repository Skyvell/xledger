# Flexlink pointing to the Excel file containing the cost categories.
FLEX_LINK = "https://demo.xledger.net/Flex/112706068542803.xlsx?t=Ag9kyWRzmQIx1lQSlIdPv4ZFMUOF8t77zf83uyHSZ5_ylYq5UD5hFx-2T8WlBGi1P1zwuQAo4f56XNlV4N-x1LVUmXDJbLbQOjtS0A5ijY7QHubJfPW8Xy-i9H-2m8r5wQfPrgWt0zNUh3YXbSq_K3_SdkazR_HJZaxn3uMoQcebyOEj9ycZQ9J9cqWsTfQ_vV9EI2HEw6-6kfAdumvZYvjqXdX-STs-r_lx9nPO-fU1tLRG6CPbtkHhSPmfLyjJ2-hhrXwuvzsIJMgEnThpqwZ0q_TU54LgwVW0-oGeRHsoAMTsjdUeXUUcBYxmaeiH8v1e70saHlOK-9rmdlgb"

# Only include these columns in the Parquet file.
COLUMNS = [
    "Owner",
    "Code",
    "Description",
    "Created",
    "Modified"
]

# Define the pandas data types for each column.
COLUMN_DATA_TYPES = [
    "string",
    "string",
    "string",
    "string",
    "string"
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))