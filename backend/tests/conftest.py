"""
Pytest configuration and fixtures for Naija Oracle backend tests
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from typing import Dict, Any, Generator
import tempfile
import os

from app.config import settings
from app.services.groq_client import GroqClient
from app.services.cultural_voice_index import CulturalVoiceIndex
from app.services.supabase_client import SupabaseClient
from app.services.persona_simulator import PersonaSimulator
from app.services.recommendation_engine import RecommendationEngine
from app.services.embedding_service import EmbeddingService
from app.models.persona import Persona, PersonaCreate
from app.models.review import ReviewRequest, Product, Context
from app.models.recommendation import RecommendationRequest
from app.ml.evaluator import NaijaOracleEvaluator


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_groq_client():
    """Mock Groq client for testing"""
    client = Mock(spec=GroqClient)
    
    # Mock chat completion
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "This is a test review from Naija Oracle."
    
    client.chat.completions.create.return_value = mock_response
    
    # Mock streaming
    async def mock_stream(*args, **kwargs):
        tokens = ["This", "is", "a", "test", "stream"]
        for token in tokens:
            yield Mock(choices=[Mock(delta=Mock(content=token))])
    
    client.chat.completions.create.side_effect = lambda *args, **kwargs: (
        mock_stream(*args, **kwargs) if kwargs.get("stream") else mock_response
    )
    
    return client


@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client for testing"""
    client = Mock(spec=SupabaseClient)
    
    # Mock persona operations
    mock_persona = Persona(
        id="test_persona_id",
        user_id="test_user_id",
        name="Test User",
        age_range="25-34",
        city="Lagos",
        lga="Ikeja",
        primary_language="english",
        review_style="casual",
        avg_rating=3.5,
        sentiment_volatility="medium",
        categories_reviewed=["food", "fashion"],
        sample_reviews=["Good service"],
        cultural_markers=["price_sensitive"],
        pidgin_intensity=0.5,
        status="active"
    )
    
    client.get_persona.return_value = mock_persona
    client.create_persona.return_value = mock_persona
    client.get_user_personas.return_value = [mock_persona]
    
    return client


@pytest.fixture
def mock_cvi():
    """Mock Cultural Voice Index"""
    cvi = Mock(spec=CulturalVoiceIndex)
    
    # Mock anchors
    mock_anchor = Mock()
    mock_anchor.phrase = "E sweet me die"
    mock_anchor.tribe_region = "Yoruba"
    mock_anchor.pidgin_intensity = 0.8
    mock_anchor.sentiment_category = "strong_positive"
    mock_anchor.avg_rating_association = 5.0
    
    cvi.get_persona_anchors.return_value = [mock_anchor]
    cvi.get_all_anchors.return_value = [mock_anchor]
    
    return cvi


@pytest.fixture
def mock_embedding_service():
    """Mock embedding service"""
    service = Mock(spec=EmbeddingService)
    
    service.generate_persona_embedding.return_value = [0.1, 0.2, 0.3, 0.4]
    service.generate_product_embedding.return_value = [0.5, 0.6, 0.7, 0.8]
    service.calculate_similarity.return_value = 0.85
    
    return service


@pytest.fixture
def persona_simulator(mock_groq_client, mock_cvi, mock_supabase_client):
    """Persona simulator fixture with mocked dependencies"""
    return PersonaSimulator(mock_groq_client, mock_cvi, mock_supabase_client)


@pytest.fixture
def recommendation_engine(mock_groq_client, mock_supabase_client, mock_embedding_service):
    """Recommendation engine fixture with mocked dependencies"""
    return RecommendationEngine(mock_groq_client, mock_supabase_client, mock_embedding_service)


@pytest.fixture
def sample_persona_create():
    """Sample persona creation data"""
    return PersonaCreate(
        user_id="test_user_id",
        name="Test User",
        age_range="25-34",
        city="Lagos",
        lga="Ikeja",
        primary_language="english",
        review_style="casual",
        avg_rating=3.5,
        sentiment_volatility="medium",
        categories_reviewed=["food", "fashion"],
        sample_reviews=["Good service"],
        cultural_markers=["price_sensitive"],
        pidgin_intensity=0.5
    )


@pytest.fixture
def sample_review_request():
    """Sample review generation request"""
    return ReviewRequest(
        user_id="test_user_id",
        persona_id="test_persona_id",
        product=Product(
            name="Test Restaurant",
            category="restaurant",
            location="Lagos",
            price_tier="mid"
        ),
        context=Context(
            time_of_day="evening",
            occasion="casual",
            recency_of_visit="first_time"
        ),
        temperature=0.7,
        max_tokens=400
    )


@pytest.fixture
def sample_recommendation_request():
    """Sample recommendation request"""
    return RecommendationRequest(
        user_id="test_user_id",
        persona_id="test_persona_id",
        domain="food",
        context={
            "current_time": "Saturday 8PM",
            "location": "Lekki Phase 1",
            "mood_signal": "celebratory",
            "budget_naira": 5000
        },
        max_recommendations=5
    )


@pytest.fixture
def evaluator():
    """ML evaluator fixture"""
    return NaijaOracleEvaluator()


