from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    """Application configuration using Pydantic Settings."""
    APP_NAME: str = "AI CoE RAG API"
    DEBUG: bool = True
    
    # Provider Selection: "google" or "vertexai"
    AI_PROVIDER: Literal["google", "vertexai"] = "google"
    
    # Google AI Settings (Gemini API)
    GOOGLE_API_KEY: str = "placeholder"
    
    # Vertex AI Settings (GCP)
    GOOGLE_CLOUD_PROJECT: str = "placeholder"
    GOOGLE_CLOUD_LOCATION: str = "us-central1"
    
    # Storage Settings
    VECTOR_DB_PATH: str = "./data/chroma_db"

    # Load from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Global settings instance
settings = Settings()
