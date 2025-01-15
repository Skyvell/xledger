# Only include these columns in the Parquet file.
COLUMNS = [
    "Owner",
    "Account",
    "Cost Center",
    "Period",
    "Amount"
]

# Define the pandas data types for each column.
COLUMN_DATA_TYPES = [
    "string",
    "string",
    "string",
    "string",
    "float64"
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))