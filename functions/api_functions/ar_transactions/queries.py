from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Name of the queries.
ITEMS_QUERY_NAME = "arTransactions"
DELTAS_QUERY_NAME = "arTransaction_deltas"


# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
# amount3 = SEK, amount4 = USD.
NODE_FIELDS = """
    dbId
    owner {
      description
      ownerCode
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
    ledgerType {
      name
    }
    transactionHeader {
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
      fiscalYear
      fromDate
      toDate
      monthNumber
    }
    invoiceDate
    dueDate
    paymentDate
    currency {
      code
    }
    exchangeRate
    amount3
    amount4
    invoiceAmount
    invoiceRemaining
    bankAccount
"""

# Updated datatypes of the columns in the resulting pandas dataframe.
COLUMN_DATA_TYPES = [
    'Int64',            # dbId
    'string',           # owner.description
    'Int64',            # owner.ownerCode
    'string',           # company.description
    'string',           # company.phone
    'string',           # company.email
    'string',           # company.address.streetAddress
    'string',           # company.address.zipCode
    'string',           # company.address.place
    'string',           # company.address.fullAddress
    'string',           # billAddress.streetAddress
    'string',           # billAddress.zipCode
    'string',           # billAddress.place
    'string',           # billAddress.fullAddress
    'string',           # account.description
    'string',           # account.code
    'string',           # account.descriptionTranslated
    'string',           # slTransactionType.name
    'string',           # glDimension.glObject1.description
    'string',           # glDimension.glObject1.code
    'string',           # glDimension.glObject1.objectKind.name
    'string',           # glDimension.glObject2.description
    'string',           # glDimension.glObject2.code
    'string',           # glDimension.glObject2.objectKind.name
    'string',           # ledgerType.name
    'string',           # transactionHeader.postedDate
    'string',           # transactionHeader.trProcessLevel.name
    'string',           # transactionHeader.transactionSource.description
    'string',           # transactionHeader.transactionSource.code
    'Int64',            # transactionHeader.trRegNumber
    'string',           # transactionHeader.transactionNumber
    'string',           # period.description
    'Int64',            # period.fiscalYear
    'string',           # period.fromDate
    'string',           # period.toDate
    'Int64',            # period.monthNumber
    'string',           # invoiceDate
    'string',           # dueDate
    'string',           # paymentDate
    'string',           # currency.code
    'float64',          # exchangeRate
    'float64',          # amount3
    'float64',          # amount4
    'float64',          # invoiceAmount
    'float64',          # invoiceRemaining
    'string'            # bankAccount
]


# This is the final list of columns that we want in the pandas dataframe,
# and the resulting parquet file.
# Derived directly from the NODE_FIELDS above to make sure the columns
# Are deterministic and up-to date.
COLUMNS = flatten_graphql_fields(NODE_FIELDS)
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))


GET_ITEMS_FROM_DBIDS = gql(f"""
    query get_{ITEMS_QUERY_NAME}($first: Int, $after: String, $ownerSet: OwnerSet, $dbIdList: [Int!]) {{
        {ITEMS_QUERY_NAME}(
            first: $first,
            after: $after,
            ownerSet: $ownerSet,
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