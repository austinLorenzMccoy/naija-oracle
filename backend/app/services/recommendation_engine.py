"""
Recommendation Engine Agent (Task B)
Hyper-personalised recommendations with Nigerian context
"""

import time
import uuid
import numpy as np
from typing import Dict, List, Optional, Any, Tuple

from app.services.groq_client import GroqClient
from app.services.supabase_client import SupabaseClient
from app.services.embedding_service import EmbeddingService
from app.models.recommendation import (
    RecommendationRequest, RecommendationResponse, RecommendationGeneration,
    RecommendationItem, RecommendationStream, TurnHistory
)
from app.models.persona import Persona
from app.config import settings

class RecommendationEngine:
    """Task B Agent: Recommendation Engine with contextual reasoning"""
    
    def __init__(self, groq_client: GroqClient, supabase: SupabaseClient, embeddings: EmbeddingService):
        self.groq = groq_client
        self.supabase = supabase
        self.embeddings = embeddings
        self.catalog = self._load_product_catalog()
    
    def _load_product_catalog(self) -> List[Dict[str, Any]]:
        """Load sample product catalog for recommendations"""
        return [
            # Food/Restaurants
            {
                "item_id": "res_yellow_chilli",
                "name": "Yellow Chilli Restaurant",
                "category": "Nigerian fine dining",
                "location": "Victoria Island, Lagos",
                "price_tier": "premium",
                "avg_rating": 4.4,
                "price_range": (8000, 15000),
                "features": ["Live music", "Outdoor seating", "Full bar", "African fusion"],
                "description": "Upscale Nigerian restaurant with modern fusion dishes"
            },
            {
                "item_id": "res_bucket",
                "name": "Bucket Restaurant",
                "category": "Casual dining",
                "location": "Lekki Phase 1, Lagos",
                "price_tier": "mid",
                "avg_rating": 4.1,
                "price_range": (3000, 7000),
                "features": ["Family friendly", "Local cuisine", "Quick service"],
                "description": "Popular spot for authentic Nigerian dishes"
            },
            {
                "item_id": "res_suya_spot",
                "name": "Mama T's Suya Spot",
                "category": "Street food",
                "location": "Surulere, Lagos",
                "price_tier": "budget",
                "avg_rating": 4.6,
                "price_range": (500, 2000),
                "features": ["Late night", "Takeaway", "Authentic suya"],
                "description": "Legendary suya joint with secret spices"
            },
            # Entertainment
            {
                "item_id": "ent_afrika_shrine",
                "name": "New Afrika Shrine",
                "category": "Music venue",
                "location": "Ikeja, Lagos",
                "price_tier": "mid",
                "avg_rating": 4.7,
                "price_range": (2000, 5000),
                "features": ["Live music", "Cultural performances", "Outdoor"],
                "description": "Fela Kuti's legendary music venue"
            },
            {
                "item_id": "ent_cinema",
                "name": "Filmhouse Cinemas",
                "category": "Movie theater",
                "location": "Ikeja City Mall, Lagos",
                "price_tier": "mid",
                "avg_rating": 4.2,
                "price_range": (1500, 3000),
                "features": ["Latest movies", "Comfortable seating", "Snacks"],
                "description": "Modern cinema complex"
            },
            # Fashion
            {
                "item_id": "fash_lagos_fashion",
                "name": "Lagos Fashion Hub",
                "category": "Boutique",
                "location": "Victoria Island, Lagos",
                "price_tier": "premium",
                "avg_rating": 4.3,
                "price_range": (10000, 50000),
                "features": ["Designer wear", "Custom tailoring", "Accessories"],
                "description": "Contemporary Nigerian fashion boutique"
            },
            # Fintech
            {
                "item_id": "fint_kuda_bank",
                "name": "Kuda Bank",
                "category": "Digital banking",
                "location": "Online",
                "price_tier": "free",
                "avg_rating": 4.0,
                "price_range": (0, 0),
                "features": ["No fees", "Instant transfers", "Savings goals"],
                "description": "Digital-first banking app"
            }
        ]
    
    async def generate_recommendations(self, request: RecommendationRequest) -> RecommendationResponse:
        """Generate personalized recommendations"""
        start_time = time.time()
        
        try:
            # Get persona data
            persona = await self.supabase.get_persona(request.persona_id)
            if not persona:
                return RecommendationResponse(
                    success=False,
                    error=f"Persona {request.persona_id} not found",
                    request_id=str(uuid.uuid4())
                )
            
            # Execute R4 pipeline
            reasoning_result = await self._reason_about_request(persona, request)
            retrieval_result = await self._retrieve_candidates(persona, request, reasoning_result)
            ranking_result = await self._rank_recommendations(persona, request, retrieval_result)
            ranked_recommendations = ranking_result["recommendations"]
            refined_result = await self._refine_with_context(persona, request, ranked_recommendations)
            
            # Generate explanation
            explanation = await self._generate_explanation(persona, request, refined_result)
            
            # Calculate metrics
            ndcg_score = await self._calculate_ndcg(refined_result[:request.max_recommendations])
            hit_rate = await self._calculate_hit_rate(refined_result[:5])
            
            generation_time = int((time.time() - start_time) * 1000)
            
            # Create recommendation items
            items = []
            for i, rec in enumerate(refined_result[:request.max_recommendations]):
                item = RecommendationItem(
                    item_id=rec["item_id"],
                    name=rec["name"],
                    category=rec["category"],
                    location=rec["location"],
                    description=rec.get("description"),
                    price_tier=rec["price_tier"],
                    predicted_rating=rec["predicted_rating"],
                    context_score=rec["context_score"],
                    reasoning=rec["reasoning"],
                    distance_km=rec.get("distance_km"),
                    price_range_naira=rec.get("price_range"),
                    features=rec.get("features", []),
                    images=rec.get("images", [])
                )
                items.append(item)
            
            # Generate next turn prompt
            next_prompt = await self._generate_next_turn_prompt(persona, request, items)
            
            # Create response
            recommendation_gen = RecommendationGeneration(
                recommendations=items,
                explanation=explanation,
                next_turn_prompt=next_prompt,
                cold_start_used=request.cold_start,
                ndcg_at_10=ndcg_score,
                hit_rate_at_5=hit_rate,
                reasoning_trace=reasoning_result["trace"],
                context_boost_factors=ranking_result["boost_factors"],
                generation_time_ms=generation_time,
                model_used=settings.GROQ_MODEL,
                temperature_used=request.temperature
            )
            
            # Store interaction
            await self._store_interaction(request, recommendation_gen)
            
            return RecommendationResponse(
                success=True,
                data=recommendation_gen,
                request_id=str(uuid.uuid4())
            )
            
        except Exception as e:
            return RecommendationResponse(
                success=False,
                error=str(e),
                request_id=str(uuid.uuid4())
            )
    
    async def _reason_about_request(self, persona: Persona, request: RecommendationRequest) -> Dict[str, Any]:
        """R4 Step 1: Reason about user intent and constraints"""
        
        reasoning_trace = []
        
        # Analyze user context
        context = request.context
        
        # Time-based reasoning
        time_reasoning = f"Time: {context.current_time}"
        if "evening" in context.current_time.lower() or "night" in context.current_time.lower():
            time_reasoning += " → Focus on dinner, entertainment, late-night options"
        elif "morning" in context.current_time.lower():
            time_reasoning += " → Focus on breakfast, early activities"
        reasoning_trace.append(time_reasoning)
        
        # Location reasoning
        location_reasoning = f"Location: {context.location}"
        if "lagos" in context.location.lower():
            location_reasoning += " → Consider traffic, island/mainland dynamics"
        reasoning_trace.append(location_reasoning)
        
        # Budget reasoning
        budget_reasoning = f"Budget: ₦{context.budget_naira or 'unspecified'}"
        if context.budget_naira:
            if context.budget_naira < 2000:
                budget_reasoning += " → Budget-friendly options only"
            elif context.budget_naira < 8000:
                budget_reasoning += " → Mid-range options"
            else:
                budget_reasoning += " → Premium options available"
        reasoning_trace.append(budget_reasoning)
        
        # Mood reasoning
        mood_reasoning = f"Mood: {context.mood_signal}"
        mood_mapping = {
            "celebratory": " → Upscale, lively venues, group activities",
            "casual": " → Relaxed, comfortable, value for money",
            "romantic": " → Intimate settings, quality experiences",
            "professional": " → Appropriate for business meetings"
        }
        budget_reasoning += mood_mapping.get(context.mood_signal, "")
        reasoning_trace.append(mood_reasoning)
        
        # Persona preferences
        persona_reasoning = f"Persona: {persona.name} from {persona.city}"
        persona_reasoning += f" → Avg rating: {persona.avg_rating}, Style: {persona.review_style}"
        reasoning_trace.append(persona_reasoning)
        
        return {
            "trace": reasoning_trace,
            "intent": "general_recommendation",
            "constraints": {
                "location": context.location,
                "budget": context.budget_naira,
                "time": context.current_time,
                "mood": context.mood_signal
            }
        }
    
    async def _retrieve_candidates(
        self, 
        persona: Persona, 
        request: RecommendationRequest, 
        reasoning: Dict[str, Any]
    ) -> Dict[str, Any]:
        """R4 Step 2: Retrieve candidate recommendations"""
        
        candidates = []
        
        # Filter by domain
        domain_mapping = {
            "food": ["Nigerian fine dining", "Casual dining", "Street food"],
            "entertainment": ["Music venue", "Movie theater"],
            "fashion": ["Boutique"],
            "fintech": ["Digital banking"]
        }
        
        valid_categories = domain_mapping.get(request.domain.value, [])
        
        for item in self.catalog:
            # Domain filter
            if valid_categories and item["category"] not in valid_categories:
                continue
            
            # Budget filter
            if request.context.budget_naira and item["price_range"][1] > request.context.budget_naira:
                continue
            
            # Location preference (simplified)
            if "lagos" in request.context.location.lower() and "lagos" not in item["location"].lower():
                continue
            
            # Add to candidates with base score
            candidate = item.copy()
            candidate["base_score"] = item["avg_rating"] / 5.0
            candidates.append(candidate)
        
        # Collaborative filtering simulation
        # In real implementation, this would use user similarity
        for candidate in candidates:
            # Boost based on persona preferences
            if persona.avg_rating >= 4.0 and candidate["avg_rating"] >= 4.0:
                candidate["collab_boost"] = 0.2
            elif persona.avg_rating <= 3.0 and candidate["avg_rating"] <= 3.5:
                candidate["collab_boost"] = 0.15
            else:
                candidate["collab_boost"] = 0.0
        
        return candidates
    
    async def _rank_recommendations(
        self, 
        persona: Persona, 
        request: RecommendationRequest, 
        candidates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """R4 Step 3: Rank candidates with contextual boosting"""
        
        boost_factors = {}
        
        for candidate in candidates:
            score = candidate["base_score"] + candidate.get("collab_boost", 0)
            
            # Contextual boosts
            context_boosts = 0.0
            
            # Mood boost
            mood_boosts = {
                "celebratory": {"premium": 0.3, "mid": 0.1},
                "casual": {"mid": 0.2, "budget": 0.15},
                "romantic": {"premium": 0.25}
            }
            
            mood_boost = mood_boosts.get(request.context.mood_signal, {})
            context_boosts += mood_boost.get(candidate["price_tier"], 0)
            
            # Time boost
            if "night" in request.context.current_time.lower():
                if "late night" in candidate.get("features", []):
                    context_boosts += 0.2
            
            # Location boost (simplified distance simulation)
            if "lagos" in request.context.location.lower():
                if "Victoria Island" in candidate["location"] and "lekki" in request.context.location.lower():
                    context_boosts += 0.15
                elif "Surulere" in candidate["location"] and "surulere" in request.context.location.lower():
                    context_boosts += 0.2
            
            # Persona alignment boost
            if persona.avg_rating >= 4.0 and candidate["avg_rating"] >= 4.0:
                context_boosts += 0.1
            
            candidate["context_score"] = min(1.0, score + context_boosts)
            candidate["context_boost"] = context_boosts
            candidate["predicted_rating"] = candidate["avg_rating"]
            
            # Generate reasoning
            candidate["reasoning"] = await self._generate_item_reasoning(
                persona, request, candidate
            )
        
        # Sort by context score
        candidates.sort(key=lambda x: x["context_score"], reverse=True)
        
        boost_factors = {
            "mood_boost": max(mood_boosts.get(request.context.mood_signal, {}).values(), default=0.0),
            "time_boost": 0.1 if "night" in request.context.current_time.lower() else 0.0,
            "location_boost": 0.15 if "lagos" in request.context.location.lower() else 0.0
        }
        
        return {
            "recommendations": candidates[:20],
            "boost_factors": boost_factors,
        }
    
    async def _refine_with_context(
        self, 
        persona: Persona, 
        request: RecommendationRequest, 
        ranked: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """R4 Step 4: Refine with multi-turn context"""
        
        refined = ranked.copy()
        
        # Apply conversation history adjustments
        if request.turn_history:
            recent_feedback = request.turn_history[-1].user_feedback.lower() if request.turn_history[-1].user_feedback else ""
            
            # Adjust based on user feedback
            if "expensive" in recent_feedback:
                for item in refined:
                    if item["price_tier"] == "premium":
                        item["context_score"] -= 0.2
                    elif item["price_tier"] == "budget":
                        item["context_score"] += 0.1
            
            elif "far" in recent_feedback or "distance" in recent_feedback:
                # Prioritize closer locations (simplified)
                for item in refined:
                    if "ikeja" in item["location"].lower() and "ikeja" in request.context.location.lower():
                        item["context_score"] += 0.15
            
            # Re-sort after adjustments
            refined.sort(key=lambda x: x["context_score"], reverse=True)
        
        return refined
    
    async def _generate_item_reasoning(
        self, 
        persona: Persona, 
        request: RecommendationRequest, 
        item: Dict[str, Any]
    ) -> str:
        """Generate reasoning for individual recommendation"""
        
        reasoning_parts = []
        
        # Location relevance
        if "lagos" in request.context.location.lower() and "lagos" in item["location"].lower():
            reasoning_parts.append(f"Matches your {request.context.location} location")
        
        # Mood alignment
        mood_mapping = {
            "celebratory": "perfect for celebration",
            "casual": "great for casual outing",
            "romantic": "ideal for romantic experience",
            "professional": "suitable for professional setting"
        }
        if request.context.mood_signal in mood_mapping:
            reasoning_parts.append(mood_mapping[request.context.mood_signal])
        
        # Rating alignment
        if abs(item["avg_rating"] - persona.avg_rating) <= 0.5:
            reasoning_parts.append("matches your rating preferences")
        
        # Budget fit
        if request.context.budget_naira:
            if item["price_range"][1] <= request.context.budget_naira:
                reasoning_parts.append("fits your budget")
        
        return " | ".join(reasoning_parts) if reasoning_parts else "Recommended based on your preferences"
    
    async def _generate_explanation(
        self, 
        persona: Persona, 
        request: RecommendationRequest, 
        recommendations: List[Dict[str, Any]]
    ) -> str:
        """Generate overall explanation for recommendations"""
        
        explanation_parts = []
        
        # Context summary
        explanation_parts.append(f"Based on your location in {request.context.location}")
        
        if request.context.mood_signal:
            explanation_parts.append(f"and {request.context.mood_signal} mood")
        
        if request.context.budget_naira:
            explanation_parts.append(f"with ₦{request.context.budget_naira} budget")
        
        # Personalization note
        explanation_parts.append(f"I've selected options that match your {persona.review_style} style")
        
        # Top recommendation highlight
        if recommendations:
            top_rec = recommendations[0]
            explanation_parts.append(f"Top pick: {top_rec['name']} ({top_rec['avg_rating']}⭐)")
        
        return ", ".join(explanation_parts) + "."
    
    async def _generate_next_turn_prompt(
        self, 
        persona: Persona, 
        request: RecommendationRequest, 
        items: List[RecommendationItem]
    ) -> Optional[str]:
        """Generate prompt for next conversation turn"""
        
        if not items:
            return "Would you like me to search for something different?"
        
        # Contextual follow-up suggestions
        prompts = []
        
        # Budget-based
        if request.context.budget_naira and request.context.budget_naira > 5000:
            prompts.append("Want to see more premium options?")
        elif request.context.budget_naira and request.context.budget_naira < 3000:
            prompts.append("Need more budget-friendly choices?")
        
        # Location-based
        if "lagos" in request.context.location.lower():
            prompts.append("Prefer island or mainland locations?")
        
        # Feature-based
        if any("live music" in item.features for item in items):
            prompts.append("Interested in places with live music?")
        
        # Generic fallback
        if not prompts:
            prompts.append("Would you like more details about any of these?")
        
        return prompts[0]
    
    async def _calculate_ndcg(self, recommendations: List[Dict[str, Any]]) -> float:
        """Calculate NDCG@10 for recommendations"""
        if not recommendations:
            return 0.0
        
        # Simplified NDCG calculation
        # In real implementation, this would compare against ground truth
        relevance_scores = [rec["context_score"] for rec in recommendations[:10]]
        
        # DCG calculation
        dcg = sum(score / (i + 1) for i, score in enumerate(relevance_scores))
        
        # IDCG (ideal DCG) - assume perfect ranking
        ideal_scores = sorted(relevance_scores, reverse=True)
        idcg = sum(score / (i + 1) for i, score in enumerate(ideal_scores))
        
        return dcg / idcg if idcg > 0 else 0.0
    
    async def _calculate_hit_rate(self, recommendations: List[Dict[str, Any]]) -> float:
        """Calculate Hit Rate @5"""
        if not recommendations:
            return 0.0
        
        # Simplified hit rate - count items with score > 0.7
        hits = sum(1 for rec in recommendations[:5] if rec["context_score"] > 0.7)
        return hits / min(5, len(recommendations))
    
    async def _store_interaction(self, request: RecommendationRequest, generation: RecommendationGeneration):
        """Store recommendation interaction for analytics"""
        try:
            await self.supabase.store_recommendation_interaction(
                user_id=request.user_id,
                persona_id=request.persona_id,
                request=request.dict(),
                response=generation.dict()
            )
        except Exception as e:
            print(f"Failed to store recommendation interaction: {e}")
