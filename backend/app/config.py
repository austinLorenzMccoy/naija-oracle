"""
Configuration settings for Naija Oracle
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_V1_STR = "/api/v1"
PROJECT_NAME = "Naija Oracle"

# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.1-70b-versatile"

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

# DagsHub Configuration
DAGSHUB_TOKEN = os.getenv("DAGSHUB_TOKEN", "")
DAGSHUB_USERNAME = os.getenv("DAGSHUB_USERNAME", "")

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "")

# ML Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
BERTSCORE_MODEL = "bert-base-multilingual-cased"

# Cultural Voice Index Settings
CVI_THRESHOLD = 0.6
PIDGIN_INTENSITY_DEFAULT = 0.5

# Evaluation Settings
BERTSCORE_TARGET = 0.82
ROUGE_L_TARGET = 0.35
RMSE_TARGET = 0.75
NDCG_TARGET = 0.847

# Rate Limiting
RATE_LIMIT_PER_MINUTE = 30
