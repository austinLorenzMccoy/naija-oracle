"""
Persona models for Naija Oracle — Task B
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class PersonaLanguage(str, Enum):
    ENGLISH = "english"
    PIDGIN = "pidgin"
    YORUBA = "yoruba"
    IGBO = "igbo"
    HAUSA = "hausa"

class ReviewStyle(str, Enum):
    EXPRESSIVE = "expressive"
    ANALYTICAL = "analytical"
    CASUAL = "casual"
    TERSE = "terse"
    FORMAL = "formal"
    STREET_HONEST = "street_honest"
    HYPER_CRITICAL = "hyper_critical"
    ASPIRATIONAL = "aspirational"

class PersonaStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TRAINING = "training"
    ACTIVE_ORACLE = "active_oracle"

class Persona(BaseModel):
    id: str
    user_id: str
    name: str
    age_range: str
    city: str
    lga: str
    primary_language: PersonaLanguage
    review_style: ReviewStyle
    avg_rating: float = Field(ge=1.0, le=5.0)
    sentiment_volatility: str = Field(default="medium")
    categories_reviewed: List[str] = Field(default_factory=list)
    sample_reviews: List[str] = Field(default_factory=list)
    cultural_markers: List[str] = Field(default_factory=list)
    pidgin_intensity: float = Field(ge=0.0, le=1.0, default=0.5)
    voice_radar: Dict[str, float] = Field(default_factory=dict)
    cultural_density: float = Field(ge=0.0, le=100.0)
    status: PersonaStatus = PersonaStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PersonaCreate(BaseModel):
    user_id: str
    name: str
    age_range: str
    city: str
    lga: str
    primary_language: PersonaLanguage
    review_style: ReviewStyle
    avg_rating: float = Field(ge=1.0, le=5.0)
    sentiment_volatility: str = "medium"
    categories_reviewed: List[str] = Field(default_factory=list)
    sample_reviews: List[str] = Field(default_factory=list)
    cultural_markers: List[str] = Field(default_factory=list)
    pidgin_intensity: float = Field(ge=0.0, le=1.0, default=0.5)

class PersonaUpdate(BaseModel):
    name: Optional[str] = None
    age_range: Optional[str] = None
    city: Optional[str] = None
    lga: Optional[str] = None
    primary_language: Optional[PersonaLanguage] = None
    review_style: Optional[ReviewStyle] = None
    avg_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    sentiment_volatility: Optional[str] = None
    categories_reviewed: Optional[List[str]] = None
    sample_reviews: Optional[List[str]] = None
    cultural_markers: Optional[List[str]] = None
    pidgin_intensity: Optional[float] = Field(None, ge=0.0, le=1.0)
    voice_radar: Optional[Dict[str, float]] = None
    cultural_density: Optional[float] = Field(None, ge=0.0, le=100.0)
    status: Optional[PersonaStatus] = None
