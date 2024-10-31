from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Name of the queries.
ITEMS_QUERY_NAME = "employees"
DELTAS_QUERY_NAME = "employee_deltas"


# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
NODE_FIELDS = """
    dbId
    email
    description
    code
    createdAt
    modifiedAt
    employmentFrom
    employmentTo
    positionValue {
        dbId
        description
        code
    }
    positionCategory {
        dbId
        description
        code
    }
    compensationType {
        dbId
        description
        code
    }
    employmentType {
        description
        owner {
            description
        }
    }
    employmentGroup {
        description
        code
    }
    contact {
        firstName
        lastName
        birthday
        age
        country {
            description
        }
        gender {
            name
        }
    }
    exitReason {
        dbId
        description
        code
    }
    glObject1 {
        dbId
        description
        code
        id
    }
"""

# Datatypes of the columns in the resulting pandas dataframe.
COLUMN_DATA_TYPES = [
    'Int64',            # dbId
    'string',           # email
    'string',           # description
    'string',           # code
    'string',           # createdAt
    'string',           # modifiedAt
    'string',           # employmentFrom
    'string',           # employmentTo
    'Int64',            # positionValue.dbId
    'string',           # positionValue.description
    'string',           # positionValue.code
    'Int64',            # positionCategory.dbId
    'string',           # positionCategory.description
    'string',           # positionCategory.code
    'Int64',            # compensationType.dbId
    'string',           # compensationType.description
    'string',           # compensationType.code
    'string',           # employmentType.description
    'string',           # employmentType.owner.description
    'string',           # employmentGroup.description
    'string',           # employmentGroup.code
    'string',           # contact.firstName
    'string',           # contact.lastName
    'string',           # contact.birthday
    'Int64',            # contact.age
    'string',           # contact.country.description
    'string',           # contact.gender.name
    'Int64',            # exitReason.dbId
    'string',           # exitReason.description
    'string',           # exitReason.code
    'Int64',            # glObject1.dbId
    'string',           # glObject1.description
    'string',           # glObject1.code
    'string'            # glObject1.id
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