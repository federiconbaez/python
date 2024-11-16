
import logging
from typing import Dict, List
from datetime import datetime
from core.git_scraper import GitHubScraper
from core.date_handler import DateHandler

# -----------------------------------------------------------------------------------------------------
# @ Contribution Analyzer
# -----------------------------------------------------------------------------------------------------

class ContributionAnalyzer:
    """
    Class responsible for analyzing contributions in a Git repository.
    """
    
    def __init__(self, repo_url: str):
        self.repo_url = repo_url
        logging.info(f"ContributionAnalyzer initialized for repository: {repo_url}")
    
    async def analyze_contributions(self, start_date: datetime, end_date: datetime) -> Dict[str, int]:
        """
        Analyze contributions within a given date range.

        Args:
            start_date (datetime): The start date for analyzing contributions.
            end_date (datetime): The end date for analyzing contributions.

        Returns:
            Dict[str, int]: A dictionary with contributors as keys and their contribution counts as values.
        """
        try:
            logging.info(f"Starting contribution analysis from {start_date} to {end_date}")
            contributions = {}
            async with GitHubScraper() as scraper:
                commit_data = await scraper.fetch_contributions(self.repo_url, start_date, end_date)
                for commit in commit_data:
                    author = commit.get("commit", {}).get("author", {}).get("name", "Unknown")
                    if author in contributions:
                        contributions[author] += 1
                    else:
                        contributions[author] = 1
            logging.info(f"Contribution analysis completed successfully.")
            return contributions
        except Exception as e:
            logging.error(f"Failed to analyze contributions for {self.repo_url}: {e}")
            raise

    async def get_top_contributors(self, start_date: datetime, end_date: datetime, top_n: int = 5) -> List[Dict[str, int]]:
        """
        Get the top N contributors within a given date range.

        Args:
            start_date (datetime): The start date for analyzing contributions.
            end_date (datetime): The end date for analyzing contributions.
            top_n (int): Number of top contributors to return. Default is 5.

        Returns:
            List[Dict[str, int]]: A list of dictionaries representing the top N contributors and their contribution counts.
        """
        try:
            logging.info(f"Getting top {top_n} contributors from {start_date} to {end_date}")
            contributions = await self.analyze_contributions(start_date, end_date)
            sorted_contributions = sorted(contributions.items(), key=lambda x: x[1], reverse=True)
            top_contributors = [{"name": name, "contributions": count} for name, count in sorted_contributions[:top_n]]
            logging.info(f"Top contributors retrieved successfully.")
            return top_contributors
        except Exception as e:
            logging.error(f"Failed to get top contributors for {self.repo_url}: {e}")
            raise

    async def analyze_daily_contributions(self, start_date: datetime, end_date: datetime) -> Dict[str, int]:
        """
        Analyze the number of contributions made on each day within a given date range.

        Args:
            start_date (datetime): The start date for analyzing daily contributions.
            end_date (datetime): The end date for analyzing daily contributions.

        Returns:
            Dict[str, int]: A dictionary with dates as keys and the number of contributions as values.
        """
        try:
            logging.info(f"Starting daily contribution analysis from {start_date} to {end_date}")
            daily_contributions = {}
            async with GitHubScraper() as scraper:
                commit_data = await scraper.fetch_contributions(self.repo_url, start_date, end_date)
                for commit in commit_data:
                    commit_date_str = commit.get("commit", {}).get("author", {}).get("date", "")
                    if commit_date_str:
                        commit_date = datetime.strptime(commit_date_str, "%Y-%m-%dT%H:%M:%SZ").date()
                        commit_date_key = commit_date.strftime("%Y-%m-%d")
                        if commit_date_key in daily_contributions:
                            daily_contributions[commit_date_key] += 1
                        else:
                            daily_contributions[commit_date_key] = 1
            logging.info(f"Daily contribution analysis completed successfully.")
            return daily_contributions
        except Exception as e:
            logging.error(f"Failed to analyze daily contributions for {self.repo_url}: {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Contribution Analyzer
# -----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    repo_url = ""
    start_date = DateHandler.parse_date("2021-01-01")
    end_date = DateHandler.parse_date("2021-12-31")

    analyzer = ContributionAnalyzer(repo_url)
    top_contributors = analyzer.get_top_contributors(start_date, end_date)
    print(f"Top contributors: {top_contributors}")

    daily_contributions = analyzer.analyze_daily_contributions(start_date, end_date)
    print(f"Daily contributions: {daily_contributions}")

# -----------------------------------------------------------------------------------------------------