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
    period = int(get_previous_month_yy_mm())
    logging.info(f"Scheduled run for period: {period}")
    process_financial_results([period])

@bp.function_name(f"get_{NAME}_noon")
@bp.schedule(schedule="0 30 12 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def scheduled_financial_results_noon(myTimer: func.TimerRequest) -> None:
    """Scheduled execution for retrieving financial results at 12:30 PM."""
    if not is_between_days(datetime.now(ZoneInfo("Europe/Stockholm")), 7, 15, exclude_weekend_days=True):
        logging.info("Skipping scheduled run as it is not a weekday.")
        return

    period = int(get_previous_month_yy_mm())
    logging.info(f"Scheduled run for period: {period}")
    process_financial_results([period])

@bp.function_name(f"manual_trigger_get_{NAME}")
@bp.route(route=f"trigger-{NAME}", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def manual_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """
    Manual HTTP trigger to process financial results for specific periods.
    
    Request Body:
    {
        "periods": int | list[int]  # Single or multiple periods in YYMM format, e.g., 2409 or [2409, 2410]
    }
    
    Returns:
        HTTP 200: Success message if processing is successful.
        HTTP 400: Validation error if the input is invalid.
        HTTP 500: Internal server error for unexpected issues.
    """
    try:
        req_body = req.get_json()
        periods = req_body.get("periods")

        if not periods:
            raise ValueError("The 'periods' parameter is required.")

        # Ensure periods is a list.
        periods = [periods] if isinstance(periods, int) else periods

        if not all(isinstance(p, int) and 2000 <= p <= 9999 for p in periods):
            raise ValueError(
                "The 'periods' parameter must be a single integer or a list of valid integers in YYMM format (e.g., 2409, 2410)."
            )
        
        logging.info(f"Manual trigger received for periods: {periods}")
        
        process_financial_results(periods)

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

def process_financial_results(periods: list[int]) -> None:
    """
    Processes financial results for multiple periods and writes the data to Azure Data Lake.

    This function retrieves financial results for the specified periods by querying 
    the FlexLink data source, applying necessary filters, and storing the results 
    as Parquet files in Azure Data Lake.

    Args:
        periods (list[int]): A list of financial periods in YYMM format (e.g., [2409, 2410]).

    Workflow:
        1. Initializes Azure authentication credentials.
        2. Loads environment configuration settings.
        3. Instantiates a DataLakeWriter for writing processed data.
        4. Uses FlexLinkReader to fetch financial results for each period.
        5. Applies necessary query filters to exclude balance accounts.
        6. Writes the processed data as Parquet files, named in the format `{YYMM}-financial_results.parquet`.
        7. Logs processing steps and completion status.

    Logs:
        - Logs the start and end of processing for each period.
        - Logs overall processing completion.

    Raises:
        KeyError: If a period is not found in the `YYMM_TO_PK` mapping.
        Exception: If an error occurs during data retrieval or storage.

    Returns:
        None
    """
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

    for period in periods:
        logging.info(f"Processing financial results for period: {period}")

        # Read data from FlexLink and write to blob storage.
        query_params = {
            "r_period-er": YYMM_TO_PK[period],

            # Exclude balance accounts.
            "rv_account_group-nbt": "4558532,4559413",
        }
        data = flex_link_reader.read_xlsx_flex_link(
            config.financial_results_flex_link, 
            COLUMN_DTYPES, 
            query_params
        )
        data_lake_writer.write_data(f"{period}-{NAME}.parquet", data)

    logging.info(f"Finished processing financial results for periods: {periods}")