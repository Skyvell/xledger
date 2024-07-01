from shared.gql_client import GraphQLClient, PaginationQueryResult
from typing import Dict, Any
import logging


class DeltasResult:
    """
    A class to store the result of Xledger deltas queries. Deltas queries are used
    to get information about items that have been added, updated, or deleted. These 
    changes are available via the API for 3 days before they are removed.

    Attributes:
    additions (set): A set of dbIds corresponding to a GraphQL item that has been added.
    updates (set): A set of dbIds corresponding to a GraphQL item that has been updated.
    deletions (set): A set of dbIds corresponding to a GraphQL item that has been deleted.
    last_cursor (str): The cursor for the last processed item.
    """

    def __init__(self, additions: set, updates: set, deletions: set, last_cursor: str) -> None:
        """
        Initialize a new instance of DeltasResult.

        Args:
        additions (set): A set of dbIds corresponding to a GraphQL item that has been added.
        updates (set): A set of dbIds corresponding to a GraphQL item that has been updated.
        deletions (set): A set of dbIds corresponding to a GraphQL item that has been deleted.
        last_cursor (str): The cursor of the last delta processed.
        """
        self.additions = additions
        self.updates = updates
        self.deletions = deletions
        self.last_cursor = last_cursor

    def has_changes(self) -> bool:
        """
        Check if there are any changes (additions, updates, or deletions).

        Returns:
        bool: True if there are changes, False otherwise.
        """
        return bool(self.additions or self.updates or self.deletions)

    def has_additions(self) -> bool:
        """
        Check if there are any additions.

        Returns:
        bool: True if there are additions, False otherwise.
        """
        return len(self.additions) > 0
    
    def has_updates(self) -> bool:
        """
        Check if there are any updates.

        Returns:
        bool: True if there are updates, False otherwise.
        """
        return len(self.updates) > 0
    
    def has_deletions(self) -> bool:
        """
        Check if there are any deletions.

        Returns:
        bool: True if there are deletions, False otherwise.
        """
        return len(self.deletions) > 0
    
    def get_additions(self) -> list:
        """
        Get the list of additions.

        Returns:
        list: A list of dbIds corresponding to a GraphQL item that has been added.
        """
        return list(self.additions)
    
    def get_updates(self) -> list:
        """
        Get the list of updates.

        Returns:
        list: A list of dbIds corresponding to a GraphQL item that has been updated.
        """
        return list(self.updates)
    
    def get_deletions(self) -> list:
        """
        Get the list of deletions.

        Returns:
        list: A list of dbIds corresponding to a GraphQL item that has been deleted.
        """
        return list(self.deletions)
    

class DeltaFetcher:
    """
    A class to fetch deltas from Xledger API. Delta endpoints give information
    about items that have been added, updated or deleted. These changes are available
    for 3 days in the API before they are removed.

    Attributes:
    graphql_client (GraphQLClient): The GraphQL client used to execute queries.
    query (str): The GraphQL query to execute.
    """

    def __init__(self, client: GraphQLClient, query: str) -> None:
        """
        Initialize a new instance of DeltaFetcher.

        Args:
        client (GraphQLClient): The GraphQL client used to execute queries.
        query (str): The GraphQL query to execute. Example query here?
        """
        self.graphql_client = client
        self.query = query

    def fetch_deltas(self, variables: Dict[str, Any]) -> DeltasResult:
        """
        Fetch deltas (items that have been added, updated, or deleted) based on the provided variables.

        Args:
        variables (Dict[str, Any]): A dictionary of variables to pass to the GraphQL query.

        Returns:
        DeltasResult: The result of the deltas.

        Raises:
        Exception: If an error occurs while fetching deltas.
        """
        try:
            query_result = self._execute_paginated_query(variables)
            return self._extract_deltas(query_result)
        except Exception as e:
            logging.error(f"Error fetching deltas: {e}")
            raise

    def _execute_paginated_query(self, variables: Dict[str, Any]) -> PaginationQueryResult:
        """
        Execute a paginated GraphQL query.

        Args:
        variables (Dict[str, Any]): A dictionary of variables to pass to the GraphQL query.

        Returns:
        PaginationQueryResult: The result of the paginated query.
        """
        return self.graphql_client.paginate_gql_query(self.query, variables)

    def _extract_deltas(self, result: PaginationQueryResult) -> DeltasResult:
        """
        Extract deltas (items that have been added, updated, or deleted) from the paginated query result.

        Args:
        result (PaginationQueryResult): The result of the paginated query.

        Returns:
        DeltasResult: The extracted deltas.
        """
        additions = set()
        updates = set()
        deletions = set()

        if not result.has_results():
            return DeltasResult(additions, updates, deletions, result.get_last_cursor())

        for edge in result.edges:
            node = edge['node']
            mutation_type = node.get('mutationType')
            db_id = node.get('dbId')

            if mutation_type == "DELETED":
                deletions.add(db_id)
            elif mutation_type == "UPDATED":
                updates.add(db_id)
            elif mutation_type == "ADDED":
                additions.add(db_id)

        # Ensure no updates or additions are in deletions.
        updates -= deletions
        additions -= deletions

        return DeltasResult(additions, updates, deletions, result.get_last_cursor())
