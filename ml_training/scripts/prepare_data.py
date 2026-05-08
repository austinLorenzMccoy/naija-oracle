"""
Data preparation script for Naija Oracle ML training
Generates synthetic Nigerian cultural data with DVC tracking
"""

import json
import csv
import os
import argparse
from datetime import datetime
from typing import Dict, List, Any
import numpy as np
import pandas as pd
from dvclive import Live

def generate_persona_data(num_personas: int = 500, cvi_expansion: bool = True) -> List[Dict[str, Any]]:
    """Generate synthetic Nigerian persona data"""
    
    # Persona templates
    persona_templates = [
        {
            "name_base": "Emeka",
            "surname": "Okafor, Nwankwo, Eze, Okonkwo, Iwu",
            "city": "Lagos",
            "lgas": ["Surulere", "Ikeja", "Eti-Osa", "Lagos Mainland"],
            "language": "Igbo",
            "pidgin_intensity": 0.7,
            "review_styles": ["expressive", "analytical"],
            "avg_rating_range": (3.5, 4.5)
        },
        {
            "name_base": "Aisha",
            "surname": "Muhammad, Ibrahim, Yusuf, Abubakar",
            "city": "Kano",
            "lgas": ["Kano Municipal", "Nassarawa", "Dala", "Gwale"],
            "language": "Hausa",
            "pidgin_intensity": 0.3,
            "review_styles": ["formal", "analytical"],
            "avg_rating_range": (3.2, 4.2)
        },
        {
            "name_base": "Tunde",
            "surname": "Adeyemi, Ogunleye, Eko, Balogun",
            "city": "Lagos",
            "lgas": ["Ikeja", "Surulere", "Lagos Mainland", "Eti-Osa"],
            "language": "Yoruba",
            "pidgin_intensity": 0.8,
            "review_styles": ["casual", "expressive"],
            "avg_rating_range": (3.0, 4.0)
        },
        {
            "name_base": "Chinedu",
            "surname": "Okoro, Nwosu, Eze, Anayo",
            "city": "Enugu",
            "lgas": ["Enugu South", "Enugu North", "Enugu East"],
            "language": "Igbo",
            "pidgin_intensity": 0.6,
            "review_styles": ["expressive", "casual"],
            "avg_rating_range": (3.3, 4.3)
        },
        {
            "name_base": "Fatima",
            "surname": "Suleiman, Bello, Garba, Lawal",
            "city": "Abuja",
            "lgas": ["Abuja Municipal", "Bwari", "Gwagwalada"],
            "language": "Hausa",
            "pidgin_intensity": 0.4,
            "review_styles": ["formal", "analytical"],
            "avg_rating_range": (3.6, 4.4)
        }
    ]
    
    personas = []
    
    for i in range(num_personas):
        template = np.random.choice(persona_templates)
        
        # Generate persona
        surname = np.random.choice(template["surname"].split(", "))
        name = f"{template['name_base']} {surname}"
        
        age_ranges = ["18-24", "25-34", "35-44", "45-54", "55+"]
        age_range = np.random.choice(age_ranges)
        
        lga = np.random.choice(template["lgas"])
        review_style = np.random.choice(template["review_styles"])
        
        avg_rating = np.random.uniform(*template["avg_rating_range"])
        
        # Cultural markers
        all_markers = ["price_sensitive", "brand_loyal", "quality_focused", 
                      "convenience_seeker", "trend_follower", "traditional_values"]
        cultural_markers = np.random.choice(all_markers, size=np.random.randint(2, 5), replace=False).tolist()
        
        # Sample reviews (simplified)
        sample_reviews = [
            f"The service was {np.random.choice(['good', 'excellent', 'okay'])} but {np.random.choice(['price', 'quality', 'timing'])} could be better.",
            f"I {np.random.choice(['love', 'like', 'enjoy'])} this place! {np.random.choice(['Highly recommend', 'Will visit again', 'Great value'])}."
        ]
        
        persona = {
            "id": f"persona_{i:04d}",
            "name": name,
            "age_range": age_range,
            "city": template["city"],
            "lga": lga,
            "primary_language": template["language"],
            "review_style": review_style,
            "avg_rating": round(avg_rating, 1),
            "sentiment_volatility": np.random.choice(["low", "medium", "high"]),
            "categories_reviewed": np.random.choice(["food", "fashion", "fintech", "entertainment"], 
                                                 size=np.random.randint(2, 4), replace=False).tolist(),
            "sample_reviews": sample_reviews,
            "cultural_markers": cultural_markers,
            "pidgin_intensity": round(np.random.normal(template["pidgin_intensity"], 0.1), 2),
            "status": "active"
        }
        
        personas.append(persona)
    
    return personas

