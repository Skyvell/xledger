from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging
import os
from datetime import timedelta, datetime, timezone
from shared.configuration_manager import SynchronizerStateManager
from shared.environment_config import EnvironmentConfig

NAME = "sync_healthchech"
SCHEDULE = os.getenv("SYNC_HEALTHCHECH_SCHEDULE")
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

@bp.function_name(NAME)
@bp.schedule(schedule=SCHEDULE, arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def sync_healthcheck(myTimer: func.TimerRequest) -> None:
    logging.info("Sync healthcheck function triggered.")

    credential = DefaultAzureCredential()
    config = EnvironmentConfig()
    now = datetime.now(timezone.utc)

    for function_name, threshold in SYNC_FUNCTIONS_WARNING_THRESHOLDS.items():
        prefix = function_name + "-"
        state_manager = SynchronizerStateManager(config.app_config_endpoint, credential, prefix)
        updated_at = state_manager.delta_cursor_updated_at

        if updated_at is None:
            logging.warning(
                f"[{function_name}] No delta_cursor_updated_at timestamp found.",
                extra={
                    "custom_dimensions": {
                        "sync_function": function_name,
                        "healthcheck": "sync_missing"
                    }
                }
            )
            continue

        age = now - updated_at

        if age > threshold:
            logging.warning(
                f"[{function_name}] Sync stale ({age.days}d > {threshold.days}d)",
                extra={
                    "custom_dimensions": {
                        "sync_function": function_name,
                        "last_updated": updated_at.isoformat(),
                        "threshold_days": threshold.days,
                        "age_days": age.days,
                        "healthcheck": "sync_stale"
                    }
                }
            )
        else:
            logging.info(
                f"[{function_name}] Sync OK: {updated_at.isoformat()} ({age.days}d)",
                extra={
                    "custom_dimensions": {
                        "sync_function": function_name,
                        "last_updated": updated_at.isoformat(),
                        "age_days": age.days,
                        "threshold_days": threshold.days,
                        "healthcheck": "sync_ok"
                    }
                }
            )
