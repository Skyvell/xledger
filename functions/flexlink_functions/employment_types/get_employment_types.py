import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential

from shared.data_lake_writer import DataLakeWriter
from shared.environment_config import EnvironmentConfig
from shared.utils.time import get_current_time_for_filename
from shared.flex_link_reader import FlexLinkReader

from functions.flexlink_functions.employment_types.settings import (
    COLUMN_DTYPES
)

NAME = "employment_types"
OUTPUT_DIR = "employment_types"

logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name(f"get_{NAME}")
@bp.schedule(
    schedule="0 0 0 * * *", 
    arg_name="myTimer", 
    run_on_startup=False,
    use_monitor=False
)
def get_employment_types_timer(myTimer: func.TimerRequest) -> None:
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    # Get and write employment types to Azure.
    get_employment_types(credential, config)

def get_employment_types(credential: DefaultAzureCredential, config: EnvironmentConfig) -> None:
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
    data = flex_link_reader.read_xlsx_flex_link(config.emploment_types_flex_link, COLUMN_DTYPES)
    data_lake_writer.write_data(f"{NAME}.parquet", data)