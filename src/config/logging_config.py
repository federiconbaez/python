# src/config/logging_config.py
import logging
import logging.config
import os
from typing import Dict
import json
from pathlib import Path

class LoggingSetup:
    """Configure logging for the application"""
    
    @staticmethod
    def setup_logging(
        default_path: str = 'logging_config.json',
        default_level: int = logging.INFO,
        env_key: str = 'LOG_CFG'
    ) -> None:
        """Setup logging configuration"""
        path = Path(__file__).parent / default_path
        value = os.getenv(env_key, None)
        
        if value:
            path = Path(value)
            
        if path.exists():
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
