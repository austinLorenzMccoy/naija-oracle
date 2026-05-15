"""
Cultural Voice Index (CVI) Service
Manages Nigerian linguistic patterns and cultural authenticity
"""

import json
import uuid
from typing import Dict, List, Optional, Any
import numpy as np

from app.models.cultural_voice import (
    CVIAnchor, CulturalVoiceIndex, CVIMatch, CVIProfile,
    TribeRegion, FormalityRegister, SentimentCategory, ProductContext
)
from app.config import settings

class CulturalVoiceIndex:
    """Service for managing Cultural Voice Index data"""
    
    def __init__(self):
        self.anchors = self._load_default_anchors()
        self.profiles = {}  # persona_id -> CVIProfile
    
    def _load_default_anchors(self) -> List[CVIAnchor]:
        """Load default CVI anchors for Nigerian linguistic patterns"""
        default_data = [
            # Strong Positive - Food
            {
                "phrase": "E sweet me die",
                "tribe_region": TribeRegion.YORUBA,
                "pidgin_intensity": 0.8,
                "formality_register": FormalityRegister.CASUAL,
                "sentiment_category": SentimentCategory.STRONG_POSITIVE,
                "product_context": ProductContext.FOOD,
                "avg_rating_association": 5.0,
                "frequency_score": 0.9,
                "confidence_score": 0.95,
                "examples": ["The jollof rice sweet me die!", "This suya e sweet me die"]
            },
            {
                "phrase": "Wahala be like bicycle",
                "tribe_region": TribeRegion.PAN_NIGERIAN,
                "pidgin_intensity": 0.7,
                "formality_register": FormalityRegister.CASUAL,
                "sentiment_category": SentimentCategory.NEGATIVE,
                "product_context": ProductContext.SERVICE,
                "avg_rating_association": 1.5,
                "frequency_score": 0.8,
                "confidence_score": 0.9,
                "examples": ["The service wahala be like bicycle", "Queue wahala be like bicycle"]
            },
            {
                "phrase": "E dey manage",
                "tribe_region": TribeRegion.PAN_NIGERIAN,
                "pidgin_intensity": 0.6,
                "formality_register": FormalityRegister.CASUAL,
                "sentiment_category": SentimentCategory.MIXED_POSITIVE,
                "product_context": ProductContext.GENERAL,
                "avg_rating_association": 2.5,
                "frequency_score": 0.85,
                "confidence_score": 0.88,
                "examples": ["The food e dey manage", "Service e dey manage"]
            },
            {
                "phrase": "Dem cheat me",
                "tribe_region": TribeRegion.PAN_NIGERIAN,
                "pidgin_intensity": 0.9,
                "formality_register": FormalityRegister.CASUAL,
                "sentiment_category": SentimentCategory.STRONG_NEGATIVE,
                "product_context": ProductContext.PRICE,
                "avg_rating_association": 1.0,
                "frequency_score": 0.7,
                "confidence_score": 0.85,
                "examples": ["Dem cheat me for price", "Portion small, dem cheat me"]
            },
            {
                "phrase": "The vibe no catch me",
                "tribe_region": TribeRegion.PAN_NIGERIAN,
                "pidgin_intensity": 0.7,
                "formality_register": FormalityRegister.EXPRESSIVE,
                "sentiment_category": SentimentCategory.NEUTRAL,
                "product_context": ProductContext.AMBIENCE,
                "avg_rating_association": 3.0,
                "frequency_score": 0.8,
                "confidence_score": 0.9,
                "examples": ["The place vibe no catch me", "Music vibe no catch me"]
            },
            {
                "phrase": "Gbam!",
                "tribe_region": TribeRegion.PAN_NIGERIAN,
                "pidgin_intensity": 0.5,
                "formality_register": FormalityRegister.CASUAL,
                "sentiment_category": SentimentCategory.STRONG_POSITIVE,
                "product_context": ProductContext.GENERAL,
                "avg_rating_association": 4.5,
                "frequency_score": 0.75,
                "confidence_score": 0.8,
                "examples": ["The taste gbam!", "Service gbam!"]
            },
            {
                "phrase": "E go be",
                "tribe_region": TribeRegion.PAN_NIGERIAN,
                "pidgin_intensity": 0.6,
                "formality_register": FormalityRegister.CASUAL,
                "sentiment_category": SentimentCategory.POSITIVE,
                "product_context": ProductContext.GENERAL,
                "avg_rating_association": 4.0,
                "frequency_score": 0.9,
                "confidence_score": 0.92,
                "examples": ["Everything e go be", "Don worry, e go be"]
            },
            # Yoruba-specific
            {
                "phrase": "Orente",
                "tribe_region": TribeRegion.YORUBA,
                "pidgin_intensity": 0.4,
                "formality_register": FormalityRegister.EXPRESSIVE,
                "sentiment_category": SentimentCategory.POSITIVE,
                "product_context": ProductContext.GENERAL,
                "avg_rating_association": 4.2,
                "frequency_score": 0.6,
                "confidence_score": 0.75,
                "examples": ["Customer service orente", "The place orente"]
            },
            # Igbo-specific
            {
                "phrase": "Nwoke oma",
                "tribe_region": TribeRegion.IGBO,
                "pidgin_intensity": 0.3,
                "formality_register": FormalityRegister.CASUAL,
                "sentiment_category": SentimentCategory.POSITIVE,
                "product_context": ProductContext.SERVICE,
                "avg_rating_association": 4.3,
                "frequency_score": 0.5,
                "confidence_score": 0.7,
                "examples": ["The waiter nwoke oma", "Service nwoke oma"]
            },
            # Hausa-specific
            {
                "phrase": "Lafiya",
                "tribe_region": TribeRegion.HAUSA,
                "pidgin_intensity": 0.2,
                "formality_register": FormalityRegister.CASUAL,
                "sentiment_category": SentimentCategory.POSITIVE,
                "product_context": ProductContext.GENERAL,
                "avg_rating_association": 4.1,
                "frequency_score": 0.6,
                "confidence_score": 0.75,
                "examples": ["Everything lafiya", "Place lafiya"]
            },
            # Price sensitivity
            {
                "phrase": "Cost like madness",
                "tribe_region": TribeRegion.PAN_NIGERIAN,
                "pidgin_intensity": 0.8,
                "formality_register": FormalityRegister.CASUAL,
                "sentiment_category": SentimentCategory.NEGATIVE,
                "product_context": ProductContext.PRICE,
                "avg_rating_association": 1.8,
                "frequency_score": 0.7,
                "confidence_score": 0.85,
                "examples": ["Price cost like madness", "Everything cost like madness"]
            },
            # Service quality
            {
                "phrase": "Slow like NEPA",
                "tribe_region": TribeRegion.PAN_NIGERIAN,
                "pidgin_intensity": 0.7,
                "formality_register": FormalityRegister.CASUAL,
                "sentiment_category": SentimentCategory.NEGATIVE,
                "product_context": ProductContext.SERVICE,
                "avg_rating_association": 2.0,
                "frequency_score": 0.8,
                "confidence_score": 0.9,
                "examples": ["Service slow like NEPA", "Wait time slow like NEPA"]
            },
            # Quality appreciation
            {
                "phrase": "Correct!",
                "tribe_region": TribeRegion.PAN_NIGERIAN,
                "pidgin_intensity": 0.4,
                "formality_register": FormalityRegister.CASUAL,
                "sentiment_category": SentimentCategory.STRONG_POSITIVE,
                "product_context": ProductContext.GENERAL,
                "avg_rating_association": 4.6,
                "frequency_score": 0.85,
                "confidence_score": 0.9,
                "examples": ["The food correct!", "Quality correct!"]
            }
        ]
        
        return [CVIAnchor(**data) for data in default_data]
    
    async def get_persona_anchors(
        self,
        city: str,
        language: str,
        pidgin_intensity: float,
        product_category: str
    ) -> List[CVIAnchor]:
        """Get CVI anchors matched to persona characteristics"""
        
        # Map city to tribe region
        tribe_mapping = {
            "lagos": TribeRegion.PAN_NIGERIAN,
            "abuja": TribeRegion.PAN_NIGERIAN,
            "kano": TribeRegion.HAUSA,
            "enugu": TribeRegion.IGBO,
            "ibadan": TribeRegion.YORUBA,
            "port harcourt": TribeRegion.PAN_NIGERIAN,
            "benin": TribeRegion.EDO,
            "warri": TribeRegion.URHOBO
        }
        
        persona_tribe = tribe_mapping.get(city.lower(), TribeRegion.PAN_NIGERIAN)
        
        # Map product category
        category_mapping = {
            "fast_food": ProductContext.FOOD,
            "restaurant": ProductContext.FOOD,
            "beverage": ProductContext.FOOD,
            "fashion": ProductContext.FASHION,
            "fintech": ProductContext.TECH,
            "tech_gadget": ProductContext.TECH,
            "entertainment": ProductContext.GENERAL
        }
        
        product_context = category_mapping.get(product_category, ProductContext.GENERAL)
        
        # Filter and score anchors
        matched_anchors = []
        for anchor in self.anchors:
            score = 0.0
            
            # Tribe region matching
            if anchor.tribe_region == persona_tribe:
                score += 0.3
            elif anchor.tribe_region == TribeRegion.PAN_NIGERIAN:
                score += 0.2
            
            # Pidgin intensity matching
            pidgin_diff = abs(anchor.pidgin_intensity - pidgin_intensity)
            score += max(0, 0.3 - pidgin_diff)
            
            # Product context matching
            if anchor.product_context == product_context:
                score += 0.2
            elif anchor.product_context == ProductContext.GENERAL:
                score += 0.1
            
            # Frequency and confidence boost
            score += (anchor.frequency_score * 0.1) + (anchor.confidence_score * 0.1)
            
            if score >= settings.CVI_THRESHOLD:
                matched_anchors.append((anchor, score))
        
        # Sort by score and return top anchors
        matched_anchors.sort(key=lambda x: x[1], reverse=True)
        return [anchor for anchor, _ in matched_anchors[:5]]
    
    async def create_persona_profile(
        self,
        persona_id: str,
        city: str,
        language: str,
        pidgin_intensity: float,
        review_style: str,
        cultural_markers: List[str]
    ) -> CVIProfile:
        """Create CVI profile for a persona"""
        
        tribe_mapping = {
            "lagos": TribeRegion.PAN_NIGERIAN,
            "kano": TribeRegion.HAUSA,
            "enugu": TribeRegion.IGBO,
            "ibadan": TribeRegion.YORUBA
        }
        
        dominant_tribe = tribe_mapping.get(city.lower(), TribeRegion.PAN_NIGERIAN)
        
        formality_mapping = {
            "expressive": FormalityRegister.EXPRESSIVE,
            "casual": FormalityRegister.CASUAL,
            "analytical": FormalityRegister.FORMAL,
            "formal": FormalityRegister.FORMAL,
            "terse": FormalityRegister.CASUAL
        }
        
        formality_preference = formality_mapping.get(review_style, FormalityRegister.CASUAL)
        
        # Calculate sentiment patterns
        sentiment_patterns = {}
        for sentiment in SentimentCategory:
            sentiment_patterns[sentiment] = np.random.uniform(0.2, 0.8)
        
        # Calculate context specializations
        context_specializations = {}
        for context in ProductContext:
            context_specializations[context] = np.random.uniform(0.1, 0.9)
        
        profile = CVIProfile(
            persona_id=persona_id,
            dominant_tribe_region=dominant_tribe,
            pidgin_intensity=pidgin_intensity,
            formality_preference=formality_preference,
            sentiment_patterns=sentiment_patterns,
            context_specializations=context_specializations,
            preferred_anchors=[],
            voice_consistency_score=np.random.uniform(0.7, 0.95),
            cultural_authenticity_score=np.random.uniform(0.8, 0.98)
        )
        
        self.profiles[persona_id] = profile
        return profile
    
    async def evaluate_cultural_fidelity(
        self,
        persona_id: str,
        generated_text: str,
        expected_anchors: List[str]
    ) -> Dict[str, float]:
        """Evaluate cultural authenticity of generated text"""
        
        profile = self.profiles.get(persona_id)
        if not profile:
            return {"overall_cvi_score": 0.0}
        
        # Anchor hit rate
        anchor_hits = sum(1 for anchor in expected_anchors if anchor.lower() in generated_text.lower())
        anchor_hit_rate = anchor_hits / len(expected_anchors) if expected_anchors else 0.0
        
        # Pidgin accuracy
        pidgin_indicators = ["na", "o", "sha", "abeg", "wahala", "gbam", "e go be", "dey", "dem"]
        pidgin_count = sum(1 for indicator in pidgin_indicators if indicator.lower() in generated_text.lower())
        pidgin_accuracy = 1.0 - abs((pidgin_count / 20) - profile.pidgin_intensity)
        
        # Regional authenticity
        tribe_keywords = {
            TribeRegion.YORUBA: ["orente", "baba", "iya", "jare"],
            TribeRegion.IGBO: ["nwoke oma", "nwa", "biko", "kedu"],
            TribeRegion.HAUSA: ["lafiya", "sannu", "inka", "gaskiya"],
            TribeRegion.PAN_NIGERIAN: pidgin_indicators
        }
        
        tribe_keywords_count = sum(1 for keyword in tribe_keywords.get(profile.dominant_tribe_region, []) 
                                 if keyword.lower() in generated_text.lower())
        regional_authenticity = min(1.0, tribe_keywords_count / 3)
        
        # Formality appropriateness
        formal_indicators = ["excellent", "outstanding", "superb", "magnificent"]
        casual_indicators = pidgin_indicators + ["correct", "nice", "good", "fine"]
        
        if profile.formality_preference == FormalityRegister.FORMAL:
            formal_count = sum(1 for word in formal_indicators if word.lower() in generated_text.lower())
            formality_score = min(1.0, formal_count / 2)
        else:
            casual_count = sum(1 for word in casual_indicators if word.lower() in generated_text.lower())
            formality_score = min(1.0, casual_count / 5)
        
        overall_score = (
            anchor_hit_rate * 0.3 +
            pidgin_accuracy * 0.25 +
            regional_authenticity * 0.25 +
            formality_score * 0.2
        )
        
        return {
            "anchor_hit_rate": anchor_hit_rate,
            "cultural_fidelity": pidgin_accuracy,
            "pidgin_accuracy": pidgin_accuracy,
            "regional_authenticity": regional_authenticity,
            "formality_appropriateness": formality_score,
            "overall_cvi_score": overall_score
        }
    
    async def add_anchor(self, anchor_data: Dict[str, Any]) -> CVIAnchor:
        """Add new CVI anchor"""
        anchor = CVIAnchor(**anchor_data)
        self.anchors.append(anchor)
        return anchor
    
    def get_all_anchors(self) -> List[CVIAnchor]:
        """Get all CVI anchors"""
        return self.anchors
    
    def get_persona_profile(self, persona_id: str) -> Optional[CVIProfile]:
        """Get CVI profile for persona"""
        return self.profiles.get(persona_id)
