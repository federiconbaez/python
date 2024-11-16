
import logging
from typing import Dict, List, Any
from repositories.git_repository import GitRepository

# -----------------------------------------------------------------------------------------------------
# @ Git Service
# -----------------------------------------------------------------------------------------------------

class GitService:
    """
    Service for managing high-level Git operations such as branches, tags, and synchronization with remotes.
    """

    def __init__(self, repo_path: str):
        self.repo = GitRepository(repo_path)

    def list_branches(self) -> List[str]:
        """
        Lists all branches in the repository.

        Returns:
            List[str]: A list of branch names.
        """
        try:
            logging.info("Listing all branches in the repository.")
            branches = self.repo.get_branches()
            logging.info(f"Branches listed successfully: {branches}")
            return branches
        except Exception as e:
            logging.error(f"Unexpected error while listing branches: {e}")
            raise

    def create_branch(self, branch_name: str, base_branch: str = 'develop') -> None:
        """
        Creates a new branch from the specified base branch.

        Args:
            branch_name (str): The name of the new branch.
            base_branch (str): The branch to base the new branch on. Defaults to 'develop'.
        """
        try:
            logging.info(f"Creating branch '{branch_name}' from base branch '{base_branch}'.")
            self.repo.create_branch(branch_name, base_branch)
            logging.info(f"Branch '{branch_name}' created successfully from '{base_branch}'.")
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
            self.repo.delete_branch(branch_name)
            logging.info(f"Branch '{branch_name}' deleted successfully.")
        except Exception as e:
            logging.error(f"Unexpected error while deleting branch: {e}")
            raise

    def list_tags(self) -> List[str]:
        """
        Lists all tags in the repository.

        Returns:
            List[str]: A list of tag names.
        """
        try:
            logging.info("Listing all tags in the repository.")
            tags = self.repo.get_tags()
            logging.info(f"Tags listed successfully: {tags}")
            return tags
        except Exception as e:
            logging.error(f"Unexpected error while listing tags: {e}")
            raise

    def create_tag(self, tag_name: str, message: str = '') -> None:
        """
        Creates a new tag in the repository.

        Args:
            tag_name (str): The name of the tag to create.
            message (str): An optional message for the tag.
        """
        try:
            logging.info(f"Creating tag '{tag_name}' with message: '{message}'.")
            self.repo.create_tag(tag_name, message)
            logging.info(f"Tag '{tag_name}' created successfully.")
        except Exception as e:
            logging.error(f"Unexpected error while creating tag: {e}")
            raise

    def pull_updates(self, remote_name: str = 'origin', branch_name: str = 'develop') -> None:
        """
        Pulls updates from a remote repository for a specific branch.

        Args:
            remote_name (str): The name of the remote to pull from. Defaults to 'origin'.
            branch_name (str): The branch to pull updates for. Defaults to 'develop'.
        """
        try:
            logging.info(f"Pulling updates from remote '{remote_name}' on branch '{branch_name}'.")
            self.repo.pull_updates(remote_name, branch_name)
            logging.info(f"Updates pulled successfully from '{remote_name}/{branch_name}'.")
        except Exception as e:
            logging.error(f"Unexpected error while pulling updates: {e}")
            raise

    def push_changes(self, remote_name: str = 'origin', branch_name: str = 'develop') -> None:
        """
        Pushes local changes to a remote repository.

        Args:
            remote_name (str): The name of the remote to push to. Defaults to 'origin'.
            branch_name (str): The branch to push changes for. Defaults to 'develop'.
        """
        try:
            logging.info(f"Pushing changes to remote '{remote_name}' on branch '{branch_name}'.")
            self.repo.push_changes(remote_name, branch_name)
            logging.info(f"Changes pushed successfully to '{remote_name}/{branch_name}'.")
        except Exception as e:
            logging.error(f"Unexpected error while pushing changes: {e}")
            raise

    def get_repository_status(self) -> Dict[str, Any]:
        """
        Retrieves the current status of the repository.

        Returns:
            Dict[str, Any]: A dictionary containing information about the repository status.
        """
        try:
            logging.info("Getting repository status.")
            status = self.repo.get_repository_status()
            logging.info(f"Repository status retrieved successfully: {status}")
            return status
        except Exception as e:
            logging.error(f"Unexpected error while retrieving repository status: {e}")
            raise

    def merge_branches(self, source_branch: str, target_branch: str = 'develop') -> None:
        """
        Merges the source branch into the target branch.

        Args:
            source_branch (str): The name of the branch to merge from.
            target_branch (str): The name of the branch to merge into. Defaults to 'develop'.
        """
        try:
            logging.info(f"Merging branch '{source_branch}' into '{target_branch}'.")
            self.repo.repo.git.checkout(target_branch)
            self.repo.repo.git.merge(source_branch)
            logging.info(f"Branch '{source_branch}' merged successfully into '{target_branch}'.")
        except Exception as e:
            logging.error(f"Unexpected error while merging branches: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Git Service
# -----------------------------------------------------------------------------------------------------