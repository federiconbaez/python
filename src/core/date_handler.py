
# src/core/date_handler.py
from datetime import datetime, timedelta
import logging
from typing import List, Tuple, Optional
from zoneinfo import ZoneInfo
from src.config import settings

class DateHandler:
    """Handle date-related operations for git contributions"""
    
    def __init__(self):
        self.date_config = settings.date
        self.timezone = ZoneInfo(self.date_config.timezone)

    def validate_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Tuple[datetime, datetime]:
        """Validate and normalize date range"""
        if start_date > end_date:
            raise ValueError("Start date must be before end date")

        # Apply configured limits
        now = datetime.now(self.timezone)
        max_past = now - timedelta(days=self.date_config.max_days_lookback)
        max_future = now + timedelta(days=self.date_config.max_days_ahead)

        if start_date < max_past:
            start_date = max_past
        if end_date > max_future:
            end_date = max_future

        return start_date, end_date

    def generate_date_windows(
        self,
        start_date: datetime,
        end_date: datetime,
        window_size: int = 7
    ) -> List[Tuple[datetime, datetime]]:
        """Generate time windows for processing"""
        windows = []
        current_start = start_date

        while current_start < end_date:
            window_end = min(
                current_start + timedelta(days=window_size),
                end_date
            )
            windows.append((current_start, window_end))
            current_start = window_end + timedelta(seconds=1)

        return windows

    def format_date(self, date: datetime) -> str:
        """Format date according to configuration"""
        return date.strftime(self.date_config.date_format)

    def parse_date(self, date_str: str) -> datetime:
        """Parse date string according to configuration"""
        try:
            return datetime.strptime(
                date_str,
                self.date_config.date_format
            ).replace(tzinfo=self.timezone)
        except ValueError as e:
            raise ValueError(f"Invalid date format: {str(e)}")
        
    """
    Utility class for handling date operations.
    """

    @staticmethod
    def get_date_range(start_date: datetime, end_date: datetime) -> List[datetime]:
        """
        Generates a list of dates between start_date and end_date inclusive.

        Args:
            start_date (datetime): The start date of the range.
            end_date (datetime): The end date of the range.

        Returns:
            List[datetime]: A list of datetime objects between the start and end dates.
        """
        try:
            logging.info(f"Generating date range from {start_date} to {end_date}")
            date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            logging.info(f"Date range generated successfully with {len(date_list)} dates.")
            return date_list
        except Exception as e:
            logging.error(f"Failed to generate date range from {start_date} to {end_date}: {e}")
            raise

    @staticmethod
    def parse_date_string(date_string: str, date_format: str = "%Y-%m-%d") -> Optional[datetime]:
        """
        Parses a date string into a datetime object.

        Args:
            date_string (str): The date string to parse.
            date_format (str): The format of the date string. Default is "%Y-%m-%d".

        Returns:
            Optional[datetime]: The parsed datetime object, or None if parsing fails.
        """
        try:
            logging.info(f"Parsing date string '{date_string}' with format '{date_format}'")
            parsed_date = datetime.strptime(date_string, date_format)
            logging.info(f"Date string '{date_string}' parsed successfully to {parsed_date}")
            return parsed_date
        except ValueError as e:
            logging.error(f"Failed to parse date string '{date_string}': {e}")
            return None

    @staticmethod
    def get_current_utc_datetime() -> datetime:
        """
        Gets the current UTC datetime.

        Returns:
            datetime: The current datetime in UTC.
        """
        current_utc = datetime.utcnow()
        logging.info(f"Current UTC datetime: {current_utc}")
        return current_utc

    @staticmethod
    def add_days_to_date(date: datetime, days: int) -> datetime:
        """
        Adds a specific number of days to a date.

        Args:
            date (datetime): The date to which days will be added.
            days (int): The number of days to add.

        Returns:
            datetime: The new date after adding the specified number of days.
        """
        try:
            logging.info(f"Adding {days} days to date {date}")
            new_date = date + timedelta(days=days)
            logging.info(f"New date after adding {days} days: {new_date}")
            return new_date
        except Exception as e:
            logging.error(f"Failed to add {days} days to date {date}: {e}")
            raise

    @staticmethod
    def subtract_days_from_date(date: datetime, days: int) -> datetime:
        """
        Subtracts a specific number of days from a date.

        Args:
            date (datetime): The date from which days will be subtracted.
            days (int): The number of days to subtract.

        Returns:
            datetime: The new date after subtracting the specified number of days.
        """
        try:
            logging.info(f"Subtracting {days} days from date {date}")
            new_date = date - timedelta(days=days)
            logging.info(f"New date after subtracting {days} days: {new_date}")
            return new_date
        except Exception as e:
            logging.error(f"Failed to subtract {days} days from date {date}: {e}")
            raise

    @staticmethod
    def is_weekend(date: datetime) -> bool:
        """
        Checks if a given date falls on a weekend.

        Args:
            date (datetime): The date to check.

        Returns:
            bool: True if the date is a Saturday or Sunday, False otherwise.
        """
        try:
            logging.info(f"Checking if date {date} is a weekend.")
            is_weekend = date.weekday() in [5, 6]
            logging.info(f"Date {date} is {'a weekend' if is_weekend else 'not a weekend'}.")
            return is_weekend
        except Exception as e:
            logging.error(f"Failed to determine if date {date} is a weekend: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Date Handler
# -----------------------------------------------------------------------------------------------------
