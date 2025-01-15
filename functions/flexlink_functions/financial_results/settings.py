# Only include these columns in the Parquet file.
COLUMNS = [
    "Owner",
    "Account Name",
    "Account #",
    "Cost Center Name",
    "Cost Center #",
    "Period",
    "Amount in USD",
    "Amount in SEK"
]

# Define the pandas data types for each column.
COLUMN_DATA_TYPES = [
    "string",
    "string",
    "Int64",
    "string",
    "Int64",
    "string",
    "float64",
    "float64"
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))