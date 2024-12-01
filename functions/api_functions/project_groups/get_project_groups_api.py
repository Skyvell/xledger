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

from functions.api_functions.ap_transactions.queries import (
    COLUMN_DTYPES,
    GET_ITEMS_AFTER_CURSOR
)


NAME = "project_groups_api"
logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name(f"get_{NAME}")
@bp.schedule(schedule="0 0 0 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def syncronize(myTimer: func.TimerRequest) -> None:
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    # Initialize classes needed for syncronizing data.
    grapql_client = GraphQLClient(config.api_endpoint, config.api_key)
    data_lake_writer = DataLakeWriter(config.data_storage_account, credential, config.data_storage_container, NAME)
    item_fetcher = ItemFetcher(grapql_client, query_by_cursor = GET_ITEMS_AFTER_CURSOR)
    state_manager = SynchronizerStateManager(config.app_config_endpoint, credential, f"{NAME}-")

    # Initialize the data syncronizer.
    syncronizer = DataSynchronizer(
        NAME,
        COLUMN_DTYPES,
        item_fetcher,
        data_lake_writer,
        state_manager,
    )

    # Fetch data.
    syncronizer.syncronize(sync_from_scratch = True)