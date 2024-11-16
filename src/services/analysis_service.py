
import logging
from datetime import datetime
from typing import Dict, Any, List
from repositories.git_repository import GitRepository
from repositories.commit_repository import CommitRepository

# -----------------------------------------------------------------------------------------------------
# @ Analysis Service
# -----------------------------------------------------------------------------------------------------

class AnalysisService:
    """
    Service for analyzing Git repository data such as commits, contributors, branches, and more.
    """

    def __init__(self, repo_path: str):
        self.repo = GitRepository(repo_path)
        self.commit_repo = CommitRepository(repo_path)

    def analyze_commit_activity(self, branch_name: str = 'develop') -> Dict[str, Any]:
        """
        Analyzes commit activity for a specific branch.

        Args:
            branch_name (str): The branch to analyze. Defaults to 'develop'.

        Returns:
            Dict[str, Any]: Analysis of commit activity, including frequency and recent commit details.
        """
        try:
            logging.info(f"Analyzing commit activity for branch '{branch_name}'.")
            commits = self.commit_repo.list_commits(branch_name=branch_name, limit=100)
            activity_summary = {
                "total_commits": len(commits),
                "commits_per_day": self._calculate_commits_per_day(commits),
                "most_recent_commit": commits[0] if commits else None,
                "author_activity": self._calculate_author_activity(commits)
            }
            logging.info(f"Commit activity analysis for branch '{branch_name}' completed successfully.")
            return activity_summary
        except Exception as e:
            logging.error(f"Unexpected error while analyzing commit activity: {e}")
            raise

    def _calculate_commits_per_day(self, commits: List[Dict[str, str]]) -> Dict[str, int]:
        """
        Helper function to calculate commits per day.

        Args:
            commits (List[Dict[str, str]]): List of commits.

        Returns:
            Dict[str, int]: Number of commits per day.
        """
        try:
            commits_per_day = {}
            for commit in commits:
                commit_date = datetime.fromisoformat(commit["date"]).date().isoformat()
                if commit_date not in commits_per_day:
                    commits_per_day[commit_date] = 0
                commits_per_day[commit_date] += 1
            logging.info(f"Calculated commits per day: {commits_per_day}")
            return commits_per_day
        except Exception as e:
            logging.error(f"Unexpected error while calculating commits per day: {e}")
            raise

    def _calculate_author_activity(self, commits: List[Dict[str, str]]) -> Dict[str, int]:
        """
        Helper function to calculate commit activity by author.

        Args:
            commits (List[Dict[str, str]]): List of commits.

        Returns:
            Dict[str, int]: Number of commits by each author.
        """
        try:
            author_activity = {}
            for commit in commits:
                author = commit["author"]
                if author not in author_activity:
                    author_activity[author] = 0
                author_activity[author] += 1
            logging.info(f"Calculated author activity: {author_activity}")
            return author_activity
        except Exception as e:
            logging.error(f"Unexpected error while calculating author activity: {e}")
            raise

    def analyze_branch_contributions(self) -> List[Dict[str, Any]]:
        """
        Analyzes contributions across all branches in the repository.

        Returns:
            List[Dict[str, Any]]: List of branch contributions containing branch name and total commits.
        """
        try:
            logging.info("Analyzing contributions across all branches.")
            branches = self.repo.get_branches()
            branch_contributions = []
            for branch in branches:
                commits = self.commit_repo.list_commits(branch_name=branch, limit=1000)
                branch_contributions.append({
                    "branch_name": branch,
                    "total_commits": len(commits)
                })
            logging.info(f"Branch contributions analysis completed successfully: {branch_contributions}")
            return branch_contributions
        except Exception as e:
            logging.error(f"Unexpected error while analyzing branch contributions: {e}")
            raise

    def identify_active_contributors(self, branch_name: str = 'develop') -> List[str]:
        """
        Identifies active contributors for a specific branch.

        Args:
            branch_name (str): The branch to analyze. Defaults to 'develop'.

        Returns:
            List[str]: List of active contributors' names.
        """
        try:
            logging.info(f"Identifying active contributors for branch '{branch_name}'.")
            commits = self.commit_repo.list_commits(branch_name=branch_name, limit=1000)
            author_activity = self._calculate_author_activity(commits)
            sorted_contributors = sorted(author_activity.items(), key=lambda x: x[1], reverse=True)
            active_contributors = [author for author, count in sorted_contributors]
            logging.info(f"Active contributors identified: {active_contributors}")
            return active_contributors
        except Exception as e:
            logging.error(f"Unexpected error while identifying active contributors: {e}")
            raise

    def generate_commit_statistics(self, branch_name: str = 'develop') -> Dict[str, Any]:
        """
        Generates commit statistics such as average commits per day.

        Args:
            branch_name (str): The branch to analyze. Defaults to 'develop'.

        Returns:
            Dict[str, Any]: Statistics related to commits.
        """
        try:
            logging.info(f"Generating commit statistics for branch '{branch_name}'.")
            commits = self.commit_repo.list_commits(branch_name=branch_name, limit=1000)
            commits_per_day = self._calculate_commits_per_day(commits)
            total_commits = len(commits)
            unique_days = len(commits_per_day)
            average_commits_per_day = total_commits / unique_days if unique_days > 0 else 0

            commit_statistics = {
                "total_commits": total_commits,
                "average_commits_per_day": average_commits_per_day,
                "unique_commit_days": unique_days
            }

            logging.info(f"Commit statistics generated successfully: {commit_statistics}")
            return commit_statistics
        except Exception as e:
            logging.error(f"Unexpected error while generating commit statistics: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Analysis Service
# -----------------------------------------------------------------------------------------------------