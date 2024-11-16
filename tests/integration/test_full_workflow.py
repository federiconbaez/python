
import unittest
import tempfile
import os
import logging
from services.git_service import GitService
from services.commit_service import CommitService
from services.analysis_service import AnalysisService
from utils.date_utils import DateUtils
from utils.logger import LoggerUtils

# -----------------------------------------------------------------------------------------------------
# @ Test Full Workflow
# -----------------------------------------------------------------------------------------------------

class TestFullWorkflow(unittest.TestCase):
    """
    Integration tests to validate the full workflow of the Git services and utilities.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the testing environment, including initializing logging and creating a temporary repository.
        """
        # Setup logging for the test
        LoggerUtils.setup_logging("logs/test_full_workflow.log", level=logging.DEBUG)
        cls.logger = LoggerUtils.get_logger(__name__)

        # Create a temporary directory to initialize the test repository
        cls.repo_dir = tempfile.mkdtemp()
        cls.logger.info(f"Temporary repository created at: {cls.repo_dir}")

        # Initialize GitService, CommitService, and AnalysisService
        cls.git_service = GitService(repo_path=cls.repo_dir)
        cls.commit_service = CommitService(repo_path=cls.repo_dir)
        cls.analysis_service = AnalysisService(repo_path=cls.repo_dir)

        # Initialize an empty git repository
        cls.git_service.repo.repo.init(cls.repo_dir)
        cls.logger.info("Initialized empty Git repository for testing.")

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clean up the testing environment by removing the temporary repository.
        """
        cls.logger.info(f"Cleaning up the temporary repository at: {cls.repo_dir}")
        if os.path.exists(cls.repo_dir):
            for root, dirs, files in os.walk(cls.repo_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(cls.repo_dir)
            cls.logger.info("Temporary repository cleaned up successfully.")

    def test_branch_creation_and_deletion(self):
        """
        Test the creation and deletion of branches in the repository.
        """
        branch_name = "test_branch"
        self.logger.info(f"Testing branch creation: {branch_name}")
        self.git_service.create_branch(branch_name)
        branches = self.git_service.list_branches()
        self.assertIn(branch_name, branches, "Branch was not created successfully.")

        self.logger.info(f"Testing branch deletion: {branch_name}")
        self.git_service.delete_branch(branch_name)
        branches = self.git_service.list_branches()
        self.assertNotIn(branch_name, branches, "Branch was not deleted successfully.")

    def test_commit_creation_and_reversion(self):
        """
        Test creating a commit and then reverting the last commit.
        """
        # Create a file to commit
        file_path = os.path.join(self.repo_dir, "README.md")
        with open(file_path, "w") as f:
            f.write("# Test Repository\nThis is a test repository.")
        self.logger.info("Created README.md for commit testing.")

        # Commit the file
        commit_message = "Initial commit for README.md"
        commit_hash = self.commit_service.commit_changes(commit_message, files=[file_path])
        self.logger.info(f"Commit created with hash: {commit_hash}")
        recent_commits = self.commit_service.list_recent_commits(limit=1)
        self.assertEqual(recent_commits[0]["message"], commit_message, "Commit message does not match.")

        # Revert the commit
        self.logger.info(f"Reverting commit with hash: {commit_hash}")
        self.commit_service.revert_last_commit()
        recent_commits = self.commit_service.list_recent_commits(limit=1)
        self.assertNotEqual(recent_commits[0]["hash"], commit_hash, "Commit was not reverted successfully.")

    def test_tag_creation(self):
        """
        Test creating a tag in the repository.
        """
        tag_name = "v1.0"
        tag_message = "Release version 1.0"
        self.logger.info(f"Testing tag creation: {tag_name}")
        self.git_service.create_tag(tag_name, tag_message)
        tags = self.git_service.list_tags()
        self.assertIn(tag_name, tags, "Tag was not created successfully.")

    def test_commit_statistics_analysis(self):
        """
        Test generating commit statistics for the main branch.
        """
        self.logger.info("Testing commit statistics analysis.")
        statistics = self.analysis_service.generate_commit_statistics()
        self.assertIsInstance(statistics, dict, "Statistics should be returned as a dictionary.")
        self.assertIn("total_commits", statistics, "'total_commits' should be present in statistics.")
        self.assertIn("average_commits_per_day", statistics, "'average_commits_per_day' should be present in statistics.")

if __name__ == "__main__":
    unittest.main()

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Test Full Workflow
# -----------------------------------------------------------------------------------------------------