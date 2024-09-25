from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields

# Name of the queries.
ITEMS_QUERY_NAME = "timesheets"
DELTAS_QUERY_NAME = "timesheet_deltas"

# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
NODE_FIELDS = """
    dbId
    createdAt
    modifiedAt
    assignmentDate
    workingHours
    isHeaderApproved
    headerApprovedAt
    hourlyRevenueCurrency
    owner {
        dbId
        description
    }
    employee {
        dbId
        description
        code
    }
    activity {
        code
        description
    }
    timeType {
        code
        description
    }
    project {
        dbId
        description
        code
    }
"""


DATA_TYPES_LIST = [
    'Int64',            # dbId
    'datetime64[ns]',   # createdAt
    'datetime64[ns]',   # modifiedAt
    'datetime64[ns]',   # assignmentDate
    'float64',          # workingHours
    'boolean',          # isHeaderApproved
    'datetime64[ns]',   # headerApprovedAt
    'string',           # hourlyRevenueCurrency
    'Int64',            # owner.dbId
    'string',           # owner.description
    'Int64',            # employee.dbId
    'string',           # employee.description
    'string',           # employee.code
    'string',           # activity.code
    'string',           # activity.description
    'string',           # timeType.code
    'string',           # timeType.description
    'Int64',            # project.dbId
    'string',           # project.description
    'string'            # project.code
]


# This is the final list of columns that we want in the pandas dataframe,
# and the resulting parquet file.
# Derived directly from the NODE_FIELDS above to make sure the columns
# Are deterministic and up-to date.
COLUMNS = flatten_graphql_fields(NODE_FIELDS)
COLUMN_DTYPES = dict(zip(COLUMNS, DATA_TYPES_LIST))


GET_ITEMS_FROM_DBIDS = gql(f"""
    query get_{ITEMS_QUERY_NAME}($first: Int, $after: String, $dbIdList: [Int64String!]) {{
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