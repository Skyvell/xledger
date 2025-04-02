from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging

from shared.data_lake_writer import DataLakeWriter
from shared.item_fetcher import ItemFetcher
from shared.gql_client import GraphQLClient
from shared.environment_config import EnvironmentConfig
from shared.utils.data_transformation import flatten_list_of_dicts
from shared.utils.files import convert_dicts_to_parquet_pandas

from functions.api_functions.budget_details.queries import (
    COLUMN_DTYPES,
    GET_ITEMS_AFTER_CURSOR
)


NAME = "budget_details"
logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name(f"get_{NAME}")
@bp.schedule(schedule="15 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def get_budget_details(myTimer: func.TimerRequest) -> None:
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    # Initialize classes needed for syncronizing data.
    grapql_client = GraphQLClient(config.api_endpoint, config.api_key)
    data_lake_writer = DataLakeWriter(config.data_storage_account, credential, config.data_storage_container, NAME)
    item_fetcher = ItemFetcher(grapql_client, query_by_cursor = GET_ITEMS_AFTER_CURSOR)

    # Fetch all budget data and write to storage account.
    items = item_fetcher.fetch_all_items_after_cursor()
    items_transformed = convert_dicts_to_parquet_pandas(flatten_list_of_dicts(items.get_items()), COLUMN_DTYPES)
    data_lake_writer.write_data(f"{NAME}.parquet", items_transformed)