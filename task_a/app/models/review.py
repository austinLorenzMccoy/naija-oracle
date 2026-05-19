"""
Review generation models for Task A - Persona Simulator
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class ProductCategory(str, Enum):
    FAST_FOOD = "fast_food"
    RESTAURANT = "restaurant"
    FASHION = "fashion"
    FINTECH = "fintech"
    ENTERTAINMENT = "entertainment"
    BEVERAGE = "beverage"
    TECH_GADGET = "tech_gadget"
    BEAUTY = "beauty"
    TRANSPORT = "transport"
    GROCERY = "grocery"

class PriceTier(str, Enum):
    BUDGET = "budget"
    MID = "mid"
    PREMIUM = "premium"
    LUXURY = "luxury"

class TimeOfDay(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    LATE_NIGHT = "late_night"

class Occasion(str, Enum):
    CASUAL = "casual"
    AFTER_WORK = "after_work"
    DATE = "date"
    CELEBRATION = "celebration"
    IMPULSE = "impulse"
    BUSINESS = "business"

class Product(BaseModel):
    name: str
    category: ProductCategory
    location: str
    price_tier: PriceTier
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Context(BaseModel):
    time_of_day: TimeOfDay
    weather: Optional[str] = None
    occasion: Occasion
    recency_of_visit: str = Field(default="first_time")
    mood_signal: Optional[str] = None

class ReviewRequest(BaseModel):
    user_id: str
    persona_id: str
    product: Product
    context: Context
    cultural_markers: List[str] = Field(default_factory=list)
    temperature: float = Field(default=0.85, ge=0.0, le=1.0)
    max_tokens: int = Field(default=400, ge=50, le=1000)

class VoiceProfile(BaseModel):
    pidgin_intensity: float = Field(ge=0.0, le=1.0)
    sentiment_category: str
    cultural_markers_activated: List[str]
    language_patterns: Dict[str, float] = Field(default_factory=dict)

class ReviewGeneration(BaseModel):
    predicted_rating: float = Field(ge=1.0, le=5.0)
    confidence_interval: List[float] = Field(min_length=2, max_length=2)
    review_text: str
    voice_profile_used: VoiceProfile
    behavioural_fidelity_score: float = Field(ge=0.0, le=1.0)
    cvi_anchors_used: List[str] = Field(default_factory=list)
    generation_time_ms: int
    model_used: str
    temperature_used: float
    human_eval_rubric: Optional[Dict[str, float]] = Field(default=None)

class ReviewResponse(BaseModel):
    success: bool
    data: Optional[ReviewGeneration] = None
    error: Optional[str] = None
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ReviewStream(BaseModel):
    request_id: str
    token: str
    is_complete: bool = False
    metadata: Optional[Dict[str, Any]] = None

class ReviewEvaluation(BaseModel):
    bertscore_f1: float = Field(ge=0.0, le=1.0)
    rouge_l: float = Field(ge=0.0, le=1.0)
    rmse: float
    cvi_hit_rate: float = Field(ge=0.0, le=1.0)
    behavioural_fidelity: float = Field(ge=0.0, le=5.0)
    cultural_authenticity: float = Field(ge=0.0, le=5.0)
