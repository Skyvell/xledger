from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
PROJECT_NODE_FIELDS = """
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


# This is the final list of columns that we want in the pandas dataframe,
# and the resulting parquet file.
# Derived directly from the TIMESHEET_NODE_FIELDS above to make sure the columns
# Are deterministic and up-to date.
COLUMNS = flatten_graphql_fields(TIMESHEET_NODE_FIELDS)


GET_TIMESHEETS_FROM_DBIDS = gql(f"""
    query getTimesheets($first: Int, $after: String, $dbIdList: [Int64String!]) {{
        timesheets(
            first: $first,
            after: $after, 
            filter: {{ 
                dbId_in: $dbIdList
            }}
        ) {{
            edges {{
                node {{
                    {TIMESHEET_NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_TIMESHEETS_AFTER_CURSOR = gql(f"""
    query getTimesheets($first: Int, $after: String) {{
        timesheets(
            first: $first,
            after: $after
        ) {{
            edges {{
                node {{
                    {TIMESHEET_NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_TIMESHEET_DELTAS = gql("""
    query getTimesheetDeltas($first: Int, $last: Int, $after: String) {
        timesheet_deltas(
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