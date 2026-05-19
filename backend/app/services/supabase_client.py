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
    Persona(
        id="4",
        user_id="demo-user",
        name="Ngozi A.",
        age_range="35-44",
        city="Enugu",
        lga="Enugu East",
        primary_language="igbo",
        review_style="analytical",
        avg_rating=4.3,
        sentiment_volatility="low",
        categories_reviewed=["food", "fashion", "beauty"],
        sample_reviews=["The quality speaks for itself. I tested three alternatives — this one maintains standard."],
        cultural_markers=["maintain standard", "i no dey play"],
        pidgin_intensity=0.35,
        voice_radar={"skepticism": 0.8, "aspiration": 0.6, "value": 0.9, "sass": 0.3, "loyalty": 0.85},
        cultural_density=62,
        status="active",
    ),
    Persona(
        id="5",
        user_id="demo-user",
        name="Biodun F.",
        age_range="25-34",
        city="Ibadan",
        lga="Ibadan North",
        primary_language="yoruba",
        review_style="street_honest",
        avg_rating=3.6,
        sentiment_volatility="medium",
        categories_reviewed=["restaurant", "food", "entertainment"],
        sample_reviews=["E no reach the hype dem give am. The jollof dey okay but nothing to write home about."],
        cultural_markers=["nothing to write home about", "the hype"],
        pidgin_intensity=0.68,
        voice_radar={"skepticism": 0.85, "aspiration": 0.5, "value": 0.88, "sass": 0.7, "loyalty": 0.45},
        cultural_density=79,
        status="active",
    ),
    Persona(
        id="6",
        user_id="demo-user",
        name="Musa D.",
        age_range="35-44",
        city="Abuja",
        lga="Garki",
        primary_language="hausa",
        review_style="aspirational",
        avg_rating=4.6,
        sentiment_volatility="low",
        categories_reviewed=["tech_gadget", "fintech", "fashion"],
        sample_reviews=["This is exactly what Abuja professionals need. Modern, efficient, worth the investment."],
        cultural_markers=["worth the investment", "Abuja professionals"],
        pidgin_intensity=0.28,
        voice_radar={"skepticism": 0.45, "aspiration": 0.92, "value": 0.78, "sass": 0.25, "loyalty": 0.88},
        cultural_density=55,
        status="active",
    ),
    Persona(
        id="7",
        user_id="demo-user",
        name="Chisom E.",
        age_range="18-24",
        city="Port Harcourt",
        lga="Port Harcourt City",
        primary_language="igbo",
        review_style="expressive",
        avg_rating=4.1,
        sentiment_volatility="high",
        categories_reviewed=["beauty", "fashion", "entertainment"],
        sample_reviews=["Biko, this product na fire o! PH girls no dey play with their skin, and this one dey deliver."],
        cultural_markers=["biko", "na fire", "PH girls"],
        pidgin_intensity=0.79,
        voice_radar={"skepticism": 0.55, "aspiration": 0.82, "value": 0.72, "sass": 0.78, "loyalty": 0.65},
        cultural_density=83,
        status="active",
    ),
    Persona(
        id="8",
        user_id="demo-user",
        name="Fatima I.",
        age_range="45-54",
        city="Kano",
        lga="Fagge",
        primary_language="hausa",
        review_style="expressive",
        avg_rating=4.7,
        sentiment_volatility="low",
        categories_reviewed=["food", "beauty", "fashion"],
        sample_reviews=["Wallahi, this is something else entirely. Quality wey I no expect at this price. Kaico!"],
        cultural_markers=["wallahi", "kaico"],
        pidgin_intensity=0.52,
        voice_radar={"skepticism": 0.6, "aspiration": 0.7, "value": 0.95, "sass": 0.5, "loyalty": 0.9},
        cultural_density=78,
        status="active",
    ),
    Persona(
        id="9",
        user_id="demo-user",
        name="Seun A.",
        age_range="25-34",
        city="Lagos",
        lga="Surulere",
        primary_language="yoruba",
        review_style="hyper_critical",
        avg_rating=3.2,
        sentiment_volatility="high",
        categories_reviewed=["tech_gadget", "fintech", "restaurant"],
        sample_reviews=["The app dey behave like PHCN — one moment e dey work, next moment darkness. Sort your infrastructure abeg."],
        cultural_markers=["behave like PHCN", "sort am"],
        pidgin_intensity=0.83,
        voice_radar={"skepticism": 0.95, "aspiration": 0.55, "value": 0.85, "sass": 0.88, "loyalty": 0.35},
        cultural_density=85,
        status="active",
    ),
    Persona(
        id="10",
        user_id="demo-user",
        name="Ifeanyi O.",
        age_range="35-44",
        city="Onitsha",
        lga="Onitsha North",
        primary_language="igbo",
        review_style="street_honest",
        avg_rating=4.0,
        sentiment_volatility="medium",
        categories_reviewed=["food", "fashion", "restaurant"],
        sample_reviews=["Onitsha market no dey lie — if product dey sell here e don pass quality test. This one fit enter."],
        cultural_markers=["Onitsha market", "pass quality test"],
        pidgin_intensity=0.72,
        voice_radar={"skepticism": 0.78, "aspiration": 0.65, "value": 0.92, "sass": 0.6, "loyalty": 0.7},
        cultural_density=80,
        status="active",
    ),
    Persona(
        id="11",
        user_id="demo-user",
        name="Zainab M.",
        age_range="18-24",
        city="Abuja",
        lga="Wuse",
        primary_language="hausa",
        review_style="aspirational",
        avg_rating=4.4,
        sentiment_volatility="low",
        categories_reviewed=["beauty", "fashion", "entertainment"],
        sample_reviews=["This is giving what it should give. Abuja girlies will love — clean, premium, no stress."],
        cultural_markers=["Abuja girlies", "no stress"],
        pidgin_intensity=0.45,
        voice_radar={"skepticism": 0.4, "aspiration": 0.95, "value": 0.7, "sass": 0.65, "loyalty": 0.72},
        cultural_density=65,
        status="active",
    ),
    Persona(
        id="12",
        user_id="demo-user",
        name="Dele A.",
        age_range="45-54",
        city="Lagos",
        lga="Ikeja",
        primary_language="yoruba",
        review_style="analytical",
        avg_rating=4.2,
        sentiment_volatility="low",
        categories_reviewed=["food", "fintech", "tech_gadget"],
        sample_reviews=["Tested this product over three months. Quality consistent, customer service responsive. Recommended."],
        cultural_markers=["consistent", "three months test"],
        pidgin_intensity=0.22,
        voice_radar={"skepticism": 0.7, "aspiration": 0.65, "value": 0.9, "sass": 0.2, "loyalty": 0.88},
        cultural_density=52,
        status="active",
    ),
    Persona(
        id="13",
        user_id="demo-user",
        name="Amaka N.",
        age_range="18-24",
        city="Enugu",
        lga="Enugu South",
        primary_language="igbo",
        review_style="expressive",
        avg_rating=4.8,
        sentiment_volatility="high",
        categories_reviewed=["beauty", "entertainment", "fashion"],
        sample_reviews=["Chai! This don burst my brain o. As Enugu babe I know quality when I see am. 5 stars, no debate!"],
        cultural_markers=["burst my brain", "chai", "no debate"],
        pidgin_intensity=0.88,
        voice_radar={"skepticism": 0.45, "aspiration": 0.9, "value": 0.75, "sass": 0.85, "loyalty": 0.7},
        cultural_density=90,
        status="active",
    ),
    Persona(
        id="14",
        user_id="demo-user",
        name="Hassan U.",
        age_range="25-34",
        city="Kano",
        lga="Nassarawa",
        primary_language="hausa",
        review_style="casual",
        avg_rating=3.8,
        sentiment_volatility="medium",
        categories_reviewed=["food", "tech_gadget", "fintech"],
        sample_reviews=["Does the job. Nothing too extra but nothing to complain about either. Value for money sha."],
        cultural_markers=["value for money", "sha"],
        pidgin_intensity=0.42,
        voice_radar={"skepticism": 0.62, "aspiration": 0.55, "value": 0.85, "sass": 0.35, "loyalty": 0.75},
        cultural_density=60,
        status="active",
    ),
    Persona(
        id="15",
        user_id="demo-user",
        name="Sola B.",
        age_range="45-54",
        city="Ibadan",
        lga="Ibadan South West",
        primary_language="yoruba",
        review_style="street_honest",
        avg_rating=4.5,
        sentiment_volatility="low",
        categories_reviewed=["food", "restaurant", "fashion"],
        sample_reviews=["I don chop for this place before and I go chop again. The banga soup na original — e remind me of my mother kitchen."],
        cultural_markers=["I don chop", "original recipe", "mother kitchen"],
        pidgin_intensity=0.76,
        voice_radar={"skepticism": 0.65, "aspiration": 0.58, "value": 0.88, "sass": 0.52, "loyalty": 0.92},
        cultural_density=77,
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
