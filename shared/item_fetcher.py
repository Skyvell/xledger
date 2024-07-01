from shared.gql_client import GraphQLClient, PaginationQueryResult
from shared.utils.data_transformation import add_key_value_to_dicts
from typing import Dict, Any, List
import logging


class ItemsResult:
    """
    A class to store the result of items fetched, including the items and the last cursor.

    Attributes:
    items (list[Dict]): A list of items retrieved from the GraphQL query.
    cursor (str): The cursor for the last processed item.
    """

    def __init__(self, items: List[Dict], cursor: str) -> None:
        """
        Initialize a new instance of ItemsResult.

        Args:
        items (list[Dict]): A list of items retrieved from the GraphQL query.
        cursor (str): The cursor for the last processed item.
        """
        self.items = items
        self.cursor = cursor

    def has_items(self) -> bool:
        """
        Check if there are any items.

        Returns:
        bool: True if there are items, False otherwise.
        """
        return bool(self.items)
    
    def get_items(self) -> List[Dict]:
        """
        Get the list of items.

        Returns:
        list[Dict]: A list of items.
        """
        return self.items
    
    def get_last_item_cursor(self) -> str:
        """
        Get the cursor for the last item.

        Returns:
        str: The cursor for the last item.
        """
        return self.cursor
    
    def add_key_value_to_items(self, key: str, value: Any) -> None:
        """
        Add a key-value pair to each item in the list of items.

        Args:
        key (str): The key to add.
        value (Any): The value to add.
        """
        add_key_value_to_dicts(self.items, key, value)


class ItemFetcher:
    """
    A class to fetch items using a GraphQL client.

    Attributes:
    graphql_client (GraphQLClient): The GraphQL client used to execute queries.
    query_by_dbids (str): The GraphQL query to execute by database IDs.
    query_by_cursor (str): The GraphQL query to execute by cursor.
    """

    def __init__(self, client: GraphQLClient, query_by_dbids: str, query_by_cursor: str) -> None:
        """
        Initialize a new instance of ItemFetcher.

        Args:
        client (GraphQLClient): The GraphQL client used to execute queries.
        query_by_dbids (str): The GraphQL query to execute by database IDs.
        query_by_cursor (str): The GraphQL query to execute by cursor.
        """
        self.graphql_client = client
        self.query_by_dbids = query_by_dbids
        self.query_by_cursor = query_by_cursor

    def fetch_items_by_ids(self, db_ids: List[str], first: int = 10000) -> ItemsResult:
        """
        Fetch items by their dbIds.

        Args:
        db_ids (list[str]): A list of dbIds to fetch.
        first (int): The maximum number of items to fetch in each batch. Defaults to 10000.

        Returns:
        ItemsResult: The result of the fetched items.
        """
        if not db_ids:
            return ItemsResult([], None)
        
        variables = {"first": first, "dbIdList": db_ids}
        query_result = self._execute_paginated_query(self.query_by_dbids, variables)

        return ItemsResult(query_result.get_nodes(), query_result.get_last_cursor())

    def fetch_all_items_after_cursor(self, after: str = None, first: int = 10000) -> ItemsResult:
        """
        Fetch all items after a given cursor.

        Args:
        after (str): The cursor to start fetching items after. Defaults to None.
        first (int): The maximum number of items to fetch in each batch. Defaults to 10000.

        Returns:
        ItemsResult: The result of the fetched items.
        """
        variables = {"first": first, "after": after}
        query_result = self._execute_paginated_query(self.query_by_cursor, variables)
        return ItemsResult(query_result.get_nodes(), query_result.get_last_cursor())

    def _execute_paginated_query(self, query: str, variables: Dict[str, Any]) -> PaginationQueryResult:
        """
        Execute a paginated GraphQL query. The query will continue to fetch items in batches
        according to what is epcified in the variables, until there are no more items to fetch.

        Args:
        query (str): The GraphQL query to execute.
        variables (Dict[str, Any]): A dictionary of variables to pass to the GraphQL query.

        Returns:
        PaginationQueryResult: The result of the paginated query.

        Raises:
        Exception: If an error occurs while fetching items.
        """
        try:
            return self.graphql_client.paginate_gql_query(query, variables)
        except Exception as e:
            logging.error(f"Error fetching items: {e}")
            raise