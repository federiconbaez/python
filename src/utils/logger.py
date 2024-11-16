
import logging
import os
from datetime import datetime

# -----------------------------------------------------------------------------------------------------
# @ Logger Utilities
# -----------------------------------------------------------------------------------------------------

class LoggerUtils:
    """
    Utility class for configuring and managing logging.
    """

    @staticmethod
    def setup_logging(log_file_path: str = "logs/app.log", level: int = logging.INFO) -> None:
        """
        Sets up logging configuration for the application.

        Args:
            log_file_path (str): The file path for the log file.
            level (int): The logging level. Defaults to logging.INFO.
        """
        try:
            # Create directories if they do not exist
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

            # Setup logging format
            logging.basicConfig(
                level=level,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                handlers=[
                    logging.FileHandler(log_file_path),
                    logging.StreamHandler()
                ]
            )
            logging.info(f"Logging setup completed. Log file: {log_file_path}")
        except Exception as e:
            print(f"Error setting up logging: {e}")
            raise

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Gets a logger instance by name.

        Args:
            name (str): The name of the logger.

        Returns:
            logging.Logger: Configured logger instance.
        """
        try:
            logger = logging.getLogger(name)
            logging.info(f"Logger instance created for '{name}'")
            return logger
        except Exception as e:
            logging.error(f"Error while creating logger instance for '{name}': {e}")
            raise

    @staticmethod
    def log_performance(func):
        """
        Decorator to log the performance (execution time) of a function.

        Args:
            func (function): The function to be decorated.

        Returns:
            function: Wrapped function with logging.
        """
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            logging.info(f"Started execution of '{func.__name__}' at {start_time}")
            try:
                result = func(*args, **kwargs)
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logging.info(f"Finished execution of '{func.__name__}' at {end_time}, Duration: {duration:.2f} seconds.")
                return result
            except Exception as e:
                logging.error(f"Unexpected error in '{func.__name__}': {e}")
                raise

        return wrapper

    @staticmethod
    def log_exception(logger: logging.Logger):
        """
        Decorator to log any exceptions raised by a function.

        Args:
            logger (logging.Logger): The logger instance to log exceptions.

        Returns:
            function: Wrapped function with exception logging.
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Exception occurred in '{func.__name__}': {e}", exc_info=True)
                    raise
            return wrapper
        return decorator

    @staticmethod
    def log_to_file_only(log_file_path: str) -> None:
        """
        Configures logging to write only to a specified file.

        Args:
            log_file_path (str): The path to the log file.
        """
        try:
            # Create directories if they do not exist
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                handlers=[
                    logging.FileHandler(log_file_path)
                ]
            )
            logging.info(f"Logging setup for file-only logging. Log file: {log_file_path}")
        except Exception as e:
            print(f"Error setting up file-only logging: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Logger Utilities
# -----------------------------------------------------------------------------------------------------