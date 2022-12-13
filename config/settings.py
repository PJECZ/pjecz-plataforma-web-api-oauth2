"""
Settings: first environment variables, then .env file, then google cloud secret manager
"""
import os

from functools import lru_cache
from google.cloud import secretmanager
from pydantic import BaseSettings

PROJECT_ID = os.getenv("PROJECT_ID", "")


def get_secret(secret_id: str) -> str:
    """Get secret from google cloud secret manager"""

    # If not in google cloud, return environment variable
    if PROJECT_ID == "":
        return os.getenv(secret_id.upper(), "")

    # Create the secret manager client
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    name = client.secret_version_path(PROJECT_ID, f"pjecz_plataforma_web_{secret_id}", "latest")

    # Access the secret version
    response = client.access_secret_version(name=name)

    # Return the decoded payload
    return response.payload.data.decode("UTF-8")


class Settings(BaseSettings):
    """Settings"""

    db_host: str = get_secret("db_host")
    db_name: str = get_secret("db_name")
    db_pass: str = get_secret("db_pass")
    db_user: str = get_secret("db_user")
    origins: str = "https://plataforma-web.justiciadigital.gob.mx"
    salt: str = get_secret("salt")
    tz: str = "America/Mexico_City"

    class Config:
        """Config"""

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Customise sources, first environment variables, then .env file, then google cloud secret manager"""
            return env_settings, file_secret_settings, init_settings


@lru_cache()
def get_settings():
    """Get Settings"""
    return Settings()
