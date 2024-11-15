import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential

from shared.data_lake_writer import DataLakeWriter
from shared.environment_config import EnvironmentConfig
from shared.utils.time import get_current_time_for_filename
from shared.flex_link_reader import FlexLinkReader

from functions.flexlink_functions.project_cost_setups.settings import (
    COLUMN_DTYPES, 
    FLEX_LINK
)

NAME = "project_cost_setups"
OUTPUT_DIR = "setups"

logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name(f"get_{NAME}")
@bp.schedule(
    schedule="0 0 0 * * *", 
    arg_name="myTimer", 
    run_on_startup=False,
    use_monitor=False
)
def report(myTimer: func.TimerRequest) -> None:
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    # Initialize writer.
    data_lake_writer = DataLakeWriter(
        config.data_storage_account, 
        credential,
        config.data_storage_container, 
        OUTPUT_DIR, 
    )

    # Initialize FlexLinkReader.
    flex_link_reader = FlexLinkReader()
    
    # Read data from flexlink and write to blob storage.
    data = flex_link_reader.read_xlsx_flex_link(FLEX_LINK, COLUMN_DTYPES)
    data_lake_writer.write_data(f"{NAME}.parquet", data)