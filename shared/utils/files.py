import io
import csv
import pandas as pd


def convert_dicts_to_csv(data: list[dict], separator: str = ';', encoding: str = 'utf-8') -> str:
    """
    Convert a list of dictionaries to a CSV formatted string.
    
    Parameters:
        data (list[dict]): A list of dictionaries to convert to CSV.
        separator (str): The separator character used in the CSV file (default is ';').
        encoding (str): The encoding format for the CSV content (default is 'utf-8').
    
    Returns:
        str: The CSV formatted string.
    """
    # Get the column names from the first dictionary in the list
    column_names = list(data[0].keys())

    # Use StringIO to mimic file writing.
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=column_names, delimiter=separator)

    # Write the CSV data to the StringIO buffer
    writer.writeheader()
    for item in data:
        writer.writerow(item)

    # Get the CSV data as a string
    csv_data = output.getvalue()
    output.close()

    return csv_data


def write_buffer_to_file(buffer: io.BytesIO, file_path: str) -> None:
    """
    Writes the contents of a buffer to a specified file.

    Args:
        buffer (io.BytesIO): The buffer containing data to write.
        file_path (str): The path to the file where the data should be saved.

    Returns:
        None
    """
    # Ensure the buffer's position is at the beginning
    buffer.seek(0)

    # Open the file in binary write mode and write the buffer
    with open(file_path, 'wb') as f:
        f.write(buffer.read())


def convert_dicts_to_parquet_pandas(data: list[dict], column_dtypes: dict) -> io.BytesIO:
    """
    Convert a list of dictionaries to a Parquet file stored in a BytesIO buffer.

    Parameters:
    data (list[dict]): A list of dictionaries containing the data.
    column_dtypes (dict): A dictionary mapping column names to their data types.

    Returns:
    io.BytesIO: A BytesIO buffer containing the Parquet file.
    """
    # Create a DataFrame from the list of dictionaries, including only specified columns.
    df = pd.DataFrame(data, columns=column_dtypes.keys()).astype(column_dtypes)
    
    # Create a BytesIO buffer to hold the Parquet data.
    buffer = io.BytesIO()
    
    # Write the DataFrame to the buffer in Parquet format, excluding the index.
    df.to_parquet(buffer, engine='pyarrow', index=False)
    
    # Reset the buffer's position to the beginning.
    buffer.seek(0)
    
    # Return the buffer containing the Parquet data.
    return buffer

def convert_xlsx_to_parquet_pandas(data: io.BytesIO, column_dtypes: dict) -> io.BytesIO:
    """
    Converts an Excel (.xlsx) file from a BytesIO stream into a Parquet file stored in a BytesIO buffer.

    Parameters:
        data (io.BytesIO): A BytesIO stream containing the Excel file.
        column_dtypes (dict): A dictionary mapping column names to their desired data types.

    Returns:
        io.BytesIO: A BytesIO buffer containing the Parquet file.
    """

    # Read the Excel file into a DataFrame, including only specified columns,
    # and convert the data types of the columns.
    df = pd.read_excel(data)
    df = df[list(column_dtypes.keys())].astype(column_dtypes)
    
    # Create a BytesIO buffer to hold the Parquet data.
    buffer = io.BytesIO()
    
    # Write the DataFrame to the buffer in Parquet format, excluding the index.
    df.to_parquet(buffer, engine='pyarrow', index=False)
    
    # Reset the buffer's position to the beginning.
    buffer.seek(0)
    
    # Return the buffer containing the Parquet data.
    return buffer
