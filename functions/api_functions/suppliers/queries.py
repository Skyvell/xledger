from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Name of the queries.
ITEMS_QUERY_NAME = "suppliers"
DELTAS_QUERY_NAME = "supplier_deltas"


# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
NODE_FIELDS = """
    dbId
    description
    code
    number
    phone
    bankAccount
    notes
    company {
        dbId
        companyNumber
    }
    subledgerGroup {
        dbId
        description
    }
    address {
        dbId    
        streetAddress
        zipCode
        place
        fullAddress
    }
    contact {
        dbId
        name
    }
"""

# Datatypes of the columns in the resulting pandas dataframe.
COLUMN_DATA_TYPES = [
    'Int64',            # dbId
    'string',           # description
    'string',           # code
    'Int64',            # number
    'string',           # phone
    'string',           # bankAccount
    'string',           # notes
    'Int64',            # company.dbId
    'string',           # company.companyNumber
    'Int64',            # subledgerGroup.dbId
    'string',           # subledgerGroup.description
    'Int64',            # address.dbId
    'string',           # address.streetAddress
    'string',           # address.zipCode
    'string',           # address.place
    'string',           # address.fullAddress
    'Int64',            # contact.dbId
    'string'            # contact.name
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