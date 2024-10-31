# Flexlink pointing to the Excel file containing the cost categories.
FLEX_LINK = "https://demo.xledger.net/Flex/112706068021943.xlsx?t=Ag9kyfFfNodF_07SNLGT-5wBphRYDOCGXYyzvH9P181e3CIYRQuXOzU7uRuNxKOv4iEvkHFXMhS1VkLH-OSpgbv2sQTau5f-lC0BOKoMRXrmY9jFVMgbFJdOseR6ry_w4AkflLC4UOAftPoLolGAXQprQz8Stov_BkshhKzA1ONsskhGXJGBSMqy4dNUU-UJ0P_ZbJI7lPivUyt_SWAsoJamiROAKek3NVkWyVVgOabx_LlQYqsPemwd9HOuyV5-NC5fbuQJud9kULwwc-GJExckbPaYCUYHsGm_e0kO1ob7sye21R1KJ4ziWtlt-3bpzaQE_cIvzPYU_Le5uFE-"

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