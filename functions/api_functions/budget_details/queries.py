from gql import gql
from shared.utils.data_transformation import flatten_graphql_fields


# Name of the queries.
ITEMS_QUERY_NAME = "budgetDetails"


# Define all the fields that we want to fetch from the xledger API here. 
# This way we only need to add/remove fields in one place.
NODE_FIELDS = """
    dbId
    amount3
    amount4

    owner {
        description
        ownerCode
    }

    account {
        description
        code
    }

    budget {
        description
        code
    }

    period {
        fiscalYear
        fiscalPeriod
    }

    glObject1 {
        description
        code
        objectKind {
            name
        }
    }

    glObject2 {
        description
        code
        objectKind {
            name
        }
    } 
"""

# Updated datatypes of the columns in the resulting pandas dataframe.
COLUMN_DATA_TYPES = [
    'Int64',            # dbId
    'float64',          # amount

    'string',           # owner.description
    'Int64',            # owner.ownerCode

    'string',           # account.description
    'string',           # account.code

    'string',           # budget.description
    'string',           # budget.code

    'Int64',            # period.fiscalYear
    'Int64',            # period.fiscalPeriod

    'string',           # glDimension.glObject1.description
    'string',           # glDimension.glObject1.code
    'string',           # glDimension.glObject1.objectKind.name

    'string',           # glDimension.glObject2.description
    'string',           # glDimension.glObject2.code
    'string'            # glDimension.glObject2.objectKind.name
]


# This is the final list of columns that we want in the pandas dataframe,
# and the resulting parquet file.
# Derived directly from the NODE_FIELDS above to make sure the columns
# Are deterministic and up-to date.
COLUMNS = flatten_graphql_fields(NODE_FIELDS)
COLUMN_DTYPES = dict(zip(COLUMNS, COLUMN_DATA_TYPES))

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