"""
Test suite for service layer
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any, List

from app.services.groq_client import GroqClient
from app.services.cultural_voice_index import CulturalVoiceIndex
from app.services.supabase_client import SupabaseClient
from app.services.persona_simulator import PersonaSimulator
from app.services.recommendation_engine import RecommendationEngine
from app.services.embedding_service import EmbeddingService
from app.models.persona import Persona, PersonaCreate
from app.models.review import ReviewRequest, ReviewResponse, Product, Context
from app.models.recommendation import RecommendationRequest, RecommendationResponse
from app.models.cultural_voice import CVIAnchor, TribeRegion, SentimentCategory


class TestGroqClient:
    """Test Groq client service"""
    
    @pytest.fixture
    def groq_client(self):
        """Groq client fixture"""
        with patch('app.services.groq_client.Groq'):
            client = GroqClient()
            client.client = Mock()
            return client
    
    def test_groq_client_initialization(self):
        """Test Groq client initialization"""
        with patch('app.services.groq_client.Groq'):
            client = GroqClient()
            assert client.model == "llama-3.1-70b-versatile"
            assert client.client is not None
    
    @pytest.mark.asyncio
    async def test_chat_completion(self, groq_client):
        """Test chat completion"""
        # Mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "Test response"
        
        groq_client.client.chat.completions.create.return_value = mock_response
        
        messages = [{"role": "user", "content": "Test message"}]
        response = await groq_client.chat_completion(messages)
        
        assert response == mock_response
        groq_client.client.chat.completions.create.assert_called_once_with(
            model="llama-3.1-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            stream=False
        )
    
    @pytest.mark.asyncio
    async def test_chat_completion_with_params(self, groq_client):
        """Test chat completion with custom parameters"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "Test response"
        
        groq_client.client.chat.completions.create.return_value = mock_response
        
        messages = [{"role": "user", "content": "Test message"}]
        response = await groq_client.chat_completion(
            messages,
            temperature=0.5,
            max_tokens=500,
            top_p=0.9
        )
        
        assert response == mock_response
        groq_client.client.chat.completions.create.assert_called_once_with(
            model="llama-3.1-70b-versatile",
            messages=messages,
            temperature=0.5,
            max_tokens=500,
            top_p=0.9,
            stream=False
        )
    
    @pytest.mark.asyncio
    async def test_chat_completion_streaming(self, groq_client):
        """Test streaming chat completion"""
        # Mock streaming response
        async def mock_stream():
            chunks = [
                Mock(choices=[Mock(delta=Mock(content="Hello"))]),
                Mock(choices=[Mock(delta=Mock(content=" world"))]),
                Mock(choices=[Mock(delta=Mock(content="!"))])
            ]
            for chunk in chunks:
                yield chunk
        
        groq_client.client.chat.completions.create.return_value = mock_stream()
        
        messages = [{"role": "user", "content": "Test message"}]
        response = await groq_client.chat_completion(messages, stream=True)
        
        # Verify it's an async generator
        assert hasattr(response, '__aiter__')
        
        # Collect all chunks
        chunks = []
        async for chunk in response:
            chunks.append(chunk)
        
        assert len(chunks) == 3
        assert chunks[0].choices[0].delta.content == "Hello"
    
    def test_generate_review_prompt(self, groq_client):
        """Test review prompt generation"""
        persona = {
            "name": "Test User",
            "city": "Lagos",
            "primary_language": "english",
            "pidgin_intensity": 0.5,
            "review_style": "casual"
        }
        
        product = {
            "name": "Test Restaurant",
            "category": "restaurant",
            "location": "Lagos"
        }
        
        context = {
            "time_of_day": "evening",
            "occasion": "casual"
        }
        
        cvi_anchors = [
            {
                "phrase": "E sweet me die",
                "sentiment_category": "positive",
                "pidgin_intensity": 0.8
            }
        ]
        
        prompt = groq_client.generate_review_prompt(persona, product, context, cvi_anchors)
        
        assert "Test User" in prompt
        assert "Test Restaurant" in prompt
        assert "Lagos" in prompt
        assert "E sweet me die" in prompt
        assert "[INST]" in prompt
        assert "[/INST]" in prompt
    
    def test_generate_recommendation_prompt(self, groq_client):
        """Test recommendation prompt generation"""
        persona = {
            "name": "Test User",
            "city": "Lagos",
            "avg_rating": 3.5
        }
        
        context = {
            "current_time": "Saturday 8PM",
            "location": "Lekki Phase 1",
            "mood_signal": "celebratory",
            "budget_naira": 5000
        }
        
        candidates = [
            {
                "name": "Restaurant 1",
                "category": "food",
                "location": "Victoria Island",
                "avg_rating": 4.2
            }
        ]
        
        prompt = groq_client.generate_recommendation_prompt(persona, context, candidates)
        
        assert "Test User" in prompt
        assert "Lagos" in prompt
        assert "celebratory" in prompt
        assert "Restaurant 1" in prompt
        assert "[INST]" in prompt


