from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Name of the queries.
ITEMS_QUERY_NAME = "customers"
DELTAS_QUERY_NAME = "customer_deltas"


# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
NODE_FIELDS = """
    dbId
    description
    email
    code
    number
    company {
        dbId
        description
        companyNumber
        address {
            streetAddress
            zipCode
            place
            fullAddress
        }
        billAddress {
            streetAddress
            zipCode
            place
            fullAddress
        }
        shipAddress {
            streetAddress
            zipCode
            place
            fullAddress
          }
        email
        phone
    }
    subledgerGroup {
        dbId
        description
    }
    accountsPayableAccount {
        description
        code
        accountGroup {
            description
            code
        }
    }
"""

# Datatypes of the columns in the resulting pandas dataframe.
COLUMN_DATA_TYPES = [
    'Int64',            # dbId
    'string',           # description
    'string',           # email
    'string',           # code
    'Int64',            # number
    'Int64',            # company.dbId
    'string',           # company.description
    'string',           # company.companyNumber
    'string',           # company.address.streetAddress
    'string',           # company.address.zipCode
    'string',           # company.address.place
    'string',           # company.address.fullAddress
    'string',           # company.billAddress.streetAddress
    'string',           # company.billAddress.zipCode
    'string',           # company.billAddress.place
    'string',           # company.billAddress.fullAddress
    'string',           # company.shipAddress.streetAddress
    'string',           # company.shipAddress.zipCode
    'string',           # company.shipAddress.place
    'string',           # company.shipAddress.fullAddress
    'string',           # company.email
    'string',           # company.phone
    'Int64',            # subledgerGroup.dbId
    'string',           # subledgerGroup.description
    'string',           # accountsPayableAccount.description
    'Int64',            # accountsPayableAccount.code
    'string',           # accountsPayableAccount.accountGroup.description
    'Int64'             # accountsPayableAccount.accountGroup.code
]


# This is the final list of columns that we want in the pandas dataframe,
# and the resulting parquet file.
# Derived directly from the NODE_FIELDS above to make sure the columns
# Are deterministic and up-to date.
COLUMNS = flatten_graphql_fields(NODE_FIELDS)
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))


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