def generate_product_data(num_products: int = 100) -> List[Dict[str, Any]]:
    """Generate synthetic product data"""
    
    product_templates = [
        {
            "name_base": "Chicken Republic",
            "category": "fast_food",
            "locations": ["Ikeja", "Victoria Island", "Lekki", "Surulere"],
            "price_tiers": ["budget", "mid"],
            "avg_rating_range": (3.5, 4.5)
        },
        {
            "name_base": "Yellow Chilli",
            "category": "restaurant",
            "locations": ["Victoria Island", "Ikoyi", "Lekki Phase 1"],
            "price_tiers": ["premium", "luxury"],
            "avg_rating_range": (4.0, 4.8)
        },
        {
            "name_base": "Shoprite",
            "category": "grocery",
            "locations": ["Lekki", "Ikeja City Mall", "Surulere", "Victoria Island"],
            "price_tiers": ["mid", "premium"],
            "avg_rating_range": (3.8, 4.3)
        },
        {
            "name_base": "Jumia",
            "category": "fintech",
            "locations": ["Online"],
            "price_tiers": ["free", "budget"],
            "avg_rating_range": (3.2, 4.1)
        },
        {
            "name_base": "Silverbird Cinema",
            "category": "entertainment",
            "locations": ["Ikeja City Mall", "Victoria Island", "Lekki"],
            "price_tiers": ["mid", "premium"],
            "avg_rating_range": (4.0, 4.6)
        }
    ]
    
    products = []
    
    for i in range(num_products):
        template = np.random.choice(product_templates)
        
        location = np.random.choice(template["locations"])
        price_tier = np.random.choice(template["price_tiers"])
        avg_rating = np.random.uniform(*template["avg_rating_range"])
        
        product = {
            "id": f"product_{i:04d}",
            "name": template["name_base"],
            "category": template["category"],
            "location": location,
            "price_tier": price_tier,
            "avg_rating": round(avg_rating, 1),
            "metadata": {
                "features": np.random.choice(["WiFi", "Parking", "Delivery", "Live Music", "Outdoor Seating"], 
                                         size=np.random.randint(1, 4), replace=False).tolist(),
                "price_range": get_price_range(price_tier)
            }
        }
        
        products.append(product)
    
    return products

def get_price_range(price_tier: str) -> tuple:
    """Get price range for tier"""
    price_ranges = {
        "free": (0, 0),
        "budget": (500, 3000),
        "mid": (3000, 8000),
        "premium": (8000, 20000),
        "luxury": (20000, 100000)
    }
    return price_ranges.get(price_tier, (1000, 5000))

def generate_cvi_anchors() -> List[Dict[str, Any]]:
    """Generate Cultural Voice Index anchors"""
    
    anchors = [
        # Strong Positive
        {
            "phrase": "E sweet me die",
            "tribe_region": "Yoruba",
            "pidgin_intensity": 0.8,
            "formality_register": "casual",
            "sentiment_category": "strong_positive",
            "product_context": "food",
            "avg_rating_association": 5.0,
            "frequency_score": 0.9,
            "confidence_score": 0.95,
            "examples": ["The jollof rice sweet me die!", "This suya e sweet me die"]
        },
        {
            "phrase": "Gbam!",
            "tribe_region": "Pan-Nigerian",
            "pidgin_intensity": 0.5,
            "formality_register": "casual",
            "sentiment_category": "strong_positive",
            "product_context": "general",
            "avg_rating_association": 4.5,
            "frequency_score": 0.75,
            "confidence_score": 0.8,
            "examples": ["The taste gbam!", "Service gbam!"]
        },
        # Negative
        {
            "phrase": "Wahala be like bicycle",
            "tribe_region": "Pan-Nigerian",
            "pidgin_intensity": 0.7,
            "formality_register": "casual",
            "sentiment_category": "negative",
            "product_context": "service",
            "avg_rating_association": 1.5,
            "frequency_score": 0.8,
            "confidence_score": 0.9,
            "examples": ["The service wahala be like bicycle", "Queue wahala be like bicycle"]
        },
        {
            "phrase": "Dem cheat me",
            "tribe_region": "Pan-Nigerian",
            "pidgin_intensity": 0.9,
            "formality_register": "casual",
            "sentiment_category": "strong_negative",
            "product_context": "price",
            "avg_rating_association": 1.0,
            "frequency_score": 0.7,
            "confidence_score": 0.85,
            "examples": ["Dem cheat me for price", "Portion small, dem cheat me"]
        },
        # Mixed/Neutral
        {
            "phrase": "E dey manage",
            "tribe_region": "Pan-Nigerian",
            "pidgin_intensity": 0.6,
            "formality_register": "casual",
            "sentiment_category": "mixed_positive",
            "product_context": "general",
            "avg_rating_association": 2.5,
            "frequency_score": 0.85,
            "confidence_score": 0.88,
            "examples": ["The food e dey manage", "Service e dey manage"]
        },
        {
            "phrase": "The vibe no catch me",
            "tribe_region": "Pan-Nigerian",
            "pidgin_intensity": 0.7,
            "formality_register": "expressive",
            "sentiment_category": "neutral",
            "product_context": "ambience",
            "avg_rating_association": 3.0,
            "frequency_score": 0.8,
            "confidence_score": 0.9,
            "examples": ["The place vibe no catch me", "Music vibe no catch me"]
        },
        # Service Issues
        {
            "phrase": "Slow like NEPA",
            "tribe_region": "Pan-Nigerian",
            "pidgin_intensity": 0.7,
            "formality_register": "casual",
            "sentiment_category": "negative",
            "product_context": "service",
            "avg_rating_association": 2.0,
            "frequency_score": 0.8,
            "confidence_score": 0.9,
            "examples": ["Service slow like NEPA", "Wait time slow like NEPA"]
        },
        # Price Sensitivity
        {
            "phrase": "Cost like madness",
            "tribe_region": "Pan-Nigerian",
            "pidgin_intensity": 0.8,
            "formality_register": "casual",
            "sentiment_category": "negative",
            "product_context": "price",
            "avg_rating_association": 1.8,
            "frequency_score": 0.7,
            "confidence_score": 0.85,
            "examples": ["Price cost like madness", "Everything cost like madness"]
        }
    ]
    
    return anchors

