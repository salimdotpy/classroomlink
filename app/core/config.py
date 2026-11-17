
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    """
    Central application configuration.

    Values are loaded from environment variables
    and the project's .env file.
    """

    app_name: str = "ClassroomLink"
    app_env: str = "development"
    debug: bool = False

    secret_key: str = "development-only-change-this-secret"

    database_url: str = "sqlite+aiosqlite:///./classroomlink.db"
    sql_echo: bool = False

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    """
    Return a cached application settings instance.
    """
    return Settings()

settings = get_settings()