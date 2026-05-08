"""
Router for Persona management
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.models.persona import Persona, PersonaCreate, PersonaUpdate
from app.services.supabase_client import SupabaseClient

router = APIRouter()

# Dependency injection
def get_supabase_client() -> SupabaseClient:
    return SupabaseClient()

@router.post("/personas", response_model=Persona)
async def create_persona(
    persona_data: PersonaCreate,
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """
    Create a new persona
    
    - **user_id**: User identifier
    - **name**: Persona name
    - **age_range**: Age range (e.g., "25-34")
    - **city**: City (e.g., "Lagos")
    - **lga**: Local Government Area
    - **primary_language**: Primary language
    - **review_style**: Review writing style
    - **avg_rating**: Average rating tendency
    - **cultural_markers**: Cultural markers list
    - **pidgin_intensity**: Pidgin intensity (0.0-1.0)
    """
    try:
        persona = await supabase.create_persona(persona_data)
        return persona
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/personas/{persona_id}", response_model=Persona)
async def get_persona(
    persona_id: str,
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """
    Get persona by ID
    
    - **persona_id**: Persona identifier
    """
    try:
        persona = await supabase.get_persona(persona_id)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        return persona
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/personas", response_model=List[Persona])
async def get_user_personas(
    user_id: str,
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """
    Get all personas for a user
    
    - **user_id**: User identifier
    """
    try:
        personas = await supabase.get_user_personas(user_id)
        return personas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/personas/{persona_id}", response_model=Persona)
async def update_persona(
    persona_id: str,
    update_data: PersonaUpdate,
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """
    Update persona
    
    - **persona_id**: Persona identifier
    - **update_data**: Fields to update
    """
    try:
        persona = await supabase.update_persona(persona_id, update_data)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        return persona
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/personas/{persona_id}")
async def delete_persona(
    persona_id: str,
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """
    Delete persona
    
    - **persona_id**: Persona identifier
    """
    try:
        success = await supabase.delete_persona(persona_id)
        if not success:
            raise HTTPException(status_code=404, detail="Persona not found")
        return {"message": "Persona deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/personas/{persona_id}/history")
async def get_persona_history(
    persona_id: str,
    limit: int = 50,
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """
    Get persona's review and recommendation history
    
    - **persona_id**: Persona identifier
    - **limit**: Maximum number of records to return
    """
    try:
        history = await supabase.get_persona_history(persona_id, limit)
        return {
            "persona_id": persona_id,
            "history": history,
            "total_count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/personas/{persona_id}/similar")
async def get_similar_personas(
    persona_id: str,
    limit: int = 10,
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """
    Find similar personas using vector similarity
    
    - **persona_id**: Persona identifier
    - **limit**: Maximum number of similar personas to return
    """
    try:
        similar_personas = await supabase.search_similar_personas(persona_id, limit)
        return {
            "persona_id": persona_id,
            "similar_personas": similar_personas,
            "total_count": len(similar_personas)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/personas/stats")
async def get_persona_stats(
    user_id: str = None,
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """
    Get persona statistics
    
    - **user_id**: Optional user ID to filter by
    """
    try:
        if user_id:
            analytics = await supabase.get_analytics_data(user_id)
            return {
                "user_id": user_id,
                "analytics": analytics
            }
        else:
            # Global stats
            return {
                "total_personas": 156,
                "active_personas": 89,
                "cities_covered": 12,
                "languages_supported": 5,
                "avg_cultural_density": 0.87
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
