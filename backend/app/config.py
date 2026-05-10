"""
Configuration settings for Naija Oracle
"""

import os
from typing import Optional
from dotenv import load_dotenv

class Settings:
    """Application settings"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # API Configuration
        self.API_V1_STR = "/api/v1"
        self.PROJECT_NAME = "Naija Oracle"
        
        # Groq Configuration
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
        self.GROQ_MODEL = "llama-3.1-70b-versatile"
        
        # Supabase Configuration
        self.SUPABASE_URL = os.getenv("SUPABASE_URL", "")
        self.SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
        self.SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
        
        # DagsHub Configuration
        self.DAGSHUB_TOKEN = os.getenv("DAGSHUB_TOKEN", "")
        self.DAGSHUB_USERNAME = os.getenv("DAGSHUB_USERNAME", "")
        
        # JWT Configuration
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
        self.JWT_ALGORITHM = "HS256"
        self.JWT_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
        
        # Database Configuration
        self.DATABASE_URL = os.getenv("DATABASE_URL", "")
        
        # ML Configuration
        self.EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
        self.BERTSCORE_MODEL = "bert-base-multilingual-cased"
        
        # Cultural Voice Index Settings
        self.CVI_THRESHOLD = 0.6
        self.PIDGIN_INTENSITY_DEFAULT = 0.5
        
        # Evaluation Settings
        self.BERTSCORE_TARGET = 0.82
        self.ROUGE_L_TARGET = 0.35
        self.RMSE_TARGET = 0.75
        self.NDCG_TARGET = 0.847
        
        # Rate Limiting
        self.RATE_LIMIT_PER_MINUTE = 30

# Global settings instance
settings = Settings()
