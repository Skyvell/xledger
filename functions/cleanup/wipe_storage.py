from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging

from shared.data_lake_writer import DataLakeWriter
from shared.environment_config import EnvironmentConfig

NAME = "wipe_storage"
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
    data_lake_writer = DataLakeWriter(config.data_storage_account, credential, config.data_storage_container)
    data_lake_writer.delete_all_folders()