def generate_training_data(personas: List[Dict], products: List[Dict], cvi_anchors: List[Dict]) -> List[Dict]:
    """Generate training data for persona simulator"""
    
    training_data = []
    
    for persona in personas:
        for product in products[:50]:  # Limit products per persona
            for rating in [1, 2, 3, 4, 5]:
                # Generate review based on persona and rating
                review = generate_review(persona, product, rating, cvi_anchors)
                
                # Create training prompt
                prompt = create_training_prompt(persona, product, review)
                
                training_data.append({
                    "text": prompt,
                    "persona": persona,
                    "product": product,
                    "rating": rating,
                    "review": review
                })
    
    return training_data

def generate_review(persona: Dict, product: Dict, rating: int, cvi_anchors: List[Dict]) -> str:
    """Generate authentic Nigerian review"""
    
    # Select CVI phrases based on persona and rating
    if rating >= 4:
        positive_phrases = [a["phrase"] for a in cvi_anchors 
                           if a["sentiment_category"] in ["strong_positive", "positive"]]
        anchor = np.random.choice(positive_phrases) if positive_phrases else "Correct!"
    elif rating <= 2:
        negative_phrases = [a["phrase"] for a in cvi_anchors 
                           if a["sentiment_category"] in ["strong_negative", "negative"]]
        anchor = np.random.choice(negative_phrases) if negative_phrases else "E dey manage"
    else:
        anchor = np.random.choice([a["phrase"] for a in cvi_anchors])
    
    # Generate review based on persona characteristics
    if persona["pidgin_intensity"] > 0.6:
        # High pidgin
        if rating >= 4:
            return f"This {product['name']} for {product['location']}, {anchor}! The service correct, I go come back for sure. {rating} stars!"
        elif rating <= 2:
            return f"This {product['name']} {anchor}. Service slow like NEPA and price cost like madness. No recommend."
        else:
            return f"This {product['name']} e dey manage. Not bad but not great either. {product['location']} branch need improvement."
    else:
        # Lower pidgin, more formal
        if rating >= 4:
            return f"The {product['name']} at {product['location']} was excellent. Great service and quality. Highly recommended."
        elif rating <= 2:
            return f"I was disappointed with {product['name']} at {product['location']}. Poor service and overpriced."
        else:
            return f"The {product['name']} at {product['location']} was average. Some good aspects but needs improvement."

