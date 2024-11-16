
import unittest
import tempfile
import os
import logging
from datetime import datetime
from src.core.git_scraper import GitHubScraper
from src.utils.logger import LoggerUtils
from git import Repo

# -----------------------------------------------------------------------------------------------------
# @ Test Git Scraper
# -----------------------------------------------------------------------------------------------------

class TestGitHubScraper(unittest.TestCase):
    """
    Unit tests to validate the behavior of the GitHubScraper.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the testing environment, including initializing logging and creating a temporary repository.
        """
        # Setup logging for the test
        LoggerUtils.setup_logging("logs/test_git_scraper.log", level=logging.DEBUG)
        cls.logger = LoggerUtils.get_logger(__name__)

        # Create a temporary directory to initialize the test repository
        cls.repo_dir = tempfile.mkdtemp()
        cls.logger.info(f"Temporary repository created at: {cls.repo_dir}")

        # Initialize an empty Git repository for testing
        cls.repo = Repo.init(cls.repo_dir)
        cls.logger.info("Initialized empty Git repository for testing.")

        # Initialize GitHubScraper
        cls.git_scraper = GitHubScraper(cls.repo_dir)

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

    def test_scrape_commits(self):
        """
        Test scraping commits from the repository.
        """
        # Create a file to commit
        file_path = os.path.join(self.repo_dir, "README.md")
        with open(file_path, "w") as f:
            f.write("# Test Repository\nThis is a test repository.")
        self.logger.info("Created README.md for commit testing.")

        # Commit the file
        self.repo.index.add([file_path])
        commit_message = "Initial commit for README.md"
        self.repo.index.commit(commit_message)
        self.logger.info("Initial commit created in the repository.")

        # Scrape the commits using GitHubScraper
        commits = self.git_scraper.scrape_commits(branch_name="main")
        self.assertEqual(len(commits), 1, "Number of commits scraped is incorrect.")
        self.assertEqual(commits[0]["message"], commit_message, "Commit message does not match.")

    def test_scrape_contributors(self):
        """
        Test scraping contributors from the repository.
        """
        # Create a file to commit
        file_path = os.path.join(self.repo_dir, "CONTRIBUTORS.md")
        with open(file_path, "w") as f:
            f.write("# Contributors\nList of contributors.")
        self.logger.info("Created CONTRIBUTORS.md for testing contributor scraping.")

        # Commit the file
        self.repo.index.add([file_path])
        author_name = "Test Author"
        author_email = "author@example.com"
        self.repo.index.commit("Add CONTRIBUTORS.md", author=author_name, author_email=author_email)
        self.logger.info("Commit created with a specific author.")

        # Scrape the contributors using GitHubScraper
        contributors = self.git_scraper.scrape_contributors()
        self.assertEqual(len(contributors), 1, "Number of contributors scraped is incorrect.")
        self.assertEqual(contributors[0]["name"], author_name, "Contributor name does not match.")
        self.assertEqual(contributors[0]["email"], author_email, "Contributor email does not match.")

    def test_checkout_branch(self):
        """
        Test checking out a new branch in the repository.
        """
        branch_name = "feature-branch"
        self.logger.info(f"Testing branch checkout for branch: {branch_name}")
        new_branch = self.repo.create_head(branch_name)
        self.git_scraper.checkout_branch(branch_name)

        # Verify current branch is the new branch
        current_branch = self.repo.active_branch
        self.assertEqual(current_branch.name, branch_name, "Failed to check out the correct branch.")

    def test_fetch_tags(self):
        """
        Test fetching tags from the repository.
        """
        tag_name = "v1.0"
        self.logger.info(f"Testing tag creation: {tag_name}")
        self.repo.create_tag(tag_name)
        tags = self.git_scraper.fetch_tags()
        self.assertIn(tag_name, tags, "Tag was not fetched successfully.")

if __name__ == "__main__":
    unittest.main()

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Test Git Scraper
# -----------------------------------------------------------------------------------------------------
