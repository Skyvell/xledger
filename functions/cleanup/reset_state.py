from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging

from shared.configuration_manager import SynchronizerStateManager
from shared.environment_config import EnvironmentConfig

NAME = "reset_state"
logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

# This schedule will never run. February does not have 31 days.
# This function should only be triggered manually via the azure portal.
@bp.function_name(NAME)
@bp.schedule(schedule="0 0 31 2 * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def reset_state(myTimer: func.TimerRequest) -> None:
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    ## Initialize classes needed for syncronizing data.
    state_manager = SynchronizerStateManager(config.app_config_endpoint, credential)
    state_manager.reset_state()