class TestCulturalVoiceIndex:
    """Test Cultural Voice Index service"""
    
    @pytest.fixture
    def cvi(self):
        """Cultural Voice Index fixture"""
        return CulturalVoiceIndex()
    
    def test_cvi_initialization(self, cvi):
        """Test CVI initialization"""
        assert len(cvi.anchors) > 0
        assert all(hasattr(anchor, 'phrase') for anchor in cvi.anchors)
    
    def test_get_all_anchors(self, cvi):
        """Test getting all anchors"""
        anchors = cvi.get_all_anchors()
        
        assert isinstance(anchors, list)
        assert len(anchors) > 0
        assert all(isinstance(anchor, CVIAnchor) for anchor in anchors)
    
    @pytest.mark.asyncio
    async def test_get_persona_anchors(self, cvi):
        """Test getting persona-specific anchors"""
        anchors = await cvi.get_persona_anchors(
            city="Lagos",
            language="english",
            pidgin_intensity=0.7,
            product_category="food"
        )
        
        assert isinstance(anchors, list)
        assert len(anchors) <= 5  # Should return top 5
        
        # Verify anchors are relevant
        for anchor in anchors:
            assert isinstance(anchor, CVIAnchor)
            assert anchor.product_context.value in ["food", "general"]
    
    @pytest.mark.asyncio
    async def test_get_persona_anchors_yoruba(self, cvi):
        """Test getting anchors for Yoruba persona"""
        anchors = await cvi.get_persona_anchors(
            city="Lagos",
            language="yoruba",
            pidgin_intensity=0.8,
            product_category="food"
        )
        
        # Should prefer Yoruba or Pan-Nigerian anchors
        yoruba_or_pan = [
            anchor for anchor in anchors
            if anchor.tribe_region in [TribeRegion.YORUBA, TribeRegion.PAN_NIGERIAN]
        ]
        
        assert len(yoruba_or_pan) > 0
    
    @pytest.mark.asyncio
    async def test_get_persona_anchors_low_pidgin(self, cvi):
        """Test getting anchors for low pidgin intensity"""
        anchors = await cvi.get_persona_anchors(
            city="Lagos",
            language="english",
            pidgin_intensity=0.2,
            product_category="restaurant"
        )
        
        # Should prefer anchors with lower pidgin intensity
        for anchor in anchors:
            assert anchor.pidgin_intensity <= 0.6
    
    @pytest.mark.asyncio
    async def test_create_persona_profile(self, cvi):
        """Test creating persona profile"""
        persona = Persona(
            id="test_persona",
            user_id="test_user",
            name="Test User",
            age_range="25-34",
            city="Lagos",
            lga="Ikeja",
            primary_language="english",
            review_style="casual",
            avg_rating=3.5,
            sentiment_volatility="medium",
            categories_reviewed=["food"],
            sample_reviews=["Good place"],
            cultural_markers=["price_sensitive"],
            pidgin_intensity=0.5,
            status="active"
        )
        
        profile = await cvi.create_persona_profile(persona)
        
        assert profile.persona_id == "test_persona"
        assert profile.pidgin_intensity == 0.5
        assert profile.voice_consistency_score > 0
        assert profile.cultural_authenticity_score > 0
    
    @pytest.mark.asyncio
    async def test_evaluate_cultural_fidelity(self, cvi):
        """Test cultural fidelity evaluation"""
        text = "This jollof rice sweet me die! The service correct."
        persona_profile = Mock()
        persona_profile.preferred_anchors = ["E sweet me die", "Gbam!"]
        persona_profile.pidgin_intensity = 0.7
        
        score = await cvi.evaluate_cultural_fidelity(text, persona_profile)
        
        assert 0 <= score <= 1
        assert score > 0.5  # Should be high for good cultural match
    
    @pytest.mark.asyncio
    async def test_add_anchor(self, cvi):
        """Test adding new anchor"""
        initial_count = len(cvi.anchors)
        
        new_anchor = CVIAnchor(
            phrase="New test phrase",
            tribe_region=TribeRegion.PAN_NIGERIAN,
            pidgin_intensity=0.6,
            formality_register="casual",
            sentiment_category="positive",
            product_context="general",
            avg_rating_association=4.0,
            frequency_score=0.7,
            confidence_score=0.8
        )
        
        await cvi.add_anchor(new_anchor)
        
        assert len(cvi.anchors) == initial_count + 1
        assert new_anchor in cvi.anchors
    
    @pytest.mark.asyncio
    async def test_remove_anchor(self, cvi):
        """Test removing anchor"""
        if len(cvi.anchors) > 0:
            initial_count = len(cvi.anchors)
            anchor_to_remove = cvi.anchors[0]
            
            await cvi.remove_anchor(anchor_to_remove.phrase)
            
            assert len(cvi.anchors) == initial_count - 1
            assert anchor_to_remove not in cvi.anchors


