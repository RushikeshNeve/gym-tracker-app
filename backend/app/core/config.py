from pathlib import Path

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Fitness Tracker API"
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/fitness_tracker"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000", "http://localhost:5173", "http://localhost:4173"])
    default_profile_id: int = 1
    use_null_pool: bool = False
    storage_backend: str = "local"
    blob_read_write_token: str | None = None
    blob_api_base_url: str = "https://blob.vercel-storage.com"
    media_root: str = str(Path(__file__).resolve().parents[2] / "media")
    media_url_prefix: str = "/media"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="FITNESS_",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
