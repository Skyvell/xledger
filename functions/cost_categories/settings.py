# Flexlink pointing to the Excel file containing the cost categories.
FLEXLINK = "https://demo.xledger.net/Flex/112706066960924.xlsx?t=Ag9kyeRaNrajDAdVN-yO371sV0PiVRIO_gwW9-OGTDebjFLLcEK5wzPh90enehKTiekbP4i7tKinC3TZJb3EU3OjfiYvNf_oI-DV1OUHR6qZmyw0ZAV96mWLoJ3Y3HRd3sAr4scGXNuzpThaBBQiNhYvTJHtqzasZOW2vYFaiK_68ot2VAmQL7dSB9p-51PIOb4YnIAjbMydiBu-PEa2YfV-eIfR3X1zzai9K_GLFR-gmyUmWzt5ddjmDXiDXn41dApzxEIKvROP3WAlf5_BDw717ygLXX0EcskyBQPnPGncvQhuF2CtOO2v86tsQLFWMsV61PeD4k5vR9MReBsd"

# Only include these columns in the Parquet file.
COLUMNS = [
    "Owner",
    "Code",
    "Description",
    "Created",
    "Modified"
]

# Define the pandas data types for each column.
COLUMN_DATA_TYPES = [
    "string",
    "string",
    "string",
    "datetime64[ns]",
    "datetime64[ns]"
]

# Create a dictionary mapping columns to their data types.
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))