def create_training_prompt(persona: Dict, product: Dict, review: str) -> str:
    """Create training prompt with persona context"""
    
    prompt = f"""<s>[INST]
You are Naija Oracle — a cultural intelligence system that generates authentic Nigerian consumer reviews.

PERSONA:
- Name: {persona['name']}
- City: {persona['city']} | LGA: {persona['lga']}
- Language: {persona['primary_language']} | Pidgin intensity: {persona['pidgin_intensity']:.1f}/1.0
- Style: {persona['review_style']}

PRODUCT TO REVIEW:
- Name: {product['name']}
- Category: {product['category']}
- Location: {product['location']}

Generate an authentic review that sounds exactly like this persona would write it.
[/INST]

{review}</s>"""
    
    return prompt

def generate_recommendation_data(personas: List[Dict], products: List[Dict]) -> List[Dict]:
    """Generate training data for recommendation engine"""
    
    training_data = []
    
    for persona in personas:
        for _ in range(20):  # 20 interactions per persona
            # Simulate recommendation context
            context = {
                "current_time": np.random.choice(["morning", "afternoon", "evening", "night"]),
                "location": persona["city"],
                "mood_signal": np.random.choice(["celebratory", "casual", "romantic", "professional"]),
                "budget_naira": np.random.uniform(1000, 20000),
                "occasion": np.random.choice(["casual", "after_work", "date", "celebration", "impulse"])
            }
            
            # Generate features
            features = {
                "user_rating_tendency": persona["avg_rating"],
                "item_avg_rating": np.random.uniform(2.0, 5.0),
                "price_match_score": np.random.uniform(0.0, 1.0),
                "location_proximity": np.random.uniform(0.0, 1.0),
                "category_preference": np.random.uniform(0.0, 1.0),
                "time_relevance": np.random.uniform(0.0, 1.0),
                "mood_alignment": np.random.uniform(0.0, 1.0),
                "budget_fit": np.random.uniform(0.0, 1.0),
                "collaborative_score": np.random.uniform(0.0, 1.0),
                "popularity_score": np.random.uniform(0.0, 1.0),
                "relevance_score": np.random.uniform(0.0, 1.0)
            }
            
            training_data.append(features)
    
    return training_data

def main():
    parser = argparse.ArgumentParser(description="Prepare training data for Naija Oracle")
    parser.add_argument("--num-personas", type=int, default=500, help="Number of personas to generate")
    parser.add_argument("--num-products", type=int, default=100, help="Number of products to generate")
    parser.add_argument("--cvi-expansion", action="store_true", help="Expand CVI anchors")
    parser.add_argument("--output-dir", type=str, default="data", help="Output directory")
    
    args = parser.parse_args()
    
    # Initialize DVC Live
    with Live("data_preparation") as live:
        live.log_param("num_personas", args.num_personas)
        live.log_param("num_products", args.num_products)
        live.log_param("cvi_expansion", args.cvi_expansion)
        
        print("Generating personas...")
        personas = generate_persona_data(args.num_personas, args.cvi_expansion)
        live.log_metric("personas_generated", len(personas))
        
        print("Generating products...")
        products = generate_product_data(args.num_products)
        live.log_metric("products_generated", len(products))
        
        print("Generating CVI anchors...")
        cvi_anchors = generate_cvi_anchors()
        live.log_metric("cvi_anchors_generated", len(cvi_anchors))
        
        print("Generating persona simulator training data...")
        persona_training_data = generate_training_data(personas, products, cvi_anchors)
        live.log_metric("persona_training_examples", len(persona_training_data))
        
        print("Generating recommendation engine training data...")
        recommendation_training_data = generate_recommendation_data(personas, products)
        live.log_metric("recommendation_training_examples", len(recommendation_training_data))
        
        # Create output directory
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Save files
        print("Saving data files...")
        
        # Persona training data
        with open(f"{args.output_dir}/persona_training_data.json", "w") as f:
            json.dump(persona_training_data, f, indent=2)
        
        # Recommendation training data
        df = pd.DataFrame(recommendation_training_data)
        df.to_csv(f"{args.output_dir}/recommendation_training_data.csv", index=False)
        
        # CVI anchors
        with open(f"{args.output_dir}/cvi_anchors.json", "w") as f:
            json.dump(cvi_anchors, f, indent=2)
        
        # Metadata
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "num_personas": len(personas),
            "num_products": len(products),
            "cvi_anchors": len(cvi_anchors),
            "persona_training_examples": len(persona_training_data),
            "recommendation_training_examples": len(recommendation_training_data)
        }
        
        with open(f"{args.output_dir}/metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Data preparation completed! Files saved to {args.output_dir}/")
        print(f"- persona_training_data.json: {len(persona_training_data)} examples")
        print(f"- recommendation_training_data.csv: {len(recommendation_training_data)} examples")
        print(f"- cvi_anchors.json: {len(cvi_anchors)} anchors")

if __name__ == "__main__":
    main()
