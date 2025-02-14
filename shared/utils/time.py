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


def is_between_days(
    date: datetime,
    start_day: int,
    end_day: int,
    exclude_weekend_days: bool = False
) -> bool:
    """
    Check if the given date is within the start and end days (inclusive) in a month,
    optionally excluding weekends.

    Args:
        date (datetime): The date to check.
        start_day (int): The starting day of the range.
        end_day (int): The ending day of the range.
        exclude_weekend_days (bool): Whether to exclude weekends in the range.

    Returns:
        bool: True if the date meets the criteria; False otherwise.
    """
    # Check if the date falls within the day range.
    is_in_range = start_day <= date.day <= end_day

    # Check if it's a weekend. 5 = Saturday, 6 = Sunday.
    is_weekend = date.weekday() >= 5  

    # Logic to determine if the date is valid.
    if exclude_weekend_days:
        return is_in_range and not is_weekend
    else:
        return is_in_range
    
def generate_periods(start_period: int, end_period: int):
    """
    Generate a list of financial periods in YYMM format from start_period to end_period.

    Ensures valid month values (01-12) and that the start period is not after the end period.

    Args:
        start_period (int): The starting period in YYMM format.
        end_period (int): The ending period in YYMM format.

    Returns:
        list[int]: A list of consecutive periods in YYMM format.

    Raises:
        ValueError: If months are out of range or start_period > end_period.
    """
    periods = []
    start_year = start_period // 100
    start_month = start_period % 100
    end_month = end_period % 100

    # Ensure valid months for both start and end.
    if not (1 <= start_month <= 12):
        raise ValueError(f"Start month {start_month} is invalid. Month must be between 01 - 12.")
    if not (1 <= end_month <= 12):
        raise ValueError(f"End month {end_month} is invalid. Month must be between 01 - 12.")

    # Ensure valid period range.
    if start_period > end_period:
        raise ValueError("Start period must be before or equal to end period.")

    year, month = start_year, start_month

    while True:
        period = (year * 100) + month
        periods.append(period)

        if period >= end_period:
            break 

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

    return periods
