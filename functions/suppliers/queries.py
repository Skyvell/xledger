from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
SUPPLIER_NODE_FIELDS = """
    dbId
    description
    code
    companyId
    number
    phone
    address {
        dbId    
        streetAddress
        zipCode
        place
    }
"""


# This is the final list of columns that we want in the pandas dataframe,
# and the resulting parquet file.
# Derived directly from the SUPPLIERS_NODE_FIELDS above to make sure the columns
# Are deterministic and up-to date.
COLUMNS = flatten_graphql_fields(SUPPLIER_NODE_FIELDS)


GET_SUPPLIERS_FROM_DBIDS = gql(f"""
    query getSuppliers($first: Int, $after: String, $dbIdList: [Int64String!]) {{
        suppliers(
            first: $first,
            after: $after, 
            filter: {{ 
                dbId_in: $dbIdList
            }}
        ) {{
            edges {{
                node {{
                    {SUPPLIER_NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_SUPPLIERS_AFTER_CURSOR = gql(f"""
    query getSuppliers($first: Int, $after: String) {{
        suppliers(
            first: $first,
            after: $after
        ) {{
            edges {{
                node {{
                    {SUPPLIER_NODE_FIELDS}
                }}
                cursor
            }}
            pageInfo {{
                hasNextPage
            }}
        }}
    }}
""")


GET_SUPPLIERS_DELTAS = gql("""
    query getSuppliersDeltas($first: Int, $last: Int, $after: String) {
        supplier_deltas(
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