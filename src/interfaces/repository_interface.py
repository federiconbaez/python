
import argparse
import os
from datetime import datetime
from datetime import timedelta
from random import randint
from subprocess import Popen, PIPE, check_output, CalledProcessError
import sys
from abc import ABC, abstractmethod
import logging
import json
import time
import git

# -----------------------------------------------------------------------------------------------------
# @ Repository Interface
# -----------------------------------------------------------------------------------------------------

class RepositoryInterface(ABC):
    """
    Abstract base class for all repository interactions.
    """

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.repo = None

    def connect(self) -> None:
        """
        Establishes a connection to the repository.
        """
        try:
            logging.info(f"Connecting to repository at path: {self.repo_path}")
            if not os.path.exists(self.repo_path):
                raise FileNotFoundError(f"Repository path does not exist: {self.repo_path}")
            self.repo = git.Repo(self.repo_path)
            if self.repo.bare:
                raise ValueError(f"The repository at {self.repo_path} is not initialized.")
            logging.info("Connected to the repository successfully.")
        except FileNotFoundError as fnf:
            logging.error(f"Repository path error: {fnf}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while connecting to repository: {e}")
            raise

    def fetch_data(self, branch_name: str) -> dict:
        """
        Fetches all commits from the specified branch of the repository.

        Args:
            branch_name (str): The name of the branch to fetch commits from.

        Returns:
            dict: Retrieved commit data in dictionary form.
        """
        try:
            logging.info(f"Fetching commit data from branch: {branch_name}")
            if branch_name not in self.repo.heads:
                raise ValueError(f"Branch '{branch_name}' does not exist in the repository.")
            branch = self.repo.heads[branch_name]
            commits = list(branch.commit.iter_items(self.repo, f'{branch_name}'))
            commit_data = [{
                "hash": commit.hexsha,
                "author": commit.author.name,
                "message": commit.message,
                "date": commit.committed_datetime.isoformat()
            } for commit in commits]
            logging.info(f"Commit data fetched successfully from branch '{branch_name}'")
            return {"branch": branch_name, "commits": commit_data}
        except ValueError as ve:
            logging.error(f"Value error during fetching commits: {ve}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while fetching commit data: {e}")
            raise

    def save_data(self, data: dict) -> None:
        """
        Saves data as a file in the repository and commits it.

        Args:
            data (dict): Data to be saved to the repository.
        """
        try:
            logging.info(f"Saving data to repository: {json.dumps(data)}")
            file_path = os.path.join(self.repo_path, 'data.json')
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            self.repo.index.add([file_path])
            self.repo.index.commit(f"Add/update data file: data.json")
            logging.info("Data saved and committed successfully.")
        except Exception as e:
            logging.error(f"Unexpected error while saving data: {e}")
            raise

    def update_data(self, identifier: str, data: dict) -> None:
        """
        Updates specific data in the repository by modifying a JSON file and committing changes.

        Args:
            identifier (str): Unique identifier to locate the data to update.
            data (dict): Updated data.
        """
        try:
            logging.info(f"Updating data for identifier '{identifier}' in repository.")
            file_path = os.path.join(self.repo_path, 'data.json')
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Data file not found: {file_path}")
            with open(file_path, 'r') as f:
                existing_data = json.load(f)
            if identifier not in existing_data:
                raise ValueError(f"Identifier '{identifier}' not found in data.")
            existing_data[identifier].update(data)
            with open(file_path, 'w') as f:
                json.dump(existing_data, f, indent=4)
            self.repo.index.add([file_path])
            self.repo.index.commit(f"Update data for identifier: {identifier}")
            logging.info(f"Data for identifier '{identifier}' updated and committed successfully.")
        except FileNotFoundError as fnf:
            logging.error(f"File not found during update: {fnf}")
            raise
        except ValueError as ve:
            logging.error(f"Value error during update: {ve}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while updating data: {e}")
            raise

    def delete_data(self, identifier: str) -> None:
        """
        Deletes data from the repository by modifying a JSON file and committing changes.

        Args:
            identifier (str): Unique identifier to locate the data to delete.
        """
        try:
            logging.info(f"Deleting data for identifier '{identifier}' from repository.")
            file_path = os.path.join(self.repo_path, 'data.json')
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Data file not found: {file_path}")
            with open(file_path, 'r') as f:
                existing_data = json.load(f)
            if identifier not in existing_data:
                raise ValueError(f"Identifier '{identifier}' not found in data.")
            del existing_data[identifier]
            with open(file_path, 'w') as f:
                json.dump(existing_data, f, indent=4)
            self.repo.index.add([file_path])
            self.repo.index.commit(f"Delete data for identifier: {identifier}")
            logging.info(f"Data for identifier '{identifier}' deleted and committed successfully.")
        except FileNotFoundError as fnf:
            logging.error(f"File not found during deletion: {fnf}")
            raise
        except ValueError as ve:
            logging.error(f"Value error during deletion: {ve}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while deleting data: {e}")
            raise

    def validate_connection(self) -> bool:
        """
        Validates if the repository connection is active and operational.

        Returns:
            bool: True if the connection is valid, False otherwise.
        """
        try:
            logging.info("Validating repository connection...")
            if self.repo is None or self.repo.bare:
                raise ConnectionError("No valid repository connection established.")
            # Attempting to get the latest commit to validate connection
            latest_commit = self.repo.head.commit
            logging.info(f"Repository connection is valid. Latest commit: {latest_commit.hexsha}")
            return True
        except Exception as e:
            logging.error(f"Unexpected error during connection validation: {e}")
            return False

    def list_all(self, limit: int = 100, offset: int = 0) -> list:
        """
        Lists all commits in the repository with optional pagination.

        Args:
            limit (int): The maximum number of records to return. Defaults to 100.
            offset (int): The number of records to skip before starting to return results. Defaults to 0.

        Returns:
            list: A list of commit records from the repository.
        """
        try:
            logging.info(f"Listing all commits with limit {limit} and offset {offset}")
            commits = list(self.repo.iter_commits())[offset:offset + limit]
            commit_data = [{
                "hash": commit.hexsha,
                "author": commit.author.name,
                "message": commit.message,
                "date": commit.committed_datetime.isoformat()
            } for commit in commits]
            logging.info(f"Commits listed successfully. Total listed: {len(commit_data)}")
            return commit_data
        except Exception as e:
            logging.error(f"Unexpected error while listing commits: {e}")
            raise

    def search(self, search_criteria: dict) -> list:
        """
        Searches for commits that match the specified criteria.

        Args:
            search_criteria (dict): A dictionary defining the search parameters and their values.

        Returns:
            list: A list of commits matching the search criteria.
        """
        try:
            logging.info(f"Searching commits with criteria: {search_criteria}")
            commits = list(self.repo.iter_commits())
            results = []
            for commit in commits:
                match = all(
                    (getattr(commit, key, None) == value) if hasattr(commit, key) else False
                    for key, value in search_criteria.items()
                )
                if match:
                    results.append({
                        "hash": commit.hexsha,
                        "author": commit.author.name,
                        "message": commit.message,
                        "date": commit.committed_datetime.isoformat()
                    })
            logging.info(f"Search completed successfully. Matches found: {len(results)}")
            return results
        except Exception as e:
            logging.error(f"Unexpected error while searching commits: {e}")
            raise

    def bulk_insert(self, data_list: list) -> None:
        """
        Inserts multiple records into the repository by creating files and committing them.

        Args:
            data_list (list): A list of dictionaries, each representing a record to be inserted.
        """
        try:
            logging.info(f"Bulk inserting data into repository.")
            for idx, data in enumerate(data_list):
                file_path = os.path.join(self.repo_path, f'data_{idx}.json')
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                self.repo.index.add([file_path])
            self.repo.index.commit(f"Bulk insert of {len(data_list)} data files.")
            logging.info("Bulk insert completed successfully.")
        except Exception as e:
            logging.error(f"Unexpected error during bulk insert: {e}")
            raise

    def execute_custom_query(self, query: str) -> dict:
        """
        Executes a custom Git command in the repository and returns the result.

        Args:
            query (str): The custom Git command string to be executed.

        Returns:
            dict: The result of executing the custom query.
        """
        try:
            logging.info(f"Executing custom Git command: {query}")
            result = check_output(query.split(), cwd=self.repo_path, stderr=PIPE).decode('utf-8')
            logging.info(f"Custom command executed successfully. Output: {result}")
            return {"output": result}
        except CalledProcessError as cpe:
            logging.error(f"Error during command execution: {cpe.output.decode('utf-8')}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during custom query execution: {e}")
            raise

    def close_connection(self) -> None:
        """
        Closes the connection to the repository.
        """
        try:
            logging.info("Closing repository connection...")
            self.repo = None  # Clearing repository object to close connection
            logging.info("Connection closed successfully.")
        except Exception as e:
            logging.error(f"Error closing connection: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Repository Interface
# -----------------------------------------------------------------------------------------------------
