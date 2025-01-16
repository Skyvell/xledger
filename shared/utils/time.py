from datetime import datetime
from dateutil.relativedelta import relativedelta


def generate_iso_8601_timestamp(remove_microseconds: bool = True):
    """
    Generates the current date and time in ISO 8601 format.
    
    Args:
        remove_microseconds (bool): If True, the microseconds part will be removed. Default is True.
    
    Returns:
        str: The current date and time in ISO 8601 format.
    """
    current_time = datetime.now()
    if remove_microseconds:
        current_time = current_time.replace(microsecond=0)
    return current_time.isoformat()


def get_current_time_for_filename():
    """
    Retrieves the current system time and formats it as a string suitable for file naming.

    This function fetches the current datetime using the system's local time and formats it
    into a compact form. The output format is 'YYYYMMDD_HH_MM_SS', where:
    - YYYY: Full year
    - MM: Month (01 to 12)
    - DD: Day of the month (01 to 31)
    - HH: Hour in 24-hour format (00 to 23)
    - MM: Minute (00 to 59)
    - SS: Second (00 to 59)
    
    The formatted time is useful for generating time-stamped filenames to ensure uniqueness or
    for sorting files chronologically based on their creation time.

    Returns:
        str: The current datetime formatted as 'YYYYMMDD_HH_MM_SS'.
    """
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y%m%d_%H_%M_%S')
    return formatted_time


def get_previous_month_yy_mm():
    """
    Calculate and return the year and month of the previous month in YYMM format.

    The function determines the current date, subtracts one month using the `relativedelta`
    module, and formats the resulting year and month as a two-digit year and two-digit month.

    Returns:
        str: A string representing the year and month of the previous month in YYMM format.
             For example, if the current date is January 2024, the output will be '2312'.

    Example:
        >>> get_previous_month_yy_mm()
        '2312'  # Assuming the current date is January 2024
    """
    # Get today's date.
    today = datetime.now()

    # Subtract one month using relativedelta.
    previous_month_date = today - relativedelta(months=1)

    # Format year and month as YYMM.
    return f"{previous_month_date.year % 100:02}{previous_month_date.month:02}"