"""
Cultural Voice Index (CVI) models for Nigerian linguistic patterns — Task A
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class TribeRegion(str, Enum):
    YORUBA = "yoruba"
    IGBO = "igbo"
    HAUSA = "hausa"
    PAN_NIGERIAN = "pan_nigerian"
    EDO = "edo"
    URHOBO = "urhobo"
    IJAW = "ijaw"
    Ibibio = "ibibio"

class FormalityRegister(str, Enum):
    CASUAL = "casual"
    EXPRESSIVE = "expressive"
    FORMAL = "formal"
    SEMI_FORMAL = "semi_formal"

class SentimentCategory(str, Enum):
    STRONG_POSITIVE = "strong_positive"
    POSITIVE = "positive"
    MIXED_POSITIVE = "mixed_positive"
    NEUTRAL = "neutral"
    MIXED_NEGATIVE = "mixed_negative"
    NEGATIVE = "negative"
    STRONG_NEGATIVE = "strong_negative"

class ProductContext(str, Enum):
    FOOD = "food"
    SERVICE = "service"
    AMBIENCE = "ambience"
    PRICE = "price"
    GENERAL = "general"
    TRANSPORT = "transport"
    TECH = "tech"
    FASHION = "fashion"

class CVIAnchor(BaseModel):
    phrase: str
    tribe_region: TribeRegion
    pidgin_intensity: float = Field(ge=0.0, le=1.0)
    formality_register: FormalityRegister
    sentiment_category: SentimentCategory
    product_context: ProductContext
    avg_rating_association: float = Field(ge=1.0, le=5.0)
    frequency_score: float = Field(ge=0.0, le=1.0)
    confidence_score: float = Field(ge=0.0, le=1.0)
    examples: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CulturalVoiceIndex(BaseModel):
    id: str
    anchors: List[CVIAnchor]
    persona_match_score: float = Field(ge=0.0, le=1.0)
    context_relevance: float = Field(ge=0.0, le=1.0)
    activation_threshold: float = Field(default=0.6)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CVIMatch(BaseModel):
    anchor: CVIAnchor
    match_score: float = Field(ge=0.0, le=1.0)
    relevance_score: float = Field(ge=0.0, le=1.0)
    activation_weight: float = Field(ge=0.0, le=1.0)

class CVIProfile(BaseModel):
    persona_id: str
    dominant_tribe_region: TribeRegion
    pidgin_intensity: float = Field(ge=0.0, le=1.0)
    formality_preference: FormalityRegister
    sentiment_patterns: Dict[SentimentCategory, float] = Field(default_factory=dict)
    context_specializations: Dict[ProductContext, float] = Field(default_factory=dict)
    preferred_anchors: List[str] = Field(default_factory=list)
    voice_consistency_score: float = Field(ge=0.0, le=1.0)
    cultural_authenticity_score: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CVIEvaluation(BaseModel):
    anchor_hit_rate: float = Field(ge=0.0, le=1.0)
    cultural_fidelity: float = Field(ge=0.0, le=1.0)
    pidgin_accuracy: float = Field(ge=0.0, le=1.0)
    regional_authenticity: float = Field(ge=0.0, le=1.0)
    formality_appropriateness: float = Field(ge=0.0, le=1.0)
    overall_cvi_score: float = Field(ge=0.0, le=1.0)
