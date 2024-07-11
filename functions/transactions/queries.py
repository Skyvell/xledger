from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
TRANSACTION_NODE_FIELDS = """
    dbId
    owner {
      description
    }
    account {
      accountGroup {
        description
        codeTranslated
      }
      sysAccount {
        description
        codeTranslated
      }
      descriptionTranslated
      code
    }
    company {
      description
      address {
        fullAddress
      }
    }
    glDimension {
      glObject1 {
        description
        objectKind {
          name
        }
      }
      glObject2 {
        description
        code
        objectKind {
          name
        }
      }
    }
    currency {
      code
    }
    invoiceAmount
    taxRule {
      description
      code
    }
    taxAmount
"""


# This is the final list of columns that we want in the pandas dataframe,
# and the resulting parquet file.
# Derived directly from the TRANSACTION_NODE_FIELDS above to make sure the columns
# Are deterministic and up-to date.
COLUMNS = flatten_graphql_fields(TRANSACTION_NODE_FIELDS)


GET_TRANSACTIONS_FROM_DBIDS = gql(f"""
    query getTransactions($first: Int, $after: String, $dbIdList: [Int!]) {{
        transactions(
            first: $first,
            after: $after, 
            filter: {{ 
                dbId_in: $dbIdList
            }}
        ) {{
            edges {{
                node {{
                    {TRANSACTION_NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_TRANSACTIONS_AFTER_CURSOR = gql(f"""
    query getTransactions($first: Int, $after: String) {{
        transactions(
            first: $first,
            after: $after
        ) {{
            edges {{
                node {{
                    {TRANSACTION_NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_TRANSACTION_DELTAS = gql("""
    query getTransactionDeltas($first: Int, $last: Int, $after: String) {
        transaction_deltas(
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