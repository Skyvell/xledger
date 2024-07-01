from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging
import os

from shared.data_lake_writer import DataLakeWriter
from shared.configuration_manager import SynchronizerStateManager
from shared.delta_fetcher import DeltaFetcher
from shared.item_fetcher import ItemFetcher
from shared.data_syncronizer import DataSynchronizer
from shared.gql_client import GraphQLClient
from shared.environment_config import EnvironmentConfig

from functions.projects.queries import (
    COLUMNS,
    GET_PROJECT_DELTAS,
    GET_PROJECTS_AFTER_CURSOR,
    GET_PROJECTS_FROM_DBIDS
)


NAME = "projects"
logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name("SyncronizeProjects")
@bp.schedule(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def syncronize_projects(myTimer: func.TimerRequest) -> None:
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    ## Initialize classes needed for syncronizing data.
    grapql_client = GraphQLClient(config.api_endpoint, config.api_key)
    data_lake_writer = DataLakeWriter(config.data_storage_account, credential, config.data_storage_container, NAME)
    delta_fetcher = DeltaFetcher(grapql_client, GET_PROJECT_DELTAS)
    item_fetcher = ItemFetcher(grapql_client, GET_PROJECTS_FROM_DBIDS, GET_PROJECTS_AFTER_CURSOR)
    state_manager = SynchronizerStateManager(config.app_config_endpoint, credential, f"{NAME}-")

    # Initialize the data syncronizer.
    syncronizer = DataSynchronizer(
        NAME,
        COLUMNS,
        item_fetcher,
        data_lake_writer,
        state_manager,
        delta_fetcher,
    )

    # Syncronize the data.
    if not syncronizer.state_manager.initial_sync_complete:
        syncronizer.syncronize(sync_from_scratch = True)
    else:
        syncronizer.syncronize(sync_from_scratch = False)