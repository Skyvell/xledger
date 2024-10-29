# Flexlink pointing to the Excel file containing the cost categories.
FLEX_LINK = "https://demo.xledger.net/Flex/112706068539122.xlsx?t=Ag9kyQ8yb9hkFr9HxgcatsLmIFrxZAiRUMEIYXnHnSozlTE3dzUvbnKa4ab33B0exDIND9OIoXYHzvgjXWfms1HJL_Nc-kJIvaqoKe6AEINnWmESBU9bKUnJiDG7NP4Zql_mrAK2en-Xe_yN9au2xkKklMfFu3IyRUGJWgeGSNJSgwicHAvVzRMlNi1yVaXCuAqSxhu4o5xbOs9xLmYUBfcjvzI27cNDoBpnUvwRB4qDiC02Kw6_coFm6jUoaG9nlnLez9lwOlbXjyCdBUbOOLBNxPutvhiIQG2x7yCIGe8l3ujVCPqZQ5RSERe62sxRRUaawdR5rPNEEcLaVoCs"

# Only include these columns in the Parquet file.
COLUMNS = [
    "Pricelist",
    "Product",
    "Project",
    "Object",
    "Object Value",
    "Date From",
    "Unit",
    "Cur",
    "Price",
]

# Define the pandas data types for each column.
COLUMN_DATA_TYPES = [
    "string",
    "string",
    "string",
    "string",
    "string",
    "string",
    "string",
    "string",
    "float64",
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))