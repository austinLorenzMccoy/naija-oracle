# Naija Oracle ML Training

Machine learning pipeline for training and evaluating cultural AI models for Nigerian consumer intelligence.

## Training Pipeline Overview

### **Task A - Persona Simulator Training**
Fine-tunes LLaMA-3.1-8B to generate authentic Nigerian reviews with cultural voice patterns.

### **Task B - Recommendation Engine Training**
Trains neural ranking models with contextual features for hyper-personalised recommendations.

## Setup with UV

### Prerequisites
- Python 3.11+
- UV package manager
- CUDA-compatible GPU (for LLM training)
- 16GB+ VRAM (for Persona Simulator)

### Installation
```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup environment
cd ml_training
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

## Training Scripts

### Persona Simulator (Task A)

```bash
# Full training pipeline
uv run python train_persona_simulator.py \
    --model "meta-llama/Llama-3.1-8B" \
    --data "data/persona_training_data.json" \
    --output "models/persona_simulator" \
    --epochs 3

# Evaluation only
uv run python train_persona_simulator.py \
    --eval-only \
    --data "data/persona_training_data.json" \
    --output "models/persona_simulator"

# Custom hyperparameters
uv run python train_persona_simulator.py \
    --model "meta-llama/Llama-3.1-8B" \
    --data "data/persona_training_data.json" \
    --output "models/persona_simulator" \
    --epochs 5 \
    --learning-rate 1e-5 \
    --batch-size 2
```

### Recommendation Engine (Task B)

```bash
# Full training pipeline
uv run python train_recommendation_engine.py \
    --data "data/recommendation_training_data.csv" \
    --epochs 50 \
    --lr 0.001

# Evaluation only
uv run python train_recommendation_engine.py \
    --eval-only \
    --data "data/recommendation_training_data.csv" \
    --model-path "models/recommendation_ranker_best.pth"

# Hyperparameter tuning
uv run python train_recommendation_engine.py \
    --data "data/recommendation_training_data.csv" \
    --epochs 100 \
    --lr 0.0005 \
    --hidden-dims 512 256 128
```

## Data Generation

### Synthetic Persona Data
The training pipeline automatically generates 500+ Nigerian personas with realistic distributions:

```python
# Persona Template
{
    "name": "Emeka O.",
    "age_range": "25-34",
    "city": "Lagos",
    "lga": "Surulere",
    "primary_language": "Igbo",
    "review_style": "expressive",
    "avg_rating": 3.8,
    "pidgin_intensity": 0.7,
    "cultural_markers": ["price_sensitive", "brand_loyal_food"]
}
```

### Cultural Voice Index Training Data
13+ authentic Nigerian phrases with cultural context:

| Phrase | Tribe | Pidgin Intensity | Sentiment | Context |
|--------|-------|------------------|-----------|---------|
| "E sweet me die" | Yoruba | 0.8 | Strong Positive | Food |
| "Wahala be like bicycle" | Pan-Nigerian | 0.7 | Negative | Service |
| "E dey manage" | Pan-Nigerian | 0.6 | Mixed | General |
| "Dem cheat me" | Pan-Nigerian | 0.9 | Strong Negative | Price |
| "The vibe no catch me" | Pan-Nigerian | 0.7 | Neutral | Ambience |

### Training Prompt Format
```python
prompt = f"""<s>[INST]
You are Naija Oracle — a cultural intelligence system.

PERSONA:
- Name: {persona['name']}
- City: {persona['city']} | LGA: {persona['lga']}
- Language: {persona['language']} | Pidgin intensity: {persona['pidgin_intensity']:.1f}/1.0
- Style: {persona['style']}

PRODUCT TO REVIEW:
- Name: {product['name']}
- Category: {product['category']}
- Location: {product['location']}

Generate an authentic review that sounds exactly like this persona would write it.
[/INST]

{review}</s>"""
```

## Model Architecture

### Persona Simulator
- **Base Model**: LLaMA-3.1-8B-Versatile
- **Fine-tuning**: LoRA adapters for efficiency
- **Input Length**: 512 tokens
- **Temperature**: 0.85 for generation
- **Cultural Prompting**: CVI anchor injection

### Recommendation Ranker
```python
class RecommendationRanker(nn.Module):
    def __init__(self, input_dim=10, hidden_dims=[256, 128, 64]):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dims[0]),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dims[0], hidden_dims[1]),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dims[1], hidden_dims[2]),
            nn.ReLU(),
            nn.Linear(hidden_dims[2], 1)
        )
