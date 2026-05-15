"""
Router for Persona management
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from uuid import UUID

from app.models.persona import Persona, PersonaCreate, PersonaUpdate
from app.services.supabase_client import SupabaseClient

router = APIRouter()

DEMO_PERSONAS = [
    Persona(
        id="1",
        user_id="demo-user",
        name="Emeka O.",
        age_range="25-34",
        city="Lagos",
        lga="Eti-Osa",
        primary_language="igbo",
        review_style="expressive",
        avg_rating=4.2,
        sentiment_volatility="medium",
        categories_reviewed=["tech_gadget", "fintech", "restaurant"],
        sample_reviews=[
            "The speed dey sharp sharp, but price high like NEPA restoring light.",
            "Everything set finish, clean design."
        ],
        cultural_markers=["sharp sharp", "NEPA", "fall hand"],
        pidgin_intensity=0.82,
        voice_radar={"skepticism": 0.72, "aspiration": 0.88, "value": 0.76, "sass": 0.68, "loyalty": 0.64},
        cultural_density=88,
        status="active_oracle",
    ),
    Persona(
        id="2",
        user_id="demo-user",
        name="Aisha H.",
        age_range="25-34",
        city="Kano",
        lga="Tarauni",
        primary_language="hausa",
        review_style="analytical",
        avg_rating=4.5,
        sentiment_volatility="low",
        categories_reviewed=["fashion", "beauty", "food"],
        sample_reviews=["Quality dey, but delivery timing needs discipline."],
        cultural_markers=["quality dey", "timing"],
        pidgin_intensity=0.55,
        voice_radar={"skepticism": 0.58, "aspiration": 0.74, "value": 0.82, "sass": 0.42, "loyalty": 0.79},
        cultural_density=86,
        status="active",
    ),
    Persona(
        id="3",
        user_id="demo-user",
        name="Tunde B.",
        age_range="18-24",
        city="Lagos",
        lga="Yaba",
        primary_language="yoruba",
        review_style="casual",
        avg_rating=3.9,
        sentiment_volatility="high",
        categories_reviewed=["tech_gadget", "entertainment", "fintech"],
        sample_reviews=["App clean, but the onboarding stress no make sense."],
        cultural_markers=["no make sense", "clean"],
        pidgin_intensity=0.75,
        voice_radar={"skepticism": 0.8, "aspiration": 0.66, "value": 0.7, "sass": 0.73, "loyalty": 0.52},
        cultural_density=75,
        status="active",
    ),
]

DEMO_PERSONA_BY_ID = {persona.id: persona for persona in DEMO_PERSONAS}

# Dependency injection — returns None gracefully when Supabase env vars are absent
def get_supabase_client() -> Optional[SupabaseClient]:
    try:
        return SupabaseClient()
    except Exception:
        return None

# ============================================================================
# ROUTE ORDER MATTERS IN FASTAPI!
# More specific routes must come BEFORE more general ones
# ============================================================================

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

# SPECIFIC ROUTES (must come BEFORE generic {id} routes)
@router.get("/personas/stats")
async def get_persona_stats(
    user_id: str = None,
    supabase: Optional[SupabaseClient] = Depends(get_supabase_client)
):
    """Get persona statistics"""
    try:
        if user_id and supabase:
            analytics = await supabase.get_analytics_data(user_id)
            return {"user_id": user_id, "analytics": analytics}
        # Global demo stats — always available
        return {
            "total_personas": 156,
            "active_personas": 89,
            "cities_covered": 12,
            "languages_supported": 5,
            "avg_cultural_density": 0.87,
        }
    except Exception as e:
        # Return demo stats rather than 500 so the dashboard never breaks
        return {
            "total_personas": 156,
            "active_personas": 89,
            "cities_covered": 12,
            "languages_supported": 5,
            "avg_cultural_density": 0.87,
        }

@router.get("/personas", response_model=List[Persona])
async def get_user_personas(
    user_id: str = "demo-user",
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """
    Get all personas for a user
    
    - **user_id**: User identifier
    """
    try:
        personas = await supabase.get_user_personas(user_id)
        return personas or (DEMO_PERSONAS if user_id == "demo-user" else [])
    except Exception as e:
        if user_id == "demo-user":
            return DEMO_PERSONAS
        raise HTTPException(status_code=500, detail=str(e))

# NESTED ROUTES (must come BEFORE generic {persona_id} route)
@router.get("/personas/{persona_id}/history")
async def get_persona_history(
    persona_id: str,
    limit: int = 50,
    supabase: Optional[SupabaseClient] = Depends(get_supabase_client)
):
    """Get persona review and recommendation history"""
    try:
        history = await supabase.get_persona_history(persona_id, limit) if supabase else []
        return {"persona_id": persona_id, "history": history or [], "total_count": len(history or [])}
    except Exception:
        return {"persona_id": persona_id, "history": [], "total_count": 0}

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

# GENERIC ROUTES (come AFTER specific ones)
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
        if persona_id in DEMO_PERSONA_BY_ID:
            return DEMO_PERSONA_BY_ID[persona_id]

        try:
            UUID(persona_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="Persona not found")

        persona = await supabase.get_persona(persona_id)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        return persona
    except HTTPException:
        raise
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
