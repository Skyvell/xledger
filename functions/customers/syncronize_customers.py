from azure import functions as func
from azure.identity import DefaultAzureCredential

import logging

from shared.data_lake_writer import DataLakeWriter
from shared.configuration_manager import SynchronizerStateManager
from shared.delta_fetcher import DeltaFetcher
from shared.item_fetcher import ItemFetcher
from shared.data_syncronizer import DataSynchronizer
from shared.gql_client import GraphQLClient
from shared.environment_config import EnvironmentConfig

from functions.customers.queries import (
    GET_CUSTOMERS_FROM_DBIDS,
    GET_CUSTOMERS_AFTER_CURSOR,
    GET_CUSTOMER_DELTAS
)


NAME = "customers"
logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name("SyncronizeCustomers")
@bp.schedule(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def syncronize_customers(myTimer: func.TimerRequest) -> None:
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    # Initialize classes needed for syncronizing data.
    grapql_client = GraphQLClient(config.api_endpoint, config.api_key)
    data_lake_writer = DataLakeWriter(config.data_storage_account, credential, config.data_storage_container, NAME)
    delta_fetcher = DeltaFetcher(grapql_client, GET_CUSTOMER_DELTAS)
    item_fetcher = ItemFetcher(grapql_client, GET_CUSTOMERS_FROM_DBIDS, GET_CUSTOMERS_AFTER_CURSOR)
    state_manager = SynchronizerStateManager(config.app_config_endpoint, credential, f"{NAME}-")

    # Initialize the data syncronizer.
    syncronizer = DataSynchronizer(
        NAME, 
        delta_fetcher,
        item_fetcher,
        data_lake_writer,
        state_manager
    )

    # Syncronize the data.
    if not syncronizer.state_manager.initial_sync_complete:
        syncronizer.syncronize(sync_from_scratch = True)
    else:
        syncronizer.syncronize(sync_from_scratch = False)