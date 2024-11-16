
from datetime import datetime, timedelta
import tempfile
import unittest
import os
import logging
from datetime import datetime, timedelta
from src.factories.generator_factory import ContributionGeneratorFactory
from src.utils.logger import LoggerUtils

# -----------------------------------------------------------------------------------------------------
# @ Test Contribution Generator
# -----------------------------------------------------------------------------------------------------

class TestContributionGenerator(unittest.TestCase):
    """
    Unit tests to validate the behavior of the Contribution Generator.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the testing environment, including initializing logging and creating a temporary repository.
        """
        # Setup logging for the test
        LoggerUtils.setup_logging("logs/test_contribution_generator.log", level=logging.DEBUG)
        cls.logger = LoggerUtils.get_logger(__name__)

        # Create a temporary directory to initialize the test repository
        cls.repo_dir = tempfile.mkdtemp()
        cls.logger.info(f"Temporary repository created at: {cls.repo_dir}")

        # Initialize a contribution generator using the factory
        cls.contribution_generator = ContributionGeneratorFactory.create_generator("simple", cls.repo_dir)

    
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

    def test_generate_single_commit(self):
        """
        Test generating a single commit on a specific date.
        """
        target_date = datetime.now() - timedelta(days=10)
        self.logger.info(f"Testing single commit generation for date: {target_date.isoformat()}")
        self.contribution_generator.generate_single_commit(target_date)

        # Verify commit presence in the repository
        commit_log = list(self.contribution_generator.repo.iter_commits(max_count=1))
        self.assertEqual(len(commit_log), 1, "No commits were found in the repository.")
        commit_date = datetime.fromtimestamp(commit_log[0].committed_date)
        self.assertEqual(commit_date.date(), target_date.date(), "Commit date does not match the expected date.")

    def test_generate_commits_over_period(self):
        """
        Test generating multiple commits over a period.
        """
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now() - timedelta(days=1)
        frequency = 0.5  # 50% chance to generate a commit each day
        self.logger.info(f"Testing commit generation over period from {start_date.date()} to {end_date.date()}.")
        self.contribution_generator.generate_commits_over_period(start_date, end_date, frequency)

        # Verify that some commits are generated (since frequency is 50%, we expect some commits but not all days)
        commit_log = list(self.contribution_generator.repo.iter_commits())
        self.assertGreater(len(commit_log), 0, "No commits were generated over the period.")
        self.assertLessEqual(len(commit_log), 30, "Generated more commits than possible for the given period.")

    def test_generate_commits_without_weekends(self):
        """
        Test generating commits over a period without creating commits on weekends.
        """
        start_date = datetime.now() - timedelta(days=20)
        end_date = datetime.now() - timedelta(days=1)
        self.logger.info(f"Testing commit generation over period from {start_date.date()} to {end_date.date()} excluding weekends.")
        self.contribution_generator.generate_commits_over_period(start_date, end_date, frequency=1.0, no_weekends=True)

        # Verify that no commits are on weekends
        commit_log = list(self.contribution_generator.repo.iter_commits())
        for commit in commit_log:
            commit_date = datetime.fromtimestamp(commit.committed_date)
            self.assertNotIn(commit_date.weekday(), [5, 6], "Commit was generated on a weekend.")

    def test_commit_message_format(self):
        """
        Test that generated commit messages follow the expected format.
        """
        target_date = datetime.now() - timedelta(days=5)
        self.logger.info(f"Testing commit message format for commit generated on: {target_date.isoformat()}")
        self.contribution_generator.generate_single_commit(target_date)

        # Verify the commit message format
        commit_log = list(self.contribution_generator.repo.iter_commits(max_count=1))
        commit_message = commit_log[0].message
        self.assertRegex(commit_message, r"^Contribution: \d{4}-\d{2}-\d{2} \d{2}:\d{2}$", "Commit message format is incorrect.")

if __name__ == "__main__":
    unittest.main()

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Test Contribution Generator
# -----------------------------------------------------------------------------------------------------