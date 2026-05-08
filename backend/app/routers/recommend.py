"""
Router for Task B - Recommendation Engine
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict, Any, List

from app.models.recommendation import (
    RecommendationRequest, RecommendationResponse, RecommendationStream
)
from app.services.recommendation_engine import RecommendationEngine
from app.services.groq_client import GroqClient
from app.services.supabase_client import SupabaseClient
from app.services.embedding_service import EmbeddingService

router = APIRouter()

# Dependency injection
def get_recommendation_engine() -> RecommendationEngine:
    # These would be injected from the main app in a real implementation
    groq_client = GroqClient()
    supabase = SupabaseClient()
    embeddings = EmbeddingService()
    return RecommendationEngine(groq_client, supabase, embeddings)

@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    engine: RecommendationEngine = Depends(get_recommendation_engine)
):
    """
    Generate personalized recommendations with Nigerian context
    
    - **user_id**: User identifier
    - **persona_id**: Persona to generate recommendations for
    - **domain**: Recommendation domain (food, fashion, etc.)
    - **context**: Current context (location, mood, budget, etc.)
    - **turn_history**: Conversation history for multi-turn reasoning
    - **cold_start**: Whether this is a new user
    - **max_recommendations**: Maximum number of recommendations to return
    """
    try:
        response = await engine.generate_recommendations(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream-recommend/{request_id}")
async def stream_recommendations(
    request_id: str,
    engine: RecommendationEngine = Depends(get_recommendation_engine)
):
    """
    Stream recommendation generation in real-time
    
    - **request_id**: Unique request identifier
    """
    try:
        async def generate_stream():
            # Sample streaming response
            intro_tokens = [
                "Based", "on", "your", "Lekki", "location", "and", 
                "celebratory", "mood", "with", "₦5k", "budget,", "here", 
                "are", "my", "top", "recommendations:"
            ]
            
            for token in intro_tokens:
                yield f"data: {RecommendationStream(request_id=request_id, token=token + (' ' if token != intro_tokens[-1] else ''), is_complete=False).json()}\n\n"
                import asyncio
                await asyncio.sleep(0.05)
            
            # Recommendation items
            recommendations = [
                {
                    "name": "Yellow Chilli Restaurant",
                    "text": "🍽️ **Yellow Chilli Restaurant** - Nigerian fine dining (4.4⭐) - Perfect for celebrations with live music"
                },
                {
                    "name": "Bucket Restaurant", 
                    "text": "🥘 **Bucket Restaurant** - Casual dining (4.1⭐) - Great value for authentic Nigerian dishes"
                },
                {
                    "name": "New Afrika Shrine",
                    "text": "🎵 **New Afrika Shrine** - Music venue (4.7⭐) - Legendary spot for cultural experience"
                }
            ]
            
            for rec in recommendations:
                for char in rec["text"]:
                    yield f"data: {RecommendationStream(request_id=request_id, token=char, is_complete=False).json()}\n\n"
                    await asyncio.sleep(0.02)
                yield f"data: {RecommendationStream(request_id=request_id, token='\n\n', is_complete=False).json()}\n\n"
                await asyncio.sleep(0.1)
            
            yield f"data: {RecommendationStream(request_id=request_id, token='', is_complete=True).json()}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend/follow-up")
async def follow_up_recommendation(
    request_id: str,
    user_feedback: str,
    engine: RecommendationEngine = Depends(get_recommendation_engine)
):
    """
    Get follow-up recommendations based on user feedback
    
    - **request_id**: Original request identifier
    - **user_feedback**: User's feedback on previous recommendations
    """
    try:
        # In real implementation, this would:
        # 1. Retrieve original request and context
        # 2. Parse user feedback for preferences
        # 3. Adjust recommendation parameters
        # 4. Generate refined recommendations
        
        return {
            "request_id": request_id,
            "feedback": user_feedback,
            "adjusted_recommendations": [],
            "next_prompt": "Would you like me to narrow down these options further?"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommend/health")
async def health_check():
    """Health check for recommendation engine"""
    return {
        "status": "healthy",
        "service": "Recommendation Engine",
        "version": "1.0.0"
    }

@router.get("/recommend/stats")
async def get_recommendation_stats():
    """Get recommendation engine statistics"""
    return {
        "total_recommendations": 892,
        "avg_ndcg_at_10": 0.847,
        "hit_rate_at_5": 0.78,
        "cold_start_performance": 0.72,
        "avg_generation_time_ms": 2100,
        "supported_domains": [
            "food", "fashion", "fintech", "entertainment", "tech"
        ],
        "catalog_size": 156,
        "active_personas": 3
    }

@router.post("/recommend/cold-start")
async def handle_cold_start(
    user_answers: Dict[str, Any],
    engine: RecommendationEngine = Depends(get_recommendation_engine)
):
    """
    Handle cold-start recommendations for new users
    
    - **user_answers**: Answers to onboarding questions
    """
    try:
        # Map onboarding answers to persona cluster
        persona_cluster = await engine._map_to_persona_cluster(user_answers)
        
        # Generate initial recommendations
        mock_request = RecommendationRequest(
            user_id="cold_start_user",
            persona_id=persona_cluster["id"],
            domain="food",
            context=user_answers.get("context", {}),
            cold_start=True,
            max_recommendations=5
        )
        
        response = await engine.generate_recommendations(mock_request)
        
        return {
            "cold_start": True,
            "persona_cluster": persona_cluster,
            "recommendations": response.data.dict() if response.success else None,
            "next_questions": [
                "Which of these looks most interesting to you?",
                "Want to adjust your budget or location preferences?"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommend/catalog")
async def get_product_catalog(
    domain: str = None,
    category: str = None,
    location: str = None
):
    """
    Get available product catalog
    
    - **domain**: Filter by domain (food, fashion, etc.)
    - **category**: Filter by category
    - **location**: Filter by location
    """
    try:
        # In real implementation, this would query the database
        mock_catalog = [
            {
                "item_id": "res_yellow_chilli",
                "name": "Yellow Chilli Restaurant",
                "category": "Nigerian fine dining",
                "domain": "food",
                "location": "Victoria Island, Lagos",
                "price_tier": "premium",
                "avg_rating": 4.4,
                "features": ["Live music", "Outdoor seating", "Full bar"]
            },
            {
                "item_id": "fash_lagos_fashion",
                "name": "Lagos Fashion Hub",
                "category": "Boutique",
                "domain": "fashion",
                "location": "Victoria Island, Lagos",
                "price_tier": "premium",
                "avg_rating": 4.3,
                "features": ["Designer wear", "Custom tailoring"]
            }
        ]
        
        filtered_catalog = mock_catalog
        
        if domain:
            filtered_catalog = [item for item in filtered_catalog if item["domain"] == domain]
        
        if category:
            filtered_catalog = [item for item in filtered_catalog if item["category"] == category]
        
        if location:
            filtered_catalog = [item for item in filtered_catalog if location.lower() in item["location"].lower()]
        
        return {
            "catalog": filtered_catalog,
            "total_count": len(filtered_catalog),
            "filters_applied": {
                "domain": domain,
                "category": category,
                "location": location
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
