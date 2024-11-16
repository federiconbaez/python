# src/config/settings.py
from dataclasses import dataclass
from typing import Dict, Any, Optional
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

@dataclass
class GitConfig:
    """Configuration for Git operations"""
    default_branch: str
    commit_message_template: str
    max_commits_per_day: int
    min_commits_per_day: int
    default_author: str
    default_email: str

@dataclass
class ScraperConfig:
    """Configuration for scraping operations"""
    request_timeout: int
    max_retries: int
    retry_delay: int
    user_agent: str
    max_concurrent_requests: int

@dataclass
class DateConfig:
    """Configuration for date handling"""
    date_format: str
    timezone: str
    weekend_policy: str
    max_days_lookback: int
    max_days_ahead: int

class Settings:
    """
    Singleton class for managing application settings
    Uses environment variables and YAML configuration
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self._load_environment()
        self._load_config()
        self._setup_configurations()

    def _load_environment(self):
        """Load environment variables"""
        load_dotenv()
        self.env = os.getenv('APP_ENV', 'development')
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'

    def _load_config(self):
        """Load configuration from YAML file based on environment"""
        config_path = Path(__file__).parent / f'config_{self.env}.yaml'
        with open(config_path, 'r') as file:
            self._config = yaml.safe_load(file)

    def _setup_configurations(self):
        """Setup specific configuration objects"""
        self.git = GitConfig(
            default_branch=self._config['git']['default_branch'],
            commit_message_template=self._config['git']['commit_message_template'],
            max_commits_per_day=self._config['git']['max_commits_per_day'],
            min_commits_per_day=self._config['git']['min_commits_per_day'],
            default_author=os.getenv('GIT_AUTHOR', self._config['git']['default_author']),
            default_email=os.getenv('GIT_EMAIL', self._config['git']['default_email'])
        )

        self.scraper = ScraperConfig(
            request_timeout=self._config['scraper']['request_timeout'],
            max_retries=self._config['scraper']['max_retries'],
            retry_delay=self._config['scraper']['retry_delay'],
            user_agent=self._config['scraper']['user_agent'],
            max_concurrent_requests=self._config['scraper']['max_concurrent_requests']
        )

        self.date = DateConfig(
            date_format=self._config['date']['date_format'],
            timezone=self._config['date']['timezone'],
            weekend_policy=self._config['date']['weekend_policy'],
            max_days_lookback=self._config['date']['max_days_lookback'],
            max_days_ahead=self._config['date']['max_days_ahead']
        )

    @property
    def version(self) -> str:
        """Get application version"""
        return self._config['version']

    def get_database_url(self) -> str:
        """Get database URL with priority to environment variable"""
        return os.getenv('DATABASE_URL', self._config['database']['url'])
