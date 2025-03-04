import requests
import io
import pandas as pd
from shared.utils.files import convert_xlsx_to_parquet_pandas

class FlexLinkReader:
    """
    A utility class for fetching Excel (.xlsx) files from URLs from Xledger, converting them to Parquet format,
    and handling multiple files by merging them into a single dataset.
    """

    def read_xlsx_flex_link(self, flex_link: str, column_dtypes: dict, parameter_filters: dict = None) -> io.BytesIO:
        """
        Fetches an Excel (.xlsx) file from a URL, converts it to Parquet format, and returns the result as an in-memory byte stream.

        Args:
            flex_link (str): The URL of the Excel file to be fetched.
            column_dtypes (dict): A dictionary specifying the expected data types of the columns.
            parameter_filters (dict | None, optional): A dictionary of query parameters to append to the URL. Defaults to None.

        Returns:
            io.BytesIO: An in-memory byte stream containing the Parquet data.
        """
        excel_bytes = self._read_excel_flex_link(flex_link, parameter_filters)
        return convert_xlsx_to_parquet_pandas(excel_bytes, column_dtypes)

    def read_xlsx_flex_links(self, flex_links: list, column_dtypes: dict, parameter_filters: dict = None) -> io.BytesIO:
        """
        Fetches multiple Excel (.xlsx) files from URLs, converts them to Parquet format, merges them into a single dataset,
        and returns the result as an in-memory byte stream.

        Args:
            flex_links (list[str]): A list of URLs pointing to the Excel files.
            column_dtypes (dict): A dictionary specifying the expected data types of the columns.
            parameter_filters (dict | None, optional): A dictionary of query parameters to append to the URLs. Defaults to None.

        Returns:
            io.BytesIO: An in-memory byte stream containing the merged Parquet data from all fetched Excel files.
        """
        dataframes = []
        for flex_link in flex_links:
            excel_bytes = self._read_excel_flex_link(flex_link, parameter_filters)
            df = pd.read_excel(excel_bytes)
            df = df[list(column_dtypes.keys())].astype(column_dtypes)
            dataframes.append(df)

        if not dataframes:
            raise ValueError("No valid data retrieved from the provided links.")

        # Merge all DataFrames and convert back to Parquet BytesIO.
        merged_df = pd.concat(dataframes, ignore_index=True)
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
            parameter_filters (dict | None, optional): Query parameters to append to the request. Defaults to None.

        Returns:
            io.BytesIO: An in-memory byte stream containing the raw Excel file content.
        """
        response = requests.get(flex_link, params=parameter_filters)
        response.raise_for_status()
        return io.BytesIO(response.content)
