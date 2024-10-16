# Flexlink pointing to the Excel file containing the cost categories.
FLEX_LINK = "https://www.xledger.net/Flex/112706068021943.xlsx?t=Ag9kyal4mPoU7PaOxEKofb3x_cJEjUXJ8ayFBBmmIxTF8dkAi1EJRMPFgGsJavbMf7_C0ALtoT_ku-E8dhBzatOGM1SmzxxsSD2amPHQN26scKgvG2zQUehALQjNK13HzsM9ET0x1mDr8_-9u-ytP6z5Ishsxa5x-Qr-169tLQhEn6Y21JBc2tz-PImu1Tm_ialiGIC4j3tkKWyy54ZaovCzYV-J0QMX1aLKTBNENnCwKgGYMb6PynxCsVCC8fHttjoU9fcuEuPbO4QJivXcn5jj8c1TQvVIx9wlJWpVGkpQOSNI2bLUYfET4BjqN2nFC8Ya1SHPaoBC1IP6yzSr"

# Only include these columns in the Parquet file.
COLUMNS = [
    "Time Type",
    "Project Cost Element",
    "Cost Factor",
    "Created",
    "Modified"
]

# Define the pandas data types for each column.
COLUMN_DATA_TYPES = [
    "string",
    "string",
    "float64",
    "string",
    "string"
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))