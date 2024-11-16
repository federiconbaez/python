
import os
from typing import List, Dict, Optional
import aiohttp
import asyncio
from datetime import datetime
from interfaces.scraper_interface import ScraperInterface
from config import settings
import logging

# -----------------------------------------------------------------------------------------------------
# @ Git Scraper
# -----------------------------------------------------------------------------------------------------

class GitHubScraper(ScraperInterface):
    """
    Implementation of GitHub scraping functionality
    """
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.base_url = "https://api.github.com"
        self.headers = {
            "User-Agent": settings.scraper.user_agent,
            "Accept": "application/vnd.github.v3+json"
        }
        if token := os.getenv("GITHUB_TOKEN"):
            self.headers["Authorization"] = f"token {token}"
        logging.info("GitHubScraper initialized with headers: %s", self.headers)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        logging.info("Client session for GitHubScraper started.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            logging.info("Client session for GitHubScraper closed.")

    async def fetch_repository_data(self, repo_url: str) -> Dict:
        """
        Fetch repository data from GitHub

        Args:
            repo_url (str): The URL of the GitHub repository.

        Returns:
            Dict: A dictionary containing the repository data.
        """
        repo_info = self._parse_repo_url(repo_url)
        try:
            async with self.session.get(
                f"{self.base_url}/repos/{repo_info['owner']}/{repo_info['name']}"
            ) as response:
                response.raise_for_status()
                repo_data = await response.json()
                logging.info(f"Repository data fetched successfully for {repo_url}")
                return repo_data
        except aiohttp.ClientError as e:
            logging.error(f"Failed to fetch repository data for {repo_url}: {e}")
            return {}

    async def fetch_contributions(
        self,
        repo_url: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """
        Fetch contribution data for a specific time period

        Args:
            repo_url (str): The URL of the GitHub repository.
            start_date (datetime): The start date of the contribution period.
            end_date (datetime): The end date of the contribution period.

        Returns:
            List[Dict]: A list of dictionaries containing commit data.
        """
        repo_info = self._parse_repo_url(repo_url)
        try:
            async with self.session.get(
                f"{self.base_url}/repos/{repo_info['owner']}/{repo_info['name']}/commits",
                params={
                    "since": start_date.isoformat(),
                    "until": end_date.isoformat()
                }
            ) as response:
                response.raise_for_status()
                commits_data = await response.json()
                logging.info(f"Commits data fetched successfully for {repo_url} from {start_date} to {end_date}")
                return await self._process_commits(commits_data)
        except aiohttp.ClientError as e:
            logging.error(f"Failed to fetch contributions for {repo_url}: {e}")
            return []

    async def _process_commits(self, commits_data: List[Dict]) -> List[Dict]:
        """
        Process and enrich commit data

        Args:
            commits_data (List[Dict]): A list of commit data dictionaries.

        Returns:
            List[Dict]: A list of enriched commit data dictionaries.
        """
        tasks = []
        try:
            for commit in commits_data:
                tasks.append(self._fetch_commit_details(commit["url"]))
            enriched_data = await asyncio.gather(*tasks)
            logging.info("Successfully processed commit details.")
            return enriched_data
        except Exception as e:
            logging.error(f"Error processing commit data: {e}")
            return []

    async def _fetch_commit_details(self, commit_url: str) -> Dict:
        """
        Fetch detailed information for a specific commit

        Args:
            commit_url (str): The URL of the commit to fetch.

        Returns:
            Dict: A dictionary containing commit details.
        """
        try:
            async with self.session.get(commit_url) as response:
                response.raise_for_status()
                commit_details = await response.json()
                logging.info(f"Commit details fetched successfully for {commit_url}")
                return commit_details
        except aiohttp.ClientError as e:
            logging.error(f"Failed to fetch commit details for {commit_url}: {e}")
            return {}

    def _parse_repo_url(self, repo_url: str) -> Dict[str, str]:
        """
        Parse repository URL to extract owner and name

        Args:
            repo_url (str): The URL of the GitHub repository.

        Returns:
            Dict[str, str]: A dictionary with 'owner' and 'name' of the repository.
        """
        try:
            parts = repo_url.rstrip("/").split("/")
            owner, name = parts[-2], parts[-1].replace(".git", "")
            logging.info(f"Parsed repository URL: owner={owner}, name={name}")
            return {
                "owner": owner,
                "name": name
            }
        except Exception as e:
            logging.error(f"Failed to parse repository URL '{repo_url}': {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Git Scraper
# -----------------------------------------------------------------------------------------------------
