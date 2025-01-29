from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite:///./legislation.db"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Legislation Tracker"
    
    # API Keys
    CONGRESS_API_KEY: str | None = None
    NY_LEGISLATURE_API_KEY: str | None = None
    CA_LEGISLATURE_API_KEY: str | None = None
    
    # External API URLs
    CONGRESS_API_BASE_URL: str = "https://api.congress.gov/v3"
    
    # Rate limiting
    RATELIMIT_STORAGE_URL: str = "memory://"
    DEFAULT_RATE_LIMIT: str = "100/minute"
    
    # CORS Settings
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()
