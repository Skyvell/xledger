# Flexlink pointing to the Excel file containing the cost categories.
FLEX_LINK = "https://demo.xledger.net/Flex/112706068543188.xlsx?t=Ag9kyVsm_dnYjkIQWMqdCPsvDdxuZTYFJGuwVheyB_gOzGdDefB2ig3T_k6iEEdpDTZSrcWSPpGQ_9uTTXLDXu6eY1aLJ3rFTv2eIfRxbq9Av8rmej1rHZfIEhPMAJKGg84dVHaFkPKLe00RXYfmFfo1coLH0EpeYO-bkh3HLtun_OjRZs5rMRiVWVF8lH7gL9kgkRR8FLs3xkN_oZl-ch73mKJo10QtV60YwwGcGoiItUAtuVTvNoJsWm1EwSpkekpTbNPx_v4oZjSdVh1vQ2jbr07TNAZTlSmEV8TA8PmXKi9xMAr1VCv3aZdYN2dNO--ClmP__oxqt4zPwBzq"

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