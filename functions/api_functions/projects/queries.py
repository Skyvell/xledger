from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Name of the queries.
ITEMS_QUERY_NAME = "projects"
DELTAS_QUERY_NAME = "project_deltas"

# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.

# Not sure I should use company or customer here.
NODE_FIELDS = """
    dbId
    description
    code
    toDate
    shortInfo
    shortInternalInfo
    yourReference

    owner {
        description
        ownerCode
    }

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
        code
        objectKind {
            name
        }
    }
    
    projectManager {
        dbId
        description
    }

    projectGroup {
        description
        code
        levelParent {
            description
            code
            levelParent {
                description
                code
                levelParent {
                    description
                    code
                }
            }
        }
    }

    flexiFieldsItem {
        code2 {
            description
            code
        }
    }
"""

# Datatypes of the columns in the resulting pandas dataframe.
COLUMN_DATA_TYPES = [
    'Int64',            # dbId
    'string',           # description
    'string',           # code
    'string',           # toDate
    'string',           # shortInfo
    'string',           # shortInternalInfo
    'string',           # yourReference
    'string',           # owner.description
    'Int64',            # owner.ownerCode
    'Int64',            # customer.dbId
    'string',           # customer.description
    'string',           # customer.email
    'string',           # customer.code
    'string',           # customer.address.country.description
    'Int64',            # company.dbId
    'string',           # company.description
    'string',           # company.companyNumber
    'string',           # company.code
    'string',           # company.country
    'string',           # glObject1.description
    'string',           # glObject1.code
    'string',           # glObject1.objectKind.name
    'Int64',            # projectManager.dbId
    'string',           # projectManager.description
    'string',           # projectGroup.description
    'Int64',            # projectGroup.code
    'string',           # projectGroup.levelParent.description
    'Int64',            # projectGroup.levelParent.code
    'string',           # projectGroup.levelParent.levelParent.description
    'Int64',            # projectGroup.levelParent.levelParent.code
    'string',           # projectGroup.levelParent.levelParent.levelParent.description
    'Int64',            # projectGroup.levelParent.levelParent.levelParent.code
    'string',           # flexiFieldsItem.code2.description
    'Int64'             # flexiFieldsItem.code2.code
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
            ownerSet: $ownerSet
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