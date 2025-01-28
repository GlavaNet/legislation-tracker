from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./legislation.db"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Legislation Tracker"
    CONGRESS_API_KEY: str | None = None
    CONGRESS_API_BASE_URL: str = "https://api.congress.gov/v3"
    RATELIMIT_STORAGE_URL: str = "memory://"
    DEFAULT_RATE_LIMIT: str = "100/minute"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
