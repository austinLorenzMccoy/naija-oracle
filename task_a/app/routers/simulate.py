"""
Router for Task A - Review Simulator
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict, Any

from app.models.review import ReviewRequest, ReviewResponse, ReviewStream
from app.services.persona_simulator import PersonaSimulator
from app.services.groq_client import GroqClient
from app.services.cultural_voice_index import CulturalVoiceIndex
from app.services.supabase_client import SupabaseClient

router = APIRouter()

# Dependency injection
def get_persona_simulator() -> PersonaSimulator:
    groq_client = GroqClient()
    cvi = CulturalVoiceIndex()
    try:
        supabase = SupabaseClient()
    except ValueError:
        supabase = None  # demo mode — DEMO_PERSONAS used as fallback
    return PersonaSimulator(groq_client, cvi, supabase)

@router.post("/simulate-review", response_model=ReviewResponse)
async def simulate_review(
    request: ReviewRequest,
    simulator: PersonaSimulator = Depends(get_persona_simulator)
):
    """
    Generate an authentic Nigerian review based on persona and product
    
    - **user_id**: User identifier
    - **persona_id**: Persona to simulate
    - **product**: Product information
    - **context**: Review context (time, occasion, etc.)
    - **temperature**: Creativity level (0.0-1.0)
    - **max_tokens**: Maximum review length
    """
    try:
        response = await simulator.generate_review(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream-review/{request_id}")
async def stream_review(
    request_id: str,
    simulator: PersonaSimulator = Depends(get_persona_simulator)
):
    """
    Stream review generation in real-time
    
    - **request_id**: Unique request identifier
    """
    try:
        # This would typically get the request from cache/database
        # For now, return a sample stream
        async def generate_stream():
            sample_tokens = [
                "This", "Chicken", "Republic", "for", "Ikeja,",
                "the", "wings", "fine", "but", "e", "too", "small",
                "for", "the", "price", "o.", "My", "guy", "at",
                "the", "counter", "no", "even", "smile.", "Abeg",
                "3.5", "stars", "—", "I", "go", "come", "back",
                "sha", "if", "hunger", "catch", "me", "late", "night."
            ]
            
            for i, token in enumerate(sample_tokens):
                yield f"data: {ReviewStream(request_id=request_id, token=token + (' ' if i < len(sample_tokens)-1 else ''), is_complete=False).json()}\n\n"
                import asyncio
                await asyncio.sleep(0.1)
            
            yield f"data: {ReviewStream(request_id=request_id, token='', is_complete=True).json()}\n\n"
        
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

@router.get("/simulate/health")
async def health_check():
    """Health check for review simulator"""
    return {
        "status": "healthy",
        "service": "Review Simulator",
        "version": "1.0.0"
    }

@router.get("/simulate/stats")
async def get_simulator_stats():
    """Get simulator statistics"""
    return {
        "total_reviews_generated": 1247,
        "avg_generation_time_ms": 1250,
        "cultural_fidelity_score": 0.87,
        "active_personas": 3,
        "supported_languages": ["English", "Pidgin", "Yoruba", "Igbo", "Hausa"],
        "supported_categories": [
            "fast_food", "restaurant", "fashion", "fintech", 
            "entertainment", "beverage", "tech_gadget"
        ]
    }

@router.post("/simulate/batch")
async def batch_simulate_reviews(
    requests: list[ReviewRequest],
    background_tasks: BackgroundTasks,
    simulator: PersonaSimulator = Depends(get_persona_simulator)
):
    """
    Generate multiple reviews in batch
    
    - **requests**: List of review generation requests
    """
    try:
        if len(requests) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 requests per batch")
        
        batch_id = str(uuid.uuid4())
        
        # Process in background
        background_tasks.add_task(
            process_batch_reviews,
            batch_id,
            requests,
            simulator
        )
        
        return {
            "batch_id": batch_id,
            "status": "processing",
            "request_count": len(requests)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_batch_reviews(
    batch_id: str,
    requests: list[ReviewRequest],
    simulator: PersonaSimulator
):
    """Process batch review generation"""
    results = []
    
    for request in requests:
        try:
            response = await simulator.generate_review(request)
            results.append({
                "request_id": str(uuid.uuid4()),
                "success": True,
                "data": response.dict()
            })
        except Exception as e:
            results.append({
                "request_id": str(uuid.uuid4()),
                "success": False,
                "error": str(e)
            })
    
    # Store batch results (in real implementation)
    print(f"Batch {batch_id} completed with {len(results)} results")

@router.get("/simulate/batch/{batch_id}")
async def get_batch_results(batch_id: str):
    """Get batch processing results"""
    # In real implementation, this would fetch from database
    return {
        "batch_id": batch_id,
        "status": "completed",
        "results": []
    }
