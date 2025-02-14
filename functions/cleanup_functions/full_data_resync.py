from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging

from shared.data_lake_writer import DataLakeWriter
from shared.configuration_manager import SynchronizerStateManager
from shared.environment_config import EnvironmentConfig
from shared.utils.time import get_previous_month_yy_mm, generate_periods
from functions.flexlink_functions.financial_results.get_financial_results import process_financial_results
from functions.flexlink_functions.employee_groups.get_employee_groups import get_employee_groups
from functions.flexlink_functions.employment_types.get_employment_types import write_employment_types

NAME = "full_data_resync"
FINANCIAL_RESULTS_START_PERIOD = 2401
FINANCIAL_RESULTS_END_PERIOD = get_previous_month_yy_mm()
logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()


@bp.function_name(NAME)
@bp.route(route=NAME, methods=["POST"], auth_level=func.AuthLevel.ADMIN)
def reset_state_and_wipe_storage(req: func.HttpRequest) -> func.HttpResponse:
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

    # Fetch all financial reports.
    process_financial_results(generate_periods(FINANCIAL_RESULTS_START_PERIOD, FINANCIAL_RESULTS_END_PERIOD))

    # Fetch all other flexlink reports.
    get_employee_groups(credential, config)
    write_employment_types(credential, config)


    return func.HttpResponse("Storage wiped and syncronizer state reset successfully.", status_code=200)