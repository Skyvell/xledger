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
    year_month = int(get_previous_month_yy_mm())
    logging.info(f"Scheduled run for month: {year_month}")
    process_financial_results(year_month)


@bp.function_name(f"get_{NAME}_noon")
@bp.schedule(schedule="0 30 12 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def scheduled_financial_results_noon(myTimer: func.TimerRequest) -> None:
    """Scheduled execution for retrieving financial results at 12:30 PM."""
    if not is_between_days(datetime.now(ZoneInfo("Europe/Stockholm")), 7, 15, exclude_weekend_days=True):
        logging.info("Skipping scheduled run as it is not a weekday.")
        return

    year_month = int(get_previous_month_yy_mm())
    logging.info(f"Scheduled run for month: {year_month}")
    process_financial_results(year_month)


@bp.function_name(f"manual_trigger_get_{NAME}")
@bp.route(route=f"trigger-{NAME}", methods=["POST"], auth_level=func.AuthLevel.ADMIN)
def manual_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """
    Manual HTTP trigger to process financial results for a specific month.
    
    Request Body:
    {
        "month": int  # Month in YYMM format, e.g., 2409 for September 2024
    }
    
    Returns:
        HTTP 200: Success message if processing is successful.
        HTTP 400: Validation error if the input is invalid.
        HTTP 500: Internal server error for unexpected issues.
    """
    try:
        # Parse the JSON body and validate input.
        req_body = req.get_json()
        year_month = req_body.get("month")

        if not isinstance(year_month, int) or not (2000 <= year_month <= 9999):
            raise ValueError(
                "The 'month' parameter must be a valid integer in YYMM format (e.g., 2409 for September 2024)."
            )
        
        logging.info(f"Manual trigger received for month: {year_month}")
        
        # Process the financial results for the given month.
        process_financial_results(year_month)

        # Respond with success.
        return func.HttpResponse(
            f"Successfully processed data for month: {year_month}", 
            status_code=200
        )
    except ValueError as e:
        logging.warning(f"Validation error in manual trigger: {e}")
        return func.HttpResponse(
            str(e), 
            status_code=400
        )
    except Exception as e:
        logging.error(f"Unexpected error during manual trigger: {e}", exc_info=True)
        return func.HttpResponse(
            "An internal server error occurred. Please contact support.",
            status_code=500
        )


def process_financial_results(year_month: int) -> None:
    """Core logic for processing financial results."""
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
    query_params = {
        "r_period-er": YYMM_TO_PK[year_month],
        "rv_account_group-nbt": "4558532,4559413",  # Exclude balance accounts.
    }
    data = flex_link_reader.read_xlsx_flex_link(
        config.financial_results_flex_link, 
        COLUMN_DTYPES, 
        query_params
    )
    data_lake_writer.write_data(f"{year_month}-{NAME}.parquet", data)
