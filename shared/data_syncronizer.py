from typing import List, Optional
import logging
from shared.delta_fetcher import DeltaFetcher
from shared.item_fetcher import ItemFetcher
from shared.data_lake_writer import DataLakeWriter
from shared.configuration_manager import SynchronizerStateManager
from shared.utils.data_transformation import flatten_list_of_dicts
from shared.utils.time import get_current_time_for_filename
from shared.utils.time import generate_iso_8601_timestamp
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
    column_dtypes (List[str]): The list of column_dtypes that should be included in the data lake.
    delta_fetcher (DeltaFetcher): The instance to fetch deltas (added, updated, or deleted items).
    item_fetcher (ItemFetcher): The instance to fetch items.
    data_lake_writer (DataLakeWriter): The instance to write data to the data lake.
    state_manager (SynchronizerStateManager): The instance to manage synchronization state.
    """

    def __init__(self, 
                 name: str,
                 column_dtypes: dict,
                 item_fetcher: ItemFetcher,
                 data_lake_writer: DataLakeWriter,
                 state_manager: SynchronizerStateManager,
                 delta_fetcher: Optional[DeltaFetcher] = None,
                 add_mutation_type_to_columns: bool = True,
                 add_mutated_at_to_columns: bool = False) -> None:
        """
        Initialize a new instance of DataSynchronizer.

        Args:
        name (str): The name of the synchronizer.
        column_dtypes (Dict): A dictionary of columns and their data types for pandas to use.
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
        self.column_dtypes = column_dtypes
        self.add_mutation_type_to_columns = add_mutation_type_to_columns
        self.add_mutated_at_to_columns = add_mutated_at_to_columns

        if add_mutation_type_to_columns:
            self.column_dtypes["mutationType"] = "string"

        if add_mutated_at_to_columns:
            self.column_dtypes["mutatedAt"] = "string"

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
            deltas = self.delta_fetcher.fetch_deltas({"last": 1, "ownerSet": "MINE"})
        
        # Fetch all items.
        items = self.item_fetcher.fetch_all_items_after_cursor(first=10000)
        if not items.has_items():
            logging.info(f"No items found for {self.name}.")
            return
        
        # Transform items.
        # Current time is used as the mutatedAt timestamp when there is no mutation time.
        current_time = generate_iso_8601_timestamp()

        if self.add_mutation_type_to_columns:
            items.add_key_value_to_items("mutationType", "ADDED")

        if self.add_mutated_at_to_columns:
            items.add_key_value_to_items("mutatedAt", current_time)
        
        items_transformed = convert_dicts_to_parquet_pandas(flatten_list_of_dicts(items.get_items()), self.column_dtypes)

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
        deltas = self.delta_fetcher.fetch_deltas({"first": 10000, "after": self.state_manager.deltas_cursor, "ownerSet": "MINE"})
        mutation_times = deltas.get_mutation_times()

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
        
        # Add mutationTimes to all changed items.
        if self.add_mutated_at_to_columns:
            for item in all_changed_items:
                db_id = item.get("dbId")
                mutated_at = mutation_times.get(db_id)
                if mutated_at:
                    item['mutatedAt'] = mutation_times[db_id]

        # Transform items.
        parquet = convert_dicts_to_parquet_pandas(flatten_list_of_dicts(all_changed_items), self.column_dtypes)

        # Write items to data lake.
        self.data_lake_writer.write_data(f"sync_changes-{get_current_time_for_filename()}-{self.name}.parquet", parquet)

        # Update state.
        self.state_manager.deltas_cursor = deltas.last_cursor