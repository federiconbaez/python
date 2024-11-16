
import os
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json
import random
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------------------------------
# @ Generator Interface
# -----------------------------------------------------------------------------------------------------

class GeneratorInterface(ABC):
    """
    Abstract base class for all contribution generators.
    """

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        if not os.path.exists(repo_path):
            raise FileNotFoundError(f"Repository path '{repo_path}' does not exist.")
        self.commit_log_file = os.path.join(repo_path, 'commit_log.json')
        logging.info(f"Generator initialized for repository at {repo_path}")

    def generate_contributions(self, days: int, frequency: float) -> None:
        """
        Generates random contributions for the repository over a specified number of days.

        Args:
            days (int): Number of days in the past over which contributions are generated.
            frequency (float): Frequency (0.0 to 1.0) determining the likelihood of committing on a given day.
        """
        try:
            if not (0 <= frequency <= 1):
                raise ValueError("Frequency must be between 0 and 1.")

            start_date = datetime.now() - timedelta(days=days)
            contributions = []

            for day in range(days):
                current_date = start_date + timedelta(days=day)
                if random.random() <= frequency:
                    contribution = self._generate_commit(current_date)
                    contributions.append(contribution)
                    logging.info(f"Generated contribution on {current_date.date()}.")

            # Save all generated contributions to a log file
            with open(self.commit_log_file, 'w') as f:
                json.dump(contributions, f, indent=4)
            logging.info(f"Successfully generated and logged contributions for {days} days.")

        except ValueError as ve:
            logging.error(f"Invalid frequency value: {ve}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during contribution generation: {e}")
            raise

    @abstractmethod
    def _generate_commit(self, commit_date: datetime) -> Dict[str, Any]:
        """
        Abstract method for generating a commit based on a specified date.

        Args:
            commit_date (datetime): The date of the commit to be generated.

        Returns:
            Dict[str, Any]: Details of the generated commit.
        """
        pass

    def validate_repository(self) -> bool:
        """
        Validates that the repository path is a valid Git repository.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            logging.info(f"Validating repository path: {self.repo_path}")
            git_dir = os.path.join(self.repo_path, ".git")
            if not os.path.isdir(git_dir):
                raise FileNotFoundError(f"The directory '{git_dir}' does not exist. Not a valid Git repository.")
            logging.info("Repository path is valid.")
            return True
        except FileNotFoundError as fnf:
            logging.error(f"Repository validation error: {fnf}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error during repository validation: {e}")
            return False

    @abstractmethod
    def save_contribution_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Abstract method for saving contribution data.

        Args:
            data (List[Dict[str, Any]]): Contribution data to be saved.
        """
        pass

    def log_activity(self, message: str) -> None:
        """
        Logs activity in the repository's contribution log.

        Args:
            message (str): The activity message to be logged.
        """
        try:
            timestamp = datetime.now().isoformat()
            log_entry = {"timestamp": timestamp, "message": message}
            if not os.path.exists(self.commit_log_file):
                log_data = []
            else:
                with open(self.commit_log_file, 'r') as f:
                    log_data = json.load(f)
            log_data.append(log_entry)
            with open(self.commit_log_file, 'w') as f:
                json.dump(log_data, f, indent=4)
            logging.info(f"Logged activity: {message}")
        except Exception as e:
            logging.error(f"Unexpected error during activity logging: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Generator Interface
# -----------------------------------------------------------------------------------------------------