# Flexlink pointing to the Excel file containing the cost categories.
FLEX_LINK = "https://demo.xledger.net/Flex/112706068539122.xlsx?t=Ag9kycMmAtgCg3WGLB3FZWp0cW4Kqu1itaKyv1qeU86SKgrN5kUiIjYxY6KwtkaWcJGB3XqI3vWCAt1nqhKR6x9vrHLL6rHIlnEZUr2I0q5ZnKT44B_hM0yAiDv8EYe5g2dY0IFIbOe6Qdd8HCERYO8C3mbQo_U_nVNlDvrRpa_by_A5D8FwPUGd37JSZOIHR6RSXWHCJ_9f_ihMCLEniGHrQwJzzm1jlhABX5hlj_0Tifx-Nfq_8aNFWHYR8G4MMfERRber5WPVyZooW88DtLI4yD2eKRzyg1owGiHI6c4SEOPpVJrdWAiPjuvMXca_4PatqNnT3E2KU9B9xwtz"

# Only include these columns in the Parquet file.
COLUMNS = [
    "Pricelist",
    "Product",
    "Product Group",
    "Project",
    "Object",
    "Object Value",
    "Date From",
    "Date To",
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
    "string",
    "string",
    "float64",
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))