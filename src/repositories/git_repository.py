
import os
import logging
from git import Repo, GitCommandError
from typing import List, Dict, Any

# -----------------------------------------------------------------------------------------------------
# @ Git Repository
# -----------------------------------------------------------------------------------------------------

class GitRepository:
    """
    Class responsible for managing general Git repository operations.
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

    def get_branches(self) -> List[str]:
        """
        Retrieves a list of all branches in the repository.

        Returns:
            List[str]: A list of branch names in the repository.
        """
        try:
            logging.info("Retrieving branch list from repository.")
            branches = [head.name for head in self.repo.heads]
            logging.info(f"Branches retrieved successfully: {branches}")
            return branches
        except Exception as e:
            logging.error(f"Unexpected error while retrieving branches: {e}")
            raise
    
    def push_changes(self, remote_name: str = 'origin', branch_name: str = 'develop') -> None:
        """
        Pushes local changes to a remote repository.

        Args:
            remote_name (str): The name of the remote to push to. Defaults to 'origin'.
            branch_name (str): The name of the branch to push. Defaults to 'develop'.
        """
        try:
            logging.info(f"Pushing changes to remote '{remote_name}' branch '{branch_name}'.")
            remote = self.repo.remote(name=remote_name)
            remote.push(branch_name)
            logging.info(f"Changes pushed successfully to '{remote_name}/{branch_name}'.")
        except GitCommandError as gce:
            logging.error(f"Git command error while pushing changes: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while pushing changes: {e}")
            raise

    def create_branch(self, branch_name: str, base_branch: str = 'develop') -> None:
        """
        Creates a new branch in the repository.

        Args:
            branch_name (str): The name of the new branch.
            base_branch (str): The branch to base the new branch on. Defaults to 'develop'.
        """
        try:
            logging.info(f"Creating branch '{branch_name}' based on '{base_branch}'.")
            if branch_name in self.repo.heads:
                raise ValueError(f"Branch '{branch_name}' already exists.")
            base = self.repo.heads[base_branch]
            new_branch = self.repo.create_head(branch_name, base.commit)
            logging.info(f"Branch '{branch_name}' created successfully from '{base_branch}'.")
        except ValueError as ve:
            logging.error(f"Branch creation error: {ve}")
            raise
        except GitCommandError as gce:
            logging.error(f"Git command error while creating branch: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while creating branch: {e}")
            raise

    def delete_branch(self, branch_name: str) -> None:
        """
        Deletes a branch from the repository.

        Args:
            branch_name (str): The name of the branch to delete.
        """
        try:
            logging.info(f"Deleting branch '{branch_name}'.")
            if branch_name not in self.repo.heads:
                raise ValueError(f"Branch '{branch_name}' does not exist.")
            branch = self.repo.heads[branch_name]
            branch.delete(self.repo, branch)
            logging.info(f"Branch '{branch_name}' deleted successfully.")
        except ValueError as ve:
            logging.error(f"Branch deletion error: {ve}")
            raise
        except GitCommandError as gce:
            logging.error(f"Git command error while deleting branch: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while deleting branch: {e}")
            raise

    def get_tags(self) -> List[str]:
        """
        Retrieves a list of all tags in the repository.

        Returns:
            List[str]: A list of tag names in the repository.
        """
        try:
            logging.info("Retrieving tag list from repository.")
            tags = [tag.name for tag in self.repo.tags]
            logging.info(f"Tags retrieved successfully: {tags}")
            return tags
        except Exception as e:
            logging.error(f"Unexpected error while retrieving tags: {e}")
            raise

    def create_tag(self, tag_name: str, message: str = '') -> None:
        """
        Creates a new tag in the repository.

        Args:
            tag_name (str): The name of the tag to create.
            message (str): The message for the tag. Defaults to empty.
        """
        try:
            logging.info(f"Creating tag '{tag_name}' with message: '{message}'.")
            self.repo.create_tag(tag_name, message=message)
            logging.info(f"Tag '{tag_name}' created successfully.")
        except GitCommandError as gce:
            logging.error(f"Git command error while creating tag: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while creating tag: {e}")
            raise

    def pull_updates(self, remote_name: str = 'origin', branch_name: str = 'develop') -> None:
        """
        Pulls updates from a remote repository for a specific branch.

        Args:
            remote_name (str): The name of the remote to pull from. Defaults to 'origin'.
            branch_name (str): The name of the branch to pull. Defaults to 'develop'.
        """
        try:
            logging.info(f"Pulling updates from remote '{remote_name}' branch '{branch_name}'.")
            remote = self.repo.remote(name=remote_name)
            remote.pull(branch_name)
            logging.info(f"Updates pulled successfully from '{remote_name}/{branch_name}'.")
        except GitCommandError as gce:
            logging.error(f"Git command error while pulling updates: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while pulling updates: {e}")
            raise

    def push_changes(self, remote_name: str = 'origin', branch_name: str = 'develop') -> None:
        """
        Pushes local changes to a remote repository.

        Args:
            remote_name (str): The name of the remote to push to. Defaults to 'origin'.
            branch_name (str): The name of the branch to push. Defaults to 'develop'.
        """
        try:
            logging.info(f"Pushing changes to remote '{remote_name}' branch '{branch_name}'.")
            remote = self.repo.remote(name=remote_name)
            remote.push(branch_name)
            logging.info(f"Changes pushed successfully to '{remote_name}/{branch_name}'.")
        except GitCommandError as gce:
            logging.error(f"Git command error while pushing changes: {gce}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while pushing changes: {e}")
            raise

    def get_repository_status(self) -> Dict[str, Any]:
        """
        Retrieves the current status of the repository.

        Returns:
            Dict[str, Any]: Dictionary containing information about the repository status.
        """
        try:
            logging.info("Retrieving repository status.")
            status = {
                "untracked_files": self.repo.untracked_files,
                "is_dirty": self.repo.is_dirty(untracked_files=True),
                "branches": self.get_branches(),
                "tags": self.get_tags()
            }
            logging.info(f"Repository status retrieved successfully: {status}")
            return status
        except Exception as e:
            logging.error(f"Unexpected error while retrieving repository status: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Git Repository
# -----------------------------------------------------------------------------------------------------
