
from typing import Optional
from core.git_scraper import GitHubScraper
from interfaces.scraper_interface import ScraperInterface
import logging

# -----------------------------------------------------------------------------------------------------
# @ Scraper Factory
# -----------------------------------------------------------------------------------------------------

class GitScraperFactory:
    """
    Factory class to create different types of Git scrapers.
    """

    @staticmethod
    def create_scraper(scraper_type: str, repo_path: str, **kwargs) -> Optional[GitHubScraper]:
        """
        Creates an instance of a Git scraper based on the specified type.

        Args:
            scraper_type (str): The type of scraper to create. Options are "simple" or "advanced".
            repo_path (str): The path to the repository to be scraped.
            **kwargs: Additional arguments to customize the scraper behavior.

        Returns:
            GitHubScraper: An instance of the requested Git scraper.
        """
        logging.info(f"Creating Git scraper of type: {scraper_type}")
        try:
            if scraper_type.lower() == "simple":
                return GitHubScraper(repo_path, **kwargs)
            elif scraper_type.lower() == "advanced":
                return GitHubScraper(repo_path, **kwargs)
            else:
                logging.error(f"Unknown scraper type: {scraper_type}")
                return None
        except Exception as e:
            logging.error(f"Error creating scraper of type '{scraper_type}': {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Scraper Factory
# -----------------------------------------------------------------------------------------------------