import requests
import io
from shared.utils.files import convert_xlsx_to_parquet_pandas

class FlexLinkReader:
    """
    A utility class for fetching Excel (.xlsx) files from a URL and converting them to Parquet format.
    """

    def read_xlsx_flex_link(self, flex_link: str, column_dtypes: dict, parameter_filters: dict = None) -> io.BytesIO:
        """
        Fetches an Excel file, converts it to Parquet, and returns it as a byte stream.

        Args:
            flex_link (str): URL of the Excel file.
            column_dtypes (dict): Column data types for conversion.
            parameter_filters (dict, optional): Query parameters for the request.

        Returns:
            io.BytesIO: Parquet data as a byte stream.

        Raises:
            requests.exceptions.HTTPError: If the request fails.
        """
        if parameter_filters:
            response = requests.get(flex_link, params=parameter_filters)
        else:
            response = requests.get(flex_link)
            
        if response.status_code == 200:
            data_bytes_xlsx = io.BytesIO(response.content)
            return convert_xlsx_to_parquet_pandas(data_bytes_xlsx, column_dtypes)
        else:
            raise requests.exceptions.HTTPError(f"Failed to retrieve data from the flex_link. HTTP Status Code: {response.status_code}")