```

### Feature Engineering
```python
features = [
    'user_rating_tendency',    # Persona's average rating
    'item_avg_rating',         # Item's historical rating
    'price_match_score',       # Budget alignment
    'location_proximity',      # Geographic relevance
    'category_preference',     # Mood-category matching
    'time_relevance',          # Time-appropriate
    'mood_alignment',          # Occasion suitability
    'budget_fit',              # Price range match
    'collaborative_score',     # User similarity
    'popularity_score'         # Item popularity
]
```

## Evaluation Metrics

### Task A - Review Generation
```python
# BERTScore (multilingual)
P, R, F1 = bert_score(predictions, references, lang="en")
bertscore_f1 = F1.mean().item()

# ROUGE-L
rouge_scores = [rouge_scorer.score(pred, ref)["rougeL"].fmeasure 
                for pred, ref in zip(predictions, references)]
avg_rouge_l = np.mean(rouge_scores)

# Rating RMSE
rmse = np.sqrt(mean_squared_error(true_ratings, predicted_ratings))

# Cultural Voice Index Hit Rate
cvi_hit_rate = calculate_cvi_hits(predictions, cvi_anchors)
```

### Task B - Recommendations
```python
# NDCG@10
ndcg_scores = [ndcg_score([relevance], [predicted], k=10) 
               for relevance, predicted in zip(true_relevances, predictions)]
avg_ndcg_10 = np.mean(ndcg_scores)

# Hit Rate @5
hit_rates = [calculate_hit_rate(recs[:5], true_items) 
             for recs, true_items in zip(recommendations, ground_truth)]
avg_hit_rate_5 = np.mean(hit_rates)
```

## DVC & DagsHub Integration

### Why DVC + DagsHub?
- **Data Version Control**: Track large datasets and model files without bloating git
- **Experiment Reproducibility**: Complete reproducibility with data, code, and parameters
- **Remote Storage**: Secure cloud storage for models and datasets
- **Collaboration**: Share experiments and models with your team
- **Competition Submission**: Public reproducibility for judges

### Setup DVC and DagsHub
```bash
# Initialize DVC
cd ml_training
dvc init

# Setup DagsHub remote
dvc remote add -d origin dagsHub://your-username/naija-oracle
dvc remote modify origin username your-username
dvc remote modify origin password DVC_TOKEN

# Track data and models
dvc add data/persona_training_data.json
dvc add data/recommendation_training_data.csv
dvc add models/persona_simulator
dvc add models/recommendation_engine

# Push to DagsHub
dvc push
```

### Automated Setup Script
```bash
# Run the setup script
uv run python scripts/setup_dvc.py \
    --dagshub-username your-username \
    --dvc-token your-dvc-token

# Or set environment variables
export DAGSHUB_USERNAME=your-username
export DVC_TOKEN=your-dvc-token
```

### DVC Pipeline
```bash
# Run complete pipeline
dvc repro

# Run specific stage
dvc repro prepare_data
dvc repro train_persona_simulator
dvc repro evaluate

# Visualize pipeline
dvc dag
```

### DVC Commands
```bash
# Check status
dvc status

# Show data dependencies
dvc data diff

# Pull data from remote
dvc pull

# Push data to remote
dvc push

# Remove from DVC tracking
dvc remove data/persona_training_data.json
```

## MLflow + DagsHub Integration

### Setup
```bash
# Start MLflow server with DagsHub backend
mlflow server --host 0.0.0.0 --port 5000 \
    --backend-store-uri postgresql://postgres:password@localhost:5432/naija_oracle \
    --default-artifact-root ./mlflow/artifacts \
    --experiment-name naija-oracle

# View experiments
# http://localhost:5000
```

### Experiment Logging with DVC
```python
import dvclive

with dvclive.Live("persona_simulator") as live:
    # Log parameters
    live.log_param("model_name", "meta-llama/Llama-3.1-8B")
    live.log_param("learning_rate", 2e-5)
    live.log_param("batch_size", 4)
    live.log_param("num_epochs", 3)
    
    # Training loop
    for epoch in range(num_epochs):
        train_loss = train_one_epoch()
        eval_loss = evaluate()
        
        # Log metrics
        live.log_metric("train_loss", train_loss)
        live.log_metric("eval_loss", eval_loss)
        live.log_metric("bertscore_f1", calculate_bertscore())
        live.log_metric("rouge_l", calculate_rouge())
        
        # Log model checkpoint
        if epoch % 5 == 0:
            live.log_artifact("model_checkpoint.pth", "model")
```

### DagsHub MLflow Integration
```python
import dagshub

# Initialize DagsHub
dagshub.init("naija-oracle", "your-username", mlflow=True)

# Your MLflow experiments will now be tracked on DagsHub
with mlflow.start_run(run_name="persona_simulator_experiment"):
    # Your training code here
    pass
