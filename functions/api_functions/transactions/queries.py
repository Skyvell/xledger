from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Name of the queries.
ITEMS_QUERY_NAME = "transactions"
DELTAS_QUERY_NAME = "transaction_deltas"

# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
NODE_FIELDS = """
    dbId
    text
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
      description
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
        code
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
    amount
    invoiceAmount
    taxRule {
      description
      code
    }
    taxAmount
    header {
      postedDate
      trProcessLevel {
        name
      }
      transactionSource {
        description
        code
      }
      trRegNumber
      transactionNumber
    }
    period {
      description
      fromDate
      toDate  
      monthNumber
    }
"""

# Datatypes of the columns in the resulting pandas dataframe.
COLUMN_DATA_TYPES = [
    'Int64',            # dbId
    'string',           # text
    'string',           # owner.description
    'string',           # account.accountGroup.description
    'string',           # account.accountGroup.codeTranslated
    'string',           # account.sysAccount.description
    'string',           # account.sysAccount.codeTranslated
    'string',           # account.description
    'string',           # account.descriptionTranslated
    'string',           # account.code
    'string',           # company.description
    'string',           # company.address.fullAddress
    'string',           # glDimension.glObject1.description
    'string',           # glDimension.glObject1.code
    'string',           # glDimension.glObject1.objectKind.name
    'string',           # glDimension.glObject2.description
    'string',           # glDimension.glObject2.code
    'string',           # glDimension.glObject2.objectKind.name
    'string',           # currency.code
    'float64',          # amount
    'float64',          # invoiceAmount
    'string',           # taxRule.description
    'string',           # taxRule.code
    'float64',          # taxAmount
    'string',           # header.postedDate
    'string',           # header.trProcessLevel.name
    'string',           # header.transactionSource.description
    'string',           # header.transactionSource.code
    'Int64',            # header.trRegNumber
    'Int64',            # header.transactionNumber
    'string',           # period.description
    'string',           # period.fromDate
    'string',           # period.toDate
    'Int64'             # period.monthNumber
]



# This is the final list of columns that we want in the pandas dataframe,
# and the resulting parquet file.
# Derived directly from the NODE_FIELDS above to make sure the columns
# Are deterministic and up-to date.
COLUMNS = flatten_graphql_fields(NODE_FIELDS)
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))


GET_ITEMS_FROM_DBIDS = gql(f"""
    query get_{ITEMS_QUERY_NAME}($first: Int, $after: String, $ownerSet: OwnerSet, $dbIdList: [Int64String!]) {{
        {ITEMS_QUERY_NAME}(
            first: $first,
            after: $after,
            ownerSet: $ownerSet
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
    query get_{ITEMS_QUERY_NAME}($first: Int, $after: String, $ownerSet: OwnerSet) {{
        {ITEMS_QUERY_NAME}(
            first: $first,
            after: $after,
            ownerSet: $ownerSet
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
    query get_{DELTAS_QUERY_NAME}($first: Int, $last: Int, $after: String, $ownerSet: OwnerSet) {{
        {DELTAS_QUERY_NAME}(
            first: $first,
            last: $last, 
            after: $after,
            ownerSet: $ownerSet
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