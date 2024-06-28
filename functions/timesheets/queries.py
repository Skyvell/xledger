from gql import gql 


GET_TIMESHEETS_FROM_DBIDS = gql("""
    query getTimesheets($first: Int, $after: String, $dbIdList: [Int64String!]) {
        timesheets(
            first: $first,
            after: $after, 
            filter: { 
                dbId_in: $dbIdList
            }
        ) {
            edges {
                node {
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
                }
                cursor
            }
            pageInfo {
                hasNextPage
            }
        }
    }
""")

GET_TIMESHEETS_AFTER_CURSOR = gql("""
    query getTimesheets($first: Int, $after: String) {
        timesheets(
            first: $first,
            after: $after
        ) {
            edges {
                node {
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
                }
                cursor
            }
            pageInfo {
                hasNextPage
            }
        }
    }
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