from gql import gql


GET_EMPLOYEES_FROM_DBIDS = gql("""
    query getEmployees($first: Int, $after: String, $dbIdList: [Int64String!]) {
        employees(
            first: $first,
            after: $after, 
            filter: { 
                dbId_in: $dbIdList
            }
        ) {
            edges {
                cursor
                node {
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
                }
            }
            pageInfo {
                hasNextPage
            }
        }
    }
""")

GET_EMPLOYEES_AFTER_CURSOR = gql("""
    query getEmployees($first: Int, $last: Int, $after: String) {
        employees(
            first: $first,
            last: $last,
            after: $after
        ) {
            edges {
                cursor
                node {
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
                }
            }
            pageInfo {
                hasNextPage
            }
        }
    }
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