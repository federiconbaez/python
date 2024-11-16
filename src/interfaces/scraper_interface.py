
import os
import logging
from abc import ABC, abstractmethod
from git import Repo
from datetime import datetime
from typing import List, Dict

# -----------------------------------------------------------------------------------------------------
# @ Scraper Interface
# -----------------------------------------------------------------------------------------------------

class ScraperInterface(ABC):
    """
    Abstract base class for all scrapers interacting with Git repositories.
    """

    def __init__(self, repo_url: str, local_path: str):
        self.repo_url = repo_url
        self.local_path = local_path
        self.repo = None

    def clone_repository(self) -> None:
        """
        Clones a Git repository to a local path.
        """
        try:
            logging.info(f"Cloning repository from {self.repo_url} to {self.local_path}")
            if not os.path.exists(self.local_path):
                os.makedirs(self.local_path)
            self.repo = Repo.clone_from(self.repo_url, self.local_path)
            logging.info(f"Repository cloned successfully to {self.local_path}")
        except Exception as e:
            logging.error(f"Failed to clone repository: {e}")
            raise

    @abstractmethod
    def scrape_commits(self, branch_name: str) -> List[Dict[str, str]]:
        """
        Scrapes all commit details from the specified branch.

        Args:
            branch_name (str): The name of the branch to scrape commits from.

        Returns:
            List[Dict[str, str]]: A list of dictionaries with commit details.
        """
        pass

    @abstractmethod
    def scrape_contributors(self) -> List[Dict[str, str]]:
        """
        Scrapes contributor details from the Git repository.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing contributor information.
        """
        pass

    def checkout_branch(self, branch_name: str) -> None:
        """
        Checks out a specific branch in the repository.

        Args:
            branch_name (str): The name of the branch to check out.
        """
        try:
            logging.info(f"Checking out branch '{branch_name}' in the repository.")
            if branch_name not in self.repo.heads:
                raise ValueError(f"Branch '{branch_name}' does not exist in the repository.")
            branch = self.repo.heads[branch_name]
            branch.checkout()
            logging.info(f"Checked out branch '{branch_name}' successfully.")
        except ValueError as ve:
            logging.error(f"Branch checkout error: {ve}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during branch checkout: {e}")
            raise

    def fetch_tags(self) -> List[str]:
        """
        Fetches all tags from the Git repository.

        Returns:
            List[str]: A list of tags present in the repository.
        """
        try:
            logging.info("Fetching tags from the repository.")
            tags = [tag.name for tag in self.repo.tags]
            logging.info(f"Fetched tags successfully: {tags}")
            return tags
        except Exception as e:
            logging.error(f"Unexpected error while fetching tags: {e}")
            raise

    def log_activity(self) -> None:
        """
        Logs activity for all the recent commits in the repository.
        """
        try:
            logging.info("Logging recent commits in the repository.")
            commits = list(self.repo.iter_commits('HEAD', max_count=10))
            for commit in commits:
                logging.info(f"Commit {commit.hexsha} by {commit.author.name} on {datetime.fromtimestamp(commit.committed_date).isoformat()}: {commit.message}")
        except Exception as e:
            logging.error(f"Unexpected error while logging repository activity: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Scraper Interface
# -----------------------------------------------------------------------------------------------------
