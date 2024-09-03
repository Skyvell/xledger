from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging
import requests
import json

from shared.data_lake_writer import DataLakeWriter
from shared.environment_config import EnvironmentConfig
from shared.utils.time import get_current_time_for_filename


NAME = "test_report"
URL = "https://demo.xledger.net/Flex/112706065476351.json?t=Ag9kyXxwAhgnxT4TaYtdjhWRsxAhGVm3-0F5Hg2e-ZE_QfCHSnthWVilJDUcXU3wVzDTLBV8Ty1scDOeXL2Etxn9rf3ma7Cmpxrqi8ph-LC1RdTAdVNyFl6uA_4w4d7K1ejE74u1tfrSZBs1sEUJ-cGA5dzKmaH2vAzDN9pHDsuHsPV0ewZO7Rxr8RMCGKAR67s_-E_Tns5LvzBbLwrmfiAOlR8dRuZJRVmhft-lw0kH6YehRBVD9X_LSBx9KJTRhWBfqCtZ1tCUGQxu2bL8oEh0eu2lIxh2T3mPa3IDKibrMfb3NxfnQxdtp9UU6zd1FLjmjSt0KCPqCBt4EuNl"

logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name(NAME)
@bp.schedule(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def report(myTimer: func.TimerRequest) -> None:
    # Get credentials.
    credential = DefaultAzureCredential()

    # Get environment variables.
    config = EnvironmentConfig()

    # Initialize writer.
    data_lake_writer = DataLakeWriter(config.data_storage_account, credential, config.data_storage_container, NAME)

    # Get the report data and write to storage.
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        data_lake_writer.write_data(f"{get_current_time_for_filename()}-{NAME}.json", json.dumps(data))

    else:
        print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")

