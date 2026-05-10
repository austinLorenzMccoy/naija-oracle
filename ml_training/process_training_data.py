#!/usr/bin/env python3
"""
Process training data for ML pipeline
Combines Yelp reviews, personas, and CVI into training format
"""

import json
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_training_data(
    reviews_path: Path, 
    personas_path: Path, 
    cvi_path: Path,
    output_dir: Path
) -> None:
    """Process raw data into training format"""
    
    logger.info("Processing training data...")
    
    # Load data
    with open(reviews_path, 'r') as f:
        reviews = json.load(f)
    
    with open(personas_path, 'r') as f:
        personas = json.load(f)
    
    with open(cvi_path, 'r') as f:
        cvi = json.load(f)
    
    # Create training examples
    training_examples = []
    
    for i, review in enumerate(reviews):
        # Assign a persona to this review
        persona = personas[i % len(personas)]
        
        # Create training example
        example = create_training_example(review, persona, cvi)
        training_examples.append(example)
    
    # Split into train/test
    split_idx = int(len(training_examples) * 0.8)
    train_data = training_examples[:split_idx]
    test_data = training_examples[split_idx:]
    
    # Save processed data
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / 'training_data.json', 'w') as f:
        json.dump(train_data, f, indent=2)
    
    with open(output_dir / 'test_data.json', 'w') as f:
        json.dump(test_data, f, indent=2)
    
    # Save statistics
    stats = {
        'total_examples': len(training_examples),
        'train_examples': len(train_data),
        'test_examples': len(test_data),
        'num_personas': len(personas),
        'cvi_entries': len(cvi),
        'avg_rating': np.mean([ex['rating'] for ex in training_examples])
    }
    
    with open(output_dir / 'stats.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    # Save DVC metrics
    metrics_path = Path('metrics/data_processing_stats.json')
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(metrics_path, 'w') as f:
        json.dump(stats, f, indent=2)
    
    logger.info(f"Processed {len(training_examples)} examples")
    logger.info(f"Train: {len(train_data)}, Test: {len(test_data)}")

def create_training_example(review: Dict, persona: Dict, cvi: List[Dict]) -> Dict:
    """Create a training example from review and persona"""
    
    return {
        'review_id': review['review_id'],
        'user_id': review['user_id'],
        'business_id': review['business_id'],
        'rating': review['stars'],
        'review_text': review['text'],
        'persona': persona,
        'features': extract_features(review, persona, cvi)
    }

def extract_features(review: Dict, persona: Dict, cvi: List[Dict]) -> Dict:
    """Extract features for ML training"""
    
    return {
        'persona_features': extract_persona_features(persona),
        'review_features': extract_review_features(review),
        'cvi_features': extract_cvi_features(review['text'], cvi)
    }

def extract_persona_features(persona: Dict) -> List[float]:
    """Extract persona features"""
    
    # Age encoding
    age_encoding = {
        '18-24': [1, 0, 0, 0, 0],
        '25-34': [0, 1, 0, 0, 0],
        '35-44': [0, 0, 1, 0, 0],
        '45-54': [0, 0, 0, 1, 0],
        '55+': [0, 0, 0, 0, 1]
    }
    
    # Gender encoding
    gender_encoding = {
        'Male': [1, 0],
        'Female': [0, 1]
    }
    
    # Tribe encoding
    tribe_encoding = {
        'Yoruba': [1, 0, 0],
        'Igbo': [0, 1, 0],
        'Hausa': [0, 0, 1]
    }
    
    # Income encoding
    income_encoding = {
        'Low': [1, 0, 0],
        'Medium': [0, 1, 0],
        'High': [0, 0, 1]
    }
    
    features = []
    features.extend(age_encoding.get(persona['age_range'], [0, 0, 0, 0, 0]))
    features.extend(gender_encoding.get(persona['gender'], [0, 0]))
    features.extend(tribe_encoding.get(persona['tribe'], [0, 0, 0]))
    features.extend(income_encoding.get(persona['income_bracket'], [0, 0, 0]))
    features.append(persona['pidgin_intensity'])
    features.append(persona['tech_savviness'])
    
    return features

def extract_review_features(review: Dict) -> List[float]:
    """Extract review features"""
    
    business_info = review.get('business_info', {})
    
    features = [
        business_info.get('stars', 3.0) / 5.0,  # Normalized rating
        min(business_info.get('review_count', 50) / 500, 1.0),  # Normalized review count
        1 if 'Nigerian' in str(business_info.get('categories', [])) else 0,
        1 if 'Restaurant' in str(business_info.get('categories', [])) else 0,
        1 if business_info.get('city') == 'Lagos' else 0,
        1 if business_info.get('city') == 'Abuja' else 0,
        review.get('useful', 0) / 50.0,  # Normalized useful count
        len(review.get('text', '')) / 500.0  # Normalized text length
    ]
    
    return features

def extract_cvi_features(review_text: str, cvi: List[Dict]) -> List[float]:
    """Extract CVI features from review text"""
    
    text_lower = review_text.lower()
    
    # Count CVI phrases
    cvi_count = 0
    cvi_intensity_sum = 0.0
    
    for entry in cvi:
        if entry['phrase'].lower() in text_lower:
            cvi_count += 1
            cvi_intensity_sum += entry['pidgin_intensity']
    
    # Calculate features
    total_phrases = len(cvi)
    cvi_density = cvi_count / max(len(text_lower.split()), 1)
    avg_intensity = cvi_intensity_sum / max(cvi_count, 1)
    
    features = [
        cvi_count,
        cvi_density,
        avg_intensity,
        cvi_count / total_phrases  # Coverage ratio
    ]
    
    return features

def main():
    parser = argparse.ArgumentParser(description="Process training data")
    parser.add_argument("--reviews", default="data/raw/yelp_review_sample.json", help="Reviews data path")
    parser.add_argument("--personas", default="data/processed/personas.json", help="Personas data path")
    parser.add_argument("--cvi", default="data/processed/cvi.json", help="CVI data path")
    parser.add_argument("--output", default="data/processed", help="Output directory")
    
    args = parser.parse_args()
    
    process_training_data(
        Path(args.reviews),
        Path(args.personas), 
        Path(args.cvi),
        Path(args.output)
    )

if __name__ == "__main__":
    main()
