from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging

from shared.data_lake_writer import DataLakeWriter
from shared.configuration_manager import SynchronizerStateManager
from shared.environment_config import EnvironmentConfig

NAME = "reset_state_and_wipe_storage"
logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()


@bp.function_name(NAME)
@bp.route(route=NAME, methods=["POST"], auth_level=func.AuthLevel.ADMIN)
def reset_state_and_wipe_storage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Running running reset state and wipe storage.")
    
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    # Reset the state of the synchronizer.
    logging.info("Resetting syncronizer state.")
    state_manager = SynchronizerStateManager(config.app_config_endpoint, credential)
    state_manager.reset_state()
    logging.info("Syncronizer state reset successfully.")

    # Delete all folders in the data lake.
    logging.info("Deleting all folders in the data lake.")
    data_lake_writer = DataLakeWriter(config.data_storage_account, credential, config.data_storage_container)
    data_lake_writer.delete_all_folders()
    logging.info("All folders deleted successfully.") 

    return func.HttpResponse("Storage wiped and syncronizer state reset successfully.", status_code=200)