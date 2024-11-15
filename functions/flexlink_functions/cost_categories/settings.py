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