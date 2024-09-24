from typing import List, Optional
import logging
from shared.delta_fetcher import DeltaFetcher
from shared.item_fetcher import ItemFetcher
from shared.data_lake_writer import DataLakeWriter
from shared.configuration_manager import SynchronizerStateManager
from shared.utils.data_transformation import flatten_list_of_dicts
from shared.utils.time import get_current_time_for_filename
from shared.utils.files import convert_dicts_to_parquet_pandas


class DataSynchronizer:
    """
    A class used to syncronize a specifc type of data from Xledger.
    The synchronizer can perform a full syncronization or
    fetch only the latest changes. State of syncronizations are stored in Azure. Which endpoint to fetch
    data from is defined in the item_fetcher and delta_fetcher.

    Full syncronization: 
    The synchronizer fetches all items and writes them to the data lake. The state manager updates the
    state in Azure Blob Storage with the cursor of the last item fetched, and whether the syncronization completed or not.

    Syncronize changes:
    The synchronizer uses a DeltaFetcher to get the the dbIds and which type of change occured (addition, update or deletion).
    An ItemFetcher is used to fetch the items based on the dbIds. The items are then transformed and written to the data lake.
    The state manager updates the state of Azure to keep track of the last delta processed.


    Attributes:
    name (str): The name of the synchronizer.
    columns (List[str]): The list of columns that should be included in the data lake.
    delta_fetcher (DeltaFetcher): The instance to fetch deltas (added, updated, or deleted items).
    item_fetcher (ItemFetcher): The instance to fetch items.
    data_lake_writer (DataLakeWriter): The instance to write data to the data lake.
    state_manager (SynchronizerStateManager): The instance to manage synchronization state.
    """

    def __init__(self, 
                 name: str,
                 columns: List[str],
                 item_fetcher: ItemFetcher,
                 data_lake_writer: DataLakeWriter,
                 state_manager: SynchronizerStateManager,
                 delta_fetcher: Optional[DeltaFetcher] = None,
                 add_mutation_type_to_columns: bool = True) -> None:
        """
        Initialize a new instance of DataSynchronizer.

        Args:
        name (str): The name of the synchronizer.
        columns (List[str]): The list of columns to include in the data lake.
        item_fetcher (ItemFetcher): The instance to fetch items.
        data_lake_writer (DataLakeWriter): The instance used to write data to the data lake.
        state_manager (SynchronizerStateManager): The instance used to manage synchronization state.
        delta_fetcher (Optional[DeltaFetcher]): The instance to fetch deltas (added, updated, or deleted items).
        """
        self.name = name
        self.delta_fetcher = delta_fetcher
        self.item_fetcher = item_fetcher
        self.state_manager = state_manager
        self.data_lake_writer = data_lake_writer
        self.columns = columns

        if add_mutation_type_to_columns:
            self.columns.append("mutationType")

    def syncronize(self, sync_from_scratch: bool) -> None:
        """
        Perform a full data syncronization or syncronize only changes.

        Args:
        sync_from_scratch (bool): If True, perform a full synchronization; otherwise, synchronize changes.
        """
        if not sync_from_scratch:
            if not self.delta_fetcher:
                raise ValueError("A DeltaFetcher is required for syncronizing changes.")

        if sync_from_scratch:
            self._full_syncronization()
        else:
            self._syncronize_changes()

    def _full_syncronization(self) -> None:
        """
        Perform a full synchronization of data.
        """
        # Get the last delta.
        deltas = None
        if self.delta_fetcher:
            deltas = self.delta_fetcher.fetch_deltas({"last": 1})
        
        # Fetch all items.
        items = self.item_fetcher.fetch_all_items_after_cursor(first=10000)
        if not items.has_items():
            logging.info(f"No items found for {self.name}.")
            return
        
        # Transform items.
        items.add_key_value_to_items("mutationType", "ADDED")
        items_transformed = convert_dicts_to_parquet_pandas(flatten_list_of_dicts(items.get_items()), self.columns)

        # Write items to data lake.
        self.data_lake_writer.write_data(f"full_sync-{get_current_time_for_filename()}-{self.name}.parquet", items_transformed)

        # Update state.
        self.state_manager.initial_sync_cursor = items.get_last_item_cursor()
        self.state_manager.initial_sync_complete = True
        if deltas:
            self.state_manager.deltas_cursor = deltas.last_cursor

        # Can call _syncronize_changes here to get the changes since the full sync.
        # Use the last delta fetched at the beginning of this function.

    def _syncronize_changes(self) -> None:
        """
        Synchronize only the changes (additions, updates, deletions) since the last synchronization.
        """
        # Get all deltas since last sync.
        deltas = self.delta_fetcher.fetch_deltas({"first": 10000, "after": self.state_manager.deltas_cursor})

        # No new changes found -> return.
        if not deltas.has_changes():
            logging.info(f"No changes found for {self.name}.")
            return
        
        # Get all items based from the dbids fetched with the delta_fetcher.
        all_changed_items = []
        if deltas.has_additions():
            additions = self.item_fetcher.fetch_items_by_ids(deltas.get_additions())
            additions.add_key_value_to_items("mutationType", "ADDED")
            all_changed_items.extend(additions.get_items())

        if deltas.has_updates():
            updates = self.item_fetcher.fetch_items_by_ids(deltas.get_updates())
            updates.add_key_value_to_items("mutationType", "UPDATED")
            all_changed_items.extend(updates.get_items())

        if deltas.has_deletions():
            deletions = [{"dbId": dbId, "mutationType": "DELETED"} for dbId in deltas.get_deletions()]
            all_changed_items.extend(deletions)

        # Transform items.
        parquet = convert_dicts_to_parquet_pandas(flatten_list_of_dicts(all_changed_items), self.columns)

        # Write items to data lake.
        self.data_lake_writer.write_data(f"sync_changes-{get_current_time_for_filename()}-{self.name}.parquet", parquet)

        # Update state.
        self.state_manager.deltas_cursor = deltas.last_cursor