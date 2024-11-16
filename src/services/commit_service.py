
import logging
from datetime import datetime
from typing import List, Dict

from git import GitCommandError
from repositories.commit_repository import CommitRepository

# -----------------------------------------------------------------------------------------------------
# @ Commit Service
# -----------------------------------------------------------------------------------------------------

class CommitService:
    """
    Service that provides high-level operations related to Git commits, leveraging CommitRepository.
    """

    def __init__(self, repo_path: str):
        self.commit_repo = CommitRepository(repo_path)

    def commit_changes(self, message: str, files: List[str] = None) -> str:
        """
        Creates a commit in the repository with the given message and optional files.

        Args:
            message (str): The commit message.
            files (List[str]): Optional list of files to include in the commit. If None, all changes are included.

        Returns:
            str: The hash of the created commit.
        """
        try:
            logging.info(f"Creating commit with message: '{message}'")
            commit_hash = self.commit_repo.create_commit(message, files)
            logging.info(f"Commit created successfully with hash: {commit_hash}")
            return commit_hash
        except Exception as e:
            logging.error(f"Unexpected error while creating commit: {e}")
            raise

    def revert_last_commit(self) -> None:
        """
        Reverts the most recent commit on the current branch.
        """
        try:
            logging.info("Reverting the last commit on the current branch.")
            last_commit_hash = self.commit_repo.list_commits(limit=1)[0]["hash"]
            self.commit_repo.revert_commit(last_commit_hash)
            logging.info(f"Last commit with hash {last_commit_hash} reverted successfully.")
        except IndexError:
            logging.error("No commits found to revert.")
            raise ValueError("No commits found to revert.")
        except Exception as e:
            logging.error(f"Unexpected error while reverting last commit: {e}")
            raise

    def amend_last_commit(self, new_message: str) -> None:
        """
        Amends the last commit with a new message.

        Args:
            new_message (str): The new commit message to use.
        """
        try:
            logging.info(f"Amending the last commit with a new message: '{new_message}'")
            self.commit_repo.amend_last_commit(new_message)
            logging.info("Last commit amended successfully.")
        except Exception as e:
            logging.error(f"Unexpected error while amending last commit: {e}")
            raise

    def list_recent_commits(self, branch_name: str = 'develop', limit: int = 10) -> List[Dict[str, str]]:
        """
        Lists recent commits from a specified branch.

        Args:
            branch_name (str): The branch to list commits from. Defaults to 'develop'.
            limit (int): The maximum number of commits to list.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing commit details.
        """
        try:
            logging.info(f"Listing the most recent {limit} commits from branch '{branch_name}'.")
            recent_commits = self.commit_repo.list_commits(branch_name=branch_name, limit=limit)
            logging.info(f"Successfully listed recent commits from branch '{branch_name}': {recent_commits}")
            return recent_commits
        except Exception as e:
            logging.error(f"Unexpected error while listing recent commits: {e}")
            raise

    def delete_commits_by_hashes(self, commit_hashes: List[str]) -> None:
        """
        Deletes specific commits from the repository history.

        Args:
            commit_hashes (List[str]): List of commit hashes to delete.
        """
        try:
            logging.info(f"Deleting commits with hashes: {commit_hashes}")
            self.commit_repo.delete_commits(commit_hashes)
            logging.info(f"Commits {commit_hashes} deleted successfully.")
        except Exception as e:
            logging.error(f"Unexpected error while deleting commits: {e}")
            raise

    def find_commits_by_message(self, message_substring: str, branch_name: str = 'develop') -> List[Dict[str, str]]:
        """
        Finds commits that contain a specific substring in their commit message.

        Args:
            message_substring (str): The substring to search for in commit messages.
            branch_name (str): The branch to search in. Defaults to 'develop'.

        Returns:
            List[Dict[str, str]]: A list of commits containing the specified substring.
        """
        try:
            logging.info(f"Finding commits in branch '{branch_name}' containing message substring '{message_substring}'.")
            all_commits = self.commit_repo.list_commits(branch_name=branch_name, limit=1000)
            matching_commits = [commit for commit in all_commits if message_substring in commit["message"]]
            logging.info(f"Found {len(matching_commits)} commits containing '{message_substring}'.")
            return matching_commits
        except Exception as e:
            logging.error(f"Unexpected error while finding commits by message: {e}")
            raise

    def squash_commits(self, start_hash: str, end_hash: str, new_message: str) -> None:
        """
        Squashes commits between two specified commits into one.

        Args:
            start_hash (str): The hash of the first commit in the range to squash.
            end_hash (str): The hash of the last commit in the range to squash.
            new_message (str): The new commit message for the squashed commit.
        """
        try:
            logging.info(f"Squashing commits from '{start_hash}' to '{end_hash}' with new message: '{new_message}'.")
            self.commit_repo.repo.git.rebase(f"{start_hash}^", f"{end_hash}")
            self.commit_repo.repo.git.commit(amend=True, message=new_message)
            logging.info("Commits squashed successfully.")
        except GitCommandError as gce:
            logging.error(f"Git command error while squashing commits: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while squashing commits: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Commit Service
# -----------------------------------------------------------------------------------------------------
