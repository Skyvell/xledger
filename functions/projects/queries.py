from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.

# Not sure I should use company or customer here.
PROJECT_NODE_FIELDS = """
    dbId
    description
    code
    shortInfo
    shortInternalInfo
    yourReference

    customer {
        dbId
        description
        email
        code
        address {
            country {
              description
            }
        }
    }

    company {
          dbId
          description
          companyNumber
          code
          country
        }

    glObject1 {
          description
          dbId
          code
    }
    projectManager {
          dbId
          description
    }
"""


# This is the final list of columns that we want in the pandas dataframe,
# and the resulting parquet file.
# Derived directly from the PROJECT_NODE_FIELDS above to make sure the columns
# Are deterministic and up-to date.
COLUMNS = flatten_graphql_fields(PROJECT_NODE_FIELDS)


GET_PROJECTS_FROM_DBIDS = gql(f"""
    query getProjects($first: Int, $after: String, $dbIdList: [Int!]) {{
        projects(
            first: $first,
            after: $after, 
            filter: {{ 
                dbId_in: $dbIdList
            }}
        ) {{
            edges {{
                node {{
                    {PROJECT_NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_PROJECTS_AFTER_CURSOR = gql(f"""
    query getProjects($first: Int, $after: String) {{
        projects(
            first: $first,
            after: $after
        ) {{
            edges {{
                node {{
                    {PROJECT_NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_PROJECT_DELTAS = gql("""
    query getProjectDeltas($first: Int, $last: Int, $after: String) {
        project_deltas(
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