# Flexlink pointing to the Excel file containing the cost categories.
FLEX_LINK = "https://demo.xledger.net/Flex/112706066962741.xlsx?t=Ag9kyfjyDCWFDKEtNMi92oo2wSof7u9VUytkzyd3UT3nmFMbqalbaRT8IE4xdEZcBkmsZZCMsG3c4Zrk-qoynIhccOCU_p-7yK2a4OUUgeK69jkTgPpgDH5NcJHQxJ48HEpqy5c4sZdCSFT88G4Zz5MTkS9FnrSvKM7kDbLCeD0D212bHllRPjsJK0jF5i11brRM81URp7wtb9SDf2CMMmtAc450_xaSoyzTh9ojkgTbmwETx_yct0aEKd-KKI-bYii9xvAvDCD5f6NjzWysunOOcItL4oGuZTGPbFfTpVJwtoP-x7jhLSIlN6hs07aQuHGZKIUz849u6PUeLJUZ"

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
    "datetime64[ns]",
    "string",
    "float64"
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))