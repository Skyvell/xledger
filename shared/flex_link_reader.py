import requests
import io
from shared.utils.files import convert_xlsx_to_parquet_pandas

class FlexLinkReader:
    def __init__(self):
        pass

    def read_flexlink_xlsx(self, flexlink: str, column_dtypes: dict, parameter_filters: dict = None) -> io.BytesIO:
        """
        Fetches an Excel (.xlsx) file from a URL, converts it to Parquet format, and returns the result as an in-memory byte stream.

        Args:
            flexlink (str): The URL of the Excel file to be fetched.
            column_dtypes (dict): A dictionary specifying the data types of the columns to be included during the conversion to Parquet.
            parameter_filters (dict, optional): A dictionary of query parameters to append to the URL. If None, no filters are applied.

        Returns:
            io.BytesIO: A byte stream containing the Parquet data converted from the Excel file.

        Raises:
            requests.exceptions.HTTPError: Raised when the request to retrieve the Excel file fails.
        """
        if parameter_filters:
            response = requests.get(flexlink, params=parameter_filters)
        else:
            response = requests.get(flexlink)
            
        if response.status_code == 200:
            data_bytes_xlsx = io.BytesIO(response.content)
            data_bytes_parquet = convert_xlsx_to_parquet_pandas(data_bytes_xlsx, column_dtypes)
            return data_bytes_parquet
        else:
            raise requests.exceptions.HTTPError(f"Failed to retrieve data from the flexlink. HTTP Status Code: {response.status_code}")
