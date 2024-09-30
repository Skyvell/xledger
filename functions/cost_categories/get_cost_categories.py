from azure import functions as func
from azure.identity import DefaultAzureCredential
import logging
import requests
import io

from shared.data_lake_writer import DataLakeWriter
from shared.environment_config import EnvironmentConfig
from shared.utils.time import get_current_time_for_filename
from shared.utils.files import convert_xlsx_to_parquet_pandas

from functions.cost_categories.columns import COLUMN_DTYPES


NAME = "cost_categories"
URL = "https://demo.xledger.net/Flex/112706066960924.xlsx?t=Ag9kyeRaNrajDAdVN-yO371sV0PiVRIO_gwW9-OGTDebjFLLcEK5wzPh90enehKTiekbP4i7tKinC3TZJb3EU3OjfiYvNf_oI-DV1OUHR6qZmyw0ZAV96mWLoJ3Y3HRd3sAr4scGXNuzpThaBBQiNhYvTJHtqzasZOW2vYFaiK_68ot2VAmQL7dSB9p-51PIOb4YnIAjbMydiBu-PEa2YfV-eIfR3X1zzai9K_GLFR-gmyUmWzt5ddjmDXiDXn41dApzxEIKvROP3WAlf5_BDw717ygLXX0EcskyBQPnPGncvQhuF2CtOO2v86tsQLFWMsV61PeD4k5vR9MReBsd"

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
        data = io.BytesIO(response.content)
        data = convert_xlsx_to_parquet_pandas(data, column_dtypes=COLUMN_DTYPES)
        data_lake_writer.write_data(f"{get_current_time_for_filename()}-{NAME}.parquet", data)

    else:
        print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")