# Flexlink pointing to the Excel file containing the project managers and which project they manage.
FLEX_LINK = "https://demo.xledger.net/Flex/112706067815138.xlsx?t=Ag9kyY2qF_T7Nfvhzk_yr0OipSRp0euiA1QSv_RjAa2z8AzeYf0-iTE4PODb3IQ4C8g2WkYhClZFERq3cG0rWwAJ841jiIyT3_RsoDUixvR5I8rHEnL8cCiec-4OiLawNv2tWmvOnnThOx8ZZUFdkX5iCCg-WZW3xpSWMoS6T3cX3WOtSFD_LRIF3VMQ_fDFNNvi6DHbiDtYpfLEsTE8q3x9hhBXlseNOfa-HPs7itjhyi_yvBHWtnxDZnMIn61JY_q99ugvEUV3tdEXzvVyq9HRGhVaMsRGdXCm7lA4IuIZh5t5Gl5iX-hDAr0cjFqJ21yqdQ-I2oT4RtCgll1I"

# Only include these columns in the Parquet file.
COLUMNS = [
    "User",
    "Project"
]

# Define the pandas data types for each column.
COLUMN_DATA_TYPES = [
    "string",
    "string"
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))