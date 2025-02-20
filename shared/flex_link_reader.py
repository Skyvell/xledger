import requests
import io
import pandas as pd
from shared.utils.files import convert_xlsx_to_parquet_pandas

class FlexLinkReader:
    """
    A utility class for fetching Excel (.xlsx) files from URLs, converting them to Parquet format,
    and handling multiple files by merging them into a single dataset.
    """

    def read_xlsx_flex_link(self, flex_link: str, column_dtypes: dict, parameter_filters: dict = None) -> io.BytesIO:
        """
        Fetches an Excel (.xlsx) file from a URL, converts it to Parquet format, and returns the result as an in-memory byte stream.

        Args:
            flex_link (str): The URL of the Excel file to be fetched.
            column_dtypes (dict): A dictionary specifying the expected data types of the columns.
            parameter_filters (dict, optional): A dictionary of query parameters to append to the URL. If None, no filters are applied.

        Returns:
            io.BytesIO: An in-memory byte stream containing the Parquet data.

        Raises:
            requests.exceptions.RequestException: Raised when the request to retrieve the Excel file fails.
        """
        excel_bytes = self._read_excel_flex_link(flex_link, parameter_filters)
        return convert_xlsx_to_parquet_pandas(excel_bytes, column_dtypes)

    def read_xlsx_flex_links(self, flex_links: list, column_dtypes: dict, parameter_filters: dict = None) -> io.BytesIO:
        """
        Fetches multiple Excel (.xlsx) files from URLs, converts them to Parquet format, merges them into a single dataset,
        and returns the result as an in-memory byte stream.

        Args:
            flex_links (list): A list of URLs pointing to the Excel files.
            column_dtypes (dict): A dictionary specifying the expected data types of the columns.
            parameter_filters (dict, optional): A dictionary of query parameters to append to the URLs. If None, no filters are applied.

        Returns:
            io.BytesIO: An in-memory byte stream containing the merged Parquet data from all fetched Excel files.

        Raises:
            requests.exceptions.RequestException: Propagates if any request to retrieve an Excel file fails.
            ValueError: Raised if no valid data is retrieved from the provided links.
        """
        dataframes = []
        for flex_link in flex_links:
            excel_bytes = self._read_excel_flex_link(flex_link, parameter_filters)
            df = pd.read_excel(excel_bytes)
            df = df[list(column_dtypes.keys())].astype(column_dtypes)
            dataframes.append(df)

        if not dataframes:
            raise ValueError("No valid data retrieved from the provided links.")

        # Merge all DataFrames.
        merged_df = pd.concat(dataframes, ignore_index=True)

        # Convert merged DataFrame back to Parquet BytesIO.
        output_buffer = io.BytesIO()
        merged_df.to_parquet(output_buffer, engine='pyarrow', index=False)

        # Reset buffer position for reading.
        output_buffer.seek(0)
        
        return output_buffer
    
    def _read_excel_flex_link(self, flex_link: str, parameter_filters: dict = None) -> io.BytesIO:
        """
        Internal method to fetch an Excel (.xlsx) file from a URL and return it as an in-memory byte stream.

        Args:
            flex_link (str): The URL of the Excel file.
            parameter_filters (dict, optional): Query parameters to append to the request.

        Returns:
            io.BytesIO: An in-memory byte stream containing the raw Excel file content.

        Raises:
            requests.exceptions.RequestException: Raised when the request fails.
        """
        response = requests.get(flex_link, params=parameter_filters)
        response.raise_for_status()
        return io.BytesIO(response.content)
