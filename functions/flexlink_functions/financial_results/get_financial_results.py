import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential

from shared.data_lake_writer import DataLakeWriter
from shared.environment_config import EnvironmentConfig
from shared.utils.time import (
    get_previous_month_yy_mm
)
from shared.flex_link_reader import FlexLinkReader

from functions.flexlink_functions.financial_results.settings import (
    COLUMN_DTYPES,
    YYMM_TO_PK
)

NAME = "financial_results"
OUTPUT_DIR = "financial_results"

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
    
    # Get the previous month in the format "yy-mm".
    year_month = int(get_previous_month_yy_mm())

    # Read data from flexlink and write to blob storage.
    query_params = {
        "r_period-er": YYMM_TO_PK[year_month],

        # Will exclude accounts that are balance accounts.
        "rv_account_group-nbt": "4558532,4559413"
    }
    data = flex_link_reader.read_xlsx_flex_link(config.generator_report_flex_link, COLUMN_DTYPES, query_params)
    data_lake_writer.write_data(f"{year_month}-{NAME}.parquet", data)