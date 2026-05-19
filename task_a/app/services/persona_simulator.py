"""
Persona Simulator Agent (Task A)
Generates authentic Nigerian consumer reviews with cultural voice
"""

import time
import uuid
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import numpy as np

from app.services.groq_client import GroqClient
from app.services.cultural_voice_index import CulturalVoiceIndex
from app.services.supabase_client import SupabaseClient
from app.models.review import (
    ReviewRequest, ReviewResponse, ReviewGeneration, 
    VoiceProfile, ReviewStream
)
from app.models.persona import Persona
from app.config import settings

class PersonaSimulator:
    """Task A Agent: Persona Simulator for authentic Nigerian reviews"""
    
    def __init__(self, groq_client: GroqClient, cvi: CulturalVoiceIndex, supabase: SupabaseClient):
        self.groq = groq_client
        self.cvi = cvi
        self.supabase = supabase
        self.model_path = Path("models/persona_simulator/model.pth")
        self.use_trained_model = self.model_path.exists()
    
    async def generate_review(self, request: ReviewRequest) -> ReviewResponse:
        """Generate an authentic Nigerian review"""
        start_time = time.time()
        
        try:
            # Get persona data
            persona = await self.supabase.get_persona(request.persona_id)
            if not persona:
                return ReviewResponse(
                    success=False,
                    error=f"Persona {request.persona_id} not found",
                    request_id=str(uuid.uuid4())
                )
            
            # Get CVI anchors for this persona
            cvi_anchors = await self.cvi.get_persona_anchors(
                persona.city,
                persona.primary_language,
                persona.pidgin_intensity,
                request.product.category
            )
            
            review_text = await self._generate_local_review(persona, cvi_anchors, request)
            
            # Predict rating based on sentiment and persona patterns
            predicted_rating = await self._predict_rating(
                persona, review_text, cvi_anchors
            )
            
            # Calculate confidence interval
            confidence_interval = await self._calculate_confidence_interval(
                persona, predicted_rating
            )
            
            # Create voice profile
            voice_profile = await self._create_voice_profile(
                persona, cvi_anchors, review_text
            )
            
            # Calculate behavioral fidelity
            fidelity_score = await self._calculate_behavioral_fidelity(
                persona, review_text, cvi_anchors
            )
            
            # Calculate human evaluation rubric
            human_eval_rubric = self.groq._fidelity_rubric(review_text, persona.dict())
            
            generation_time = int((time.time() - start_time) * 1000)
            
            # Create response
            review_gen = ReviewGeneration(
                predicted_rating=predicted_rating,
                confidence_interval=confidence_interval,
                review_text=review_text,
                voice_profile_used=voice_profile,
                behavioural_fidelity_score=fidelity_score,
                cvi_anchors_used=[anchor.phrase for anchor in cvi_anchors],
                generation_time_ms=generation_time,
                model_used=settings.GROQ_MODEL,
                temperature_used=request.temperature,
                human_eval_rubric=human_eval_rubric
            )
            
            # Store in database
            await self._store_generation(request, review_gen)
            
            return ReviewResponse(
                success=True,
                data=review_gen,
                request_id=str(uuid.uuid4()),
            )
            
        except Exception as e:
            return ReviewResponse(
                success=False,
                error=str(e),
                request_id=str(uuid.uuid4())
            )

    async def _generate_local_review(
        self,
        persona: Persona,
        cvi_anchors: List,
        request: ReviewRequest
    ) -> str:
        """Generate a deterministic local review for offline demos and tests."""
        anchor = cvi_anchors[0].phrase if cvi_anchors else "E make sense"
        product = request.product.name
        location = request.product.location
        style = {
            "expressive": f"{anchor}! {product} for {location} has the kind of vibe I can recommend, even if price still needs small mercy.",
            "analytical": f"{product} performs well for {location}. {anchor}, but delivery and value should stay consistent.",
            "casual": f"{product} no bad at all for {location}. {anchor}, I fit try am again if the price behaves.",
            "terse": f"{product}: {anchor}. Solid enough for {location}.",
            "formal": f"{product} is a strong option in {location}. {anchor}, with clear room to improve value perception.",
        }
        return style.get(persona.review_style.value, style["casual"])
    
    async def stream_review(self, request: ReviewRequest) -> ReviewStream:
        """Stream review generation in real-time"""
        request_id = str(uuid.uuid4())
        
        try:
            # Get persona and CVI anchors
            persona = await self.supabase.get_persona(request.persona_id)
            cvi_anchors = await self.cvi.get_persona_anchors(
                persona.city,
                persona.primary_language,
                persona.pidgin_intensity,
                request.product.category
            )
            
            # Generate streaming response
            messages = self.groq.generate_review_prompt(
                persona.dict(),
                request.product.dict(),
                request.context.dict(),
                [anchor.dict() for anchor in cvi_anchors]
            )
            
            async for token in self.groq.stream_completion(
                messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ):
                yield ReviewStream(
                    request_id=request_id,
                    token=token,
                    is_complete=False
                )
            
            # Signal completion
            yield ReviewStream(
                request_id=request_id,
                token="",
                is_complete=True,
                metadata={"anchors_used": len(cvi_anchors)}
            )
            
        except Exception as e:
            yield ReviewStream(
                request_id=request_id,
                token=f"Error: {str(e)}",
                is_complete=True
            )
    
    async def _store_generation(self, request: ReviewRequest, review_gen: ReviewGeneration) -> None:
        """Store review generation in database"""
        try:
            await self.supabase.store_review_generation(
                persona_id=request.persona_id,
                product_id=request.product.dict().get('id'),
                review_text=review_gen.review_text,
                predicted_rating=review_gen.predicted_rating,
                confidence_interval=review_gen.confidence_interval,
                voice_profile_used=review_gen.voice_profile_used,
                cvi_anchors_used=review_gen.cvi_anchors_used,
                generation_time_ms=review_gen.generation_time_ms,
                model_used=review_gen.model_used,
                temperature_used=request.temperature,
                human_eval_rubric=review_gen.human_eval_rubric
            )
        except Exception as e:
            logger.error(f"Failed to store review generation: {e}")
    
    async def _predict_rating(
        self, 
        persona: Persona, 
        review_text: str, 
        cvi_anchors: List
    ) -> float:
        """Predict star rating based on sentiment and persona patterns"""
        # Base rating from persona average
        base_rating = persona.avg_rating
        
        # Sentiment analysis (simplified)
        positive_words = ["good", "nice", "great", "excellent", "amazing", "love", "perfect"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst", "poor", "disappoint"]
        
        pos_count = sum(1 for word in positive_words if word.lower() in review_text.lower())
        neg_count = sum(1 for word in negative_words if word.lower() in review_text.lower())
        
        # CVI anchor sentiment adjustment
        cvi_sentiment = np.mean([anchor.avg_rating_association for anchor in cvi_anchors])
        
        # Calculate final rating
        sentiment_adj = (pos_count - neg_count) * 0.1
        cvi_adj = (cvi_sentiment - 3.5) * 0.3
        
        predicted = base_rating + sentiment_adj + cvi_adj
        
        # Clamp to valid range
        return max(1.0, min(5.0, predicted))
    
    async def _calculate_confidence_interval(
        self, 
        persona: Persona, 
        predicted_rating: float
    ) -> List[float]:
        """Calculate confidence interval for rating prediction"""
        # Base confidence on persona's rating consistency
        if persona.sentiment_volatility == "high":
            margin = 0.6
        elif persona.sentiment_volatility == "medium":
            margin = 0.4
        else:
            margin = 0.2
        
        lower = max(1.0, predicted_rating - margin)
        upper = min(5.0, predicted_rating + margin)
        
        return [lower, upper]
    
    async def _create_voice_profile(
        self, 
        persona: Persona, 
        cvi_anchors: List, 
        review_text: str
    ) -> VoiceProfile:
        """Create voice profile used in generation"""
        return VoiceProfile(
            pidgin_intensity=persona.pidgin_intensity,
            sentiment_category=await self._detect_sentiment_category(review_text),
            cultural_markers_activated=persona.cultural_markers[:3],  # Top 3 markers
            language_patterns={
                "english": 1.0 - persona.pidgin_intensity,
                "pidgin": persona.pidgin_intensity,
                "native": 0.2 if persona.primary_language != "english" else 0.0
            }
        )
    
    async def _calculate_behavioral_fidelity(
        self, 
        persona: Persona, 
        review_text: str, 
        cvi_anchors: List
    ) -> float:
        """Calculate how well the generated text matches persona behavior"""
        fidelity_score = 0.5  # Base score
        
        # CVI anchor matching
        anchor_matches = sum(1 for anchor in cvi_anchors if anchor.phrase.lower() in review_text.lower())
        if cvi_anchors:
            fidelity_score += (anchor_matches / len(cvi_anchors)) * 0.3
        
        # Pidgin intensity matching
        pidgin_indicators = ["na", "o", "sha", "abeg", "wahala", "gbam", "e go be"]
        pidgin_count = sum(1 for indicator in pidgin_indicators if indicator.lower() in review_text.lower())
        pidgin_match = 1.0 - abs(pidgin_count / 10 - persona.pidgin_intensity)
        fidelity_score += pidgin_match * 0.2
        
        return min(1.0, fidelity_score)
    
    async def _detect_sentiment_category(self, text: str) -> str:
        """Simple sentiment detection"""
        positive_words = ["good", "nice", "great", "excellent", "amazing", "love", "perfect", "fine"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst", "poor", "disappoint", "cheat"]
        
        pos_count = sum(1 for word in positive_words if word.lower() in text.lower())
        neg_count = sum(1 for word in negative_words if word.lower() in text.lower())
        
        if pos_count > neg_count + 1:
            return "positive"
        elif neg_count > pos_count + 1:
            return "negative"
        else:
            return "mixed_positive"
    
    async def _store_generation(self, request: ReviewRequest, generation: ReviewGeneration):
        """Store generation in database for analytics"""
        try:
            await self.supabase.store_review_generation(
                user_id=request.user_id,
                persona_id=request.persona_id,
                product=request.product.dict(),
                context=request.context.dict(),
                generation=generation.dict()
            )
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to store generation: {e}")
