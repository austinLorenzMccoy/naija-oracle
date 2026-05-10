from fastapi import APIRouter
from bert_score import BERTScorer
from rouge_score import rouge_scorer
import numpy as np
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/eval", tags=["evaluation"])

# Request/Response models
class ScoreRequest(BaseModel):
    preds: List[str]
    refs: List[str]

class RatingRequest(BaseModel):
    pred_ratings: List[float]
    true_ratings: List[float]

class BERTScoreResponse(BaseModel):
    bertscore_f1: float

class RougeResponse(BaseModel):
    rouge_l: float

class RMSEResponse(BaseModel):
    rmse: float

# Lazy initialization
_bertscorer = None
_rouge = None

def get_bert_scorer():
    global _bertscorer
    if _bertscorer is None:
        _bertscorer = BERTScorer(lang="en")
    return _bertscorer

def get_rouge_scorer():
    global _rouge
    if _rouge is None:
        _rouge = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    return _rouge

@router.post("/bertscore", response_model=BERTScoreResponse)
def bertscore(request: ScoreRequest):
    """
    Calculate BERTScore F1 between predictions and references.
    
    Args:
        request: Contains preds (predicted texts) and refs (reference texts)
    
    Returns:
        BERTScore F1 score (0-1, higher is better)
    """
    if len(request.preds) != len(request.refs):
        raise ValueError("Number of predictions and references must match")
    
    scorer = get_bert_scorer()
    _, _, f1 = scorer.score(request.preds, request.refs)
    return {"bertscore_f1": float(f1.mean().item())}

@router.post("/rouge", response_model=RougeResponse)
def rouge(request: ScoreRequest):
    """
    Calculate ROUGE-L score between predictions and references.
    
    Args:
        request: Contains preds (predicted texts) and refs (reference texts)
    
    Returns:
        ROUGE-L score (0-1, higher is better)
    """
    if len(request.preds) != len(request.refs):
        raise ValueError("Number of predictions and references must match")
    
    scorer = get_rouge_scorer()
    scores = [scorer.score(p, r)["rougeL"].fmeasure for p, r in zip(request.preds, request.refs)]
    return {"rouge_l": float(np.mean(scores))}

@router.post("/rmse", response_model=RMSEResponse)
def rmse(request: RatingRequest):
    """
    Calculate Root Mean Square Error between predicted and true ratings.
    
    Args:
        request: Contains pred_ratings and true_ratings
    
    Returns:
        RMSE score (lower is better)
    """
    if len(request.pred_ratings) != len(request.true_ratings):
        raise ValueError("Number of predicted and true ratings must match")
    
    pred_array = np.array(request.pred_ratings)
    true_array = np.array(request.true_ratings)
    rmse_value = np.sqrt(np.mean((pred_array - true_array) ** 2))
    return {"rmse": float(rmse_value)}

@router.get("/metrics")
def list_available_metrics():
    """
    List all available evaluation metrics.
    """
    return {
        "available_metrics": [
            {
                "name": "bertscore",
                "description": "BERTScore F1 - measures semantic similarity",
                "endpoint": "/eval/bertscore",
                "range": "0-1 (higher is better)"
            },
            {
                "name": "rouge",
                "description": "ROUGE-L - measures text overlap",
                "endpoint": "/eval/rouge", 
                "range": "0-1 (higher is better)"
            },
            {
                "name": "rmse",
                "description": "Root Mean Square Error - measures rating prediction accuracy",
                "endpoint": "/eval/rmse",
                "range": "0+ (lower is better)"
            }
        ]
    }