class TestSupabaseClient:
    """Test Supabase client service"""
    
    @pytest.fixture
    def supabase_client(self):
        """Supabase client fixture"""
        with patch('app.services.supabase_client.create_client'):
            client = SupabaseClient()
            client.client = Mock()
            return client
    
    @pytest.mark.asyncio
    async def test_create_persona(self, supabase_client, sample_persona_create):
        """Test persona creation"""
        # Mock response
        mock_response = Mock()
        mock_response.data = [{
            "id": "test_persona_id",
            "user_id": sample_persona_create.user_id,
            "name": sample_persona_create.name,
            "city": sample_persona_create.city,
            "primary_language": sample_persona_create.primary_language.value,
            "review_style": sample_persona_create.review_style.value,
            "avg_rating": sample_persona_create.avg_rating,
            "pidgin_intensity": sample_persona_create.pidgin_intensity,
            "status": "active"
        }]
        
        supabase_client.client.table.return_value.insert.return_value.execute.return_value = mock_response
        
        persona = await supabase_client.create_persona(sample_persona_create)
        
        assert persona.id == "test_persona_id"
        assert persona.name == sample_persona_create.name
        assert persona.status.value == "active"
        
        supabase_client.client.table.assert_called_with("personas")
    
    @pytest.mark.asyncio
    async def test_get_persona(self, supabase_client):
        """Test getting persona by ID"""
        mock_response = Mock()
        mock_response.data = [{
            "id": "test_persona_id",
            "user_id": "test_user_id",
            "name": "Test User",
            "city": "Lagos",
            "primary_language": "english",
            "review_style": "casual",
            "avg_rating": 3.5,
            "pidgin_intensity": 0.5,
            "status": "active"
        }]
        
        supabase_client.client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response
        
        persona = await supabase_client.get_persona("test_persona_id")
        
        assert persona is not None
        assert persona.id == "test_persona_id"
        assert persona.name == "Test User"
    
    @pytest.mark.asyncio
    async def test_get_persona_not_found(self, supabase_client):
        """Test getting non-existent persona"""
        mock_response = Mock()
        mock_response.data = []
        
        supabase_client.client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response
        
        persona = await supabase_client.get_persona("non_existent_id")
        
        assert persona is None
    
    @pytest.mark.asyncio
    async def test_get_user_personas(self, supabase_client):
        """Test getting all personas for a user"""
        mock_response = Mock()
        mock_response.data = [
            {
                "id": "persona_1",
                "user_id": "test_user_id",
                "name": "Persona 1",
                "city": "Lagos",
                "primary_language": "english",
                "review_style": "casual",
                "avg_rating": 3.5,
                "pidgin_intensity": 0.5,
                "status": "active"
            },
            {
                "id": "persona_2",
                "user_id": "test_user_id",
                "name": "Persona 2",
                "city": "Abuja",
                "primary_language": "hausa",
                "review_style": "formal",
                "avg_rating": 4.0,
                "pidgin_intensity": 0.3,
                "status": "active"
            }
        ]
        
        supabase_client.client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response
        
        personas = await supabase_client.get_user_personas("test_user_id")
        
        assert len(personas) == 2
        assert personas[0].name == "Persona 1"
        assert personas[1].name == "Persona 2"
    
    @pytest.mark.asyncio
    async def test_update_persona(self, supabase_client):
        """Test persona update"""
        mock_response = Mock()
        mock_response.data = [{
            "id": "test_persona_id",
            "user_id": "test_user_id",
            "name": "Updated Name",
            "city": "Lagos",
            "primary_language": "english",
            "review_style": "casual",
            "avg_rating": 4.0,
            "pidgin_intensity": 0.6,
            "status": "active"
        }]
        
        supabase_client.client.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response
        
        update_data = {"name": "Updated Name", "avg_rating": 4.0}
        persona = await supabase_client.update_persona("test_persona_id", update_data)
        
        assert persona is not None
        assert persona.name == "Updated Name"
        assert persona.avg_rating == 4.0
    
    @pytest.mark.asyncio
    async def test_delete_persona(self, supabase_client):
        """Test persona deletion"""
        mock_response = Mock()
        mock_response.data = [{"id": "test_persona_id"}]
        
        supabase_client.client.table.return_value.delete.return_value.eq.return_value.execute.return_value = mock_response
        
        result = await supabase_client.delete_persona("test_persona_id")
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_store_review_generation(self, supabase_client):
        """Test storing review generation"""
        mock_response = Mock()
        mock_response.data = [{"id": "generation_id"}]
        
        supabase_client.client.table.return_value.insert.return_value.execute.return_value = mock_response
        
        user_id = "test_user_id"
        persona_id = "test_persona_id"
        product = {"name": "Test Restaurant"}
        context = {"time_of_day": "evening"}
        generation = {"review_text": "Good place!"}
        
        result = await supabase_client.store_review_generation(
            user_id, persona_id, product, context, generation
        )
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_get_persona_history(self, supabase_client):
        """Test getting persona history"""
        mock_response = Mock()
        mock_response.data = [
            {
                "id": "review_1",
                "user_id": "test_user_id",
                "persona_id": "test_persona_id",
                "product": {"name": "Restaurant 1"},
                "context": {"time_of_day": "evening"},
                "generation": {"review_text": "Good!"},
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "id": "rec_1",
                "user_id": "test_user_id",
                "persona_id": "test_persona_id",
                "request": {"domain": "food"},
                "response": {"recommendations": []},
                "created_at": "2024-01-02T00:00:00Z"
            }
        ]
        
        # Mock both table responses
        supabase_client.client.table.return_value.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.return_value = mock_response
        
        history = await supabase_client.get_persona_history("test_persona_id", limit=50)
        
        assert isinstance(history, list)
        assert len(history) == 2
        assert history[0]["type"] == "review"
        assert history[1]["type"] == "recommendation"
    
    @pytest.mark.asyncio
    async def test_get_analytics_data(self, supabase_client):
        """Test getting analytics data"""
        mock_response = Mock()
        mock_response.data = [{"id": "persona_1"}, {"id": "persona_2"}]
        
        supabase_client.client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response
        
        analytics = await supabase_client.get_analytics_data("test_user_id")
        
        assert analytics["persona_count"] == 2
        assert "review_count" in analytics
        assert "recommendation_count" in analytics
        assert "recent_activity" in analytics
    
    @pytest.mark.asyncio
    async def test_test_connection(self, supabase_client):
        """Test database connection"""
        mock_response = Mock()
        mock_response.data = [{"count": 1}]
        
        supabase_client.client.table.return_value.select.return_value.execute.return_value = mock_response
        
        result = await supabase_client.test_connection()
        
        assert result is True


