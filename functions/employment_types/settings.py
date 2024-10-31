# Flexlink pointing to the Excel file containing the cost categories.
FLEX_LINK = "https://demo.xledger.net/Flex/112706068543198.xlsx?t=Ag9kyf0fG3TXjNxQyTppQ_xNfPPVMME8srJ7XDfNHhLZRdjG2UpfkwTVpAnjx0XeSUsFr3qI5pF5DtPubRAS4sA9w0CP-HC4m6CXvOGpZjA9EvQKMBBC1vUPwB9ry8jWRZV8E9mMHL-EAQtiGdKVX6v7hG2H2Dm6Z6XROc_lfM3RVIr0dCv1p4zgrrhS8JnxwgLDb87jYb7mbE76B1cLLjuzDvaqiF6yAcPZ2wF6nkI2a8FiFwV7xkCM3pBUq9CE5eAcSGGBMlufq4zLdyvIaQG8qtIbcL386YbKpbOT6t4FyAiHHmBAwcoFX_agqKpIS8poeenflEMF6PoK3-Pg"

# Only include these columns in the Parquet file.
COLUMNS = [
    "Owner",
    "Code",
    "Description"
]

# Define the pandas data types for each column.
COLUMN_DATA_TYPES = [
    "string",
    "Int64",
    "string"
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))