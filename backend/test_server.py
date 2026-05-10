"""
Simple test server to bypass configuration issues
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Naija Oracle Test Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Naija Oracle Test Server is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "Naija Oracle Backend"}

@app.get("/api/v1/eval/metrics")
async def get_metrics():
    return {
        "available_metrics": [
            {
                "name": "bertscore",
                "description": "BERTScore F1 - measures semantic similarity",
                "endpoint": "/api/v1/eval/bertscore",
                "range": "0-1 (higher is better)"
            },
            {
                "name": "rouge",
                "description": "ROUGE-L - measures text overlap",
                "endpoint": "/api/v1/eval/rouge", 
                "range": "0-1 (higher is better)"
            },
            {
                "name": "rmse",
                "description": "Root Mean Square Error - measures rating prediction accuracy",
                "endpoint": "/api/v1/eval/rmse",
                "range": "0+ (lower is better)"
            }
        ]
    }

@app.post("/api/v1/eval/bertscore")
async def bertscore_endpoint(request: dict):
    """Mock BERTScore calculation"""
    preds = request.get("preds", [])
    refs = request.get("refs", [])
    
    # Mock calculation
    bertscore_f1 = 0.87
    
    return {"bertscore_f1": bertscore_f1}

@app.post("/api/v1/eval/rouge")
async def rouge_endpoint(request: dict):
    """Mock ROUGE-L calculation"""
    preds = request.get("preds", [])
    refs = request.get("refs", [])
    
    # Mock calculation
    rouge_l = 0.45
    
    return {"rouge_l": rouge_l}

@app.post("/api/v1/eval/rmse")
async def rmse_endpoint(request: dict):
    """Mock RMSE calculation"""
    pred_ratings = request.get("pred_ratings", [])
    true_ratings = request.get("true_ratings", [])
    
    # Mock calculation
    rmse = 0.75
    
    return {"rmse": rmse}

@app.post("/api/v1/simulate-review")
async def simulate_review(request: dict):
    """Mock review simulation"""
    return {
        "success": True,
        "data": {
            "predicted_rating": 4.0,
            "confidence_interval": [3.5, 4.5],
            "review_text": "Omo, this product packaging reach to show off for public, but the quality for inside na different matter. No be small tin I see when I open am. The price too high for the value wey dey inside.",
            "voice_profile_used": {
                "pidgin_intensity": 0.7,
                "sentiment_category": "mixed",
                "cultural_markers_activated": ["omo", "na", "wey"],
                "language_patterns": {"pidgin": 0.7, "english": 0.3}
            },
            "behavioural_fidelity_score": 0.85,
            "cvi_anchors_used": ["omo", "na", "wey"],
            "generation_time_ms": 150,
            "model_used": "llama-3.1-70b-versatile",
            "temperature_used": 0.85,
            "human_eval_rubric": {
                "voice_consistency": 4.5,
                "pidgin_authenticity": 4.2,
                "cultural_relevance": 4.8,
                "behavioral_fidelity": 4.5,
                "overall_fidelity": 4.5
            }
        },
        "request_id": "test-request-123",
        "timestamp": "2026-05-10T12:35:00Z"
    }

@app.post("/api/v1/recommend")
async def recommend(request: dict):
    """Mock recommendation endpoint"""
    cold_start_answers = request.get("cold_start_answers", {})
    
    # Generate recommendations based on cold start answers
    recommendations = [
        {
            "id": "1",
            "name": "Iya Suya Spot",
            "category": "Restaurant",
            "rating": 4.5,
            "description": "Authentic Nigerian suya with perfect spice blend",
            "distance": "0.5 km",
            "price": "₦",
            "confidence": 0.92
        },
        {
            "id": "2", 
            "name": "Silverbird Cinemas",
            "category": "Entertainment",
            "rating": 4.3,
            "description": "Latest Nollywood and international movies",
            "distance": "2.1 km",
            "price": "₦₦",
            "confidence": 0.87
        },
        {
            "id": "3",
            "name": "GTBank Branch",
            "category": "Banking", 
            "rating": 4.1,
            "description": "24/7 ATM and reliable banking services",
            "distance": "0.8 km",
            "price": "Free",
            "confidence": 0.85
        }
    ]
    
    return {
        "success": True,
        "recommendations": recommendations,
        "user_profile": {
            "persona_type": "Urban Professional",
            "preferences": cold_start_answers
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
