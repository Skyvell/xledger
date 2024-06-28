from gql import gql


GET_CUSTOMERS_FROM_DBIDS = gql("""
    query getCustomers($first: Int, $after: String, $dbIdList: [Int!]) {
        customers(
            first: $first, 
            after: $after, 
            filter: { dbId_in: $dbIdList }
        ) {
            edges {
                cursor
                node {
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
                }
            }
            pageInfo {
                hasNextPage
            }
        }
    }
""")

GET_CUSTOMERS_AFTER_CURSOR = gql("""
    query getTimesheets($first: Int, $after: String) {
        timesheets(
            first: $first,
            after: $after
        ) {
            edges {
                node {
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
                }
                cursor
            }
            pageInfo {
                hasNextPage
            }
        }
    }
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