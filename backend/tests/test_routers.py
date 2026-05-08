"""
Test suite for API routers
"""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch

from app.main import app
from app.models.persona import PersonaCreate
from app.models.review import ReviewRequest
from app.models.recommendation import RecommendationRequest


class TestAuthRouter:
    """Test authentication router"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    def test_login_success(self, client):
        """Test successful login"""
        with patch('app.routers.auth.SupabaseClient') as mock_supabase:
            mock_supabase.return_value.create_user_session.return_value = "session_123"
            
            response = client.post("/api/v1/auth/login", json={
                "user_id": "test_user",
                "email": "test@example.com"
            })
            
            assert response.status_code == 200
            data = response.json()
            assert data["session_id"] == "session_123"
            assert "token" in data
            assert data["message"] == "Authentication successful"
    
    def test_login_invalid_data(self, client):
        """Test login with invalid data"""
        response = client.post("/api/v1/auth/login", json={})
        
        assert response.status_code == 422  # Validation error
    
    def test_logout_success(self, client):
        """Test successful logout"""
        response = client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Logout successful"
    
    def test_get_current_user(self, client):
        """Test getting current user"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer demo_token_123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "demo_user"
        assert data["email"] == "demo@naijaoracle.com"
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401
    
    def test_verify_token_success(self, client):
        """Test token verification"""
        response = client.post(
            "/api/v1/auth/verify",
            headers={"Authorization": "Bearer demo_token_123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert data["user_id"] == "demo_user"
    
    def test_verify_token_invalid(self, client):
        """Test invalid token verification"""
        response = client.post(
            "/api/v1/auth/verify",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert "error" in data
    
    def test_refresh_token(self, client):
        """Test token refresh"""
        response = client.post(
            "/api/v1/auth/refresh",
            headers={"Authorization": "Bearer demo_token_123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert data["expires_in"] == 3600


class TestPersonaRouter:
    """Test persona management router"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    def test_create_persona_success(self, client, sample_persona_create):
        """Test successful persona creation"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase:
            mock_persona = Mock()
            mock_persona.dict.return_value = sample_persona_create.dict()
            mock_persona.id = "persona_123"
            mock_supabase.return_value.create_persona.return_value = mock_persona
            
            response = client.post("/api/v1/personas", json=sample_persona_create.dict())
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "persona_123"
            assert data["name"] == sample_persona_create.name
    
    def test_create_persona_invalid_data(self, client):
        """Test persona creation with invalid data"""
        response = client.post("/api/v1/personas", json={
            "user_id": "test_user"
            # Missing required fields
        })
        
        assert response.status_code == 422
    
    def test_get_persona_success(self, client):
        """Test getting persona by ID"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase:
            mock_persona = Mock()
            mock_persona.id = "persona_123"
            mock_persona.name = "Test User"
            mock_supabase.return_value.get_persona.return_value = mock_persona
            
            response = client.get("/api/v1/personas/persona_123")
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "persona_123"
            assert data["name"] == "Test User"
    
    def test_get_persona_not_found(self, client):
        """Test getting non-existent persona"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase:
            mock_supabase.return_value.get_persona.return_value = None
            
            response = client.get("/api/v1/personas/non_existent")
            
            assert response.status_code == 404
    
    def test_get_user_personas_success(self, client):
        """Test getting user personas"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase:
            mock_persona1 = Mock()
            mock_persona1.id = "persona_1"
            mock_persona1.name = "Persona 1"
            
            mock_persona2 = Mock()
            mock_persona2.id = "persona_2"
            mock_persona2.name = "Persona 2"
            
            mock_supabase.return_value.get_user_personas.return_value = [mock_persona1, mock_persona2]
            
            response = client.get("/api/v1/personas?user_id=test_user")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["name"] == "Persona 1"
            assert data[1]["name"] == "Persona 2"
    
    def test_update_persona_success(self, client):
        """Test persona update"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase:
            mock_persona = Mock()
            mock_persona.id = "persona_123"
            mock_persona.name = "Updated Name"
            mock_supabase.return_value.update_persona.return_value = mock_persona
            
            response = client.put("/api/v1/personas/persona_123", json={
                "name": "Updated Name",
                "avg_rating": 4.0
            })
            
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "Updated Name"
    
    def test_update_persona_not_found(self, client):
        """Test updating non-existent persona"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase:
            mock_supabase.return_value.update_persona.return_value = None
            
            response = client.put("/api/v1/personas/non_existent", json={
                "name": "Updated Name"
            })
            
            assert response.status_code == 404
    
    def test_delete_persona_success(self, client):
        """Test persona deletion"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase:
            mock_supabase.return_value.delete_persona.return_value = True
            
            response = client.delete("/api/v1/personas/persona_123")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Persona deleted successfully"
    
    def test_delete_persona_not_found(self, client):
        """Test deleting non-existent persona"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase:
            mock_supabase.return_value.delete_persona.return_value = False
            
            response = client.delete("/api/v1/personas/non_existent")
            
            assert response.status_code == 404
    
    def test_get_persona_history_success(self, client):
        """Test getting persona history"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase:
            mock_history = [
                {
                    "type": "review",
                    "data": {"id": "review_1"},
                    "created_at": "2024-01-01T00:00:00Z"
                },
                {
                    "type": "recommendation",
                    "data": {"id": "rec_1"},
                    "created_at": "2024-01-02T00:00:00Z"
                }
            ]
            
            mock_supabase.return_value.get_persona_history.return_value = mock_history
            
            response = client.get("/api/v1/personas/persona_123/history")
            
            assert response.status_code == 200
            data = response.json()
            assert data["persona_id"] == "persona_123"
            assert data["total_count"] == 2
            assert len(data["history"]) == 2
    
    def test_get_similar_personas_success(self, client):
        """Test getting similar personas"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase:
            mock_persona1 = Mock()
            mock_persona1.id = "similar_1"
            mock_persona1.name = "Similar Persona 1"
            
            mock_persona2 = Mock()
            mock_persona2.id = "similar_2"
            mock_persona2.name = "Similar Persona 2"
            
            mock_supabase.return_value.search_similar_personas.return_value = [mock_persona1, mock_persona2]
            
            response = client.get("/api/v1/personas/persona_123/similar")
            
            assert response.status_code == 200
            data = response.json()
            assert data["persona_id"] == "persona_123"
            assert data["total_count"] == 2
            assert len(data["similar_personas"]) == 2
    
    def test_get_persona_stats_success(self, client):
        """Test getting persona statistics"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase:
            mock_analytics = {
                "persona_count": 5,
                "review_count": 25,
                "recommendation_count": 15,
                "recent_activity": []
            }
            
            mock_supabase.return_value.get_analytics_data.return_value = mock_analytics
            
            response = client.get("/api/v1/personas/stats?user_id=test_user")
            
            assert response.status_code == 200
            data = response.json()
            assert data["user_id"] == "test_user"
            assert data["analytics"]["persona_count"] == 5
    
    def test_get_global_persona_stats(self, client):
        """Test getting global persona statistics"""
        response = client.get("/api/v1/personas/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_personas" in data
        assert "active_personas" in data
        assert "cities_covered" in data
        assert "languages_supported" in data
        assert "avg_cultural_density" in data


class TestSimulateRouter:
    """Test review simulator router"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    def test_simulate_review_success(self, client, sample_review_request):
        """Test successful review simulation"""
        with patch('app.routers.simulate.PersonaSimulator') as mock_simulator:
            mock_response = Mock()
            mock_response.success = True
            mock_response.data = Mock()
            mock_response.data.review_text = "This place is great!"
            mock_response.data.predicted_rating = 4.5
            mock_response.request_id = "req_123"
            
            mock_simulator.return_value.generate_review.return_value = mock_response
            
            response = client.post("/api/v1/simulate-review", json=sample_review_request.dict())
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["data"]["review_text"] == "This place is great!"
            assert data["data"]["predicted_rating"] == 4.5
    
    def test_simulate_review_invalid_data(self, client):
        """Test review simulation with invalid data"""
        response = client.post("/api/v1/simulate-review", json={})
        
        assert response.status_code == 422
    
    def test_simulate_review_error(self, client, sample_review_request):
        """Test review simulation with error"""
        with patch('app.routers.simulate.PersonaSimulator') as mock_simulator:
            mock_simulator.return_value.generate_review.side_effect = Exception("API Error")
            
            response = client.post("/api/v1/simulate-review", json=sample_review_request.dict())
            
            assert response.status_code == 500
    
    def test_stream_review_success(self, client):
        """Test review streaming"""
        response = client.get("/api/v1/stream-review/req_123")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
        assert "cache-control" in response.headers
        assert "connection" in response.headers
    
    def test_health_check(self, client):
        """Test health check"""
        response = client.get("/api/v1/simulate/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Review Simulator"
        assert data["version"] == "1.0.0"
    
    def test_get_simulator_stats(self, client):
        """Test getting simulator statistics"""
        response = client.get("/api/v1/simulate/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_reviews_generated" in data
        assert "avg_generation_time_ms" in data
        assert "cultural_fidelity_score" in data
        assert "active_personas" in data
        assert "supported_languages" in data
        assert "supported_categories" in data
    
    def test_batch_simulate_success(self, client, sample_review_request):
        """Test batch review simulation"""
        requests = [sample_review_request.dict() for _ in range(3)]
        
        response = client.post("/api/v1/simulate/batch", json=requests)
        
        assert response.status_code == 200
        data = response.json()
        assert "batch_id" in data
        assert data["status"] == "processing"
        assert data["request_count"] == 3
    
    def test_batch_simulate_too_many_requests(self, client, sample_review_request):
        """Test batch simulation with too many requests"""
        requests = [sample_review_request.dict() for _ in range(15)]  # More than limit
        
        response = client.post("/api/v1/simulate/batch", json=requests)
        
        assert response.status_code == 400
        assert "Maximum 10 requests" in response.json()["detail"]
    
    def test_get_batch_results_success(self, client):
        """Test getting batch results"""
        response = client.get("/api/v1/simulate/batch/batch_123")
        
        assert response.status_code == 200
        data = response.json()
        assert data["batch_id"] == "batch_123"
        assert data["status"] == "completed"


class TestRecommendRouter:
    """Test recommendation router"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    def test_recommend_success(self, client, sample_recommendation_request):
        """Test successful recommendation"""
        with patch('app.routers.recommend.RecommendationEngine') as mock_engine:
            mock_response = Mock()
            mock_response.success = True
            mock_response.data = Mock()
            mock_response.data.recommendations = [
                {
                    "item_id": "item_1",
                    "name": "Restaurant 1",
                    "predicted_rating": 4.2,
                    "reasoning": "Good match for your preferences"
                }
            ]
            mock_response.data.explanation = "Based on your preferences..."
            mock_response.request_id = "req_123"
            
            mock_engine.return_value.generate_recommendations.return_value = mock_response
            
            response = client.post("/api/v1/recommend", json=sample_recommendation_request.dict())
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert len(data["data"]["recommendations"]) == 1
            assert data["data"]["recommendations"][0]["name"] == "Restaurant 1"
    
    def test_recommend_invalid_data(self, client):
        """Test recommendation with invalid data"""
        response = client.post("/api/v1/recommend", json={})
        
        assert response.status_code == 422
    
    def test_recommend_error(self, client, sample_recommendation_request):
        """Test recommendation with error"""
        with patch('app.routers.recommend.RecommendationEngine') as mock_engine:
            mock_engine.return_value.generate_recommendations.side_effect = Exception("API Error")
            
            response = client.post("/api/v1/recommend", json=sample_recommendation_request.dict())
            
            assert response.status_code == 500
    
    def test_stream_recommend_success(self, client):
        """Test recommendation streaming"""
        response = client.get("/api/v1/stream-recommend/req_123")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
        assert "cache-control" in response.headers
        assert "connection" in response.headers
    
    def test_follow_up_recommendation_success(self, client):
        """Test follow-up recommendation"""
        response = client.post(
            "/api/v1/recommend/follow-up/req_123",
            json={"user_feedback": "I want something cheaper"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["request_id"] == "req_123"
        assert data["feedback"] == "I want something cheaper"
        assert "adjusted_recommendations" in data
        assert "next_prompt" in data
    
    def test_health_check(self, client):
        """Test health check"""
        response = client.get("/api/v1/recommend/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Recommendation Engine"
        assert data["version"] == "1.0.0"
    
    def test_get_recommendation_stats(self, client):
        """Test getting recommendation statistics"""
        response = client.get("/api/v1/recommend/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_recommendations" in data
        assert "avg_ndcg_at_10" in data
        assert "hit_rate_at_5" in data
        assert "cold_start_performance" in data
        assert "supported_domains" in data
        assert "catalog_size" in data
        assert "active_personas" in data
    
    def test_cold_start_success(self, client):
        """Test cold-start recommendations"""
        user_answers = {
            "preferences": {"food": True, "fashion": False},
            "budget_range": "mid",
            "location": "Lagos"
        }
        
        response = client.post("/api/v1/recommend/cold-start", json=user_answers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["cold_start"] is True
        assert "persona_cluster" in data
        assert "recommendations" in data
        assert "next_questions" in data
    
    def test_get_product_catalog_success(self, client):
        """Test getting product catalog"""
        response = client.get("/api/v1/recommend/catalog")
        
        assert response.status_code == 200
        data = response.json()
        assert "catalog" in data
        assert "total_count" in data
        assert "filters_applied" in data
        assert isinstance(data["catalog"], list)
    
    def test_get_product_catalog_with_filters(self, client):
        """Test getting product catalog with filters"""
        response = client.get("/api/v1/recommend/catalog?domain=food&location=Lagos")
        
        assert response.status_code == 200
        data = response.json()
        assert data["filters_applied"]["domain"] == "food"
        assert data["filters_applied"]["location"] == "Lagos"


class TestMainRouter:
    """Test main application router"""
    
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
        assert "docs" in data
    
    def test_health_endpoint(self, client):
        """Test health endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data
    
    def test_docs_redirect(self, client):
        """Test docs redirect"""
        response = client.get("/docs")
        
        # Should redirect to Swagger UI
        assert response.status_code in [200, 307]
    
    def test_redoc_redirect(self, client):
        """Test ReDoc redirect"""
        response = client.get("/redoc")
        
        # Should redirect to ReDoc
        assert response.status_code in [200, 307]
    
    def test_cors_headers(self, client):
        """Test CORS headers"""
        response = client.options("/api/v1/personas")
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers


class TestErrorHandling:
    """Test error handling across all routers"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    def test_404_not_found(self, client):
        """Test 404 error handling"""
        response = client.get("/api/v1/nonexistent")
        
        assert response.status_code == 404
    
    def test_validation_error(self, client):
        """Test validation error handling"""
        response = client.post("/api/v1/personas", json={"invalid": "data"})
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_server_error(self, client):
        """Test server error handling"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase:
            mock_supabase.return_value.create_persona.side_effect = Exception("Database error")
            
            response = client.post("/api/v1/personas", json={
                "user_id": "test_user",
                "name": "Test User",
                "city": "Lagos",
                "primary_language": "english",
                "review_style": "casual",
                "avg_rating": 3.5,
                "pidgin_intensity": 0.5
            })
            
            assert response.status_code == 500
    
    def test_rate_limiting(self, client):
        """Test rate limiting (if implemented)"""
        # This would require rate limiting middleware
        # For now, just ensure the endpoint exists
        response = client.get("/api/v1/personas/stats")
        
        # Should succeed for normal usage
        assert response.status_code in [200, 429]


class TestStreamingEndpoints:
    """Test streaming endpoints"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    def test_review_streaming_format(self, client):
        """Test review streaming format"""
        response = client.get("/api/v1/stream-review/test_request")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
        
        # Check streaming data format
        content = response.content.decode()
        lines = content.split('\n')
        
        # Should have SSE format
        for line in lines:
            if line.strip():
                assert line.startswith('data: ')
    
    def test_recommendation_streaming_format(self, client):
        """Test recommendation streaming format"""
        response = client.get("/api/v1/stream-recommend/test_request")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
        
        # Check streaming data format
        content = response.content.decode()
        lines = content.split('\n')
        
        # Should have SSE format
        for line in lines:
            if line.strip():
                assert line.startswith('data: ')
    
    def test_streaming_error_handling(self, client):
        """Test streaming error handling"""
        # Test with invalid request ID
        response = client.get("/api/v1/stream-review/")
        
        # Should handle gracefully
        assert response.status_code in [404, 400]


class TestAuthentication:
    """Test authentication across endpoints"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    def test_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token"""
        # Most endpoints should work without token for demo purposes
        # But if authentication is required:
        response = client.get("/api/v1/auth/me")
        
        # Should require authentication
        assert response.status_code in [401, 403]
    
    def test_protected_endpoint_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401
    
    def test_protected_endpoint_with_valid_token(self, client):
        """Test accessing protected endpoint with valid token"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer demo_token_123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
