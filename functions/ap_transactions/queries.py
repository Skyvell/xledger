from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
AP_TRANSACTIONS_NODE_FIELDS = """
    dbId
    description
"""


# This is the final list of columns that we want in the pandas dataframe,
# and the resulting parquet file.
# Derived directly from the AP_TRANSACTIONS_NODE_FIELDS above to make sure the columns
# Are deterministic and up-to date.
COLUMNS = flatten_graphql_fields(AP_TRANSACTIONS_NODE_FIELDS)


GET_AP_TRANSACTIONS_FROM_DBIDS = gql(f"""
    query getApTransactions($first: Int, $after: String, $dbIdList: [Int64String!]) {{
        apTransactions(
            first: $first,
            after: $after, 
            filter: {{ 
                dbId_in: $dbIdList
            }}
        ) {{
            edges {{
                node {{
                    {AP_TRANSACTIONS_NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_AP_TRANSACTIONS_AFTER_CURSOR = gql(f"""
    query getApTransactions($first: Int, $after: String) {{
        apTransactions(
            first: $first,
            after: $after
        ) {{
            edges {{
                node {{
                    {AP_TRANSACTIONS_NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_AP_TRANSACTION_DELTAS = gql("""
    query getApTransactionDeltas($first: Int, $last: Int, $after: String) {
        arTransaction_deltas(
            first: $first,
            last: $last, 
            after: $after
        ) {
            edges {
                node {
                    dbId
                    mutationType
                }
                cursor
            }
            pageInfo {
                hasNextPage
            }
        }
    }
""")