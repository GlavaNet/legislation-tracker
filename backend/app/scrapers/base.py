from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from ratelimit import limits, sleep_and_retry
from ..database import SessionLocal
from ..config import get_settings
from ..models.legislation import Legislation

settings = get_settings()

class APIKeyMissingError(Exception):
    """Raised when a required API key is missing"""
    pass

class RateLimitError(Exception):
    """Raised when API rate limit is exceeded"""
    pass

class BaseScraper(ABC):
    def __init__(self):
        self.db = SessionLocal()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.settings = get_settings()

    def validate_api_key(self, key: Optional[str], source: str) -> None:
        """Validate that a required API key is present"""
        if not key:
            raise APIKeyMissingError(f"API key required for {source}")

    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        pass

    def save_legislation(self, data: Dict[str, Any]) -> None:
        try:
            legislation = Legislation(**data)
            self.db.add(legislation)
            self.db.commit()
        except Exception as e:
            self.logger.error(f"Error saving legislation: {e}")
            self.db.rollback()
            raise
