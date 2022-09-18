"""
Settings
"""
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings"""

    db_host: str
    db_name: str
    db_pass: str
    db_user: str
    salt: str
    tz: str

    class Config:
        """Load configuration from .env file"""

        env_file = ".env"


@lru_cache()
def get_settings():
    """Get Settings"""
    return Settings()
