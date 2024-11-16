
import logging
from datetime import datetime, timedelta
from typing import List

# -----------------------------------------------------------------------------------------------------
# @ Date Utilities
# -----------------------------------------------------------------------------------------------------

class DateUtils:
    """
    Utility class for handling common date operations.
    """

    @staticmethod
    def get_date_range(start_date: str, end_date: str, date_format: str = "%Y-%m-%d") -> List[str]:
        """
        Generates a list of dates between the start_date and end_date in the given format.

        Args:
            start_date (str): The start date as a string.
            end_date (str): The end date as a string.
            date_format (str): The format of the dates provided and returned. Defaults to "%Y-%m-%d".

        Returns:
            List[str]: A list of date strings in the specified range.
        """
        try:
            logging.info(f"Generating date range from '{start_date}' to '{end_date}' using format '{date_format}'.")
            start = datetime.strptime(start_date, date_format)
            end = datetime.strptime(end_date, date_format)
            date_list = [(start + timedelta(days=i)).strftime(date_format) for i in range((end - start).days + 1)]
            logging.info(f"Date range generated successfully: {date_list}")
            return date_list
        except ValueError as ve:
            logging.error(f"Value error while generating date range: {ve}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while generating date range: {e}")
            raise

    @staticmethod
    def is_weekend(date_str: str, date_format: str = "%Y-%m-%d") -> bool:
        """
        Determines whether the given date falls on a weekend.

        Args:
            date_str (str): The date to check as a string.
            date_format (str): The format of the date provided. Defaults to "%Y-%m-%d".

        Returns:
            bool: True if the date falls on a weekend, False otherwise.
        """
        try:
            logging.info(f"Checking if date '{date_str}' is a weekend using format '{date_format}'.")
            date_obj = datetime.strptime(date_str, date_format)
            is_weekend = date_obj.weekday() >= 5
            logging.info(f"Date '{date_str}' is {'a weekend' if is_weekend else 'not a weekend'}.")
            return is_weekend
        except ValueError as ve:
            logging.error(f"Value error while checking if date is a weekend: {ve}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while checking if date is a weekend: {e}")
            raise

    @staticmethod
    def add_days(date_str: str, days: int, date_format: str = "%Y-%m-%d") -> str:
        """
        Adds a specified number of days to the given date.

        Args:
            date_str (str): The original date as a string.
            days (int): The number of days to add.
            date_format (str): The format of the date provided and returned. Defaults to "%Y-%m-%d".

        Returns:
            str: The new date as a string in the specified format.
        """
        try:
            logging.info(f"Adding {days} days to date '{date_str}' using format '{date_format}'.")
            date_obj = datetime.strptime(date_str, date_format)
            new_date = (date_obj + timedelta(days=days)).strftime(date_format)
            logging.info(f"New date after adding {days} days: {new_date}")
            return new_date
        except ValueError as ve:
            logging.error(f"Value error while adding days to date: {ve}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while adding days to date: {e}")
            raise

    @staticmethod
    def get_current_timestamp(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Returns the current timestamp in the given format.

        Args:
            date_format (str): The format of the timestamp to be returned. Defaults to "%Y-%m-%d %H:%M:%S".

        Returns:
            str: The current timestamp as a string.
        """
        try:
            logging.info(f"Getting current timestamp with format '{date_format}'.")
            current_timestamp = datetime.now().strftime(date_format)
            logging.info(f"Current timestamp: {current_timestamp}")
            return current_timestamp
        except Exception as e:
            logging.error(f"Unexpected error while getting current timestamp: {e}")
            raise

    @staticmethod
    def get_day_of_week(date_str: str, date_format: str = "%Y-%m-%d") -> str:
        """
        Returns the day of the week for a given date.

        Args:
            date_str (str): The date to check as a string.
            date_format (str): The format of the date provided. Defaults to "%Y-%m-%d".

        Returns:
            str: The day of the week (e.g., 'Monday', 'Tuesday').
        """
        try:
            logging.info(f"Getting day of the week for date '{date_str}' using format '{date_format}'.")
            date_obj = datetime.strptime(date_str, date_format)
            day_of_week = date_obj.strftime('%A')
            logging.info(f"Day of the week for date '{date_str}': {day_of_week}")
            return day_of_week
        except ValueError as ve:
            logging.error(f"Value error while getting day of the week: {ve}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while getting day of the week: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Date Utilities
# -----------------------------------------------------------------------------------------------------
