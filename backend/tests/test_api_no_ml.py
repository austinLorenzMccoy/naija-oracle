"""
Basic API tests without ML dependencies
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os

# Mock ML dependencies before importing
sys.modules['sentence_transformers'] = Mock()
sys.modules['torch'] = Mock()
sys.modules['transformers'] = Mock()
sys.modules['bert_score'] = Mock()
sys.modules['rouge_score'] = Mock()
sys.modules['mlflow'] = Mock()

from app.main import app


class TestBasicAPI:
    """Test basic API functionality without ML dependencies"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_endpoint(self, client):
        """Test health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data
    
    def test_docs_endpoint(self, client):
        """Test docs endpoint"""
        response = client.get("/docs")
        assert response.status_code in [200, 307]
    
    def test_redoc_endpoint(self, client):
        """Test ReDoc endpoint"""
        response = client.get("/redoc")
        assert response.status_code in [200, 307]
    
    def test_cors_headers(self, client):
        """Test CORS headers"""
        response = client.options("/api/v1/personas")
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


class TestConfiguration:
    """Test application configuration"""
    
    def test_settings_initialization(self):
        """Test settings can be initialized"""
        from app.config import settings
        assert settings is not None
        assert settings.PROJECT_NAME == "Naija Oracle"
        assert settings.API_V1_STR == "/api/v1"
    
    def test_environment_variables(self):
        """Test environment variables are loaded"""
        from app.config import settings
        # Check that environment variables are loaded
        assert hasattr(settings, 'GROQ_API_KEY')
        assert hasattr(settings, 'SUPABASE_URL')
        assert hasattr(settings, 'DAGSHUB_TOKEN')
    
    def test_config_values(self):
        """Test configuration values"""
        from app.config import settings
        # Test default values
        assert settings.CVI_THRESHOLD == 0.6
        assert settings.PIDGIN_INTENSITY_DEFAULT == 0.5
        assert settings.BERTSCORE_TARGET == 0.82
        assert settings.ROUGE_L_TARGET == 0.35
        assert settings.RMSE_TARGET == 0.75
        assert settings.NDCG_TARGET == 0.847


class TestModelsWithoutML:
    """Test basic model functionality without ML dependencies"""
    
    def test_persona_model_import(self):
        """Test persona models can be imported"""
        from app.models.persona import Persona, PersonaCreate, PersonaUpdate
        assert Persona is not None
        assert PersonaCreate is not None
        assert PersonaUpdate is not None
    
    def test_review_model_import(self):
        """Test review models can be imported"""
        from app.models.review import ReviewRequest, ReviewResponse
        assert ReviewRequest is not None
        assert ReviewResponse is not None
    
    def test_recommendation_model_import(self):
        """Test recommendation models can be imported"""
        from app.models.recommendation import RecommendationRequest, RecommendationResponse
        assert RecommendationRequest is not None
        assert RecommendationResponse is not None
    
    def test_cultural_voice_model_import(self):
        """Test cultural voice models can be imported"""
        from app.models.cultural_voice import CVIAnchor, CulturalVoiceIndex
        assert CVIAnchor is not None
        assert CulturalVoiceIndex is not None


class TestBasicValidation:
    """Test basic validation functionality"""
    
    def test_persona_create_validation(self):
        """Test persona creation validation"""
        from app.models.persona import PersonaCreate, PersonaLanguage
        
        # Valid persona
        persona_data = {
            "user_id": "test_user",
            "name": "Test User",
            "age_range": "25-34",
            "city": "Lagos",
            "primary_language": PersonaLanguage.ENGLISH,
            "review_style": "casual",
            "avg_rating": 3.5,
            "pidgin_intensity": 0.5
        }
        
        persona = PersonaCreate(**persona_data)
        assert persona.name == "Test User"
        assert persona.city == "Lagos"
        assert persona.avg_rating == 3.5
    
    def test_invalid_rating_validation(self):
        """Test invalid rating validation"""
        from app.models.persona import PersonaCreate, PersonaLanguage
        from pydantic import ValidationError
        
        # Invalid rating > 5
        persona_data = {
            "user_id": "test_user",
            "name": "Test User",
            "age_range": "25-34",
            "city": "Lagos",
            "primary_language": PersonaLanguage.ENGLISH,
            "review_style": "casual",
            "avg_rating": 6.0,  # Invalid
            "pidgin_intensity": 0.5
        }
        
        with pytest.raises(ValidationError):
            PersonaCreate(**persona_data)
    
    def test_invalid_pidgin_intensity_validation(self):
        """Test invalid pidgin intensity validation"""
        from app.models.persona import PersonaCreate, PersonaLanguage
        from pydantic import ValidationError
        
        # Invalid pidgin intensity > 1.0
        persona_data = {
            "user_id": "test_user",
            "name": "Test User",
            "age_range": "25-34",
            "city": "Lagos",
            "primary_language": PersonaLanguage.ENGLISH,
            "review_style": "casual",
            "avg_rating": 3.5,
            "pidgin_intensity": 1.5  # Invalid
        }
        
        with pytest.raises(ValidationError):
            PersonaCreate(**persona_data)


class TestDatabaseSetup:
    """Test database setup without actual connections"""
    
    def test_database_import(self):
        """Test database module can be imported"""
        from app.database import Base, init_db
        assert Base is not None
        assert init_db is not None
    
    def test_database_models(self):
        """Test database models exist"""
        from app.database import Base
        # Check that Base exists and can be used
        assert hasattr(Base, 'metadata')
        assert hasattr(Base, 'registry')


class TestRoutersImport:
    """Test router imports without ML dependencies"""
    
    def test_auth_router_import(self):
        """Test auth router can be imported"""
        from app.routers import auth
        assert auth is not None
        assert hasattr(auth, 'router')
    
    def test_personas_router_import(self):
        """Test personas router can be imported"""
        from app.routers import personas
        assert personas is not None
        assert hasattr(personas, 'router')
    
    def test_simulate_router_import(self):
        """Test simulate router can be imported"""
        from app.routers import simulate
        assert simulate is not None
        assert hasattr(simulate, 'router')
    
    def test_recommend_router_import(self):
        """Test recommend router can be imported"""
        from app.routers import recommend
        assert recommend is not None
        assert hasattr(recommend, 'router')


class TestAPIEndpoints:
    """Test API endpoints with mocked services"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    @patch('app.routers.personas.SupabaseClient')
    def test_get_persona_stats_endpoint(self, mock_supabase, client):
        """Test persona stats endpoint"""
        # Mock the analytics data
        mock_supabase.return_value.get_analytics_data.return_value = {
            "persona_count": 5,
            "review_count": 25,
            "recommendation_count": 15,
            "recent_activity": []
        }
        
        response = client.get("/api/v1/personas/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_personas" in data
        assert "active_personas" in data
        assert "cities_covered" in data
    
    @patch('app.routers.simulate.PersonaSimulator')
    def test_simulator_health_endpoint(self, mock_simulator, client):
        """Test simulator health endpoint"""
        response = client.get("/api/v1/simulate/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Review Simulator"
    
    @patch('app.routers.recommend.RecommendationEngine')
    def test_recommendation_health_endpoint(self, mock_engine, client):
        """Test recommendation health endpoint"""
        response = client.get("/api/v1/recommend/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Recommendation Engine"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
