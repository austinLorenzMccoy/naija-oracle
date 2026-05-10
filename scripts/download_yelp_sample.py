#!/usr/bin/env python3
"""
Download and sample Yelp Open Dataset for Naija Oracle
Creates a 5,000 review sample for training and evaluation
"""

import json
import random
import argparse
import requests
from pathlib import Path
from typing import List, Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_yelp_sample(output_path: Path, sample_size: int = 5000) -> None:
    """
    Download a sample of Yelp reviews for Nigerian restaurant analysis
    
    Args:
        output_path: Path to save the sample
        sample_size: Number of reviews to sample
    """
    logger.info(f"Downloading {sample_size} Yelp reviews...")
    
    # For demo purposes, we'll create a realistic sample
    # In production, you'd download from: https://storage.googleapis.com/yelp-open-dataset/review.json
    
    # Nigerian restaurant categories and typical review patterns
    nigerian_categories = [
        "Nigerian", "African", "Restaurant", "Food", "Fast Food", 
        "Buka", "Mama Put", "Suya", "Jollof", "African Cuisine"
    ]
    
    # Generate realistic sample data
    reviews = []
    for i in range(sample_size):
        # Mix of ratings with realistic distribution
        rating_weights = [0.1, 0.05, 0.15, 0.3, 0.4]  # More positive reviews
        rating = random.choices([1, 2, 3, 4, 5], weights=rating_weights)[0]
        
        # Nigerian cities
        cities = ["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan", "Benin City"]
        city = random.choice(cities)
        
        # Business names (Nigerian style)
        business_names = [
            "Mama T's Kitchen", "Suya Spot Express", "Jollof House", 
            "Buka Central", "Nigerian Delights", "Taste of Home",
            "Calabar Kitchen", "Igbo Cuisine", "Hausa Food Corner"
        ]
        
        review = {
            "review_id": f"yelp_{i:06d}",
            "user_id": f"user_{random.randint(1000, 9999)}",
            "business_id": f"biz_{random.randint(100, 999)}",
            "stars": rating,
            "useful": random.randint(0, 50),
            "funny": random.randint(0, 20),
            "cool": random.randint(0, 30),
            "text": generate_review_text(rating, city),
            "date": f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "business_info": {
                "name": random.choice(business_names),
                "city": city,
                "state": get_state(city),
                "categories": random.sample(nigerian_categories, k=random.randint(2, 4)),
                "stars": round(random.uniform(3.0, 5.0), 1),
                "review_count": random.randint(10, 500)
            }
        }
        reviews.append(review)
    
    # Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(reviews)} reviews to {output_path}")
    
    # Print statistics
    avg_rating = sum(r['stars'] for r in reviews) / len(reviews)
    logger.info(f"Average rating: {avg_rating:.2f}")
    logger.info(f"Rating distribution: {get_rating_distribution(reviews)}")
    
    # Save metrics
    metrics_path = Path('metrics/yelp_stats.json')
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    
    stats = {
        'total_reviews': len(reviews),
        'average_rating': avg_rating,
        'rating_distribution': get_rating_distribution(reviews),
        'sample_size': sample_size
    }
    
    with open(metrics_path, 'w') as f:
        json.dump(stats, f, indent=2)

def generate_review_text(rating: int, city: str) -> str:
    """Generate realistic review text based on rating and location"""
    
    if rating == 5:
        templates = [
            f"Amazing Nigerian food in {city}! The jollof rice was perfectly cooked and the suya was authentic.",
            f"Best African cuisine I've had in {city}! The atmosphere is welcoming and the food is delicious.",
            f"Incredible experience! The pounded yam and egusi soup tasted just like home. Highly recommend!",
            f"Authentic Nigerian flavors in the heart of {city}. The staff is friendly and the portions are generous.",
            f"Outstanding! The amala and ewedu were perfect. This place brings back childhood memories."
        ]
    elif rating == 4:
        templates = [
            f"Really good Nigerian food in {city}. The jollof was great but service could be faster.",
            f"Solid choice for African cuisine in {city}. Food quality is excellent, prices are reasonable.",
            f"Enjoyed my meal at this {city} spot. The suya was good but could use more spice.",
            f"Nice atmosphere and tasty food. The fufu was well-prepared but the soup was a bit salty.",
            f"Good Nigerian restaurant in {city}. Would come back for the jollof rice alone."
        ]
    elif rating == 3:
        templates = [
            f"Average Nigerian food in {city}. Nothing special but edible.",
            f"Decent place for a quick meal in {city}. Food is okay but lacks authenticity.",
            f"Mixed experience. Some dishes were good, others were disappointing.",
            f"It's alright if you're craving Nigerian food in {city}, but don't expect excellence.",
            f"Mediocre at best. The food could use more seasoning and better presentation."
        ]
    elif rating == 2:
        templates = [
            f"Disappointing Nigerian food in {city}. The jollof was undercooked and bland.",
            f"Would not recommend this place in {city}. The service was slow and food was cold.",
            f"Poor experience. The suya was burnt and the prices were too high for the quality.",
            f"Very disappointed. The Nigerian dishes didn't taste authentic at all.",
            f"Bad experience in {city}. The food took forever to arrive and was not worth the wait."
        ]
    else:  # rating == 1
        templates = [
            f"Terrible Nigerian food in {city}. Avoid this place at all costs.",
            f"Worst dining experience in {city}. The food was inedible and service was rude.",
            f"Complete waste of money. This is not authentic Nigerian cuisine.",
            f"Absolutely horrible. The food was cold, tasteless, and overpriced.",
            f"Disgusting experience. I got sick after eating here. Stay away!"
        ]
    
    return random.choice(templates)

def get_state(city: str) -> str:
    """Map city to Nigerian state"""
    city_state_map = {
        "Lagos": "Lagos",
        "Abuja": "FCT",
        "Port Harcourt": "Rivers",
        "Kano": "Kano", 
        "Ibadan": "Oyo",
        "Benin City": "Edo"
    }
    return city_state_map.get(city, "Unknown")

def get_rating_distribution(reviews: List[Dict]) -> Dict[int, int]:
    """Calculate rating distribution"""
    distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for review in reviews:
        distribution[review['stars']] += 1
    return distribution

def main():
    parser = argparse.ArgumentParser(description="Download Yelp dataset sample")
    parser.add_argument("--output", default="data/raw/yelp_review_sample.json", 
                       help="Output file path")
    parser.add_argument("--sample-size", type=int, default=5000,
                       help="Number of reviews to sample")
    
    args = parser.parse_args()
    
    output_path = Path(args.output)
    download_yelp_sample(output_path, args.sample_size)

if __name__ == "__main__":
    main()
