from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging
import os
from datetime import timedelta
from shared.configuration_manager import SynchronizerStateManager
from shared.environment_config import EnvironmentConfig

NAME = "sync_healthchech"
SCHEDULE = os.getenv("SYNC_HEALTHCHECH_SCHEDULE")

# If the sync
SYNC_FUNCTIONS_WARNING_THRESHOLDS = {
    "ap_transactions": timedelta(days=3),
    "ar_transactions": timedelta(days=3),
    "customers": timedelta(days=7),
    "employees": timedelta(days=7),
    "projects": timedelta(days=7),
    "suppliers": timedelta(days=7),
    "timesheets": timedelta(days=3),
    "transactions": timedelta(days=3),
}

logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name(f"syncronize_{NAME}")
@bp.schedule(schedule=SCHEDULE, arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def syncronize(myTimer: func.TimerRequest) -> None:
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    for function in SYNC_FUNCTIONS_WARNING_THRESHOLDS:
        prefix = function + "-"
        state_manager = SynchronizerStateManager(config.app_config_endpoint, credential, prefix)