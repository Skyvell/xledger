import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential

from shared.data_lake_writer import DataLakeWriter
from shared.environment_config import EnvironmentConfig
from shared.utils.time import get_current_time_for_filename
from shared.flex_link_reader import FlexLinkReader

from functions.flexlink_functions.part_time_employees.settings import (
    COLUMN_DTYPES
)

NAME = "part_time_employees"
OUTPUT_DIR = "part_time_employees"

logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name(f"get_{NAME}")
@bp.schedule(
    schedule="0 0 0 * * *", 
    arg_name="myTimer", 
    run_on_startup=False,
    use_monitor=False
)
def get_part_time_employees_timer(myTimer: func.TimerRequest) -> None:
    credential = DefaultAzureCredential()
    config = EnvironmentConfig()
    get_part_time_employees(credential, config)

def get_part_time_employees(credential: DefaultAzureCredential, config: EnvironmentConfig) -> None:
    data_lake_writer = DataLakeWriter(
        config.data_storage_account, 
        credential,
        config.data_storage_container, 
        OUTPUT_DIR, 
    )
    flex_link_reader = FlexLinkReader()
    
    # Flexlinks to get part time data from.
    # Some of the "bolag" have dummy data in order to generate the flex link.
    # Dummy data is excluded with the query params below.
    flex_links = []
    flex_links.append(config.part_time_data_ductus_ab_flex_link)
    flex_links.append(config.part_time_data_ductus_holding_ab_flex_link)
    flex_links.append(config.part_time_data_ductus_luleå_ab_flex_link)
    flex_links.append(config.part_time_data_ductus_inc_flex_link)
    flex_links.append(config.part_time_tromb_ab_flex_link)

    # Read data from flexlinks and write to blob storage.
    # Filter out employees with start data 1999-12-31 (dummy).
    query_params = {"d_date_from-ne": "1999-12-31"}
    data = flex_link_reader.read_xlsx_flex_links(flex_links, COLUMN_DTYPES, query_params)
    data_lake_writer.write_data(f"{NAME}.parquet", data)