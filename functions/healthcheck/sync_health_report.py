from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging
import os
from datetime import datetime, timezone
from dateutil.parser import isoparse

from shared.configuration_manager import SynchronizerStateManager
from shared.environment_config import EnvironmentConfig
from shared.logging import configure_application_logger
from functions.healthcheck.config import SYNC_ALERT_THRESHOLDS_BY_FUNCTION
from functions.healthcheck.report import SyncFunctionHealthReport

NAME = "sync_health_check"
SCHEDULE = os.getenv("SYNC_HEALTH_CHECK_SCHEDULE")

logger = configure_application_logger(
    name = "sync_health_check",
    log_level = logging.INFO,
    connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", "")
)

bp = func.Blueprint()

@bp.function_name(NAME)
@bp.schedule(schedule=SCHEDULE, arg_name="myTimer", run_on_startup=False, use_monitor=False)
def sync_health_check(myTimer: func.TimerRequest) -> None:
    credential = DefaultAzureCredential()
    config = EnvironmentConfig()

    for function_name, threshold in SYNC_ALERT_THRESHOLDS_BY_FUNCTION.items():
        state_manager = SynchronizerStateManager(
            config.app_config_endpoint,
            credential,
            function_name + "-"
        )

        last_updated_iso = state_manager.delta_cursor_updated_at
        last_updated_at = isoparse(last_updated_iso) if last_updated_iso else None

        report = SyncFunctionHealthReport(
            function_name=function_name,
            time_until_warning=threshold,
            last_updated_at=last_updated_at,
            logger=logger
        )
        report.emit_telemetry(datetime.now(datetime.now(timezone.utc)))