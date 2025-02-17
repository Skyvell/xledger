from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging

from shared.data_lake_writer import DataLakeWriter
from shared.configuration_manager import SynchronizerStateManager
from shared.environment_config import EnvironmentConfig

from functions.flexlink_functions.financial_results.get_financial_results import get_financial_results
from functions.flexlink_functions.employee_groups.get_employee_groups import get_employee_groups
from functions.flexlink_functions.employment_types.get_employment_types import get_employment_types
from functions.flexlink_functions.employee_groups.get_employee_groups import get_employee_groups

from functions.cleanup_functions.full_data_resync.settings import (
    FINANCIAL_RESULTS_PERIODS
)


NAME = "full_data_resync"


logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name(NAME)
@bp.route(route=NAME, methods=["POST"], auth_level=func.AuthLevel.ADMIN)
def full_data_resync(req: func.HttpRequest) -> func.HttpResponse:
    credential = DefaultAzureCredential()
    config = EnvironmentConfig()

    # Reset the state of the synchronizer.
    state_manager = SynchronizerStateManager(config.app_config_endpoint, credential)
    state_manager.reset_state()

    # Delete all folders in the data lake.
    data_lake_writer = DataLakeWriter(config.data_storage_account, credential, config.data_storage_container)
    data_lake_writer.delete_all_folders()

    # Fetch all flexlink data.
    get_employee_groups(credential, config)
    get_employment_types(credential, config)
    get_employee_groups(credential, config)
    get_financial_results(credential, config, FINANCIAL_RESULTS_PERIODS)

    return func.HttpResponse("State reset, data deleted and flex links data retrieved.", status_code=200)