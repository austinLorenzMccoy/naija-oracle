"""
Embedding service for vector similarity search
"""

import numpy as np
from typing import List, Dict, Any, Optional

from app.config import settings

class EmbeddingService:
    """Service for generating and managing embeddings"""
    
    def __init__(self):
        try:
            from sentence_transformers import SentenceTransformer  # noqa: F401
            self._model_name = settings.EMBEDDING_MODEL
            self._model: Optional[object] = None  # loaded on first use
            self.available = True
        except ImportError:
            self.available = False
            self._model = None

    def _get_model(self):
        """Lazily load the SentenceTransformer model on first use."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self._model_name)
        return self._model
    
    async def generate_persona_embedding(self, persona: Dict[str, Any]) -> List[float]:
        """Generate embedding for persona"""
        # Combine persona features into text
        persona_text = f"""
        Name: {persona.get('name', '')}
        City: {persona.get('city', '')}
        LGA: {persona.get('lga', '')}
        Language: {persona.get('primary_language', '')}
        Style: {persona.get('review_style', '')}
        Avg Rating: {persona.get('avg_rating', 3.0)}
        Cultural Markers: {', '.join(persona.get('cultural_markers', []))}
        Sample Reviews: {' | '.join(persona.get('sample_reviews', [])[:2])}
        """
        
        embedding = self._get_model().encode(persona_text, convert_to_tensor=False)
        return embedding.tolist()
    
    async def generate_product_embedding(self, product: Dict[str, Any]) -> List[float]:
        """Generate embedding for product"""
        product_text = f"""
        Name: {product.get('name', '')}
        Category: {product.get('category', '')}
        Location: {product.get('location', '')}
        Price Tier: {product.get('price_tier', '')}
        Description: {product.get('description', '')}
        Features: {', '.join(product.get('features', []))}
        """
        
        embedding = self._get_model().encode(product_text, convert_to_tensor=False)
        return embedding.tolist()
    
    async def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        emb1 = np.array(embedding1)
        emb2 = np.array(embedding2)
        
        # Cosine similarity
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    async def find_similar_personas(
        self, 
        target_embedding: List[float], 
        candidate_embeddings: List[List[float]],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """Find most similar personas by embedding"""
        similarities = []
        
        for i, candidate_emb in enumerate(candidate_embeddings):
            similarity = await self.calculate_similarity(target_embedding, candidate_emb)
            similarities.append({"index": i, "similarity": similarity})
        
        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:top_k]
    
    async def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch of texts"""
        embeddings = self._get_model().encode(texts, convert_to_tensor=False)
        return [emb.tolist() for emb in embeddings]
