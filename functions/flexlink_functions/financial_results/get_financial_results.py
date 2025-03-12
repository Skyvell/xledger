import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from shared.data_lake_writer import DataLakeWriter
from shared.environment_config import EnvironmentConfig
from shared.utils.time import get_previous_month_yy_mm, is_between_days
from shared.flex_link_reader import FlexLinkReader
from functions.flexlink_functions.financial_results.settings import (
    COLUMN_DTYPES,
    YYMM_TO_PK,
)
from datetime import datetime
from zoneinfo import ZoneInfo

NAME = "financial_results"
OUTPUT_DIR = "financial_results"

logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name(f"get_{NAME}_midnight")
@bp.schedule(schedule="0 0 0 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def scheduled_financial_results_midnight(myTimer: func.TimerRequest) -> None:
    """Scheduled execution for retrieving financial results."""
    credential = DefaultAzureCredential()
    config = EnvironmentConfig()
    
    period = int(get_previous_month_yy_mm())
    logging.info(f"Scheduled run for period: {period}")
    get_financial_results(credential, config, [period])

@bp.function_name(f"get_{NAME}_noon")
@bp.schedule(schedule="0 50 11 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def scheduled_financial_results_noon(myTimer: func.TimerRequest) -> None:
    """Scheduled execution for retrieving financial results at 11:50 PM."""
    credential = DefaultAzureCredential()
    config = EnvironmentConfig()
    
    if not is_between_days(datetime.now(ZoneInfo("Europe/Stockholm")), 7, 15, exclude_weekend_days=True):
        logging.info("Skipping scheduled run as it is not a weekday.")
        return

    period = int(get_previous_month_yy_mm())
    logging.info(f"Scheduled run for period: {period}")
    get_financial_results(credential, config, [period])

@bp.function_name(f"manual_trigger_get_{NAME}")
@bp.route(route=f"trigger-{NAME}", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def manual_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """
    Manual HTTP trigger to get financial results for specific periods.
    
    Request Body:
    {
        "periods": int | list[int]  # Single or multiple periods in YYMM format, e.g., 2409 or [2409, 2410]
    }
    
    Returns:
        HTTP 200: Success message if retrieving the financial results is successful.
        HTTP 400: Validation error if the input is invalid.
        HTTP 500: Internal server error for unexpected issues.
    """
    credential = DefaultAzureCredential()
    config = EnvironmentConfig()
    
    try:
        req_body = req.get_json()
        periods = req_body.get("periods")

        if not periods:
            raise ValueError("The 'periods' parameter is required.")

        periods = [periods] if isinstance(periods, int) else periods

        if not all(isinstance(p, int) and 2000 <= p <= 9999 for p in periods):
            raise ValueError(
                "The 'periods' parameter must be a single integer or a list of valid integers in YYMM format (e.g., 2409, 2410)."
            )
        
        logging.info(f"Manual trigger received for periods: {periods}")
        
        get_financial_results(credential, config, periods)

        return func.HttpResponse(
            f"Successfully processed data for periods: {', '.join(map(str, periods))}", 
            status_code=200
        )
    except ValueError as e:
        logging.warning(f"Validation error in manual trigger: {e}")
        return func.HttpResponse(str(e), status_code=400)
    except Exception as e:
        logging.error(f"Unexpected error during manual trigger: {e}", exc_info=True)
        return func.HttpResponse("An internal server error occurred. Please contact support.", status_code=500)

def get_financial_results(credential: DefaultAzureCredential, config: EnvironmentConfig, periods: list[int]) -> None:
    """
    Retrieves financial results for multiple periods and writes the data to Azure Data Lake.
    
    Args:
        credential (DefaultAzureCredential): Azure authentication credential.
        config (EnvironmentConfig): Configuration settings.
        periods (list[int]): A list of financial periods in YYMM format (e.g., [2409, 2410]).
    
    Raises:
        KeyError: If a period is not found in the `YYMM_TO_PK` mapping.
        Exception: If an error occurs during data retrieval or storage.
    
    Returns:
        None
    """
    data_lake_writer = DataLakeWriter(
        config.data_storage_account,
        credential,
        config.data_storage_container,
        OUTPUT_DIR,
    )
    flex_link_reader = FlexLinkReader()

    for period in periods:
        logging.info(f"Retrieving financial results for period: {period}")

        query_params = {
            "r_period-er": YYMM_TO_PK[period],
            "rv_account_group-nbt": "4558532,4559413",
        }
        data = flex_link_reader.read_xlsx_flex_link(
            config.financial_results_flex_link, 
            COLUMN_DTYPES, 
            query_params
        )
        data_lake_writer.write_data(f"{period}-{NAME}.parquet", data)

    logging.info(f"Finished retrieving financial results for periods: {periods}")