```

### Experiment Tracking
```python
with mlflow.start_run(run_name=f"persona_simulator_{timestamp}"):
    # Log parameters
    mlflow.log_params({
        "model_name": "meta-llama/Llama-3.1-8B",
        "learning_rate": 2e-5,
        "batch_size": 4,
        "num_epochs": 3
    })
    
    # Log metrics
    mlflow.log_metrics({
        "train_loss": train_loss,
        "eval_loss": eval_loss,
        "bertscore_f1": avg_bert_score,
        "rouge_l": avg_rouge_score
    })
    
    # Log model
    mlflow.pytorch.log_model(model, "model")
    
    # Log artifacts
    mlflow.log_artifact("data/persona_training_data.json")
    mlflow.log_artifact("plots/training_curves.png")
```

## Hyperparameter Optimization

### Optuna Integration
```python
def objective(trial):
    # Suggest hyperparameters
    learning_rate = trial.suggest_float('lr', 1e-6, 1e-4, log=True)
    batch_size = trial.suggest_categorical('batch_size', [2, 4, 8])
    num_epochs = trial.suggest_int('epochs', 3, 10)
    
    # Train model
    model = train_model(learning_rate, batch_size, num_epochs)
    
    # Evaluate
    metrics = evaluate_model(model)
    
    return metrics['bertscore_f1']

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)
```

### Hyperparameter Ranges
```python
persona_simulator_params = {
    'learning_rate': (1e-6, 1e-4),
    'batch_size': [2, 4, 8],
    'num_epochs': (3, 10),
    'temperature': (0.7, 1.0),
    'max_length': (256, 1024)
}

recommendation_engine_params = {
    'learning_rate': (1e-5, 1e-2),
    'batch_size': [16, 32, 64],
    'hidden_dims': [[128, 64], [256, 128, 64], [512, 256, 128]],
    'dropout': (0.1, 0.5),
    'num_epochs': (20, 100)
}
```

## GPU Requirements

### Persona Simulator
- **VRAM**: 16GB+ (for 8B model with LoRA)
- **Training Time**: ~2-3 hours per epoch
- **Memory Optimization**: Gradient checkpointing, mixed precision

### Recommendation Engine
- **VRAM**: 4GB+ (sufficient)
- **Training Time**: ~30 minutes for 50 epochs
- **Memory Optimization**: Standard PyTorch optimization

## Jupyter Development

### Interactive Development
```bash
# Launch Jupyter with UV
uv run jupyter lab --ip=0.0.0.0 --port=8888

# Or via Docker
docker-compose up jupyter
# Access: http://localhost:8888
```

### Notebook Structure
```
notebooks/
├── 01_data_exploration.ipynb      # Analyze training data
├── 02_cultural_voice_analysis.ipynb  # CVI pattern analysis
├── 03_model_experiments.ipynb    # Quick model testing
├── 04_evaluation_metrics.ipynb   # Metric analysis
└── 05_hyperparameter_tuning.ipynb  # Optuna experiments
```

## Production Deployment

### Model Export
```python
# Save trained model
torch.save(model.state_dict(), "models/persona_simulator_best.pth")

# Export to ONNX (for inference)
torch.onnx.export(model, example_input, "models/persona_simulator.onnx")

# Log to MLflow registry
mlflow.pytorch.log_model(model, "model", registered_model_name="naija_oracle_persona_simulator")
```

### Model Versioning
- Git tags for model versions
- MLflow model registry
- Automatic artifact storage
- Model performance tracking

## Troubleshooting

### Common Issues

**CUDA Out of Memory**
```bash
# Reduce batch size
uv run python train_persona_simulator.py --batch-size 2

# Enable gradient checkpointing
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
```

**MLflow Connection Issues**
```bash
# Check MLflow server
curl http://localhost:5000/health

# Reset tracking URI
export MLFLOW_TRACKING_URI=http://localhost:5000
```

**Groq API Rate Limits**
```bash
# Check rate limits
curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/v1/rate_limits

# Implement backoff in training
python -c "import time; time.sleep(60)"  # Wait for reset
```

### Debug Mode
```bash
# Enable debug logging
export PYTHONPATH=$PWD
uv run python -m debugpy --listen 5678 train_persona_simulator.py

# Profile training
uv run python -m cProfile -o profile.stats train_persona_simulator.py
```

## Contributing

### Adding Cultural Patterns
1. Update `CulturalVoiceIndex` with new phrases
2. Add tribe/region mappings
3. Update sentiment associations
4. Retrain models with expanded data

### Improving Evaluation
1. Add new metrics to `NaijaOracleEvaluator`
2. Update target thresholds
3. Add human evaluation protocols
4. Improve cultural authenticity scoring

### Model Optimization
1. Implement quantization for inference
2. Add model distillation pipelines
3. Optimize prompt engineering
4. Improve feature engineering

## License

Apache 2.0 - See LICENSE file for details
