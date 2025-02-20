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
    flex_links = []
    flex_links.append(config.part_time_data_ductus_ab_flex_link)
    flex_links.append(config.part_time_data_ductus_holding_ab_flex_link)
    flex_links.append(config.part_time_data_ductus_luleå_ab_flex_link)

    # No part time employees for these yet, so cant add a flex link.
    # flex_links.append(config.part_time_data_ductus_inc_flex_link)
    # flex_links.append(config.part_time_tromb_ab_flex_link)

    # Read data from flexlinks and write to blob storage.
    data = flex_link_reader.read_xlsx_flex_links(config.emploment_types_flex_link, COLUMN_DTYPES)
    data_lake_writer.write_data(f"{NAME}.parquet", data)