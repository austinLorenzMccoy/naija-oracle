"""
Supabase client for database operations and real-time features
"""

import os
from typing import Dict, List, Optional, Any
from uuid import UUID
from supabase import create_client, Client
from postgrest import APIResponse

from app.config import settings
from app.models.persona import Persona, PersonaCreate, PersonaUpdate
from app.models.review import ReviewGeneration
from app.models.recommendation import RecommendationGeneration

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

class SupabaseClient:
    """Client for Supabase database and real-time operations"""
    
    def __init__(self):
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
            raise ValueError("Supabase URL and service key are required")
        
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_KEY
        )
        self.url = settings.SUPABASE_URL
        self.service_key = settings.SUPABASE_SERVICE_KEY
    
    async def create_persona(self, persona_data: PersonaCreate) -> Persona:
        """Create a new persona"""
        try:
            response = self.client.table("personas").insert({
                "user_id": persona_data.user_id,
                "name": persona_data.name,
                "age_range": persona_data.age_range,
                "city": persona_data.city,
                "lga": persona_data.lga,
                "primary_language": persona_data.primary_language.value,
                "review_style": persona_data.review_style.value,
                "avg_rating": persona_data.avg_rating,
                "sentiment_volatility": persona_data.sentiment_volatility,
                "categories_reviewed": persona_data.categories_reviewed,
                "sample_reviews": persona_data.sample_reviews,
                "cultural_markers": persona_data.cultural_markers,
                "pidgin_intensity": persona_data.pidgin_intensity,
                "status": "active"
            }).execute()
            
            if response.data:
                return Persona(**response.data[0])
            else:
                raise Exception("Failed to create persona")
                
        except Exception as e:
            raise Exception(f"Database error creating persona: {str(e)}")
    
    async def get_persona(self, persona_id: str) -> Optional[Persona]:
        """Get persona by ID"""
        try:
            if persona_id in DEMO_PERSONA_BY_ID:
                return DEMO_PERSONA_BY_ID[persona_id]

            try:
                UUID(persona_id)
            except ValueError:
                return None

            response = self.client.table("personas").select("*").eq("id", persona_id).execute()
            
            if response.data:
                return Persona(**response.data[0])
            return None
            
        except Exception as e:
            raise Exception(f"Database error getting persona: {str(e)}")
    
    async def get_user_personas(self, user_id: str) -> List[Persona]:
        """Get all personas for a user"""
        try:
            response = self.client.table("personas").select("*").eq("user_id", user_id).execute()

            personas = [Persona(**item) for item in response.data] if response.data else []
            if user_id == "demo-user" and len(personas) < len(DEMO_PERSONAS):
                existing_ids = {persona.id for persona in personas}
                personas.extend(persona for persona in DEMO_PERSONAS if persona.id not in existing_ids)
            return personas
            
        except Exception as e:
            if user_id == "demo-user":
                return DEMO_PERSONAS
            raise Exception(f"Database error getting user personas: {str(e)}")
    
    async def update_persona(self, persona_id: str, update_data: PersonaUpdate) -> Optional[Persona]:
        """Update persona"""
        try:
            # Convert enum values to strings for database
            update_dict = update_data.dict(exclude_unset=True)
            
            # Handle enum conversions
            if "primary_language" in update_dict:
                update_dict["primary_language"] = update_dict["primary_language"].value
            if "review_style" in update_dict:
                update_dict["review_style"] = update_dict["review_style"].value
            if "status" in update_dict:
                update_dict["status"] = update_dict["status"].value
            
            response = self.client.table("personas").update(update_dict).eq("id", persona_id).execute()
            
            if response.data:
                return Persona(**response.data[0])
            return None
            
        except Exception as e:
            raise Exception(f"Database error updating persona: {str(e)}")
    
    async def delete_persona(self, persona_id: str) -> bool:
        """Delete persona"""
        try:
            response = self.client.table("personas").delete().eq("id", persona_id).execute()
            return len(response.data) > 0 if response.data else False
            
        except Exception as e:
            raise Exception(f"Database error deleting persona: {str(e)}")
    
    async def store_review_generation(
        self,
        user_id: str,
        persona_id: str,
        product: Dict[str, Any],
        context: Dict[str, Any],
        generation: Dict[str, Any]
    ) -> bool:
        """Store review generation for analytics"""
        try:
            self.client.table("review_generations").insert({
                "user_id": user_id,
                "persona_id": persona_id,
                "product": product,
                "context": context,
                "generation": generation,
                "created_at": "now()"
            }).execute()
            return True
            
        except Exception as e:
            print(f"Failed to store review generation: {e}")
            return False
    
    async def store_recommendation_interaction(
        self,
        user_id: str,
        persona_id: str,
        request: Dict[str, Any],
        response: Dict[str, Any]
    ) -> bool:
        """Store recommendation interaction"""
        try:
            self.client.table("recommendation_interactions").insert({
                "user_id": user_id,
                "persona_id": persona_id,
                "request": request,
                "response": response,
                "created_at": "now()"
            }).execute()
            return True
            
        except Exception as e:
            print(f"Failed to store recommendation interaction: {e}")
            return False
    
    async def get_persona_history(self, persona_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get persona's review and recommendation history"""
        try:
            # Get review generations
            reviews_response = self.client.table("review_generations")\
                .select("*")\
                .eq("persona_id", persona_id)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            
            # Get recommendation interactions
            recs_response = self.client.table("recommendation_interactions")\
                .select("*")\
                .eq("persona_id", persona_id)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            
            history = []
            
            if reviews_response.data:
                for item in reviews_response.data:
                    history.append({
                        "type": "review",
                        "data": item,
                        "created_at": item["created_at"]
                    })
            
            if recs_response.data:
                for item in recs_response.data:
                    history.append({
                        "type": "recommendation",
                        "data": item,
                        "created_at": item["created_at"]
                    })
            
            # Sort by date
            history.sort(key=lambda x: x["created_at"], reverse=True)
            return history[:limit]
            
        except Exception as e:
            raise Exception(f"Database error getting persona history: {str(e)}")
    
    async def search_similar_personas(
        self,
        persona_id: str,
        limit: int = 10
    ) -> List[Persona]:
        """Find similar personas using vector similarity"""
        try:
            # This would use pgvector for similarity search
            # For now, return personas from same city
            persona = await self.get_persona(persona_id)
            if not persona:
                return []
            
            response = self.client.table("personas")\
                .select("*")\
                .eq("city", persona.city)\
                .neq("id", persona_id)\
                .limit(limit)\
                .execute()
            
            return [Persona(**item) for item in response.data] if response.data else []
            
        except Exception as e:
            raise Exception(f"Database error searching similar personas: {str(e)}")
    
    async def get_analytics_data(self, user_id: str) -> Dict[str, Any]:
        """Get analytics data for dashboard"""
        try:
            # Count personas
            personas_response = self.client.table("personas")\
                .select("id")\
                .eq("user_id", user_id)\
                .execute()
            
            persona_count = len(personas_response.data) if personas_response.data else 0
            
            # Count review generations
            reviews_response = self.client.table("review_generations")\
                .select("id")\
                .eq("user_id", user_id)\
                .execute()
            
            review_count = len(reviews_response.data) if reviews_response.data else 0
            
            # Count recommendation interactions
            recs_response = self.client.table("recommendation_interactions")\
                .select("id")\
                .eq("user_id", user_id)\
                .execute()
            
            rec_count = len(recs_response.data) if recs_response.data else 0
            
            # Get recent activity
            recent_response = self.client.table("review_generations")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .limit(5)\
                .execute()
            
            recent_activity = recent_response.data if recent_response.data else []
            
            return {
                "persona_count": persona_count,
                "review_count": review_count,
                "recommendation_count": rec_count,
                "recent_activity": recent_activity
            }
            
        except Exception as e:
            raise Exception(f"Database error getting analytics: {str(e)}")
    
    async def create_user_session(self, user_data: Dict[str, Any]) -> str:
        """Create user session (simplified)"""
        try:
            response = self.client.table("user_sessions").insert({
                "user_data": user_data,
                "created_at": "now()"
            }).execute()
            
            if response.data:
                return response.data[0]["id"]
            else:
                raise Exception("Failed to create session")
                
        except Exception as e:
            raise Exception(f"Database error creating session: {str(e)}")
    
    async def broadcast_realtime_update(self, channel: str, payload: Dict[str, Any]):
        """Broadcast real-time update"""
        try:
            # This would use Supabase Realtime
            # For now, just log the update
            print(f"Broadcasting to {channel}: {payload}")
            
        except Exception as e:
            print(f"Failed to broadcast update: {e}")
    
    async def test_connection(self) -> bool:
        """Test database connection"""
        try:
            response = self.client.table("personas").select("count").execute()
            return True
        except Exception:
            return False
