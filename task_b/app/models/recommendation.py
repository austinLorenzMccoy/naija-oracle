"""
Recommendation models for Task B - Recommendation Engine
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
from enum import Enum

class RecommendationDomain(str, Enum):
    FOOD = "food"
    FASHION = "fashion"
    FINTECH = "fintech"
    ENTERTAINMENT = "entertainment"
    TECH = "tech"
    BEAUTY = "beauty"
    TRANSPORT = "transport"

class RecommendationContext(BaseModel):
    current_time: str
    location: str
    mood_signal: str
    recent_searches: List[str] = Field(default_factory=list)
    budget_naira: Optional[float] = None
    occasion: Optional[str] = None
    companions: Optional[str] = None

class TurnHistory(BaseModel):
    user_query: str
    agent_response: str
    recommendations_shown: List[str] = Field(default_factory=list)
    user_feedback: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class RecommendationItem(BaseModel):
    item_id: str
    name: str
    category: str
    location: str
    description: Optional[str] = None
    price_tier: str
    predicted_rating: float = Field(ge=1.0, le=5.0)
    context_score: float = Field(ge=0.0, le=1.0)
    reasoning: str
    distance_km: Optional[float] = None
    price_range_naira: Optional[Tuple[float, float]] = None
    features: List[str] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)
    availability: Optional[Dict[str, Any]] = None

class RecommendationRequest(BaseModel):
    user_id: str
    persona_id: str
    domain: RecommendationDomain
    context: RecommendationContext
    turn_history: List[TurnHistory] = Field(default_factory=list)
    cold_start: bool = Field(default=False)
    max_recommendations: int = Field(default=5, ge=1, le=20)
    include_explanation: bool = Field(default=True)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

class RecommendationGeneration(BaseModel):
    recommendations: List[RecommendationItem]
    explanation: str
    next_turn_prompt: Optional[str] = None
    cold_start_used: bool
    ndcg_at_10: float = Field(ge=0.0, le=1.0)
    hit_rate_at_5: float = Field(ge=0.0, le=1.0)
    reasoning_trace: List[str] = Field(default_factory=list)
    context_boost_factors: Dict[str, float] = Field(default_factory=dict)
    generation_time_ms: int
    model_used: str
    temperature_used: float

class RecommendationResponse(BaseModel):
    success: bool
    data: Optional[RecommendationGeneration] = None
    error: Optional[str] = None
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class RecommendationStream(BaseModel):
    request_id: str
    token: str
    is_complete: bool = False
    metadata: Optional[Dict[str, Any]] = None

class RecommendationEvaluation(BaseModel):
    ndcg_at_10: float = Field(ge=0.0, le=1.0)
    hit_rate_at_5: float = Field(ge=0.0, le=1.0)
    cold_start_ndcg: float = Field(ge=0.0, le=1.0)
    cross_domain_hit_rate: float = Field(ge=0.0, le=1.0)
    contextual_relevance: float = Field(ge=0.0, le=5.0)
    diversity_score: float = Field(ge=0.0, le=1.0)
    novelty_score: float = Field(ge=0.0, le=1.0)