class TestEmbeddingService:
    """Test embedding service"""
    
    @pytest.fixture
    def embedding_service(self):
        """Embedding service fixture"""
        with patch('sentence_transformers.SentenceTransformer'):
            service = EmbeddingService()
            service.model = Mock()
            service.model.get_sentence_embedding_dimension.return_value = 384
            return service
    
    @pytest.mark.asyncio
    async def test_generate_persona_embedding(self, embedding_service):
        """Test persona embedding generation"""
        persona = {
            "name": "Test User",
            "city": "Lagos",
            "primary_language": "english",
            "review_style": "casual",
            "avg_rating": 3.5,
            "cultural_markers": ["price_sensitive"],
            "sample_reviews": ["Good service"]
        }
        
        mock_embedding = [0.1, 0.2, 0.3, 0.4]
        embedding_service.model.encode.return_value = mock_embedding
        
        embedding = await embedding_service.generate_persona_embedding(persona)
        
        assert embedding == mock_embedding
        embedding_service.model.encode.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_product_embedding(self, embedding_service):
        """Test product embedding generation"""
        product = {
            "name": "Test Restaurant",
            "category": "restaurant",
            "location": "Lagos",
            "price_tier": "mid",
            "description": "Good food",
            "features": ["WiFi", "Parking"]
        }
        
        mock_embedding = [0.5, 0.6, 0.7, 0.8]
        embedding_service.model.encode.return_value = mock_embedding
        
        embedding = await embedding_service.generate_product_embedding(product)
        
        assert embedding == mock_embedding
    
    @pytest.mark.asyncio
    async def test_calculate_similarity(self, embedding_service):
        """Test similarity calculation"""
        embedding1 = [0.1, 0.2, 0.3, 0.4]
        embedding2 = [0.5, 0.6, 0.7, 0.8]
        
        similarity = await embedding_service.calculate_similarity(embedding1, embedding2)
        
        assert isinstance(similarity, float)
        assert 0 <= similarity <= 1
    
    @pytest.mark.asyncio
    async def test_find_similar_personas(self, embedding_service):
        """Test finding similar personas"""
        target_embedding = [0.1, 0.2, 0.3, 0.4]
        candidate_embeddings = [
            [0.5, 0.6, 0.7, 0.8],
            [0.9, 0.8, 0.7, 0.6],
            [0.1, 0.2, 0.3, 0.4],
            [0.3, 0.4, 0.5, 0.6]
        ]
        
        # Mock similarity calculation
        embedding_service.calculate_similarity = AsyncMock(side_effect=[0.2, 0.1, 1.0, 0.8])
        
        similar = await embedding_service.find_similar_personas(
            target_embedding, candidate_embeddings, top_k=3
        )
        
        assert len(similar) == 3
        # Should be sorted by similarity (highest first)
        assert similar[0]["similarity"] == 1.0
        assert similar[1]["similarity"] == 0.8
        assert similar[2]["similarity"] == 0.2
    
    @pytest.mark.asyncio
    async def test_generate_batch_embeddings(self, embedding_service):
        """Test batch embedding generation"""
        texts = ["Text 1", "Text 2", "Text 3"]
        mock_embeddings = [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
            [0.7, 0.8, 0.9]
        ]
        
        embedding_service.model.encode.return_value = mock_embeddings
        
        embeddings = await embedding_service.generate_batch_embeddings(texts)
        
        assert len(embeddings) == 3
        assert embeddings[0] == [0.1, 0.2, 0.3]
        assert embeddings[1] == [0.4, 0.5, 0.6]
        assert embeddings[2] == [0.7, 0.8, 0.9]


