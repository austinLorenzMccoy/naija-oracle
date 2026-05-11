#!/usr/bin/env python3
"""
Train Persona Simulator Model
Fine-tunes a model on Nigerian personas and review patterns
"""

import json
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonaDataset(Dataset):
    """Dataset for persona simulator training"""
    
    def __init__(self, data: List[Dict]):
        self.data = data
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        return {
            'persona_features': torch.tensor(item['persona_features'], dtype=torch.float),
            'product_features': torch.tensor(item['product_features'], dtype=torch.float),
            'context_features': torch.tensor(item['context_features'], dtype=torch.float),
            'rating': torch.tensor(item['rating'], dtype=torch.float),
            'review_embedding': torch.tensor(item['review_embedding'], dtype=torch.float)
        }

class PersonaSimulator(nn.Module):
    """Neural network for persona-based review simulation"""
    
    def __init__(self, input_dim: int = 64, hidden_dim: int = 128, output_dim: int = 384):
        super().__init__()
        
        self.persona_encoder = nn.Sequential(
            nn.Linear(19, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim // 2)
        )
        
        self.product_encoder = nn.Sequential(
            nn.Linear(14, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        
        self.context_encoder = nn.Sequential(
            nn.Linear(10, hidden_dim // 4),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        
        self.fusion_layer = nn.Sequential(
            nn.Linear(160, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        
        self.rating_head = nn.Sequential(
            nn.Linear(160, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    
    def forward(self, persona_features, product_features, context_features):
        persona_emb = self.persona_encoder(persona_features)
        product_emb = self.product_encoder(product_features)
        context_emb = self.context_encoder(context_features)
        
        # Fuse all features
        combined = torch.cat([persona_emb, product_emb, context_emb], dim=-1)
        fused = self.fusion_layer(combined)
        
        # Generate rating
        rating = self.rating_head(combined) * 4 + 1  # Scale to 1-5
        
        return fused, rating

def load_training_data(data_path: Path, personas_path: Path, cvi_path: Path) -> List[Dict]:
    """Load and prepare training data"""
    
    logger.info("Loading training data...")
    
    # Load Yelp reviews
    with open(data_path, 'r') as f:
        reviews = json.load(f)
    
    # Load personas
    with open(personas_path, 'r') as f:
        personas = json.load(f)
    
    # Load CVI
    with open(cvi_path, 'r') as f:
        cvi = json.load(f)
    
    # Create training examples
    training_data = []
    
    for review in reviews[:1000]:  # Limit for demo
        # Randomly assign a persona
        persona = np.random.choice(personas)
        
        # Extract features
        example = create_training_example(review, persona, cvi)
        training_data.append(example)
    
    logger.info(f"Created {len(training_data)} training examples")
    return training_data

def create_training_example(review: Dict, persona: Dict, cvi: List[Dict]) -> Dict:
    """Create a training example from review and persona"""
    
    # Persona features (20 dimensions)
    persona_features = [
        # Age encoding
        1 if persona['age_range'] == '18-24' else 0,
        1 if persona['age_range'] == '25-34' else 0,
        1 if persona['age_range'] == '35-44' else 0,
        1 if persona['age_range'] == '45-54' else 0,
        1 if persona['age_range'] == '55+' else 0,
        
        # Gender
        1 if persona['gender'] == 'Male' else 0,
        1 if persona['gender'] == 'Female' else 0,
        
        # Tribe encoding (major tribes)
        1 if persona['tribe'] == 'Yoruba' else 0,
        1 if persona['tribe'] == 'Igbo' else 0,
        1 if persona['tribe'] == 'Hausa' else 0,
        
        # Cultural attributes
        persona['pidgin_intensity'],
        persona['tech_savviness'],
        1 if persona['income_bracket'] == 'Low' else 0,
        1 if persona['income_bracket'] == 'Medium' else 0,
        1 if persona['income_bracket'] == 'High' else 0,
        
        # Education
        1 if persona['education_level'] == 'Secondary' else 0,
        1 if persona['education_level'] == "Bachelor's" else 0,
        1 if persona['education_level'] == "Master's" else 0,
        1 if persona['education_level'] == 'PhD' else 0
    ]
    
    # Product features (15 dimensions)
    business_info = review.get('business_info', {})
    product_features = [
        # Rating
        business_info.get('stars', 3.0) / 5.0,
        
        # Category encoding
        1 if 'Nigerian' in str(business_info.get('categories', [])) else 0,
        1 if 'African' in str(business_info.get('categories', [])) else 0,
        1 if 'Restaurant' in str(business_info.get('categories', [])) else 0,
        1 if 'Food' in str(business_info.get('categories', [])) else 0,
        1 if 'Fast Food' in str(business_info.get('categories', [])) else 0,
        
        # Review count (normalized)
        min(business_info.get('review_count', 50) / 500, 1.0),
        
        # City encoding (major cities)
        1 if business_info.get('city') == 'Lagos' else 0,
        1 if business_info.get('city') == 'Abuja' else 0,
        1 if business_info.get('city') == 'Port Harcourt' else 0,
        1 if business_info.get('city') == 'Kano' else 0,
        1 if business_info.get('city') == 'Ibadan' else 0,
        
        # Price tier (inferred from rating and category)
        1 if business_info.get('stars', 3.0) >= 4.0 else 0,  # Premium
        1 if business_info.get('stars', 3.0) <= 3.0 else 0   # Budget
    ]
    
    # Context features (10 dimensions)
    context_features = [
        # Time features
        1 if 'morning' in review.get('text', '').lower() else 0,
        1 if 'afternoon' in review.get('text', '').lower() else 0,
        1 if 'evening' in review.get('text', '').lower() else 0,
        1 if 'night' in review.get('text', '').lower() else 0,
        
        # Occasion
        1 if 'birthday' in review.get('text', '').lower() else 0,
        1 if 'weekend' in review.get('text', '').lower() else 0,
        1 if 'holiday' in review.get('text', '').lower() else 0,
        
        # Visit type
        1 if 'first time' in review.get('text', '').lower() else 0,
        1 if 'regular' in review.get('text', '').lower() else 0,
        1 if 'family' in review.get('text', '').lower() else 0
    ]
    
    # Target rating
    rating = review.get('stars', 3.0)
    
    # Mock review embedding (384 dimensions - would be from actual embedding model)
    review_embedding = np.random.normal(0, 0.1, 384)
    
    return {
        'persona_features': persona_features,
        'product_features': product_features,
        'context_features': context_features,
        'rating': rating,
        'review_embedding': review_embedding.tolist()
    }

def train_model(model, train_loader, val_loader, epochs: int = 50, lr: float = 0.001):
    """Train the persona simulator model"""
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion_rating = nn.MSELoss()
    criterion_embedding = nn.MSELoss()
    
    train_losses = []
    val_losses = []
    
    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0.0
        
        for batch in train_loader:
            persona_features = batch['persona_features'].to(device)
            product_features = batch['product_features'].to(device)
            context_features = batch['context_features'].to(device)
            ratings = batch['rating'].to(device)
            review_embeddings = batch['review_embedding'].to(device)
            
            optimizer.zero_grad()
            
            embedding_pred, rating_pred = model(persona_features, product_features, context_features)
            
            loss_rating = criterion_rating(rating_pred.squeeze(), ratings)
            loss_embedding = criterion_embedding(embedding_pred, review_embeddings)
            loss = loss_rating + 0.5 * loss_embedding
            
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # Validation
        model.eval()
        val_loss = 0.0
        
        with torch.no_grad():
            for batch in val_loader:
                persona_features = batch['persona_features'].to(device)
                product_features = batch['product_features'].to(device)
                context_features = batch['context_features'].to(device)
                ratings = batch['rating'].to(device)
                review_embeddings = batch['review_embedding'].to(device)
                
                embedding_pred, rating_pred = model(persona_features, product_features, context_features)
                
                loss_rating = criterion_rating(rating_pred.squeeze(), ratings)
                loss_embedding = criterion_embedding(embedding_pred, review_embeddings)
                loss = loss_rating + 0.5 * loss_embedding
                
                val_loss += loss.item()
        
        avg_train_loss = train_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)
        
        train_losses.append(avg_train_loss)
        val_losses.append(avg_val_loss)
        
        if epoch % 10 == 0:
            logger.info(f"Epoch {epoch}: Train Loss = {avg_train_loss:.4f}, Val Loss = {avg_val_loss:.4f}")
    
    return train_losses, val_losses

def evaluate_model(model, test_loader):
    """Evaluate the trained model"""
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()
    
    all_ratings = []
    all_predictions = []
    
    with torch.no_grad():
        for batch in test_loader:
            persona_features = batch['persona_features'].to(device)
            product_features = batch['product_features'].to(device)
            context_features = batch['context_features'].to(device)
            ratings = batch['rating'].to(device)
            
            _, rating_pred = model(persona_features, product_features, context_features)
            
            all_ratings.extend(ratings.cpu().numpy())
            all_predictions.extend(rating_pred.squeeze().cpu().numpy())
    
    mse = mean_squared_error(all_ratings, all_predictions)
    mae = mean_absolute_error(all_ratings, all_predictions)
    
    return {
        'mse': float(mse),
        'mae': float(mae),
        'rmse': float(np.sqrt(mse))
    }

def save_model(model, model_path: Path):
    """Save the trained model"""
    model_path.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), model_path / 'model.pth')
    
    # Save model architecture
    with open(model_path / 'architecture.json', 'w') as f:
        json.dump({
            'input_dim': 64,
            'hidden_dim': 128,
            'output_dim': 384
        }, f, indent=2)

def plot_training_curves(train_losses, val_losses, plot_path: Path):
    """Plot and save model"""
    plt.figure(figsize=(10, 6))
    plt.plot(train_losses, label='Training Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.title('Persona Simulator Training')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    plot_path = Path(plot_path)
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_path)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Train persona simulator")
    parser.add_argument("--data", default="data/processed/training_data.json", help="Training data path")
    parser.add_argument("--personas", default="data/processed/personas.json", help="Personas data path")
    parser.add_argument("--cvi", default="data/processed/cvi.json", help="CVI data path")
    parser.add_argument("--model-output", default="models/persona_simulator", help="Model output path")
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    
    args = parser.parse_args()
    
    # Start MLflow run
    with mlflow.start_run(run_name="persona-simulator-training"):
        # Log parameters
        mlflow.log_param("epochs", args.epochs)
        mlflow.log_param("learning_rate", args.lr)
        
        # Load data
        training_data = load_training_data(Path(args.data), Path(args.personas), Path(args.cvi))
        
        # Split data
        train_data, test_data = train_test_split(training_data, test_size=0.2, random_state=42)
        train_data, val_data = train_test_split(train_data, test_size=0.2, random_state=42)
        
        # Create datasets
        train_dataset = PersonaDataset(train_data)
        val_dataset = PersonaDataset(val_data)
        test_dataset = PersonaDataset(test_data)
        
        # Create data loaders
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
        
        # Create model
        model = PersonaSimulator()
        
        # Train model
        train_losses, val_losses = train_model(model, train_loader, val_loader, args.epochs, args.lr)
        
        # Evaluate model
        metrics = evaluate_model(model, test_loader)
        
        # Log metrics
        mlflow.log_metrics(metrics)
        
        # Save model
        model_path = Path(args.model_output)
        save_model(model, model_path)
        mlflow.pytorch.log_model(model, "persona-simulator")
        
        # Plot training curves
        plot_path = Path("ml_pipeline/plots/persona_training_curves.png")
        plot_path.parent.mkdir(parents=True, exist_ok=True)
        plot_training_curves(train_losses, val_losses, plot_path)
        mlflow.log_artifact(plot_path)
        
        # Save metrics
        metrics_path = Path("metrics/persona_training_metrics.json")
        metrics_path.parent.mkdir(parents=True, exist_ok=True)
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        logger.info(f"Training completed. Model saved to {model_path}")
        logger.info(f"Final metrics: {metrics}")

if __name__ == "__main__":
    main()
