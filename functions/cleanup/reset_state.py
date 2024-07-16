from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging

from shared.configuration_manager import SynchronizerStateManager
from shared.environment_config import EnvironmentConfig

NAME = "reset_state"
logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()


@bp.function_name(NAME)
@bp.route(route=NAME, methods=["POST"], auth_level=func.AuthLevel.ADMIN)
def reset_state(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Running reset state.")
    
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    ## Initialize classes needed for syncronizing data.
    state_manager = SynchronizerStateManager(config.app_config_endpoint, credential)
    state_manager.reset_state()

    return func.HttpResponse("State reset successfully.", status_code=200)
