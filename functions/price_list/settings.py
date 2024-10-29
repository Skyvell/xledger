# Flexlink pointing to the Excel file containing the cost categories.
FLEX_LINK = "https://demo.xledger.net/Flex/112706068539122.xlsx?t=Ag9kyZPdVr0iQZZBICYGD1qmvQcE6Rz28Kne5851t-w4DQIsJi4ngKNh_Oj9xUf92g7EimKBub07waAvCKic_EXMbGiaZ7o-7f8cReVv5xJfZFmJ6Rbh0pXZLY-Tm68D247JxxDd9wxuII7PeU9r908S3soTmzDdGeKYBkOtyXZvg4uYhFjbTgb0Ua2r_A1uIByuaVT_38QaJSIx6-g4G7zaQViTJiMwXJpXJIy_H5ABxb_YKxKQ3kNfChOlq56gNdRJeybgMkH93AdWVglYKG3Tvyh6mmqjViYrSMnZPByqsxhX5xlYwIjF59BrcfKWW9raDF9y-n4XZWDJVpv-"

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