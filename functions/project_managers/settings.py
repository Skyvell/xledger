# Flexlink pointing to the Excel file containing the project managers and which project they manage.
FLEX_LINK = "https://demo.xledger.net/Flex/112706068542837.xlsx?t=Ag9kyZhdm_d5xaTsEosgJ-iKBvolMxj-k6LEpOR1bIOsmvL0qQyg1SdIHuhjKzLf7ybu5cj8qFfRv3s2AXpMayR9-e7B5Gk2p84rczhhIgzEjf0nS5wrmwlxb-51yJIX7ZkS4kWlwKGjc59beJbJTLJVcdDKYyKd8n6MfHgLgZ5X5WzrTbHJ3UYBX6CoqcxeOYqG3t_sTWSVxRxL-8OlnnusOSQ1_JTkksXVw3mPeOF8UGvhjQUT6GpUaC3zs3KBxhol8ABgQNoG1GY6V2l_jEImMq5rM5jvXCSVQcdXEczKbIUEbQ-7xx1FBqFxGefS317Ylsi9OYUT8HmKpKls"

# Only include these columns in the Parquet file.
COLUMNS = [
    "User",
    "Project",
    "Created",
    "Modified"
]

# Define the pandas data types for each column.
COLUMN_DATA_TYPES = [
    "string",
    "string",
    "string",
    "string"
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))