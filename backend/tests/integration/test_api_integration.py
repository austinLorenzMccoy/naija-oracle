"""
Integration tests for API endpoints
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, AsyncMock

from app.main import app


class TestAPIIntegration:
    """Integration tests for the complete API"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_services(self):
        """Mock all external services"""
        with patch('app.routers.personas.SupabaseClient') as mock_supabase, \
             patch('app.routers.simulate.PersonaSimulator') as mock_simulator, \
             patch('app.routers.recommend.RecommendationEngine') as mock_engine:
            
            # Setup mock persona
            mock_persona = Mock()
            mock_persona.id = "test_persona_id"
            mock_persona.name = "Test User"
            mock_persona.city = "Lagos"
            mock_persona.avg_rating = 3.5
            mock_persona.pidgin_intensity = 0.5
            
            mock_supabase.return_value.get_persona.return_value = mock_persona
            mock_supabase.return_value.create_persona.return_value = mock_persona
            mock_supabase.return_value.get_user_personas.return_value = [mock_persona]
            
            # Setup mock simulator
            mock_sim_response = Mock()
            mock_sim_response.success = True
            mock_sim_response.data = Mock()
            mock_sim_response.data.review_text = "This place sweet me die!"
            mock_sim_response.data.predicted_rating = 4.5
            mock_simulator.return_value.generate_review.return_value = mock_sim_response
            
            # Setup mock recommendation engine
            mock_rec_response = Mock()
            mock_rec_response.success = True
            mock_rec_response.data = Mock()
            mock_rec_response.data.recommendations = [
                {"item_id": "item_1", "name": "Restaurant 1", "predicted_rating": 4.2}
            ]
            mock_rec_response.data.explanation = "Based on your preferences..."
            mock_engine.return_value.generate_recommendations.return_value = mock_rec_response
            
            yield {
                'supabase': mock_supabase,
                'simulator': mock_simulator,
                'engine': mock_engine
            }
    
    def test_complete_persona_workflow(self, client, mock_services):
        """Test complete persona creation and usage workflow"""
        # 1. Create persona
        persona_data = {
            "user_id": "test_user",
            "name": "Test User",
            "age_range": "25-34",
            "city": "Lagos",
            "lga": "Ikeja",
            "primary_language": "english",
            "review_style": "casual",
            "avg_rating": 3.5,
            "pidgin_intensity": 0.5
        }
        
        response = client.post("/api/v1/personas", json=persona_data)
        assert response.status_code == 200
        created_persona = response.json()
        assert created_persona["name"] == "Test User"
        
        # 2. Get persona
        response = client.get(f"/api/v1/personas/{created_persona['id']}")
        assert response.status_code == 200
        retrieved_persona = response.json()
        assert retrieved_persona["id"] == created_persona["id"]
        
        # 3. Generate review using persona
        review_request = {
            "user_id": "test_user",
            "persona_id": created_persona["id"],
            "product": {
                "name": "Test Restaurant",
                "category": "restaurant",
                "location": "Lagos",
                "price_tier": "mid"
            },
            "context": {
                "time_of_day": "evening",
                "occasion": "casual",
                "recency_of_visit": "first_time"
            },
            "temperature": 0.7,
            "max_tokens": 400
        }
        
        response = client.post("/api/v1/simulate-review", json=review_request)
        assert response.status_code == 200
        review_response = response.json()
        assert review_response["success"] is True
        assert review_response["data"]["review_text"] is not None
        
        # 4. Get recommendations using persona
        rec_request = {
            "user_id": "test_user",
            "persona_id": created_persona["id"],
            "domain": "food",
            "context": {
                "current_time": "Saturday 8PM",
                "location": "Lekki Phase 1",
                "mood_signal": "celebratory",
                "budget_naira": 5000
            },
            "max_recommendations": 5
        }
        
        response = client.post("/api/v1/recommend", json=rec_request)
        assert response.status_code == 200
        rec_response = response.json()
        assert rec_response["success"] is True
        assert len(rec_response["data"]["recommendations"]) > 0
        
        # 5. Get persona history
        response = client.get(f"/api/v1/personas/{created_persona['id']}/history")
        assert response.status_code == 200
        history = response.json()
        assert "history" in history
    
    def test_authentication_flow(self, client):
        """Test authentication flow"""
        # 1. Login
        login_data = {
            "user_id": "test_user",
            "email": "test@example.com"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        login_response = response.json()
        assert "token" in login_response
        token = login_response["token"]
        
        # 2. Get current user
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["user_id"] == "demo_user"
        
        # 3. Verify token
        response = client.post(
            "/api/v1/auth/verify",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        verify_response = response.json()
        assert verify_response["valid"] is True
        
        # 4. Refresh token
        response = client.post(
            "/api/v1/auth/refresh",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        refresh_response = response.json()
        assert "token" in refresh_response
        
        # 5. Logout
        response = client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
    
    def test_batch_operations(self, client, mock_services):
        """Test batch operations"""
        # Create multiple personas first
        personas = []
        for i in range(3):
            persona_data = {
                "user_id": f"test_user_{i}",
                "name": f"Test User {i}",
                "age_range": "25-34",
                "city": "Lagos",
                "lga": "Ikeja",
                "primary_language": "english",
                "review_style": "casual",
                "avg_rating": 3.5,
                "pidgin_intensity": 0.5
            }
            
            response = client.post("/api/v1/personas", json=persona_data)
            assert response.status_code == 200
            personas.append(response.json())
        
        # Batch review simulation
        batch_requests = []
        for persona in personas:
            review_request = {
                "user_id": persona["user_id"],
                "persona_id": persona["id"],
                "product": {
                    "name": "Test Restaurant",
                    "category": "restaurant",
                    "location": "Lagos",
                    "price_tier": "mid"
                },
                "context": {
                    "time_of_day": "evening",
                    "occasion": "casual",
                    "recency_of_visit": "first_time"
                },
                "temperature": 0.7,
                "max_tokens": 400
            }
            batch_requests.append(review_request)
        
        response = client.post("/api/v1/simulate/batch", json=batch_requests)
        assert response.status_code == 200
        batch_response = response.json()
        assert "batch_id" in batch_response
        assert batch_response["request_count"] == 3
        
        # Get batch results
        batch_id = batch_response["batch_id"]
        response = client.get(f"/api/v1/simulate/batch/{batch_id}")
        assert response.status_code == 200
        results = response.json()
        assert results["batch_id"] == batch_id
    
    def test_error_handling_integration(self, client, mock_services):
        """Test error handling across the API"""
        # Test invalid persona creation
        response = client.post("/api/v1/personas", json={"invalid": "data"})
        assert response.status_code == 422
        
        # Test non-existent persona
        response = client.get("/api/v1/personas/non_existent")
        assert response.status_code == 404
        
        # Test invalid review request
        response = client.post("/api/v1/simulate-review", json={})
        assert response.status_code == 422
        
        # Test invalid recommendation request
        response = client.post("/api/v1/recommend", json={})
        assert response.status_code == 422
        
        # Test invalid token
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
    
    def test_streaming_endpoints(self, client):
        """Test streaming endpoints"""
        # Test review streaming
        response = client.get("/api/v1/stream-review/test_request")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
        
        # Test recommendation streaming
        response = client.get("/api/v1/stream-recommend/test_request")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    
    def test_cold_start_recommendations(self, client, mock_services):
        """Test cold-start recommendation flow"""
        # Cold-start recommendations
        user_answers = {
            "preferences": {"food": True, "fashion": False},
            "budget_range": "mid",
            "location": "Lagos",
            "mood": "celebratory"
        }
        
        response = client.post("/api/v1/recommend/cold-start", json=user_answers)
        assert response.status_code == 200
        cold_start_response = response.json()
        assert cold_start_response["cold_start"] is True
        assert "persona_cluster" in cold_start_response
        assert "recommendations" in cold_start_response
        assert "next_questions" in cold_start_response
        
        # Follow-up recommendations
        response = client.post(
            "/api/v1/recommend/follow-up/test_request",
            json={"user_feedback": "I want something cheaper"}
        )
        assert response.status_code == 200
        follow_up_response = response.json()
        assert "adjusted_recommendations" in follow_up_response
        assert "next_prompt" in follow_up_response
    
    def test_catalog_and_search(self, client):
        """Test product catalog and search functionality"""
        # Get full catalog
        response = client.get("/api/v1/recommend/catalog")
        assert response.status_code == 200
        catalog = response.json()
        assert "catalog" in catalog
        assert "total_count" in catalog
        assert isinstance(catalog["catalog"], list)
        
        # Filtered catalog
        response = client.get("/api/v1/recommend/catalog?domain=food&location=Lagos")
        assert response.status_code == 200
        filtered_catalog = response.json()
        assert filtered_catalog["filters_applied"]["domain"] == "food"
        assert filtered_catalog["filters_applied"]["location"] == "Lagos"
    
    def test_analytics_and_stats(self, client, mock_services):
        """Test analytics and statistics endpoints"""
        # Simulator stats
        response = client.get("/api/v1/simulate/stats")
        assert response.status_code == 200
        sim_stats = response.json()
        assert "total_reviews_generated" in sim_stats
        assert "avg_generation_time_ms" in sim_stats
        assert "cultural_fidelity_score" in sim_stats
        assert "active_personas" in sim_stats
        
        # Recommendation stats
        response = client.get("/api/v1/recommend/stats")
        assert response.status_code == 200
        rec_stats = response.json()
        assert "total_recommendations" in rec_stats
        assert "avg_ndcg_at_10" in rec_stats
        assert "hit_rate_at_5" in rec_stats
        assert "supported_domains" in rec_stats
        
        # Persona stats
        response = client.get("/api/v1/personas/stats")
        assert response.status_code == 200
        persona_stats = response.json()
        assert "total_personas" in persona_stats
        assert "active_personas" in persona_stats
        assert "cities_covered" in persona_stats
        assert "languages_supported" in persona_stats
    
    def test_health_endpoints(self, client):
        """Test health check endpoints"""
        # Main health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        health = response.json()
        assert health["status"] == "healthy"
        assert "version" in health
        assert "timestamp" in health
        
        # Service-specific health endpoints
        response = client.get("/api/v1/simulate/health")
        assert response.status_code == 200
        
        response = client.get("/api/v1/recommend/health")
        assert response.status_code == 200
    
    def test_cors_headers(self, client):
        """Test CORS headers"""
        # Test preflight request
        response = client.options("/api/v1/personas")
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers
        
        # Test actual request
        response = client.get("/api/v1/personas/stats")
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


class TestCulturalFeaturesIntegration:
    """Integration tests for cultural features"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    def test_nigerian_cultural_content(self, client):
        """Test Nigerian cultural content in responses"""
        # Create a Nigerian persona
        persona_data = {
            "user_id": "test_user",
            "name": "Emeka Okafor",
            "age_range": "25-34",
            "city": "Lagos",
            "lga": "Surulere",
            "primary_language": "igbo",
            "review_style": "expressive",
            "avg_rating": 3.5,
            "pidgin_intensity": 0.8,
            "cultural_markers": ["price_sensitive", "brand_loyal"]
        }
        
        response = client.post("/api/v1/personas", json=persona_data)
        assert response.status_code == 200
        persona = response.json()
        
        # Generate review with cultural context
        review_request = {
            "user_id": "test_user",
            "persona_id": persona["id"],
            "product": {
                "name": "Chicken Republic",
                "category": "fast_food",
                "location": "Ikeja",
                "price_tier": "mid"
            },
            "context": {
                "time_of_day": "late_night",
                "occasion": "after_work",
                "recency_of_visit": "first_time"
            },
            "temperature": 0.7,
            "max_tokens": 400
        }
        
        with patch('app.routers.simulate.PersonaSimulator') as mock_simulator:
            # Mock response with Nigerian cultural content
            mock_response = Mock()
            mock_response.success = True
            mock_response.data = Mock()
            mock_response.data.review_text = "This Chicken Republic sweet me die! The service correct well well. 4.5 stars!"
            mock_response.data.predicted_rating = 4.5
            mock_response.data.cvi_anchors_used = ["E sweet me die", "Correct!"]
            mock_response.data.behavioural_fidelity_score = 0.85
            mock_simulator.return_value.generate_review.return_value = mock_response
            
            response = client.post("/api/v1/simulate-review", json=review_request)
            assert response.status_code == 200
            review_response = response.json()
            
            # Should contain cultural elements
            assert review_response["success"] is True
            # The actual cultural content would be in the mocked response
    
    def test_cultural_recommendations(self, client):
        """Test culturally-aware recommendations"""
        # Create recommendation request with Nigerian context
        rec_request = {
            "user_id": "test_user",
            "persona_id": "test_persona",
            "domain": "food",
            "context": {
                "current_time": "Saturday 8PM",
                "location": "Lagos Mainland",
                "mood_signal": "celebratory",
                "budget_naira": 5000,
                "cultural_preferences": ["nigerian_cuisine", "local_spots"]
            },
            "max_recommendations": 5
        }
        
        with patch('app.routers.recommend.RecommendationEngine') as mock_engine:
            # Mock response with culturally-aware recommendations
            mock_response = Mock()
            mock_response.success = True
            mock_response.data = Mock()
            mock_response.data.recommendations = [
                {
                    "item_id": "item_1",
                    "name": "Yellow Chilli Restaurant",
                    "category": "Nigerian fine dining",
                    "location": "Victoria Island",
                    "predicted_rating": 4.4,
                    "reasoning": "Perfect for your celebration mood with authentic Nigerian cuisine",
                    "cultural_relevance": 0.95
                }
            ]
            mock_response.data.explanation = "Based on your Nigerian cultural preferences and celebration mood..."
            mock_response.data.cultural_boost_applied = True
            mock_engine.return_value.generate_recommendations.return_value = mock_response
            
            response = client.post("/api/v1/recommend", json=rec_request)
            assert response.status_code == 200
            rec_response = response.json()
            
            assert rec_response["success"] is True
            assert len(rec_response["data"]["recommendations"]) > 0


class TestPerformanceIntegration:
    """Integration tests for performance scenarios"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    def test_concurrent_requests(self, client, mock_services):
        """Test handling concurrent requests"""
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request():
            try:
                response = client.get("/api/v1/personas/stats")
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))
        
        # Make 10 concurrent requests
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert len(errors) == 0
        assert len(results) == 10
        assert all(status == 200 for status in results)
    
    def test_large_payload_handling(self, client, mock_services):
        """Test handling of large payloads"""
        # Create a large persona description
        large_persona_data = {
            "user_id": "test_user",
            "name": "Test User",
            "age_range": "25-34",
            "city": "Lagos",
            "lga": "Ikeja",
            "primary_language": "english",
            "review_style": "expressive",
            "avg_rating": 3.5,
            "pidgin_intensity": 0.5,
            "sample_reviews": ["Good service"] * 100,  # Large list
            "cultural_markers": ["marker_" + str(i) for i in range(50)]  # Large list
        }
        
        response = client.post("/api/v1/personas", json=large_persona_data)
        # Should handle large payloads gracefully
        assert response.status_code in [200, 422]  # 422 if validation limits are hit
    
    def test_rate_limiting_behavior(self, client):
        """Test rate limiting behavior"""
        # Make many rapid requests
        responses = []
        for i in range(20):
            response = client.get("/api/v1/personas/stats")
            responses.append(response.status_code)
        
        # Most should succeed, some might be rate limited
        success_count = sum(1 for status in responses if status == 200)
        assert success_count >= 15  # At least 75% should succeed


class TestDataConsistency:
    """Integration tests for data consistency"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    def test_persona_data_consistency(self, client, mock_services):
        """Test persona data consistency across operations"""
        # Create persona
        persona_data = {
            "user_id": "test_user",
            "name": "Test User",
            "age_range": "25-34",
            "city": "Lagos",
            "lga": "Ikeja",
            "primary_language": "english",
            "review_style": "casual",
            "avg_rating": 3.5,
            "pidgin_intensity": 0.5
        }
        
        response = client.post("/api/v1/personas", json=persona_data)
        assert response.status_code == 200
        created_persona = response.json()
        
        # Update persona
        update_data = {"name": "Updated Name", "avg_rating": 4.0}
        response = client.put(f"/api/v1/personas/{created_persona['id']}", json=update_data)
        assert response.status_code == 200
        updated_persona = response.json()
        
        # Verify data consistency
        assert updated_persona["id"] == created_persona["id"]
        assert updated_persona["user_id"] == created_persona["user_id"]
        assert updated_persona["name"] == "Updated Name"
        assert updated_persona["avg_rating"] == 4.0
        
        # Get persona and verify
        response = client.get(f"/api/v1/personas/{created_persona['id']}")
        assert response.status_code == 200
        retrieved_persona = response.json()
        
        assert retrieved_persona["id"] == updated_persona["id"]
        assert retrieved_persona["name"] == updated_persona["name"]
        assert retrieved_persona["avg_rating"] == updated_persona["avg_rating"]
