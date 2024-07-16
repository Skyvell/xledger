from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Name of the queries.
ITEMS_QUERY_NAME = "apTransactions"
DELTAS_QUERY_NAME = "apTransaction_deltas"


# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
NODE_FIELDS = """
    dbId
    owner {
      description
    }
    company {
      description
      phone
      email
      address {
        streetAddress
        zipCode
        place
        fullAddress
      }
    }
    billAddress {
      streetAddress
      zipCode
      place
      fullAddress
    }
    account {
      description
      code
      descriptionTranslated
    }
    slTransactionType {
      name
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
    ledgerType {
      name
    }
    invoiceNumber
    period {
      description
      fiscalYear
    }
    invoiceDate
    dueDate
    paymentDate
    currency {
      code
    }
    exchangeRate
    invoiceAmount
    invoiceRemaining
"""


# This is the final list of columns that we want in the pandas dataframe,
# and the resulting parquet file.
# Derived directly from the NODE_FIELDS above to make sure the columns
# Are deterministic and up-to date.
COLUMNS = flatten_graphql_fields(NODE_FIELDS)


GET_ITEMS_FROM_DBIDS = gql(f"""
    query get_{ITEMS_QUERY_NAME}($first: Int, $after: String, $dbIdList: [Int!]) {{
        {ITEMS_QUERY_NAME}(
            first: $first,
            after: $after, 
            filter: {{ 
                dbId_in: $dbIdList
            }}
        ) {{
            edges {{
                node {{
                    {NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_ITEMS_AFTER_CURSOR = gql(f"""
    query get_{ITEMS_QUERY_NAME}($first: Int, $after: String) {{
        {ITEMS_QUERY_NAME}(
            first: $first,
            after: $after
        ) {{
            edges {{
                node {{
                    {NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_DELTAS = gql(f"""
    query get_{DELTAS_QUERY_NAME}($first: Int, $last: Int, $after: String) {{
        {DELTAS_QUERY_NAME}(
            first: $first,
            last: $last, 
            after: $after
        ) {{
            edges {{
                node {{
                    dbId
                    mutationType
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")