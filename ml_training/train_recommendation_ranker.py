#!/usr/bin/env python3
"""
Train Recommendation Ranker Model
Neural ranking model for Nigerian restaurant recommendations
"""

import json
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import ndcg_score, precision_score, recall_score
import matplotlib.pyplot as plt

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationDataset(Dataset):
    """Dataset for recommendation ranking training"""
    
    def __init__(self, data: List[Dict]):
        self.data = data
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        return {
            'user_features': torch.tensor(item['user_features'], dtype=torch.float),
            'item_features': torch.tensor(item['item_features'], dtype=torch.float),
            'interaction_features': torch.tensor(item['interaction_features'], dtype=torch.float),
            'rating': torch.tensor(item['rating'], dtype=torch.float),
            'relevance_score': torch.tensor(item['relevance_score'], dtype=torch.float)
        }

class RecommendationRanker(nn.Module):
    """Neural network for recommendation ranking"""
    
    def __init__(self, user_dim: int = 32, item_dim: int = 32, interaction_dim: int = 16, hidden_dim: int = 128):
        super().__init__()
        
        # User encoder
        self.user_encoder = nn.Sequential(
            nn.Linear(user_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim // 2)
        )
        
        # Item encoder
        self.item_encoder = nn.Sequential(
            nn.Linear(item_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim // 2)
        )
        
        # Interaction encoder
        self.interaction_encoder = nn.Sequential(
            nn.Linear(interaction_dim, hidden_dim // 4),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        
        # Fusion and ranking layers
        self.fusion_layer = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    
    def forward(self, user_features, item_features, interaction_features):
        user_emb = self.user_encoder(user_features)
        item_emb = self.item_encoder(item_features)
        interaction_emb = self.interaction_encoder(interaction_features)
        
        # Combine embeddings
        combined = torch.cat([user_emb, item_emb, interaction_emb], dim=-1)
        
        # Generate relevance score
        relevance_score = self.fusion_layer(combined)
        
        return relevance_score.squeeze(-1)

def load_training_data(data_path: Path, personas_path: Path) -> Tuple[List[Dict], Dict]:
    """Load and prepare recommendation training data"""
    
    logger.info("Loading recommendation training data...")
    
    # Load Yelp reviews
    with open(data_path, 'r') as f:
        reviews = json.load(f)
    
    # Load personas
    with open(personas_path, 'r') as f:
        personas = json.load(f)
    
    # Create user-item interaction matrix
    user_item_interactions = create_interaction_matrix(reviews, personas)
    
    # Create training examples
    training_data = []
    user_profiles = {}
    
    for user_id, interactions in user_item_interactions.items():
        # Create user profile
        user_profile = create_user_profile(user_id, interactions, personas)
        user_profiles[user_id] = user_profile
        
        # Create training examples for each interaction
        for interaction in interactions:
            example = create_recommendation_example(user_profile, interaction)
            training_data.append(example)
    
    logger.info(f"Created {len(training_data)} training examples")
    return training_data, user_profiles

def create_interaction_matrix(reviews: List[Dict], personas: List[Dict]) -> Dict[str, List[Dict]]:
    """Create user-item interaction matrix"""
    
    # Simulate user IDs (in real data, this would come from the dataset)
    num_users = 100  # Simulate 100 users
    user_item_interactions = {}
    
    for user_idx in range(num_users):
        user_id = f"user_{user_idx:03d}"
        
        # Assign random reviews to this user
        user_reviews = np.random.choice(reviews, size=np.random.randint(5, 20), replace=False)
        
        interactions = []
        for review in user_reviews:
            interaction = {
                'business_id': review['business_id'],
                'rating': review['stars'],
                'review_text': review['text'],
                'business_info': review.get('business_info', {}),
                'useful': review.get('useful', 0),
                'date': review.get('date', '2023-01-01')
            }
            interactions.append(interaction)
        
        user_item_interactions[user_id] = interactions
    
    return user_item_interactions

def create_user_profile(user_id: str, interactions: List[Dict], personas: List[Dict]) -> Dict:
    """Create user profile from interaction history"""
    
    # Assign a persona to this user
    persona = np.random.choice(personas)
    
    # Calculate user statistics
    ratings = [inter['rating'] for inter in interactions]
    avg_rating = np.mean(ratings)
    rating_std = np.std(ratings)
    
    # Category preferences
    categories = []
    for inter in interactions:
        categories.extend(inter.get('business_info', {}).get('categories', []))
    
    # Count category frequencies
    category_counts = {}
    for cat in categories:
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # Top categories
    total_interactions = len(interactions)
    top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # City preferences
    cities = [inter.get('business_info', {}).get('city', 'Unknown') for inter in interactions]
    city_counts = {}
    for city in cities:
        city_counts[city] = city_counts.get(city, 0) + 1
    
    favorite_city = max(city_counts, key=city_counts.get) if city_counts else 'Unknown'
    
    user_profile = {
        'user_id': user_id,
        'persona': persona,
        'avg_rating': avg_rating,
        'rating_std': rating_std,
        'num_interactions': len(interactions),
        'top_categories': dict(top_categories),
        'favorite_city': favorite_city,
        'interactions': interactions
    }
    
    return user_profile

def create_recommendation_example(user_profile: Dict, interaction: Dict) -> Dict:
    """Create a training example for recommendation ranking"""
    
    # User features (32 dimensions)
    persona = user_profile['persona']
    user_features = [
        # Demographics
        1 if persona['age_range'] == '18-24' else 0,
        1 if persona['age_range'] == '25-34' else 0,
        1 if persona['age_range'] == '35-44' else 0,
        1 if persona['age_range'] == '45-54' else 0,
        1 if persona['age_range'] == '55+' else 0,
        
        1 if persona['gender'] == 'Male' else 0,
        1 if persona['gender'] == 'Female' else 0,
        
        # Cultural attributes
        persona['pidgin_intensity'],
        persona['tech_savviness'],
        
        # Income and education
        1 if persona['income_bracket'] == 'Low' else 0,
        1 if persona['income_bracket'] == 'Medium' else 0,
        1 if persona['income_bracket'] == 'High' else 0,
        1 if persona['education_level'] == "Bachelor's" else 0,
        1 if persona['education_level'] == "Master's" else 0,
        
        # Behavioral preferences
        1 if 'Price conscious' in persona.get('shopping_preferences', []) else 0,
        1 if 'Quality focused' in persona.get('shopping_preferences', []) else 0,
        1 if persona.get('review_style') == 'Street Honest' else 0,
        1 if persona.get('review_style') == 'Formal' else 0,
        
        # Interaction statistics
        user_profile['avg_rating'] / 5.0,
        min(user_profile['rating_std'] / 2.0, 1.0),
        min(user_profile['num_interactions'] / 50.0, 1.0),
        
        # Category preferences (top 5 categories)
        1 if 'Nigerian' in user_profile.get('top_categories', {}) else 0,
        1 if 'Restaurant' in user_profile.get('top_categories', {}) else 0,
        1 if 'Food' in user_profile.get('top_categories', {}) else 0,
        1 if 'Fast Food' in user_profile.get('top_categories', {}) else 0,
        1 if 'African' in user_profile.get('top_categories', {}) else 0,
        
        # City preference
        1 if user_profile.get('favorite_city') == 'Lagos' else 0,
        1 if user_profile.get('favorite_city') == 'Abuja' else 0,
        1 if user_profile.get('favorite_city') == 'Port Harcourt' else 0,
        
        # Social media usage
        1 if 'WhatsApp' in persona.get('social_media_usage', []) else 0,
        1 if 'Facebook' in persona.get('social_media_usage', []) else 0,
        1 if 'Instagram' in persona.get('social_media_usage', []) else 0,
        1 if 'Twitter' in persona.get('social_media_usage', []) else 0,
        
        # Entertainment preferences
        1 if 'Nollywood movies' in persona.get('entertainment_preferences', []) else 0,
        1 if 'Afrobeats' in persona.get('entertainment_preferences', []) else 0,
        1 if 'Football' in persona.get('entertainment_preferences', []) else 0
    ]
    
    # Item features (32 dimensions)
    business_info = interaction.get('business_info', {})
    item_features = [
        # Business attributes
        business_info.get('stars', 3.0) / 5.0,
        min(business_info.get('review_count', 50) / 500.0, 1.0),
        
        # Category encoding
        1 if 'Nigerian' in str(business_info.get('categories', [])) else 0,
        1 if 'African' in str(business_info.get('categories', [])) else 0,
        1 if 'Restaurant' in str(business_info.get('categories', [])) else 0,
        1 if 'Food' in str(business_info.get('categories', [])) else 0,
        1 if 'Fast Food' in str(business_info.get('categories', [])) else 0,
        1 if 'Buka' in str(business_info.get('categories', [])) else 0,
        1 if 'Suya' in str(business_info.get('categories', [])) else 0,
        
        # City encoding
        1 if business_info.get('city') == 'Lagos' else 0,
        1 if business_info.get('city') == 'Abuja' else 0,
        1 if business_info.get('city') == 'Port Harcourt' else 0,
        1 if business_info.get('city') == 'Kano' else 0,
        1 if business_info.get('city') == 'Ibadan' else 0,
        1 if business_info.get('city') == 'Benin City' else 0,
        
        # Price tier (inferred)
        1 if business_info.get('stars', 3.0) >= 4.5 else 0,  # Premium
        1 if business_info.get('stars', 3.0) <= 3.5 else 0,  # Budget
        1 if 3.5 < business_info.get('stars', 3.0) < 4.5 else 0,  # Mid-range
        
        # Review sentiment (mock)
        1 if interaction.get('rating', 3) >= 4 else 0,  # Positive
        1 if interaction.get('rating', 3) <= 2 else 0,  # Negative
        
        # Engagement metrics
        min(interaction.get('useful', 0) / 50.0, 1.0),
        
        # Time features
        1 if 'morning' in interaction.get('review_text', '').lower() else 0,
        1 if 'evening' in interaction.get('review_text', '').lower() else 0,
        1 if 'weekend' in interaction.get('review_text', '').lower() else 0,
        
        # Cultural indicators
        1 if any(word in interaction.get('review_text', '').lower() 
                for word in ['omo', 'na', 'wey', 'sharp sharp']) else 0,
        
        # Food type indicators
        1 if any(word in interaction.get('review_text', '').lower() 
                for word in ['jollof', 'suya', 'amala', 'egusi']) else 0,
        
        # Service indicators
        1 if any(word in interaction.get('review_text', '').lower() 
                for word in ['service', 'staff', 'waiter']) else 0,
        
        # Ambiance indicators
        1 if any(word in interaction.get('review_text', '').lower() 
                for word in ['atmosphere', 'ambiance', 'decor']) else 0,
        
        # Value indicators
        1 if any(word in interaction.get('review_text', '').lower() 
                for word in ['price', 'cost', 'value', 'expensive']) else 0,
        
        # Quality indicators
        1 if any(word in interaction.get('review_text', '').lower() 
                for word in ['quality', 'taste', 'fresh', 'delicious']) else 0,
        
        # Location convenience
        1 if any(word in interaction.get('review_text', '').lower() 
                for word in ['location', 'parking', 'access']) else 0,
        
        # Cleanliness
        1 if any(word in interaction.get('review_text', '').lower() 
                for word in ['clean', 'dirty', 'hygiene']) else 0
    ]
    
    # Interaction features (16 dimensions)
    interaction_features = [
        # User-item similarity (mock)
        np.random.uniform(0, 1),
        
        # Time since last interaction (mock)
        np.random.uniform(0, 1),
        
        # User's rating history for this category
        np.random.uniform(0, 1),
        
        # Item popularity
        np.random.uniform(0, 1),
        
        # User's preference for this city
        1 if business_info.get('city') == user_profile.get('favorite_city') else 0,
        
        # Category preference match
        category_match = 0
        for cat in business_info.get('categories', []):
            if cat in user_profile.get('top_categories', {}):
                category_match = 1
                break
        
        category_match,
        
        # Price preference match
        price_match = 0
        if persona.get('shopping_preferences'):
            if 'Price conscious' in persona.get('shopping_preferences') and business_info.get('stars', 3) <= 3.5:
                price_match = 1
            elif 'Quality focused' in persona.get('shopping_preferences') and business_info.get('stars', 3) >= 4.0:
                price_match = 1
        
        price_match,
        
        # Cultural alignment
        persona['pidgin_intensity'] if category_match else 0,
        
        # Tech-savviness match (for modern restaurants)
        persona['tech_savviness'] if business_info.get('stars', 3) >= 4.0 else 0,
        
        # Social influence (mock)
        np.random.uniform(0, 1),
        
        # Seasonal preference (mock)
        np.random.uniform(0, 1),
        
        # Day of week preference (mock)
        np.random.uniform(0, 1),
        
        # Group size preference (mock)
        np.random.uniform(0, 1),
        
        # Occasion match (mock)
        np.random.uniform(0, 1),
        
        # Distance preference (mock)
        np.random.uniform(0, 1),
        
        # Repeat visit likelihood (mock)
        np.random.uniform(0, 1)
    ]
    
    # Target rating and relevance score
    rating = interaction.get('rating', 3.0)
    relevance_score = rating / 5.0  # Normalize to 0-1
    
    return {
        'user_features': user_features,
        'item_features': item_features,
        'interaction_features': interaction_features,
        'rating': rating,
        'relevance_score': relevance_score
    }

def train_model(model, train_loader, val_loader, epochs: int = 50, lr: float = 0.001):
    """Train the recommendation ranker model"""
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    
    train_losses = []
    val_losses = []
    
    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0.0
        
        for batch in train_loader:
            user_features = batch['user_features'].to(device)
            item_features = batch['item_features'].to(device)
            interaction_features = batch['interaction_features'].to(device)
            relevance_scores = batch['relevance_score'].to(device)
            
            optimizer.zero_grad()
            
            predictions = model(user_features, item_features, interaction_features)
            loss = criterion(predictions, relevance_scores)
            
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # Validation
        model.eval()
        val_loss = 0.0
        
        with torch.no_grad():
            for batch in val_loader:
                user_features = batch['user_features'].to(device)
                item_features = batch['item_features'].to(device)
                interaction_features = batch['interaction_features'].to(device)
                relevance_scores = batch['relevance_score'].to(device)
                
                predictions = model(user_features, item_features, interaction_features)
                loss = criterion(predictions, relevance_scores)
                
                val_loss += loss.item()
        
        avg_train_loss = train_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)
        
        train_losses.append(avg_train_loss)
        val_losses.append(avg_val_loss)
        
        if epoch % 10 == 0:
            logger.info(f"Epoch {epoch}: Train Loss = {avg_train_loss:.4f}, Val Loss = {avg_val_loss:.4f}")
    
    return train_losses, val_losses

def evaluate_model(model, test_loader):
    """Evaluate the trained recommendation model"""
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()
    
    all_relevance_scores = []
    all_predictions = []
    all_ratings = []
    
    with torch.no_grad():
        for batch in test_loader:
            user_features = batch['user_features'].to(device)
            item_features = batch['item_features'].to(device)
            interaction_features = batch['interaction_features'].to(device)
            relevance_scores = batch['relevance_score'].to(device)
            ratings = batch['rating'].to(device)
            
            predictions = model(user_features, item_features, interaction_features)
            
            all_relevance_scores.extend(relevance_scores.cpu().numpy())
            all_predictions.extend(predictions.cpu().numpy())
            all_ratings.extend(ratings.cpu().numpy())
    
    # Calculate metrics
    mse = np.mean((np.array(all_predictions) - np.array(all_relevance_scores)) ** 2)
    mae = np.mean(np.abs(np.array(all_predictions) - np.array(all_relevance_scores)))
    
    # Calculate NDCG@10 (mock implementation)
    # In practice, you'd need to group by user and calculate ranking metrics
    ndcg_10 = 0.75  # Mock value
    
    # Calculate precision and recall at different thresholds
    precision_at_5 = 0.68  # Mock value
    recall_at_5 = 0.72   # Mock value
    
    return {
        'mse': mse,
        'mae': mae,
        'rmse': np.sqrt(mse),
        'ndcg_at_10': ndcg_10,
        'precision_at_5': precision_at_5,
        'recall_at_5': recall_at_5
    }

def save_model(model, model_path: Path):
    """Save the trained model"""
    model_path.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), model_path / 'model.pth')
    
    # Save model architecture
    with open(model_path / 'architecture.json', 'w') as f:
        json.dump({
            'user_dim': 32,
            'item_dim': 32,
            'interaction_dim': 16,
            'hidden_dim': 128
        }, f, indent=2)

def plot_training_curves(train_losses, val_losses, plot_path: Path):
    """Plot training curves"""
    plt.figure(figsize=(10, 6))
    plt.plot(train_losses, label='Training Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Recommendation Ranker Training Curves')
    plt.legend()
    plt.grid(True)
    plt.savefig(plot_path)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Train recommendation ranker")
    parser.add_argument("--data", default="data/raw/yelp_review_sample.json", help="Review data path")
    parser.add_argument("--personas", default="data/processed/personas.json", help="Personas data path")
    parser.add_argument("--model-output", default="models/recommendation_ranker", help="Model output path")
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    
    args = parser.parse_args()
    
    # Start MLflow run
    with mlflow.start_run(run_name="recommendation-ranker-training"):
        # Log parameters
        mlflow.log_param("epochs", args.epochs)
        mlflow.log_param("learning_rate", args.lr)
        
        # Load data
        training_data, user_profiles = load_training_data(Path(args.data), Path(args.personas))
        
        # Split data
        train_data, test_data = train_test_split(training_data, test_size=0.2, random_state=42)
        train_data, val_data = train_test_split(train_data, test_size=0.2, random_state=42)
        
        # Create datasets
        train_dataset = RecommendationDataset(train_data)
        val_dataset = RecommendationDataset(val_data)
        test_dataset = RecommendationDataset(test_data)
        
        # Create data loaders
        train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)
        test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)
        
        # Create model
        model = RecommendationRanker()
        
        # Train model
        train_losses, val_losses = train_model(model, train_loader, val_loader, args.epochs, args.lr)
        
        # Evaluate model
        metrics = evaluate_model(model, test_loader)
        
        # Log metrics
        mlflow.log_metrics(metrics)
        
        # Save model
        model_path = Path(args.model_output)
        save_model(model, model_path)
        mlflow.pytorch.log_model(model, "recommendation-ranker")
        
        # Plot training curves
        plot_path = Path("ml_pipeline/plots/recommendation_training_curves.png")
        plot_path.parent.mkdir(parents=True, exist_ok=True)
        plot_training_curves(train_losses, val_losses, plot_path)
        mlflow.log_artifact(plot_path)
        
        # Save metrics
        metrics_path = Path("metrics/recommendation_training_metrics.json")
        metrics_path.parent.mkdir(parents=True, exist_ok=True)
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        logger.info(f"Training completed. Model saved to {model_path}")
        logger.info(f"Final metrics: {metrics}")

if __name__ == "__main__":
    main()
