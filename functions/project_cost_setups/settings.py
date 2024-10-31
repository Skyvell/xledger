# Flexlink pointing to the Excel file containing the cost categories.
FLEX_LINK = "https://demo.xledger.net/Flex/112706068542829.xlsx?t=Ag9kydqsOHc42AQ1WcBtjFEb-Lib_-wMeX_ZGVn6BqoQQ5VnLmE7dBITndxam2rj-zrS28DIOS8b-YTz2CDrtH91zH7SR6gSp_o4rpguCHN7YdAvzSSw7nqtrijsu58TEZ2HTUCkwJX2-awLhddkforioUR8oFZag-JxUlBOXssCOMGOTXrIvEfyaRJKgjTC4JChsZUb9fGNhW6veb6dvJ7kpyGU6Y-wqMBLjmLzJSFXkTt_Pqj7OdPMA8_dtChQNHDC9kZthG0_E0aNWcqSwkx4bzJhahY1LffBhPtcUqYWjIVOJT1GCZKgREF4V8nf5mpqWv3lt6SYvggXsn38"

# Only include these columns in the Parquet file.
COLUMNS = [
    "Object",
    "Object Value",
    "Cost Element",
    "Date From",
    "Cur",
    "Rate"
]

# Define the pandas data types for each column.
COLUMN_DATA_TYPES = [
    "string",
    "string",
    "string",
    "string",
    "string",
    "float64"
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))