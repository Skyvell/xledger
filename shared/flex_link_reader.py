import requests
import io
from shared.utils.files import convert_xlsx_to_parquet_pandas

class FlexLinkReader:
    def __init__(self):
        pass

    def read_flexlink_xlsx(self, flexlink: str, column_dtypes: dict, parameter_filters: dict = None) -> io.BytesIO:
        if parameter_filters:
            for key, val in parameter_filters.items():
                flexlink += f"&{key}={val}"
            
        response = requests.get(flexlink)
        if response.status_code == 200:
            data_bytes_xlsx = io.BytesIO(response.content)
            data_bytes_parquet = convert_xlsx_to_parquet_pandas(data_bytes_xlsx, column_dtypes)
            return data_bytes_parquet
        else:
            raise requests.exceptions.HTTPError(f"Failed to retrieve data from the flexlink. HTTP Status Code: {response.status_code}")
