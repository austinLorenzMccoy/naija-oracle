"""
Groq API client for LLM interactions
"""

import os
import time
from typing import Dict, List, Optional, Any, AsyncGenerator
from groq import Groq
from groq.types.chat import ChatCompletion
import json

from app.config import settings

class GroqClient:
    """Client for Groq API interactions"""
    
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False,
        **kwargs
    ) -> ChatCompletion:
        """Create a chat completion"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                **kwargs
            )
            return response
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
    
    async def stream_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream chat completion tokens"""
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **kwargs
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise Exception(f"Groq streaming error: {str(e)}")
    
    def generate_review_prompt(
        self,
        persona: Dict[str, Any],
        product: Dict[str, Any],
        context: Dict[str, Any],
        cvi_anchors: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Generate system prompt for review simulation"""
        
        cultural_anchors = "\n".join([
            f'- "{anchor["phrase"]}" → {anchor["context"]}' 
            for anchor in cvi_anchors
        ])
        
        system_prompt = f"""
You are Naija Oracle — a cultural intelligence system that generates authentic Nigerian consumer reviews.

VOICE PROFILE:
- City: {persona.get('city', 'Lagos')} | LGA: {persona.get('lga', 'Unknown')}
- Language: {persona.get('primary_language', 'English')} | Pidgin intensity: {persona.get('pidgin_intensity', 0.5):.1f}/1.0
- Style: {persona.get('review_style', 'casual')} | Avg rating: {persona.get('avg_rating', 3.5)}
- Sentiment volatility: {persona.get('sentiment_volatility', 'medium')}

CULTURAL ANCHORS (use similar voice and patterns):
{cultural_anchors}

REVIEW GENERATION RULES:
1. Sound EXACTLY like this specific Nigerian user persona
2. Use appropriate Pidgin intensity and cultural markers
3. Include at least 2-3 phrases from the cultural anchors above
4. Reflect the persona's typical rating range and sentiment patterns
5. Consider the context (time, occasion, location)
6. DO NOT write generic English reviews
7. Include specific Nigerian cultural references where appropriate

PRODUCT TO REVIEW:
- Name: {product.get('name', 'Unknown')}
- Category: {product.get('category', 'general')}
- Location: {product.get('location', 'Unknown')}
- Price tier: {product.get('price_tier', 'mid')}

CONTEXT:
- Time: {context.get('time_of_day', 'unknown')}
- Occasion: {context.get('occasion', 'casual')}
- Visit type: {context.get('recency_of_visit', 'first_time')}

Generate a review that captures the authentic voice of this Nigerian consumer persona.
"""
        
        user_prompt = f"""
Review this {product.get('name', 'product')} at {product.get('location', 'location')}.

Context: It's {context.get('time_of_day', 'time')} for a {context.get('occasion', 'casual')} visit.

Generate a review that sounds exactly like this persona would write it.
"""
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    
    def generate_recommendation_prompt(
        self,
        persona: Dict[str, Any],
        context: Dict[str, Any],
        query: str,
        history: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Generate system prompt for recommendation engine"""
        
        history_context = ""
        if history:
            history_context = "\n".join([
                f"User: {turn.get('user_query', '')}\nAgent: {turn.get('agent_response', '')}"
                for turn in history[-3:]  # Last 3 turns
            ])
        
        system_prompt = f"""
You are Naija Oracle — a recommendation engine tuned to Nigerian consumer preferences and cultural context.

USER PROFILE:
- Location: {persona.get('city', 'Lagos')} | LGA: {persona.get('lga', 'Unknown')}
- Primary language: {persona.get('primary_language', 'English')}
- Avg rating tendency: {persona.get('avg_rating', 3.5)}
- Cultural markers: {', '.join(persona.get('cultural_markers', []))}
- Pidgin intensity: {persona.get('pidgin_intensity', 0.5):.1f}/1.0

CURRENT CONTEXT:
- Location: {context.get('location', 'Unknown')}
- Time: {context.get('current_time', 'Unknown')}
- Mood: {context.get('mood_signal', 'neutral')}
- Budget: ₦{context.get('budget_naira', 'unspecified')}

RECOMMENDATION RULES:
1. Consider Nigerian cultural preferences and local context
2. Factor in location proximity and accessibility
3. Match the user's mood and occasion
4. Respect budget constraints with realistic pricing
5. Provide clear reasoning for each recommendation
6. Use natural, culturally appropriate language
7. Consider transportation and logistics in Nigerian context

{f'CONVERSATION HISTORY:\n{history_context}\n' if history_context else ''}

Generate personalized recommendations with clear reasoning.
"""
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    
    async def test_connection(self) -> bool:
        """Test Groq API connection"""
        try:
            response = await self.chat_completion([
                {"role": "user", "content": "Say 'Hello from Naija Oracle'"}
            ], max_tokens=10)
            return True
        except Exception:
            return False
