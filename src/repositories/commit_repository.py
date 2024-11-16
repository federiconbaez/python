
import os
import logging
import json
from git import Repo, GitCommandError
from datetime import datetime
from typing import List, Dict

# -----------------------------------------------------------------------------------------------------
# @ Commit Repository
# -----------------------------------------------------------------------------------------------------

class CommitRepository:
    """
    Class responsible for managing commit operations in a Git repository.
    """

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.repo = None
        self.connect()

    def connect(self) -> None:
        """
        Establishes a connection to the repository.
        """
        try:
            logging.info(f"Connecting to repository at path: {self.repo_path}")
            if not os.path.exists(self.repo_path):
                raise FileNotFoundError(f"Repository path does not exist: {self.repo_path}")
            self.repo = Repo(self.repo_path)
            if self.repo.bare:
                raise ValueError(f"The repository at {self.repo_path} is not initialized.")
            logging.info("Connected to the repository successfully.")
        except FileNotFoundError as fnf:
            logging.error(f"Repository path error: {fnf}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while connecting to repository: {e}")
            raise

    def create_commit(self, message: str, files: List[str] = None) -> str:
        """
        Creates a commit in the repository with a given message and optional files.

        Args:
            message (str): The commit message.
            files (List[str]): List of file paths to be included in the commit. If None, all changes are committed.

        Returns:
            str: The hash of the created commit.
        """
        try:
            if not message:
                raise ValueError("Commit message cannot be empty.")

            logging.info(f"Creating commit with message: '{message}'")
            if files:
                for file in files:
                    self.repo.index.add([file])
            else:
                self.repo.git.add(A=True)  # Add all changes

            new_commit = self.repo.index.commit(message)
            logging.info(f"Commit created successfully: {new_commit.hexsha}")
            return new_commit.hexsha
        except ValueError as ve:
            logging.error(f"Commit creation error: {ve}")
            raise
        except GitCommandError as gce:
            logging.error(f"Git command error during commit: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while creating commit: {e}")
            raise

    def get_commit_details(self, commit_hash: str) -> Dict[str, str]:
        """
        Retrieves details of a specific commit.

        Args:
            commit_hash (str): The hash of the commit to retrieve details for.

        Returns:
            Dict[str, str]: Details of the specified commit.
        """
        try:
            logging.info(f"Retrieving details for commit: {commit_hash}")
            commit = self.repo.commit(commit_hash)
            commit_details = {
                "hash": commit.hexsha,
                "author": commit.author.name,
                "message": commit.message,
                "date": commit.committed_datetime.isoformat()
            }
            logging.info(f"Commit details retrieved successfully for {commit_hash}")
            return commit_details
        except GitCommandError as gce:
            logging.error(f"Git command error while retrieving commit details: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while retrieving commit details: {e}")
            raise

    def revert_commit(self, commit_hash: str) -> None:
        """
        Reverts a specific commit in the repository.

        Args:
            commit_hash (str): The hash of the commit to revert.
        """
        try:
            logging.info(f"Reverting commit: {commit_hash}")
            self.repo.git.revert(commit_hash, no_edit=True)
            logging.info(f"Commit {commit_hash} reverted successfully.")
        except GitCommandError as gce:
            logging.error(f"Git command error while reverting commit: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while reverting commit: {e}")
            raise

    def list_commits(self, branch_name: str = 'develop', limit: int = 10) -> List[Dict[str, str]]:
        """
        Lists the most recent commits from the specified branch.

        Args:
            branch_name (str): The name of the branch to list commits from. Defaults to 'develop'.
            limit (int): The maximum number of commits to return.

        Returns:
            List[Dict[str, str]]: A list of commit details.
        """
        try:
            logging.info(f"Listing the last {limit} commits from branch: {branch_name}")
            branch = self.repo.heads[branch_name]
            commits = list(branch.commit.iter_items(self.repo, f'{branch_name}', max_count=limit))
            commit_data = [{
                "hash": commit.hexsha,
                "author": commit.author.name,
                "message": commit.message,
                "date": commit.committed_datetime.isoformat()
            } for commit in commits]
            logging.info(f"Successfully listed {len(commit_data)} commits from branch '{branch_name}'")
            return commit_data
        except GitCommandError as gce:
            logging.error(f"Git command error while listing commits: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while listing commits: {e}")
            raise

    def amend_last_commit(self, new_message: str) -> None:
        """
        Amends the last commit with a new commit message.

        Args:
            new_message (str): The new commit message to use.
        """
        try:
            if not new_message:
                raise ValueError("New commit message cannot be empty.")

            logging.info(f"Amending last commit with new message: '{new_message}'")
            self.repo.git.commit(amend=True, message=new_message)
            logging.info("Last commit amended successfully.")
        except ValueError as ve:
            logging.error(f"Amend commit error: {ve}")
            raise
        except GitCommandError as gce:
            logging.error(f"Git command error during amend: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while amending last commit: {e}")
            raise

    def delete_commits(self, commit_hashes: List[str]) -> None:
        """
        Deletes a list of commits from the repository history.

        Args:
            commit_hashes (List[str]): List of commit hashes to delete.
        """
        try:
            logging.info(f"Deleting commits: {commit_hashes}")
            for commit_hash in commit_hashes:
                self.repo.git.revert(commit_hash, no_edit=True)
                self.repo.index.commit(f"Revert commit: {commit_hash}")
            logging.info(f"Commits {commit_hashes} deleted successfully.")
        except GitCommandError as gce:
            logging.error(f"Git command error while deleting commits: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while deleting commits: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Commit Repository
# -----------------------------------------------------------------------------------------------------