class TestPersonaSimulator:
    """Test persona simulator service"""
    
    @pytest.mark.asyncio
    async def test_generate_review(self, persona_simulator, sample_review_request):
        """Test review generation"""
        response = await persona_simulator.generate_review(sample_review_request)
        
        assert isinstance(response, ReviewResponse)
        assert response.success is True
        assert response.data is not None
        assert response.data.review_text is not None
        assert response.data.predicted_rating is not None
    
    @pytest.mark.asyncio
    async def test_generate_review_with_streaming(self, persona_simulator, sample_review_request):
        """Test streaming review generation"""
        response = await persona_simulator.generate_review(sample_review_request, stream=True)
        
        assert isinstance(response, ReviewResponse)
        assert response.success is True
    
    @pytest.mark.asyncio
    async def test_predict_rating(self, persona_simulator):
        """Test rating prediction"""
        persona = Mock()
        persona.avg_rating = 3.5
        persona.sentiment_volatility = "medium"
        
        product = Mock()
        product.category = "restaurant"
        product.avg_rating = 4.0
        
        context = Mock()
        context.occasion = "casual"
        
        rating = await persona_simulator.predict_rating(persona, product, context)
        
        assert isinstance(rating, float)
        assert 1.0 <= rating <= 5.0
    
    @pytest.mark.asyncio
    async def test_evaluate_behavioral_fidelity(self, persona_simulator):
        """Test behavioral fidelity evaluation"""
        persona = Mock()
        persona.avg_rating = 3.5
        persona.review_style = "casual"
        persona.pidgin_intensity = 0.5
        
        generated_review = "This place is good!"
        expected_sentiment = "positive"
        
        fidelity = await persona_simulator.evaluate_behavioral_fidelity(
            persona, generated_review, expected_sentiment
        )
        
        assert isinstance(fidelity, float)
        assert 0 <= fidelity <= 1
    
    @pytest.mark.asyncio
    async def test_detect_sentiment(self, persona_simulator):
        """Test sentiment detection"""
        text = "This place is amazing! I love it here."
        sentiment = await persona_simulator.detect_sentiment(text)
        
        assert sentiment in ["positive", "negative", "neutral"]
    
    @pytest.mark.asyncio
    async def test_generate_review_error_handling(self, persona_simulator, sample_review_request):
        """Test error handling in review generation"""
        # Mock Groq client to raise exception
        persona_simulator.groq_client.chat_completion = AsyncMock(side_effect=Exception("API Error"))
        
        response = await persona_simulator.generate_review(sample_review_request)
        
        assert response.success is False
        assert "API Error" in response.error


