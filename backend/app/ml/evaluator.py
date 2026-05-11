"""
ML Evaluation metrics for Naija Oracle
"""

import numpy as np
from typing import Dict, List, Any, Tuple
from bert_score import score as bert_score
from rouge_score import rouge_scorer
from sklearn.metrics import mean_squared_error
import json

from app.config import *

class NaijaOracleEvaluator:
    """Comprehensive evaluation for Naija Oracle agents"""
    
    def __init__(self):
        self.rouge_scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    
    async def evaluate_task_a(
        self, 
        predictions: List[str], 
        references: List[str],
        predicted_ratings: List[float] = None,
        true_ratings: List[float] = None
    ) -> Dict[str, float]:
        """Evaluate Task A - Persona Simulator"""
        
        results = {}
        
        # BERTScore
        if predictions and references:
            P, R, F1 = bert_score(predictions, references, lang="en")
            results["bertscore_f1"] = F1.mean().item()
            results["bertscore_precision"] = P.mean().item()
            results["bertscore_recall"] = R.mean().item()
        
        # ROUGE-L
        rouge_scores = []
        for pred, ref in zip(predictions, references):
            score = self.rouge_scorer.score(pred, ref)
            rouge_scores.append(score["rougeL"].fmeasure)
        
        results["rouge_l"] = np.mean(rouge_scores) if rouge_scores else 0.0
        
        # Rating RMSE
        if predicted_ratings and true_ratings:
            rmse = np.sqrt(mean_squared_error(true_ratings, predicted_ratings))
            results["rmse"] = rmse
        
        # Cultural Voice Index hit rate
        cvi_hit_rate = await self._calculate_cvi_hit_rate(predictions)
        results["cvi_hit_rate"] = cvi_hit_rate
        
        # Behavioral fidelity
        behavioral_fidelity = await self._calculate_behavioral_fidelity(predictions, references)
        results["behavioral_fidelity"] = behavioral_fidelity
        
        # Overall Task A score
        results["task_a_score"] = self._calculate_task_a_score(results)
        
        return results
    
    async def evaluate_task_b(
        self,
        recommendations: List[List[Dict[str, Any]]],
        ground_truth: List[List[Dict[str, Any]]],
        cold_start_recommendations: List[List[Dict[str, Any]]] = None
    ) -> Dict[str, float]:
        """Evaluate Task B - Recommendation Engine"""
        
        results = {}
        
        # NDCG@10
        ndcg_scores = []
        for rec_list, truth_list in zip(recommendations, ground_truth):
            ndcg = self._calculate_ndcg(rec_list, truth_list, k=10)
            ndcg_scores.append(ndcg)
        
        results["ndcg_at_10"] = np.mean(ndcg_scores) if ndcg_scores else 0.0
        
        # Hit Rate @5
        hit_rates = []
        for rec_list, truth_list in zip(recommendations, ground_truth):
            hit_rate = self._calculate_hit_rate(rec_list, truth_list, k=5)
            hit_rates.append(hit_rate)
        
        results["hit_rate_at_5"] = np.mean(hit_rates) if hit_rates else 0.0
        
        # Cold-start performance
        if cold_start_recommendations:
            cold_ndcg_scores = []
            for rec_list, truth_list in zip(cold_start_recommendations, ground_truth):
                cold_ndcg = self._calculate_ndcg(rec_list, truth_list, k=10)
                cold_ndcg_scores.append(cold_ndcg)
            
            results["cold_start_ndcg"] = np.mean(cold_ndcg_scores) if cold_ndcg_scores else 0.0
        
        # Cross-domain transfer
        cross_domain_score = await self._evaluate_cross_domain_transfer(recommendations)
        results["cross_domain_hit_rate"] = cross_domain_score
        
        # Contextual relevance
        contextual_relevance = await self._evaluate_contextual_relevance(recommendations)
        results["contextual_relevance"] = contextual_relevance
        
        # Overall Task B score
        results["task_b_score"] = self._calculate_task_b_score(results)
        
        return results
    
    async def _calculate_cvi_hit_rate(self, predictions: List[str]) -> float:
        """Calculate Cultural Voice Index hit rate"""
        
        # CVI anchor phrases
        cvi_anchors = [
            "E sweet me die", "Wahala be like bicycle", "E dey manage",
            "Dem cheat me", "The vibe no catch me", "Gbam!", "E go be",
            "Orente", "Nwoke oma", "Lafiya", "Cost like madness",
            "Slow like NEPA", "Correct!"
        ]
        
        total_hits = 0
        total_possible = len(predictions) * 3  # Expect 3 anchors per review
        
        for prediction in predictions:
            hits = 0
            for anchor in cvi_anchors:
                if anchor.lower() in prediction.lower():
                    hits += 1
            total_hits += min(hits, 3)  # Cap at 3 hits per review
        
        return total_hits / total_possible if total_possible > 0 else 0.0
    
    async def _calculate_behavioral_fidelity(self, predictions: List[str], references: List[str]) -> float:
        """Calculate behavioral fidelity score"""
        
        fidelity_scores = []
        
        for pred, ref in zip(predictions, references):
            # Length similarity
            length_ratio = min(len(pred), len(ref)) / max(len(pred), len(ref))
            
            # Pidgin intensity similarity (simplified)
            pidgin_indicators = ["na", "o", "sha", "abeg", "wahala", "gbam", "e go be", "dey", "dem"]
            pred_pidgin = sum(1 for indicator in pidgin_indicators if indicator in pred.lower())
            ref_pidgin = sum(1 for indicator in pidgin_indicators if indicator in ref.lower())
            
            pidgin_similarity = 1.0 - abs(pred_pidgin - ref_pidgin) / max(pred_pidgin, ref_pidgin, 1)
            
            # Overall fidelity
            fidelity = (length_ratio + pidgin_similarity) / 2
            fidelity_scores.append(fidelity)
        
        return np.mean(fidelity_scores) if fidelity_scores else 0.0
    
    def _calculate_ndcg(self, recommendations: List[Dict], ground_truth: List[Dict], k: int = 10) -> float:
        """Calculate NDCG@k"""
        
        # Extract relevance scores
        rec_scores = [rec.get("relevance_score", rec.get("context_score", 0)) for rec in recommendations[:k]]
        truth_scores = [item.get("relevance_score", 1.0) for item in ground_truth[:k]]
        
        if not rec_scores or not truth_scores:
            return 0.0
        
        # Calculate DCG
        dcg = 0.0
        for i, score in enumerate(rec_scores):
            dcg += score / np.log2(i + 2)  # i+2 because log2(1) = 0
        
        # Calculate IDCG (ideal DCG)
        idcg = 0.0
        sorted_truth = sorted(truth_scores, reverse=True)
        for i, score in enumerate(sorted_truth[:k]):
            idcg += score / np.log2(i + 2)
        
        return dcg / idcg if idcg > 0 else 0.0
    
    def _calculate_hit_rate(self, recommendations: List[Dict], ground_truth: List[Dict], k: int = 5) -> float:
        """Calculate Hit Rate@k"""
        
        if not recommendations or not ground_truth:
            return 0.0
        
        # Get top-k recommended item IDs
        rec_items = set(rec.get("item_id", f"item_{i}") for i, rec in enumerate(recommendations[:k]))
        
        # Get relevant item IDs
        truth_items = set(item.get("item_id", f"item_{i}") for i, item in enumerate(ground_truth))
        
        # Calculate hits
        hits = len(rec_items.intersection(truth_items))
        
        return hits / k if k > 0 else 0.0
    
    async def _evaluate_cross_domain_transfer(self, recommendations: List[List[Dict]]) -> float:
        """Evaluate cross-domain transfer capability"""
        
        # Simplified evaluation: check if recommendations span multiple domains
        domain_diversity_scores = []
        
        for rec_list in recommendations:
            domains = set(rec.get("category", "") for rec in rec_list)
            diversity_score = len(domains) / 4.0  # Normalize by max 4 domains
            domain_diversity_scores.append(min(diversity_score, 1.0))
        
        return np.mean(domain_diversity_scores) if domain_diversity_scores else 0.0
    
    async def _evaluate_contextual_relevance(self, recommendations: List[List[Dict]]) -> float:
        """Evaluate contextual relevance of recommendations"""
        
        # Check if recommendations match context (location, mood, budget)
        relevance_scores = []
        
        for rec_list in recommendations:
            # Simplified: use context_score if available
            scores = [rec.get("context_score", 0.5) for rec in rec_list]
            avg_relevance = np.mean(scores)
            relevance_scores.append(avg_relevance)
        
        return np.mean(relevance_scores) if relevance_scores else 0.0
    
    def _calculate_task_a_score(self, metrics: Dict[str, float]) -> float:
        """Calculate overall Task A score"""
        
        weights = {
            "bertscore_f1": 0.3,
            "rouge_l": 0.2,
            "rmse": 0.2,  # Will be inverted
            "cvi_hit_rate": 0.2,
            "behavioral_fidelity": 0.1
        }
        
        score = 0.0
        
        for metric, weight in weights.items():
            if metric in metrics:
                if metric == "rmse":
                    # Lower is better, so invert
                    normalized = max(0, 1 - (metrics[metric] / 2.0))  # Normalize assuming max RMSE of 2.0
                else:
                    normalized = metrics[metric]
                
                score += normalized * weight
        
        return score
    
    def _calculate_task_b_score(self, metrics: Dict[str, float]) -> float:
        """Calculate overall Task B score"""
        
        weights = {
            "ndcg_at_10": 0.3,
            "hit_rate_at_5": 0.3,
            "cold_start_ndcg": 0.25,
            "cross_domain_hit_rate": 0.1,
            "contextual_relevance": 0.05
        }
        
        score = 0.0
        
        for metric, weight in weights.items():
            if metric in metrics:
                score += metrics[metric] * weight
        
        return score
    
    async def run_full_evaluation(
        self,
        task_a_predictions: List[str] = None,
        task_a_references: List[str] = None,
        task_a_ratings: List[float] = None,
        task_a_true_ratings: List[float] = None,
        task_b_recommendations: List[List[Dict]] = None,
        task_b_ground_truth: List[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Run comprehensive evaluation for both tasks"""
        
        results = {
            "timestamp": str(np.datetime64('now')),
            "targets": {
                "bertscore_target": settings.BERTSCORE_TARGET,
                "rouge_l_target": settings.ROUGE_L_TARGET,
                "rmse_target": settings.RMSE_TARGET,
                "ndcg_target": settings.NDCG_TARGET
            }
        }
        
        # Task A evaluation
        if task_a_predictions and task_a_references:
            task_a_results = await self.evaluate_task_a(
                task_a_predictions, task_a_references,
                task_a_ratings, task_a_true_ratings
            )
            results["task_a"] = task_a_results
        
        # Task B evaluation
        if task_b_recommendations and task_b_ground_truth:
            task_b_results = await self.evaluate_task_b(
                task_b_recommendations, task_b_ground_truth
            )
            results["task_b"] = task_b_results
        
        # Overall score
        task_a_score = results.get("task_a", {}).get("task_a_score", 0.0)
        task_b_score = results.get("task_b", {}).get("task_b_score", 0.0)
        
        results["overall_score"] = (task_a_score + task_b_score) / 2.0
        
        # Target achievement
        results["targets_met"] = {
            "bertscore": task_a_results.get("bertscore_f1", 0) >= settings.BERTSCORE_TARGET if "task_a" in results else False,
            "rouge_l": task_a_results.get("rouge_l", 0) >= settings.ROUGE_L_TARGET if "task_a" in results else False,
            "rmse": task_a_results.get("rmse", 999) <= settings.RMSE_TARGET if "task_a" in results else False,
            "ndcg": task_b_results.get("ndcg_at_10", 0) >= settings.NDCG_TARGET if "task_b" in results else False
        }
        
        return results
