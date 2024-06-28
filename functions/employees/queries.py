from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
EMPLOYEE_NODE_FIELDS = """
    dbId
    email
    description
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


# This is the final list of columns that we want in the pandas dataframe,
# and the resulting parquet file.
# Derived directly from the EMPLOYEE_NODE_FIELDS above to make sure the columns
# Are deterministic and up-to date.
COLUMNS = flatten_graphql_fields(EMPLOYEE_NODE_FIELDS)


# Query to get employees from a list of database IDs
GET_EMPLOYEES_FROM_DBIDS = gql(f"""
    query getEmployees($first: Int, $after: String, $dbIdList: [Int64String!]) {{
        employees(
            first: $first,
            after: $after, 
            filter: {{ 
                dbId_in: $dbIdList
            }}
        ) {{
            edges {{
                cursor
                node {{
                    {EMPLOYEE_NODE_FIELDS}
                }}
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")

GET_EMPLOYEES_AFTER_CURSOR = gql(f"""
    query getEmployees($first: Int, $last: Int, $after: String) {{
        employees(
            first: $first,
            last: $last,
            after: $after
        ) {{
            edges {{
                cursor
                node {{
                    {EMPLOYEE_NODE_FIELDS}
                }}
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_EMPLOYEE_DELTAS = gql("""
    query getEmployeeDeltas($first: Int, $last: Int, $after: String) {
        employee_deltas(
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