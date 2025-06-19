from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging

from shared.data_lake_writer import DataLakeWriter
from shared.item_fetcher import ItemFetcher
from shared.gql_client import GraphQLClient
from shared.environment_config import EnvironmentConfig
from shared.utils.time import get_first_day_of_previous_month, get_current_time_for_filename
from shared.utils.files import convert_dicts_to_parquet_pandas
from shared.utils.data_transformation import flatten_list_of_dicts

from functions.api_functions.preliminary_timesheets.queries import (
    COLUMN_DTYPES,
    GET_ITEMS_AFTER_CURSOR,
)


NAME = "preliminary_timesheets"
logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name(f"get_{NAME}")
@bp.schedule(schedule="30 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def get_preliminary_timesheets(myTimer: func.TimerRequest) -> None:
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    # Initialize classes needed for syncronizing data.
    graphql_client = GraphQLClient(config.api_endpoint, config.api_key)
    data_lake_writer = DataLakeWriter(config.data_storage_account, credential, config.data_storage_container, NAME)
    item_fetcher = ItemFetcher(graphql_client, query_by_cursor = GET_ITEMS_AFTER_CURSOR)

    # Fetch all preliminary timesheet data starting from the first day of the previous month.
    items = item_fetcher.fetch_all_items_after_cursor(filter={"assignmentDate_gte": get_first_day_of_previous_month()})
    if not items.has_items():
        return
    
    # Transform items to the required format an write to storage account.
    items_transformed = convert_dicts_to_parquet_pandas(flatten_list_of_dicts(items.get_items()), COLUMN_DTYPES)
    data_lake_writer.delete_all_files_in_directory()
    data_lake_writer.write_data(f"{get_current_time_for_filename()}-{NAME}.parquet", items_transformed)