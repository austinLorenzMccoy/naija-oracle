"""
Test suite for data models
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from app.models.persona import (
    Persona, PersonaCreate, PersonaUpdate, PersonaLanguage,
    ReviewStyle, PersonaStatus
)
from app.models.review import (
    ReviewRequest, ReviewResponse, ReviewGeneration, VoiceProfile,
    Product, Context, ProductCategory, PriceTier, TimeOfDay, Occasion
)
from app.models.recommendation import (
    RecommendationRequest, RecommendationResponse, RecommendationGeneration,
    RecommendationItem, RecommendationContext, RecommendationDomain,
    TurnHistory
)
from app.models.cultural_voice import (
    CVIAnchor, CulturalVoiceIndex, CVIMatch, CVIProfile,
    TribeRegion, FormalityRegister, SentimentCategory, ProductContext
)


class TestPersonaModels:
    """Test persona-related models"""
    
    def test_persona_create_valid(self, sample_persona_create):
        """Test valid persona creation"""
        persona = PersonaCreate(**sample_persona_create.dict())
        
        assert persona.user_id == "test_user_id"
        assert persona.name == "Test User"
        assert persona.city == "Lagos"
        assert persona.primary_language == PersonaLanguage.ENGLISH
        assert persona.review_style == ReviewStyle.CASUAL
        assert persona.avg_rating == 3.5
        assert persona.pidgin_intensity == 0.5
    
    def test_persona_create_invalid_rating(self, sample_persona_create):
        """Test persona creation with invalid rating"""
        sample_persona_create.avg_rating = 6.0  # Invalid rating > 5
        
        with pytest.raises(ValidationError):
            PersonaCreate(**sample_persona_create.dict())
    
    def test_persona_create_invalid_pidgin_intensity(self, sample_persona_create):
        """Test persona creation with invalid pidgin intensity"""
        sample_persona_create.pidgin_intensity = 1.5  # Invalid > 1.0
        
        with pytest.raises(ValidationError):
            PersonaCreate(**sample_persona_create.dict())
    
    def test_persona_update_partial(self, sample_persona_create):
        """Test partial persona update"""
        update_data = {"name": "Updated Name", "avg_rating": 4.0}
        persona_update = PersonaUpdate(**update_data)
        
        assert persona_update.name == "Updated Name"
        assert persona_update.avg_rating == 4.0
        assert persona_update.city is None  # Not provided in update
    
    def test_persona_full_model(self, sample_persona_create):
        """Test full persona model"""
        persona = Persona(
            id="test_id",
            user_id="test_user_id",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            **sample_persona_create.dict()
        )
        
        assert persona.id == "test_id"
        assert persona.user_id == "test_user_id"
        assert persona.status == PersonaStatus.ACTIVE
        assert isinstance(persona.created_at, datetime)
    
    def test_persona_language_enum(self):
        """Test persona language enum values"""
        assert PersonaLanguage.ENGLISH == "english"
        assert PersonaLanguage.PIDGIN == "pidgin"
        assert PersonaLanguage.YORUBA == "yoruba"
        assert PersonaLanguage.IGBO == "igbo"
        assert PersonaLanguage.HAUSA == "hausa"
    
    def test_review_style_enum(self):
        """Test review style enum values"""
        assert ReviewStyle.EXPRESSIVE == "expressive"
        assert ReviewStyle.ANALYTICAL == "analytical"
        assert ReviewStyle.CASUAL == "casual"
        assert ReviewStyle.TERSE == "terse"
        assert ReviewStyle.FORMAL == "formal"
    
    def test_persona_status_enum(self):
        """Test persona status enum values"""
        assert PersonaStatus.ACTIVE == "active"
        assert PersonaStatus.INACTIVE == "inactive"
        assert PersonaStatus.TRAINING == "training"
        assert PersonaStatus.ACTIVE_ORACLE == "active_oracle"


class TestReviewModels:
    """Test review generation models"""
    
    def test_product_model_valid(self):
        """Test valid product model"""
        product = Product(
            name="Test Restaurant",
            category=ProductCategory.RESTAURANT,
            location="Lagos",
            price_tier=PriceTier.MID
        )
        
        assert product.name == "Test Restaurant"
        assert product.category == ProductCategory.RESTAURANT
        assert product.price_tier == PriceTier.MID
    
    def test_context_model_valid(self):
        """Test valid context model"""
        context = Context(
            time_of_day=TimeOfDay.EVENING,
            occasion=Occasion.CASUAL,
            recency_of_visit="first_time"
        )
        
        assert context.time_of_day == TimeOfDay.EVENING
        assert context.occasion == Occasion.CASUAL
        assert context.recency_of_visit == "first_time"
    
    def test_review_request_valid(self, sample_review_request):
        """Test valid review request"""
        request = ReviewRequest(**sample_review_request.dict())
        
        assert request.user_id == "test_user_id"
        assert request.persona_id == "test_persona_id"
        assert request.product.name == "Test Restaurant"
        assert request.context.time_of_day == TimeOfDay.EVENING
        assert request.temperature == 0.7
        assert request.max_tokens == 400
    
    def test_review_request_invalid_temperature(self, sample_review_request):
        """Test review request with invalid temperature"""
        sample_review_request.temperature = 1.5  # Invalid > 1.0
        
        with pytest.raises(ValidationError):
            ReviewRequest(**sample_review_request.dict())
    
    def test_voice_profile_valid(self):
        """Test valid voice profile"""
        profile = VoiceProfile(
            pidgin_intensity=0.7,
            sentiment_category="mixed_positive",
            cultural_markers_activated=["price_sensitive"],
            language_patterns={"english": 0.3, "pidgin": 0.7}
        )
        
        assert profile.pidgin_intensity == 0.7
        assert profile.sentiment_category == "mixed_positive"
        assert "price_sensitive" in profile.cultural_markers_activated
        assert profile.language_patterns["pidgin"] == 0.7
    
    def test_review_generation_valid(self):
        """Test valid review generation"""
        generation = ReviewGeneration(
            predicted_rating=4.2,
            confidence_interval=[3.8, 4.6],
            review_text="This place is great!",
            voice_profile_used=VoiceProfile(
                pidgin_intensity=0.5,
                sentiment_category="positive",
                cultural_markers_activated=[],
                language_patterns={}
            ),
            behavioural_fidelity_score=0.85,
            cvi_anchors_used=["E sweet me die"],
            generation_time_ms=1500,
            model_used="test-model",
            temperature_used=0.7
        )
        
        assert generation.predicted_rating == 4.2
        assert generation.confidence_interval == [3.8, 4.6]
        assert generation.behavioural_fidelity_score == 0.85
        assert "E sweet me die" in generation.cvi_anchors_used
    
    def test_review_response_success(self):
        """Test successful review response"""
        generation = ReviewGeneration(
            predicted_rating=4.2,
            confidence_interval=[3.8, 4.6],
            review_text="This place is great!",
            voice_profile_used=VoiceProfile(
                pidgin_intensity=0.5,
                sentiment_category="positive",
                cultural_markers_activated=[],
                language_patterns={}
            ),
            behavioural_fidelity_score=0.85,
            cvi_anchors_used=[],
            generation_time_ms=1500,
            model_used="test-model",
            temperature_used=0.7
        )
        
        response = ReviewResponse(
            success=True,
            data=generation,
            request_id="test_request_id"
        )
        
        assert response.success is True
        assert response.data is not None
        assert response.error is None
        assert response.request_id == "test_request_id"
    
    def test_review_response_error(self):
        """Test error review response"""
        response = ReviewResponse(
            success=False,
            error="Test error message",
            request_id="test_request_id"
        )
        
        assert response.success is False
        assert response.data is None
        assert response.error == "Test error message"
    
    def test_product_category_enum(self):
        """Test product category enum"""
        assert ProductCategory.FAST_FOOD == "fast_food"
        assert ProductCategory.RESTAURANT == "restaurant"
        assert ProductCategory.FASHION == "fashion"
        assert ProductCategory.FINTECH == "fintech"
        assert ProductCategory.ENTERTAINMENT == "entertainment"
        assert ProductCategory.BEVERAGE == "beverage"
        assert ProductCategory.TECH_GADGET == "tech_gadget"
        assert ProductCategory.BEAUTY == "beauty"
        assert ProductCategory.TRANSPORT == "transport"
        assert ProductCategory.GROCERY == "grocery"
    
    def test_price_tier_enum(self):
        """Test price tier enum"""
        assert PriceTier.BUDGET == "budget"
        assert PriceTier.MID == "mid"
        assert PriceTier.PREMIUM == "premium"
        assert PriceTier.LUXURY == "luxury"
    
    def test_time_of_day_enum(self):
        """Test time of day enum"""
        assert TimeOfDay.MORNING == "morning"
        assert TimeOfDay.AFTERNOON == "afternoon"
        assert TimeOfDay.EVENING == "evening"
        assert TimeOfDay.LATE_NIGHT == "late_night"
    
    def test_occasion_enum(self):
        """Test occasion enum"""
        assert Occasion.CASUAL == "casual"
        assert Occasion.AFTER_WORK == "after_work"
        assert Occasion.DATE == "date"
        assert Occasion.CELEBRATION == "celebration"
        assert Occasion.IMPULSE == "impulse"
        assert Occasion.BUSINESS == "business"


class TestRecommendationModels:
    """Test recommendation models"""
    
    def test_recommendation_context_valid(self):
        """Test valid recommendation context"""
        context = RecommendationContext(
            current_time="Saturday 8PM",
            location="Lekki Phase 1",
            mood_signal="celebratory",
            budget_naira=5000
        )
        
        assert context.current_time == "Saturday 8PM"
        assert context.location == "Lekki Phase 1"
        assert context.mood_signal == "celebratory"
        assert context.budget_naira == 5000
    
    def test_recommendation_request_valid(self, sample_recommendation_request):
        """Test valid recommendation request"""
        request = RecommendationRequest(**sample_recommendation_request.dict())
        
        assert request.user_id == "test_user_id"
        assert request.persona_id == "test_persona_id"
        assert request.domain == RecommendationDomain.FOOD
        assert request.context.location == "Lekki Phase 1"
        assert request.max_recommendations == 5
        assert request.cold_start is False
    
    def test_recommendation_item_valid(self):
        """Test valid recommendation item"""
        item = RecommendationItem(
            item_id="item_123",
            name="Test Restaurant",
            category="Nigerian fine dining",
            location="Victoria Island",
            price_tier="premium",
            predicted_rating=4.4,
            context_score=0.91,
            reasoning="Perfect for your celebration mood",
            distance_km=5.2,
            price_range_naira=(8000, 15000),
            features=["Live music", "Outdoor seating"]
        )
        
        assert item.item_id == "item_123"
        assert item.name == "Test Restaurant"
        assert item.predicted_rating == 4.4
        assert item.context_score == 0.91
        assert "Live music" in item.features
    
    def test_recommendation_generation_valid(self):
        """Test valid recommendation generation"""
        items = [
            RecommendationItem(
                item_id="item_1",
                name="Restaurant 1",
                category="food",
                location="Lagos",
                price_tier="mid",
                predicted_rating=4.2,
                context_score=0.85,
                reasoning="Good match for your preferences"
            )
        ]
        
        generation = RecommendationGeneration(
            recommendations=items,
            explanation="Based on your preferences, here are our recommendations",
            next_turn_prompt="Want more details?",
            cold_start_used=False,
            ndcg_at_10=0.89,
            hit_rate_at_5=0.82,
            reasoning_trace=["Analyzed preferences", "Found matches"],
            context_boost_factors={"mood": 0.2, "location": 0.1},
            generation_time_ms=2000,
            model_used="test-model",
            temperature_used=0.7
        )
        
        assert len(generation.recommendations) == 1
        assert generation.ndcg_at_10 == 0.89
        assert generation.hit_rate_at_5 == 0.82
        assert generation.cold_start_used is False
    
    def test_recommendation_response_success(self):
        """Test successful recommendation response"""
        items = [
            RecommendationItem(
                item_id="item_1",
                name="Restaurant 1",
                category="food",
                location="Lagos",
                price_tier="mid",
                predicted_rating=4.2,
                context_score=0.85,
                reasoning="Good match"
            )
        ]
        
        generation = RecommendationGeneration(
            recommendations=items,
            explanation="Test explanation",
            cold_start_used=False,
            ndcg_at_10=0.89,
            hit_rate_at_5=0.82,
            reasoning_trace=[],
            context_boost_factors={},
            generation_time_ms=2000,
            model_used="test-model",
            temperature_used=0.7
        )
        
        response = RecommendationResponse(
            success=True,
            data=generation,
            request_id="test_request_id"
        )
        
        assert response.success is True
        assert response.data is not None
        assert response.error is None
    
    def test_turn_history_valid(self):
        """Test valid turn history"""
        history = TurnHistory(
            user_query="I want good food",
            agent_response="Here are some restaurants",
            recommendations_shown=["item_1", "item_2"],
            user_feedback="Good suggestions"
        )
        
        assert history.user_query == "I want good food"
        assert history.agent_response == "Here are some restaurants"
        assert "item_1" in history.recommendations_shown
        assert history.user_feedback == "Good suggestions"
    
    def test_recommendation_domain_enum(self):
        """Test recommendation domain enum"""
        assert RecommendationDomain.FOOD == "food"
        assert RecommendationDomain.FASHION == "fashion"
        assert RecommendationDomain.FINTECH == "fintech"
        assert RecommendationDomain.ENTERTAINMENT == "entertainment"
        assert RecommendationDomain.TECH == "tech"


class TestCulturalVoiceModels:
    """Test cultural voice index models"""
    
    def test_cvi_anchor_valid(self):
        """Test valid CVI anchor"""
        anchor = CVIAnchor(
            phrase="E sweet me die",
            tribe_region=TribeRegion.YORUBA,
            pidgin_intensity=0.8,
            formality_register=FormalityRegister.CASUAL,
            sentiment_category=SentimentCategory.STRONG_POSITIVE,
            product_context=ProductContext.FOOD,
            avg_rating_association=5.0,
            frequency_score=0.9,
            confidence_score=0.95,
            examples=["The jollof sweet me die!"]
        )
        
        assert anchor.phrase == "E sweet me die"
        assert anchor.tribe_region == TribeRegion.YORUBA
        assert anchor.pidgin_intensity == 0.8
        assert anchor.avg_rating_association == 5.0
    
    def test_cvi_anchor_invalid_pidgin_intensity(self):
        """Test CVI anchor with invalid pidgin intensity"""
        with pytest.raises(ValidationError):
            CVIAnchor(
                phrase="Test phrase",
                tribe_region=TribeRegion.PAN_NIGERIAN,
                pidgin_intensity=1.5,  # Invalid > 1.0
                formality_register=FormalityRegister.CASUAL,
                sentiment_category=SentimentCategory.POSITIVE,
                product_context=ProductContext.GENERAL,
                avg_rating_association=3.0,
                frequency_score=0.5,
                confidence_score=0.7
            )
    
    def test_cvi_match_valid(self):
        """Test CVI match"""
        anchor = CVIAnchor(
            phrase="Test phrase",
            tribe_region=TribeRegion.YORUBA,
            pidgin_intensity=0.7,
            formality_register=FormalityRegister.CASUAL,
            sentiment_category=SentimentCategory.POSITIVE,
            product_context=ProductContext.FOOD,
            avg_rating_association=4.0,
            frequency_score=0.8,
            confidence_score=0.9
        )
        
        match = CVIMatch(
            anchor=anchor,
            match_score=0.85,
            relevance_score=0.9,
            activation_weight=0.8
        )
        
        assert match.anchor.phrase == "Test phrase"
        assert match.match_score == 0.85
        assert match.relevance_score == 0.9
        assert match.activation_weight == 0.8
    
    def test_cvi_profile_valid(self):
        """Test CVI profile"""
        profile = CVIProfile(
            persona_id="persona_123",
            dominant_tribe_region=TribeRegion.YORUBA,
            pidgin_intensity=0.7,
            formality_preference=FormalityRegister.CASUAL,
            sentiment_patterns={
                SentimentCategory.POSITIVE: 0.8,
                SentimentCategory.NEGATIVE: 0.2
            },
            context_specializations={
                ProductContext.FOOD: 0.9,
                ProductContext.SERVICE: 0.6
            },
            preferred_anchors=["E sweet me die", "Gbam!"],
            voice_consistency_score=0.85,
            cultural_authenticity_score=0.9
        )
        
        assert profile.persona_id == "persona_123"
        assert profile.dominant_tribe_region == TribeRegion.YORUBA
        assert profile.pidgin_intensity == 0.7
        assert profile.voice_consistency_score == 0.85
    
    def test_tribe_region_enum(self):
        """Test tribe region enum"""
        assert TribeRegion.YORUBA == "yoruba"
        assert TribeRegion.IGBO == "igbo"
        assert TribeRegion.HAUSA == "hausa"
        assert TribeRegion.PAN_NIGERIAN == "pan_nigerian"
        assert TribeRegion.EDO == "edo"
        assert TribeRegion.URHOBO == "urhobo"
        assert TribeRegion.IJAW == "ijaw"
        assert TribeRegion.Ibibio == "ibibio"
    
    def test_formality_register_enum(self):
        """Test formality register enum"""
        assert FormalityRegister.CASUAL == "casual"
        assert FormalityRegister.EXPRESSIVE == "expressive"
        assert FormalityRegister.FORMAL == "formal"
        assert FormalityRegister.SEMI_FORMAL == "semi_formal"
    
    def test_sentiment_category_enum(self):
        """Test sentiment category enum"""
        assert SentimentCategory.STRONG_POSITIVE == "strong_positive"
        assert SentimentCategory.POSITIVE == "positive"
        assert SentimentCategory.MIXED_POSITIVE == "mixed_positive"
        assert SentimentCategory.NEUTRAL == "neutral"
        assert SentimentCategory.MIXED_NEGATIVE == "mixed_negative"
        assert SentimentCategory.NEGATIVE == "negative"
        assert SentimentCategory.STRONG_NEGATIVE == "strong_negative"
    
    def test_product_context_enum(self):
        """Test product context enum"""
        assert ProductContext.FOOD == "food"
        assert ProductContext.SERVICE == "service"
        assert ProductContext.AMBIENCE == "ambience"
        assert ProductContext.PRICE == "price"
        assert ProductContext.GENERAL == "general"
        assert ProductContext.TRANSPORT == "transport"
        assert ProductContext.TECH == "tech"
        assert ProductContext.FASHION == "fashion"


class TestModelSerialization:
    """Test model serialization and deserialization"""
    
    def test_persona_serialization(self, sample_persona_create):
        """Test persona model serialization"""
        persona = PersonaCreate(**sample_persona_create.dict())
        
        # Test dict serialization
        persona_dict = persona.dict()
        assert isinstance(persona_dict, dict)
        assert persona_dict["name"] == "Test User"
        assert persona_dict["city"] == "Lagos"
        
        # Test JSON serialization
        import json
        persona_json = persona.json()
        assert isinstance(json.loads(persona_json), dict)
        assert "Test User" in persona_json
    
    def test_review_request_serialization(self, sample_review_request):
        """Test review request serialization"""
        request = ReviewRequest(**sample_review_request.dict())
        
        request_dict = request.dict()
        assert isinstance(request_dict, dict)
        assert request_dict["user_id"] == "test_user_id"
        assert request_dict["product"]["name"] == "Test Restaurant"
    
    def test_recommendation_request_serialization(self, sample_recommendation_request):
        """Test recommendation request serialization"""
        request = RecommendationRequest(**sample_recommendation_request.dict())
        
        request_dict = request.dict()
        assert isinstance(request_dict, dict)
        assert request_dict["domain"] == "food"
        assert request_dict["context"]["location"] == "Lekki Phase 1"
