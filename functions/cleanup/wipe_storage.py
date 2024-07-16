from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging

from shared.data_lake_writer import DataLakeWriter
from shared.environment_config import EnvironmentConfig

NAME = "wipe_storage"
logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()


@bp.function_name(NAME)
@bp.route(route=NAME, methods=["POST"], auth_level=func.AuthLevel.ADMIN)
def wipe_storage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Running wipe storage.")
    
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    ## Initialize classes needed for syncronizing data.
    data_lake_writer = DataLakeWriter(config.data_storage_account, credential, config.data_storage_container)
    data_lake_writer.delete_all_folders()

    return func.HttpResponse("Storage wiped successfully.", status_code=200)
