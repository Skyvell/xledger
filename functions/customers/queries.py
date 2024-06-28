from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


CUSTOMER_NODE_FIELDS = """
    dbId
    description
    email
    code
    number
    company {
        dbId
        name
        description
        email
    }
"""


COLUMNS = flatten_graphql_fields(CUSTOMER_NODE_FIELDS)


GET_CUSTOMERS_FROM_DBIDS = gql(f"""
    query getCustomers($first: Int, $after: String, $dbIdList: [Int!]) {{
        customers(
            first: $first, 
            after: $after, 
            filter: {{ dbId_in: $dbIdList }}
        ) {{
            edges {{
                cursor
                node {{
                    {CUSTOMER_NODE_FIELDS}
                }}
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_CUSTOMERS_AFTER_CURSOR = gql(f"""
    query getCustomers($first: Int, $after: String) {{
        customers(
            first: $first,
            after: $after
        ) {{
            edges {{
                node {{
                    {CUSTOMER_NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_CUSTOMER_DELTAS = gql("""
    query getCustomerDeltas($first: Int, $last: Int, $after: String) {
        customer_deltas(
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