"""
Configuration settings for Naija Oracle — Task B: Recommendation Engine
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Naija Oracle — Task B"

    # Groq Configuration
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-70b-versatile"

    # Supabase Configuration
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""

    # DagsHub Configuration
    DAGSHUB_TOKEN: str = ""
    DAGSHUB_USERNAME: str = ""

    # JWT Configuration
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7

    # Database Configuration
    DATABASE_URL: str = ""

    # ML Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Cultural Voice Index Settings
    CVI_THRESHOLD: float = 0.6
    PIDGIN_INTENSITY_DEFAULT: float = 0.5


settings = Settings()
