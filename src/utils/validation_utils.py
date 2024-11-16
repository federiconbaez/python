from utils.logger import logger
from typing import List, Dict, Any
import re

# -----------------------------------------------------------------------------------------------------
# @ Validation Utilities
# -----------------------------------------------------------------------------------------------------

class ValidationUtils:
    """
    Utility class for handling common validation operations.
    """

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validates an email address using a regular expression.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email address is valid, False otherwise.
        """
        try:
            logger.info(f"Validating email address: '{email}'")
            pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            is_valid = re.match(pattern, email) is not None
            logger.info(f"Email address '{email}' is {'valid' if is_valid else 'invalid'}.")
            return is_valid
        except Exception as e:
            logger.error(f"Unexpected error while validating email '{email}': {e}")
            raise

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validates a URL using a regular expression.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        try:
            logger.info(f"Validating URL: '{url}'")
            pattern = (r'^(https?:\/\/)?'  # Optional http or https
                       r'(([\da-z\.-]+)\.([a-z\.]{2,6})|localhost)'  # Domain name or localhost
                       r'([:\d]*)'  # Optional port
                       r'(\/[-a-zA-Z0-9@:%._\+~#=]*)*'  # Path
                       r'(\?[;&a-zA-Z0-9@:%_\+\-=]*)?'  # Query
                       r'(\#[-a-zA-Z0-9@:%_\+\/=]*)?$')  # Fragment
            is_valid = re.match(pattern, url) is not None
            logger.info(f"URL '{url}' is {'valid' if is_valid else 'invalid'}.")
            return is_valid
        except Exception as e:
            logger.error(f"Unexpected error while validating URL '{url}': {e}")
            raise

    @staticmethod
    def validate_non_empty_string(value: str) -> bool:
        """
        Checks if the provided string is non-empty and not just whitespace.

        Args:
            value (str): The string to validate.

        Returns:
            bool: True if the string is non-empty, False otherwise.
        """
        try:
            logger.info(f"Validating non-empty string: '{value}'")
            is_valid = isinstance(value, str) and bool(value.strip())
            logger.info(f"String validation result: {'valid' if is_valid else 'invalid'}.")
            return is_valid
        except Exception as e:
            logger.error(f"Unexpected error while validating string: {e}")
            raise

    @staticmethod
    def validate_positive_integer(value: Any) -> bool:
        """
        Checks if the provided value is a positive integer.

        Args:
            value (Any): The value to validate.

        Returns:
            bool: True if the value is a positive integer, False otherwise.
        """
        try:
            logger.info(f"Validating positive integer: '{value}'")
            is_valid = isinstance(value, int) and value > 0
            logger.info(f"Integer validation result for '{value}': {'valid' if is_valid else 'invalid'}.")
            return is_valid
        except Exception as e:
            logger.error(f"Unexpected error while validating positive integer: {e}")
            raise

    @staticmethod
    def validate_dictionary_keys(data: Dict[str, Any], required_keys: List[str]) -> bool:
        """
        Validates that the dictionary contains all required keys.

        Args:
            data (Dict[str, Any]): The dictionary to validate.
            required_keys (List[str]): A list of required keys that must be present in the dictionary.

        Returns:
            bool: True if all required keys are present, False otherwise.
        """
        try:
            logger.info(f"Validating dictionary keys: Required keys {required_keys}")
            missing_keys = [key for key in required_keys if key not in data]
            is_valid = len(missing_keys) == 0
            if is_valid:
                logger.info("All required keys are present in the dictionary.")
            else:
                logger.warning(f"Missing keys in the dictionary: {missing_keys}")
            return is_valid
        except Exception as e:
            logger.error(f"Unexpected error while validating dictionary keys: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Validation Utilities
# -----------------------------------------------------------------------------------------------------
