"""
Configuration settings for Naija Oracle
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Naija Oracle"
    
    # Groq Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.1-70b-versatile"
    
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")
    
    # DagsHub Configuration
    DAGSHUB_TOKEN: Optional[str] = os.getenv("DAGSHUB_TOKEN", "")
    DAGSHUB_USERNAME: Optional[str] = os.getenv("DAGSHUB_USERNAME", "")
    
    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # ML Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    BERTSCORE_MODEL: str = "bert-base-multilingual-cased"
    
    # Cultural Voice Index Settings
    CVI_THRESHOLD: float = 0.6
    PIDGIN_INTENSITY_DEFAULT: float = 0.5
    
    # Evaluation Settings
    BERTSCORE_TARGET: float = 0.82
    ROUGE_L_TARGET: float = 0.35
    RMSE_TARGET: float = 0.75
    NDCG_TARGET: float = 0.847
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 30
    
    model_config = {"env_file": ".env", "case_sensitive": True, "extra": "ignore"}

# Global settings instance
settings = Settings()
