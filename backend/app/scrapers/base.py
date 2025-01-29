from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from ratelimit import limits, sleep_and_retry
from sqlalchemy.exc import IntegrityError
from ..database import SessionLocal
from ..config import get_settings
from ..models import Legislation

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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.db:
            self.db.close()

    def validate_api_key(self, key: Optional[str], source: str) -> None:
        """Validate that a required API key is present"""
        if not key:
            raise APIKeyMissingError(f"API key required for {source}")

    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method to be implemented by subclasses"""
        pass

    def save_legislation(self, data: Dict[str, Any]) -> None:
        """Save legislation data to database"""
        try:
            # Check if legislation already exists
            existing = self.db.query(Legislation).filter(
                Legislation.id == data['id']
            ).first()

            if existing:
                # Update existing record
                for key, value in data.items():
                    setattr(existing, key, value)
                self.logger.info(f"Updated existing legislation: {data['id']}")
            else:
                # Create new record
                legislation = Legislation(**data)
                self.db.add(legislation)
                self.logger.info(f"Added new legislation: {data['id']}")

            self.db.commit()

        except Exception as e:
            self.logger.error(f"Error saving legislation: {e}")
            self.db.rollback()
            raise

    def clear_existing_data(self) -> None:
        """Clear existing data for the scraper's type"""
        try:
            count = self.db.query(Legislation).delete()
            self.db.commit()
            self.logger.info(f"Cleared {count} existing records")
        except Exception as e:
            self.logger.error(f"Error clearing existing data: {e}")
            self.db.rollback()
            raise
