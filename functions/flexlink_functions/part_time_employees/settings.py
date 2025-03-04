# Only include these columns in the Parquet file.
COLUMNS = [
    "Owner",
    "Employee #",
    "Work Schedule #",
    "Employee Name",
    "Work Schedule Name",
    "Date From",
    "Date To"
]

# Define the pandas data types for each column.
COLUMN_DATA_TYPES = [
    "string",
    "Int64",
    "string",
    "string",
    "string",
    "string",
    "string"
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))