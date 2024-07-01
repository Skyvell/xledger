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

from functions.employees.queries import (
    COLUMNS,
    GET_EMPLOYEE_DELTAS,
    GET_EMPLOYEES_AFTER_CURSOR,
    GET_EMPLOYEES_FROM_DBIDS
)

NAME = "employees"

logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name("SyncronizeEmployees")
@bp.schedule(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def syncronize_employees(myTimer: func.TimerRequest) -> None:
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    # Initialize classes needed for syncronizing data.
    grapql_client = GraphQLClient(config.api_endpoint, config.api_key)
    data_lake_writer = DataLakeWriter(config.data_storage_account, credential, config.data_storage_container, NAME)
    delta_fetcher = DeltaFetcher(grapql_client, GET_EMPLOYEE_DELTAS)
    item_fetcher = ItemFetcher(grapql_client, GET_EMPLOYEES_FROM_DBIDS, GET_EMPLOYEES_AFTER_CURSOR)
    state_manager = SynchronizerStateManager(config.app_config_endpoint, credential, f"{NAME}-")

    # Initialize the data syncronizer.
    syncronizer = DataSynchronizer(
        NAME,
        COLUMNS,
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