class TestRecommendationEngine:
    """Test recommendation engine service"""
    
    @pytest.mark.asyncio
    async def test_generate_recommendations(self, recommendation_engine, sample_recommendation_request):
        """Test recommendation generation"""
        response = await recommendation_engine.generate_recommendations(sample_recommendation_request)
        
        assert isinstance(response, RecommendationResponse)
        assert response.success is True
        assert response.data is not None
        assert len(response.data.recommendations) > 0
    
    @pytest.mark.asyncio
    async def test_reason_about_request(self, recommendation_engine):
        """Test request reasoning"""
        persona = Mock()
        persona.avg_rating = 3.5
        persona.categories_reviewed = ["food"]
        
        request = Mock()
        request.domain = "food"
        request.context = {"mood_signal": "celebratory"}
        
        reasoning = await recommendation_engine._reason_about_request(persona, request)
        
        assert "preferences" in reasoning
        assert "context" in reasoning
        assert "strategy" in reasoning
    
    @pytest.mark.asyncio
    async def test_retrieve_candidates(self, recommendation_engine):
        """Test candidate retrieval"""
        persona = Mock()
        persona.city = "Lagos"
        persona.categories_reviewed = ["food"]
        
        request = Mock()
        request.domain = "food"
        request.context = {"budget_naira": 5000}
        
        reasoning = {"preferences": {"food": 0.8}, "context": {"budget": 5000}}
        
        candidates = await recommendation_engine._retrieve_candidates(persona, request, reasoning)
        
        assert isinstance(candidates, list)
        assert len(candidates) > 0
    
    @pytest.mark.asyncio
    async def test_rank_recommendations(self, recommendation_engine):
        """Test recommendation ranking"""
        persona = Mock()
        persona.avg_rating = 3.5
        
        request = Mock()
        request.context = {"mood_signal": "celebratory"}
        
        candidates = [
            {"name": "Restaurant 1", "rating": 4.2},
            {"name": "Restaurant 2", "rating": 3.8},
            {"name": "Restaurant 3", "rating": 4.5}
        ]
        
        reasoning = {"preferences": {"food": 0.8}}
        
        ranked = await recommendation_engine._rank_recommendations(persona, request, candidates, reasoning)
        
        assert isinstance(ranked, list)
        assert len(ranked) == len(candidates)
        # Should be sorted by relevance
        assert ranked[0]["relevance_score"] >= ranked[1]["relevance_score"]
    
    @pytest.mark.asyncio
    async def test_refine_with_context(self, recommendation_engine):
        """Test context refinement"""
        persona = Mock()
        persona.avg_rating = 3.5
        
        request = Mock()
        request.context = {"mood_signal": "celebratory", "location": "Lekki"}
        
        ranked = [
            {"name": "Restaurant 1", "relevance_score": 0.9},
            {"name": "Restaurant 2", "relevance_score": 0.8}
        ]
        
        reasoning = {"preferences": {"food": 0.8}}
        
        refined = await recommendation_engine._refine_with_context(persona, request, ranked, reasoning)
        
        assert isinstance(refined, list)
        assert len(refined) <= len(ranked)
    
    @pytest.mark.asyncio
    async def test_generate_explanation(self, recommendation_engine):
        """Test explanation generation"""
        persona = Mock()
        persona.name = "Test User"
        
        request = Mock()
        request.context = {"mood_signal": "celebratory"}
        
        recommendations = [
            {"name": "Restaurant 1", "reasoning": "Good for celebrations"}
        ]
        
        explanation = await recommendation_engine._generate_explanation(persona, request, recommendations)
        
        assert isinstance(explanation, str)
        assert len(explanation) > 0
        assert "celebratory" in explanation.lower()
    
    @pytest.mark.asyncio
    async def test_calculate_ndcg(self, recommendation_engine):
        """Test NDCG calculation"""
        recommendations = [
            {"relevance_score": 1.0},
            {"relevance_score": 0.8},
            {"relevance_score": 0.6},
            {"relevance_score": 0.4},
            {"relevance_score": 0.2}
        ]
        
        ndcg = await recommendation_engine._calculate_ndcg(recommendations)
        
        assert isinstance(ndcg, float)
        assert 0 <= ndcg <= 1
    
    @pytest.mark.asyncio
    async def test_calculate_hit_rate(self, recommendation_engine):
        """Test hit rate calculation"""
        recommendations = [
            {"item_id": "item_1"},
            {"item_id": "item_2"},
            {"item_id": "item_3"},
            {"item_id": "item_4"},
            {"item_id": "item_5"}
        ]
        
        hit_rate = await recommendation_engine._calculate_hit_rate(recommendations[:5])
        
        assert isinstance(hit_rate, float)
        assert 0 <= hit_rate <= 1
    
    @pytest.mark.asyncio
    async def test_generate_recommendations_error_handling(self, recommendation_engine, sample_recommendation_request):
        """Test error handling in recommendation generation"""
        # Mock Groq client to raise exception
        recommendation_engine.groq_client.chat_completion = AsyncMock(side_effect=Exception("API Error"))
        
        response = await recommendation_engine.generate_recommendations(sample_recommendation_request)
        
        assert response.success is False
        assert "API Error" in response.error