@pytest.fixture
def temp_env_vars():
    """Temporary environment variables for testing"""
    original_env = {}
    temp_env = {
        "GROQ_API_KEY": "test_key",
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_ANON_KEY": "test_anon_key",
        "SUPABASE_SERVICE_KEY": "test_service_key",
        "DATABASE_URL": "sqlite:///test.db"
    }
    
    # Store original values
    for key, value in temp_env.items():
        original_env[key] = os.environ.get(key)
        os.environ[key] = value
    
    yield temp_env
    
    # Restore original values
    for key, value in original_env.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    original_settings = {}
    
    # Mock settings values
    settings.GROQ_API_KEY = "test_key"
    settings.SUPABASE_URL = "https://test.supabase.co"
    settings.SUPABASE_ANON_KEY = "test_anon_key"
    settings.SUPABASE_SERVICE_KEY = "test_service_key"
    settings.DATABASE_URL = "sqlite:///test.db"
    settings.GROQ_MODEL = "test-model"
    settings.EMBEDDING_MODEL = "test-embedding-model"
    settings.BERTSCORE_TARGET = 0.82
    settings.ROUGE_L_TARGET = 0.35
    settings.RMSE_TARGET = 0.75
    settings.NDCG_TARGET = 0.847
    
    yield settings
    
    # Restore original settings (if needed)
    pass


@pytest.fixture
def test_database_url():
    """Test database URL"""
    return "sqlite:///test.db"


@pytest.fixture
def sample_cvi_data():
    """Sample CVI data for testing"""
    return [
        {
            "phrase": "E sweet me die",
            "tribe_region": "Yoruba",
            "pidgin_intensity": 0.8,
            "formality_register": "casual",
            "sentiment_category": "strong_positive",
            "product_context": "food",
            "avg_rating_association": 5.0,
            "frequency_score": 0.9,
            "confidence_score": 0.95
        },
        {
            "phrase": "Wahala be like bicycle",
            "tribe_region": "Pan-Nigerian",
            "pidgin_intensity": 0.7,
            "formality_register": "casual",
            "sentiment_category": "negative",
            "product_context": "service",
            "avg_rating_association": 1.5,
            "frequency_score": 0.8,
            "confidence_score": 0.9
        }
    ]


@pytest.fixture
def sample_training_data():
    """Sample training data for testing"""
    return [
        {
            "text": "<s>[INST]Generate review for persona[/INST]This place is great!</s>",
            "persona": {
                "name": "Test User",
                "city": "Lagos",
                "pidgin_intensity": 0.5
            },
            "product": {
                "name": "Test Restaurant",
                "category": "restaurant"
            },
            "rating": 4,
            "review": "This place is great!"
        }
    ]


@pytest.fixture
def sample_recommendation_data():
    """Sample recommendation data for testing"""
    return [
        {
            "user_rating_tendency": 3.5,
            "item_avg_rating": 4.2,
            "price_match_score": 0.8,
            "location_proximity": 0.9,
            "category_preference": 0.7,
            "time_relevance": 0.8,
            "mood_alignment": 0.9,
            "budget_fit": 0.85,
            "collaborative_score": 0.7,
            "popularity_score": 0.8,
            "relevance_score": 0.85
        }
    ]


# Async test helpers
@pytest.fixture
def async_client():
    """Async test client fixture"""
    from fastapi.testclient import TestClient
    from app.main import app
    
    return TestClient(app)


@pytest.fixture
async def async_test_client():
    """Async test client for FastAPI"""
    from httpx import AsyncClient
    from app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# Test utilities
@pytest.fixture
def create_mock_response(data: Dict[str, Any], status_code: int = 200):
    """Create a mock HTTP response"""
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = data
    mock_response.text = str(data)
    return mock_response


@pytest.fixture
def mock_stream_response(tokens: list):
    """Create a mock streaming response"""
    async def mock_stream():
        for token in tokens:
            yield token
    
    return mock_stream


# Database fixtures
@pytest.fixture
def test_db():
    """Test database fixture"""
    import sqlite3
    import tempfile
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as db_file:
        conn = sqlite3.connect(db_file.name)
        
        # Create test tables
        conn.execute("""
            CREATE TABLE personas (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                city TEXT,
                lga TEXT,
                primary_language TEXT,
                review_style TEXT,
                avg_rating REAL,
                pidgin_intensity REAL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            CREATE TABLE review_generations (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                persona_id TEXT NOT NULL,
                product TEXT,
                context TEXT,
                generation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        yield db_file.name
        
        # Cleanup
        os.unlink(db_file.name)


# Performance testing fixtures
@pytest.fixture
def benchmark_data():
    """Large dataset for performance testing"""
    import pandas as pd
    import numpy as np
    
    # Generate large test dataset
    size = 10000
    data = {
        "user_id": [f"user_{i}" for i in range(size)],
        "persona_id": [f"persona_{i % 100}" for i in range(size)],
        "rating": np.random.uniform(1, 5, size),
        "text": [f"Test review text {i}" for i in range(size)]
    }
    
    return pd.DataFrame(data)
