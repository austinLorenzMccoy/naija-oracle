"""
Training script for Recommendation Engine (Task B)
Trains ranking models and evaluation metrics
"""

import os
import json
import argparse
from datetime import datetime
from typing import Dict, List, Any, Tuple
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import ndcg_score
import mlflow
import mlflow.pytorch
from tqdm import tqdm

class RecommendationDataset(Dataset):
    """Dataset for recommendation ranking"""
    
    def __init__(self, features: np.ndarray, labels: np.ndarray):
        self.features = torch.FloatTensor(features)
        self.labels = torch.FloatTensor(labels)
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

class RecommendationRanker(nn.Module):
    """Neural network for recommendation ranking"""
    
    def __init__(self, input_dim: int, hidden_dims: List[int] = [256, 128, 64]):
        super().__init__()
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.2)
            ])
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, 1))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x).squeeze(-1)

class RecommendationEngineTrainer:
    """Trainer for Task B - Recommendation Engine"""
    
    def __init__(self):
        self.model = None
        self.feature_columns = [
            'user_rating_tendency',
            'item_avg_rating',
            'price_match_score',
            'location_proximity',
            'category_preference',
            'time_relevance',
            'mood_alignment',
            'budget_fit',
            'collaborative_score',
            'popularity_score'
        ]
        
        # MLflow experiment
        self.experiment_name = "naija_oracle_task_b"
        mlflow.set_experiment(self.experiment_name)
    
    def generate_training_data(self, num_samples: int = 10000) -> pd.DataFrame:
        """Generate synthetic recommendation training data"""
        print(f"Generating {num_samples} training samples...")
        
        data = []
        
        for _ in range(num_samples):
            # User features
            user_rating_tendency = np.random.uniform(2.0, 5.0)
            user_budget = np.random.uniform(1000, 20000)
            user_location_type = np.random.choice(['island', 'mainland', 'suburban'])
            user_mood = np.random.choice(['celebratory', 'casual', 'romantic', 'professional'])
            
            # Item features
            item_avg_rating = np.random.uniform(2.0, 5.0)
            item_price_tier = np.random.choice(['budget', 'mid', 'premium', 'luxury'])
            item_category = np.random.choice(['food', 'fashion', 'entertainment', 'tech'])
            item_location_type = np.random.choice(['island', 'mainland', 'suburban'])
            
            # Context features
            time_of_day = np.random.choice(['morning', 'afternoon', 'evening', 'night'])
            current_budget = np.random.uniform(1000, 20000)
            
            # Calculate derived features
            price_match_score = self._calculate_price_match(item_price_tier, current_budget)
            location_proximity = self._calculate_location_proximity(user_location_type, item_location_type)
            category_preference = self._calculate_category_preference(user_mood, item_category)
            time_relevance = self._calculate_time_relevance(item_category, time_of_day)
            mood_alignment = self._calculate_mood_alignment(user_mood, item_category, item_price_tier)
            budget_fit = 1.0 if current_budget >= self._get_min_price(item_price_tier) else 0.0
            
            # Simulated collaborative filtering score
            collaborative_score = np.random.uniform(0.0, 1.0)
            
            # Popularity score
            popularity_score = np.random.uniform(0.0, 1.0)
            
            # Target: relevance score (0-1)
            relevance_score = self._calculate_relevance_score(
                user_rating_tendency, item_avg_rating, price_match_score,
                location_proximity, category_preference, mood_alignment
            )
            
            data.append({
                'user_rating_tendency': user_rating_tendency,
                'item_avg_rating': item_avg_rating,
                'price_match_score': price_match_score,
                'location_proximity': location_proximity,
                'category_preference': category_preference,
                'time_relevance': time_relevance,
                'mood_alignment': mood_alignment,
                'budget_fit': budget_fit,
                'collaborative_score': collaborative_score,
                'popularity_score': popularity_score,
                'relevance_score': relevance_score
            })
        
        return pd.DataFrame(data)
    
    def _calculate_price_match(self, price_tier: str, budget: float) -> float:
        """Calculate price match score"""
        tier_prices = {
            'budget': (500, 3000),
            'mid': (3000, 8000),
            'premium': (8000, 20000),
            'luxury': (20000, 100000)
        }
        
        min_price, max_price = tier_prices[price_tier]
        
        if budget < min_price:
            return 0.0
        elif budget > max_price * 2:
            return 0.5  # Can afford much better
        else:
            # Ideal range
            return min(1.0, budget / max_price)
    
    def _calculate_location_proximity(self, user_loc: str, item_loc: str) -> float:
        """Calculate location proximity score"""
        if user_loc == item_loc:
            return 1.0
        elif (user_loc == 'island' and item_loc == 'mainland') or (user_loc == 'mainland' and item_loc == 'island'):
            return 0.3  # Cross traffic considerations
        else:
            return 0.7
    
    def _calculate_category_preference(self, mood: str, category: str) -> float:
        """Calculate category preference based on mood"""
        mood_category_map = {
            'celebratory': {'food': 0.9, 'entertainment': 0.8, 'fashion': 0.7, 'tech': 0.4},
            'casual': {'food': 0.8, 'entertainment': 0.6, 'fashion': 0.5, 'tech': 0.6},
            'romantic': {'food': 0.9, 'entertainment': 0.7, 'fashion': 0.6, 'tech': 0.3},
            'professional': {'food': 0.6, 'entertainment': 0.4, 'fashion': 0.7, 'tech': 0.8}
        }
        
        return mood_category_map.get(mood, {}).get(category, 0.5)
    
    def _calculate_time_relevance(self, category: str, time: str) -> float:
        """Calculate time relevance for category"""
        time_category_map = {
            'morning': {'food': 0.9, 'fashion': 0.6, 'entertainment': 0.3, 'tech': 0.7},
            'afternoon': {'food': 0.7, 'fashion': 0.7, 'entertainment': 0.5, 'tech': 0.8},
            'evening': {'food': 0.9, 'entertainment': 0.9, 'fashion': 0.6, 'tech': 0.4},
            'night': {'food': 0.8, 'entertainment': 0.8, 'fashion': 0.3, 'tech': 0.2}
        }
        
        return time_category_map.get(time, {}).get(category, 0.5)
    
    def _calculate_mood_alignment(self, mood: str, category: str, price_tier: str) -> float:
        """Calculate mood alignment score"""
        mood_price_map = {
            'celebratory': {'budget': 0.4, 'mid': 0.7, 'premium': 0.9, 'luxury': 0.8},
            'casual': {'budget': 0.8, 'mid': 0.9, 'premium': 0.6, 'luxury': 0.3},
            'romantic': {'budget': 0.3, 'mid': 0.7, 'premium': 0.9, 'luxury': 0.8},
            'professional': {'budget': 0.5, 'mid': 0.8, 'premium': 0.8, 'luxury': 0.6}
        }
        
        price_score = mood_price_map.get(mood, {}).get(price_tier, 0.5)
        category_score = self._calculate_category_preference(mood, category)
        
        return (price_score + category_score) / 2
    
    def _get_min_price(self, price_tier: str) -> float:
        """Get minimum price for tier"""
        tier_prices = {
            'budget': 500,
            'mid': 3000,
            'premium': 8000,
            'luxury': 20000
        }
        return tier_prices[price_tier]
    
    def _calculate_relevance_score(self, *features) -> float:
        """Calculate final relevance score"""
        # Weighted combination of features
        weights = [0.2, 0.15, 0.15, 0.1, 0.1, 0.05, 0.1, 0.05, 0.05, 0.05]
        
        score = sum(w * f for w, f in zip(weights, features))
        
        # Add some noise and non-linearity
        score = np.tanh(score * 2) * 0.5 + 0.5
        
        return np.clip(score, 0.0, 1.0)
    
    def prepare_data(self, data_path: str = None) -> Tuple[DataLoader, DataLoader]:
        """Prepare training and validation data"""
        if data_path and os.path.exists(data_path):
            df = pd.read_csv(data_path)
        else:
            df = self.generate_training_data()
            if data_path:
                df.to_csv(data_path, index=False)
        
        # Split features and labels
        features = df[self.feature_columns].values
        labels = df['relevance_score'].values
        
        # Train-test split
        X_train, X_val, y_train, y_val = train_test_split(
            features, labels, test_size=0.2, random_state=42
        )
        
        # Create datasets
        train_dataset = RecommendationDataset(X_train, y_train)
        val_dataset = RecommendationDataset(X_val, y_val)
        
        # Create data loaders
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        
        return train_loader, val_loader
    
    def train_model(self, train_loader: DataLoader, val_loader: DataLoader, 
                   num_epochs: int = 50, learning_rate: float = 0.001):
        """Train the recommendation ranking model"""
        print("Starting model training...")
        
        # Initialize model
        input_dim = len(self.feature_columns)
        self.model = RecommendationRanker(input_dim)
        
        # Loss and optimizer
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)
        
        # Training loop
        with mlflow.start_run(run_name=f"recommendation_engine_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            # Log parameters
            mlflow.log_params({
                "input_dim": input_dim,
                "num_epochs": num_epochs,
                "learning_rate": learning_rate,
                "batch_size": 32
            })
            
            best_val_loss = float('inf')
            
            for epoch in range(num_epochs):
                # Training
                self.model.train()
                train_loss = 0.0
                
                for features, labels in train_loader:
                    optimizer.zero_grad()
                    outputs = self.model(features)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()
                    train_loss += loss.item()
                
                train_loss /= len(train_loader)
                
                # Validation
                self.model.eval()
                val_loss = 0.0
                
                with torch.no_grad():
                    for features, labels in val_loader:
                        outputs = self.model(features)
                        loss = criterion(outputs, labels)
                        val_loss += loss.item()
                
                val_loss /= len(val_loader)
                
                # Learning rate scheduling
                scheduler.step(val_loss)
                
                # Log metrics
                mlflow.log_metrics({
                    "train_loss": train_loss,
                    "val_loss": val_loss,
                    "learning_rate": optimizer.param_groups[0]['lr']
                }, step=epoch)
                
                print(f"Epoch {epoch+1}/{num_epochs}: Train Loss = {train_loss:.4f}, Val Loss = {val_loss:.4f}")
                
                # Save best model
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    torch.save(self.model.state_dict(), "models/recommendation_ranker_best.pth")
            
            # Evaluate final model
            metrics = self.evaluate_model(val_loader)
            mlflow.log_metrics(metrics)
            
            # Log model to MLflow
            mlflow.pytorch.log_model(
                self.model,
                "model",
                registered_model_name="naija_oracle_recommendation_engine"
            )
            
            print(f"Training completed. Best validation loss: {best_val_loss:.4f}")
            print(f"NDCG@10: {metrics['ndcg_at_10']:.4f}")
    
    def evaluate_model(self, data_loader: DataLoader) -> Dict[str, float]:
        """Evaluate model with ranking metrics"""
        self.model.eval()
        
        all_predictions = []
        all_labels = []
        
        with torch.no_grad():
            for features, labels in data_loader:
                outputs = self.model(features)
                all_predictions.extend(outputs.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        # Calculate NDCG@10
        # Group predictions into lists of 10 (simulating recommendation lists)
        ndcg_scores = []
        for i in range(0, len(all_predictions), 10):
            if i + 10 <= len(all_predictions):
                pred_list = all_predictions[i:i+10]
                true_list = all_labels[i:i+10]
                
                # Reshape for ndcg_score
                pred_2d = np.array([pred_list])
                true_2d = np.array([true_list])
                
                ndcg = ndcg_score(true_2d, pred_2d, k=10)
                ndcg_scores.append(ndcg)
        
        avg_ndcg = np.mean(ndcg_scores) if ndcg_scores else 0.0
        
        # Calculate other metrics
        mse = np.mean((np.array(all_predictions) - np.array(all_labels)) ** 2)
        mae = np.mean(np.abs(np.array(all_predictions) - np.array(all_labels)))
        
        return {
            "ndcg_at_10": avg_ndcg,
            "mse": mse,
            "mae": mae
        }
    
    def save_model(self, path: str):
        """Save trained model"""
        if self.model:
            torch.save(self.model.state_dict(), path)
            print(f"Model saved to {path}")
    
    def load_model(self, path: str, input_dim: int = None):
        """Load trained model"""
        if input_dim is None:
            input_dim = len(self.feature_columns)
        
        self.model = RecommendationRanker(input_dim)
        self.model.load_state_dict(torch.load(path, map_location='cpu'))
        self.model.eval()
        print(f"Model loaded from {path}")

def main():
    parser = argparse.ArgumentParser(description="Train Recommendation Engine")
    parser.add_argument("--data", type=str, default="data/recommendation_training_data.csv", help="Training data path")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    parser.add_argument("--eval-only", action="store_true", help="Only run evaluation")
    parser.add_argument("--model-path", type=str, default="models/recommendation_ranker_best.pth", help="Model path for evaluation")
    
    args = parser.parse_args()
    
    trainer = RecommendationEngineTrainer()
    
    if args.eval_only:
        # Load model and evaluate
        trainer.load_model(args.model_path)
        _, val_loader = trainer.prepare_data(args.data)
        metrics = trainer.evaluate_model(val_loader)
        print(f"Evaluation Results: {metrics}")
    else:
        # Full training pipeline
        train_loader, val_loader = trainer.prepare_data(args.data)
        trainer.train_model(train_loader, val_loader, args.epochs, args.lr)
        trainer.save_model(args.model_path)

if __name__ == "__main__":
    main()
