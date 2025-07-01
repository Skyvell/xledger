from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging

from shared.data_lake_writer import DataLakeWriter
from shared.item_fetcher import ItemFetcher
from shared.gql_client import GraphQLClient
from shared.environment_config import EnvironmentConfig
from shared.utils.time import get_first_day_of_previous_month, get_current_time_for_filename, is_between_days
from shared.utils.files import convert_dicts_to_parquet_pandas
from shared.utils.data_transformation import flatten_list_of_dicts

from functions.api_functions.preliminary_timesheets.queries import (
    COLUMN_DTYPES,
    GET_ITEMS_AFTER_CURSOR,
)


NAME = "preliminary_timesheets"
logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name(f"get_{NAME}_first_of_month")
@bp.schedule(schedule="25,55 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def get_preliminary_timesheets_first_of_month(myTimer: func.TimerRequest) -> None:
    # Only run this schedule if first of every month.
    if not is_between_days(myTimer.current_time, 1, 1, exclude_weekend_days=True):
        logging.info("Skipping scheduled run as it is not the first of the month.")
        return

    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    # Call the function to get preliminary timesheets.
    get_preliminary_timesheets(credential, config)

@bp.function_name(f"get_{NAME}_daily")
@bp.schedule(schedule="0 22 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def get_preliminary_timesheets_daily(myTimer: func.TimerRequest) -> None:
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    # Call the function to get preliminary timesheets.
    get_preliminary_timesheets(credential, config)

def get_preliminary_timesheets(credential: DefaultAzureCredential, config: EnvironmentConfig) -> None:
    """
    Function to get preliminary timesheets data.
    
    Args:
        credential (DefaultAzureCredential): Azure credentials for authentication.
        config (EnvironmentConfig): Environment configuration containing API and storage settings.
    """
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