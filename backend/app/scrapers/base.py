from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging
from ratelimit import limits, sleep_and_retry
from sqlalchemy.exc import IntegrityError
from sqlalchemy import literal
from ..database import SessionLocal
from ..config import get_settings
from ..models import Legislation, Status, LegislationType

class APIKeyMissingError(Exception):
    pass

class RateLimitError(Exception):
    pass

class BaseScraper(ABC):
    def __init__(self):
        self._db = None
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.settings = get_settings()

    @property
    def db(self):
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._db:
            self._db.close()
            self._db = None

    def validate_api_key(self, key: Optional[str], source: str) -> None:
        if not key:
            raise APIKeyMissingError(f"API key required for {source}")

    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        pass

    def save_legislation(self, data: Dict[str, Any]) -> None:
        try:
            # Log the data before saving
            print(f"Saving legislation: {data}")

            # Convert enums to string values
            if isinstance(data.get('type'), LegislationType):
                data['type'] = data['type'].value
            if isinstance(data.get('status'), Status):
                data['status'] = data['status'].value

            # Check if legislation already exists
            existing = self.db.query(Legislation).filter(
                Legislation.id == data['id']
            ).first()

            if existing:
                # Update existing record
                for key, value in data.items():
                    setattr(existing, key, value)
                self.logger.info(f"Updated legislation: {data['id']}")
            else:
                # Create new record
                legislation = Legislation(**data)
                self.db.add(legislation)
                self.logger.info(f"Added new legislation: {data['id']}")
            
            # Commit and verify
            self.db.commit()
            
            # Verify the save worked
            saved = self.db.query(Legislation).filter(
                Legislation.id == data['id']
            ).first()
            print(f"Verified saved legislation: {saved.id}, type: {saved.type}")

        except Exception as e:
            self.logger.error(f"Error saving legislation: {str(e)}")
            self.db.rollback()
            raise

    def clear_existing_data(self) -> None:
        try:
            print("Starting to clear data...")
            query = self.db.query(Legislation)
            count = query.delete()
            self.db.commit()
            print(f"Cleared {count} existing records")
        except Exception as e:
            self.logger.error(f"Error clearing data: {str(e)}")
            self.db.rollback()
            raise
