from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    """Application configuration."""
    AI_PROVIDER: Literal["google", "vertexai"] = "google"
    GOOGLE_API_KEY: str = "placeholder"
    GOOGLE_CLOUD_PROJECT: str = "placeholder"
    GOOGLE_CLOUD_LOCATION: str = "us-central1"
    VECTOR_DB_PATH: str = "./data/chroma_db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
