"""
Test suite for ML evaluation components
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch

from app.ml.evaluator import NaijaOracleEvaluator


class TestNaijaOracleEvaluator:
    """Test Naija Oracle ML evaluator"""
    
    @pytest.fixture
    def evaluator(self):
        """Evaluator fixture"""
        return NaijaOracleEvaluator()
    
    @pytest.mark.asyncio
    async def test_evaluate_task_a_success(self, evaluator):
        """Test successful Task A evaluation"""
        predictions = [
            "This jollof rice sweet me die! The service correct.",
            "The place good, but price cost like madness.",
            "E dey manage, not bad but not great either."
        ]
        
        references = [
            "The jollof rice was excellent! Great service.",
            "Good food but very expensive.",
            "Average experience, could be better."
        ]
        
        predicted_ratings = [4.5, 2.5, 3.0]
        true_ratings = [4.0, 2.0, 3.5]
        
        with patch('app.ml.evaluator.bert_score') as mock_bert, \
             patch('app.ml.evaluator.rouge_scorer') as mock_rouge:
            
            # Mock BERTScore
            mock_bert.score.return_value = (
                np.array([0.85, 0.80, 0.90]),  # Precision
                np.array([0.82, 0.78, 0.88]),  # Recall
                np.array([0.83, 0.79, 0.89])   # F1
            )
            
            # Mock ROUGE scorer
            mock_rouge_instance = Mock()
            mock_rouge_instance.score.side_effect = [
                Mock(fmeasure=0.42),
                Mock(fmeasure=0.38),
                Mock(fmeasure=0.40)
            ]
            mock_rouge.RougeScorer.return_value = mock_rouge_instance
            
            results = await evaluator.evaluate_task_a(
                predictions, references, predicted_ratings, true_ratings
            )
            
            assert "bertscore_f1" in results
            assert "rouge_l" in results
            assert "rmse" in results
            assert "cvi_hit_rate" in results
            assert "behavioral_fidelity" in results
            assert "task_a_score" in results
            
            # Check values are in expected ranges
            assert 0 <= results["bertscore_f1"] <= 1
            assert 0 <= results["rouge_l"] <= 1
            assert results["rmse"] >= 0
            assert 0 <= results["cvi_hit_rate"] <= 1
            assert 0 <= results["behavioral_fidelity"] <= 1
            assert 0 <= results["task_a_score"] <= 1
    
    @pytest.mark.asyncio
    async def test_evaluate_task_a_empty_inputs(self, evaluator):
        """Test Task A evaluation with empty inputs"""
        results = await evaluator.evaluate_task_a([], [], [], [])
        
        assert results["bertscore_f1"] == 0.0
        assert results["rouge_l"] == 0.0
        assert results["rmse"] == 0.0
        assert results["cvi_hit_rate"] == 0.0
        assert results["behavioral_fidelity"] == 0.0
        assert results["task_a_score"] == 0.0
    
    @pytest.mark.asyncio
    async def test_evaluate_task_b_success(self, evaluator):
        """Test successful Task B evaluation"""
        recommendations = [
            [
                {"relevance_score": 1.0, "item_id": "item_1"},
                {"relevance_score": 0.8, "item_id": "item_2"},
                {"relevance_score": 0.6, "item_id": "item_3"},
                {"relevance_score": 0.4, "item_id": "item_4"},
                {"relevance_score": 0.2, "item_id": "item_5"},
                {"relevance_score": 0.1, "item_id": "item_6"},
                {"relevance_score": 0.0, "item_id": "item_7"},
                {"relevance_score": 0.0, "item_id": "item_8"},
                {"relevance_score": 0.0, "item_id": "item_9"},
                {"relevance_score": 0.0, "item_id": "item_10"}
            ]
        ]
        
        ground_truth = [
            [
                {"relevance_score": 1.0, "item_id": "item_1"},
                {"relevance_score": 0.9, "item_id": "item_2"},
                {"relevance_score": 0.8, "item_id": "item_3"},
                {"relevance_score": 0.7, "item_id": "item_4"},
                {"relevance_score": 0.6, "item_id": "item_5"},
                {"relevance_score": 0.5, "item_id": "item_6"},
                {"relevance_score": 0.4, "item_id": "item_7"},
                {"relevance_score": 0.3, "item_id": "item_8"},
                {"relevance_score": 0.2, "item_id": "item_9"},
                {"relevance_score": 0.1, "item_id": "item_10"}
            ]
        ]
        
        cold_start_recommendations = [
            [
                {"relevance_score": 0.8, "item_id": "item_1"},
                {"relevance_score": 0.7, "item_id": "item_2"},
                {"relevance_score": 0.6, "item_id": "item_3"},
                {"relevance_score": 0.5, "item_id": "item_4"},
                {"relevance_score": 0.4, "item_id": "item_5"}
            ]
        ]
        
        with patch('app.ml.evaluator.ndcg_score') as mock_ndcg:
            # Mock NDCG score
            mock_ndcg.return_value = 0.89
            
            results = await evaluator.evaluate_task_b(
                recommendations, ground_truth, cold_start_recommendations
            )
            
            assert "ndcg_at_10" in results
            assert "hit_rate_at_5" in results
            assert "cold_start_ndcg" in results
            assert "cross_domain_hit_rate" in results
            assert "contextual_relevance" in results
            assert "task_b_score" in results
            
            # Check values are in expected ranges
            assert 0 <= results["ndcg_at_10"] <= 1
            assert 0 <= results["hit_rate_at_5"] <= 1
            assert 0 <= results["cold_start_ndcg"] <= 1
            assert 0 <= results["cross_domain_hit_rate"] <= 1
            assert 0 <= results["contextual_relevance"] <= 1
            assert 0 <= results["task_b_score"] <= 1
    
    @pytest.mark.asyncio
    async def test_evaluate_task_b_empty_inputs(self, evaluator):
        """Test Task B evaluation with empty inputs"""
        results = await evaluator.evaluate_task_b([], [])
        
        assert results["ndcg_at_10"] == 0.0
        assert results["hit_rate_at_5"] == 0.0
        assert results["cold_start_ndcg"] == 0.0
        assert results["cross_domain_hit_rate"] == 0.0
        assert results["contextual_relevance"] == 0.0
        assert results["task_b_score"] == 0.0
    
    @pytest.mark.asyncio
    async def test_calculate_cvi_hit_rate(self, evaluator):
        """Test CVI hit rate calculation"""
        predictions = [
            "This jollof rice sweet me die!",
            "Wahala be like bicycle for this place.",
            "The service e dey manage.",
            "Dem cheat me for price!",
            "The vibe no catch me."
        ]
        
        cvi_phrases = [
            "E sweet me die",
            "Wahala be like bicycle",
            "E dey manage",
            "Dem cheat me",
            "The vibe no catch me",
            "Gbam!",
            "Cost like madness"
        ]
        
        hit_rate = await evaluator._calculate_cvi_hit_rate(predictions)
        
        assert isinstance(hit_rate, float)
        assert 0 <= hit_rate <= 1
        # Should detect several matches
        assert hit_rate > 0.5
    
    @pytest.mark.asyncio
    async def test_calculate_cvi_hit_rate_no_matches(self, evaluator):
        """Test CVI hit rate with no matches"""
        predictions = [
            "This is a normal review.",
            "Good service and food.",
            "I like this place."
        ]
        
        hit_rate = await evaluator._calculate_cvi_hit_rate(predictions)
        
        assert hit_rate == 0.0
    
    @pytest.mark.asyncio
    async def test_calculate_behavioral_fidelity(self, evaluator):
        """Test behavioral fidelity calculation"""
        predictions = [
            "This jollof rice sweet me die! E correct well well.",
            "The service slow like NEPA, but food good.",
            "Price cost like madness, but portion big."
        ]
        
        references = [
            "The jollof rice was excellent! Great service.",
            "Slow service but good food quality.",
            "Expensive but large portions."
        ]
        
        fidelity = await evaluator._calculate_behavioral_fidelity(predictions, references)
        
        assert isinstance(fidelity, float)
        assert 0 <= fidelity <= 1
    
    @pytest.mark.asyncio
    async def test_calculate_behavioral_fidelity_empty(self, evaluator):
        """Test behavioral fidelity with empty inputs"""
        fidelity = await evaluator._calculate_behavioral_fidelity([], [])
        
        assert fidelity == 0.0
    
    def test_calculate_ndcg_perfect(self, evaluator):
        """Test NDCG calculation with perfect ranking"""
        recommendations = [
            {"relevance_score": 1.0},
            {"relevance_score": 0.8},
            {"relevance_score": 0.6},
            {"relevance_score": 0.4},
            {"relevance_score": 0.2}
        ]
        
        # Perfect ranking - same order
        true_relevances = [1.0, 0.8, 0.6, 0.4, 0.2]
        
        ndcg = evaluator._calculate_ndcg(recommendations, true_relevances, k=5)
        
        assert ndcg == 1.0
    
    def test_calculate_ndcg_worst(self, evaluator):
        """Test NDCG calculation with worst ranking"""
        recommendations = [
            {"relevance_score": 0.2},
            {"relevance_score": 0.4},
            {"relevance_score": 0.6},
            {"relevance_score": 0.8},
            {"relevance_score": 1.0}
        ]
        
        # Reverse order - worst ranking
        true_relevances = [1.0, 0.8, 0.6, 0.4, 0.2]
        
        ndcg = evaluator._calculate_ndcg(recommendations, true_relevances, k=5)
        
        assert ndcg < 1.0
        assert ndcg > 0.0
    
    def test_calculate_hit_rate_perfect(self, evaluator):
        """Test hit rate calculation with perfect hits"""
        recommendations = [
            {"item_id": "item_1"},
            {"item_id": "item_2"},
            {"item_id": "item_3"},
            {"item_id": "item_4"},
            {"item_id": "item_5"}
        ]
        
        # All items are relevant
        true_items = {"item_1", "item_2", "item_3", "item_4", "item_5"}
        
        hit_rate = evaluator._calculate_hit_rate(recommendations, true_items, k=5)
        
        assert hit_rate == 1.0
    
    def test_calculate_hit_rate_no_hits(self, evaluator):
        """Test hit rate calculation with no hits"""
        recommendations = [
            {"item_id": "item_1"},
            {"item_id": "item_2"},
            {"item_id": "item_3"},
            {"item_id": "item_4"},
            {"item_id": "item_5"}
        ]
        
        # No relevant items
        true_items = {"item_6", "item_7", "item_8"}
        
        hit_rate = evaluator._calculate_hit_rate(recommendations, true_items, k=5)
        
        assert hit_rate == 0.0
    
    def test_calculate_hit_rate_partial(self, evaluator):
        """Test hit rate calculation with partial hits"""
        recommendations = [
            {"item_id": "item_1"},
            {"item_id": "item_2"},
            {"item_id": "item_3"},
            {"item_id": "item_4"},
            {"item_id": "item_5"}
        ]
        
        # Some relevant items
        true_items = {"item_1", "item_3", "item_7"}
        
        hit_rate = evaluator._calculate_hit_rate(recommendations, true_items, k=5)
        
        assert hit_rate == 2.0 / 5.0  # 2 hits out of 5
    
    @pytest.mark.asyncio
    async def test_evaluate_cross_domain_transfer(self, evaluator):
        """Test cross-domain transfer evaluation"""
        recommendations = [
            [
                {"category": "food"},
                {"category": "fashion"},
                {"category": "fintech"},
                {"category": "entertainment"}
            ],
            [
                {"category": "food"},
                {"category": "tech"},
                {"category": "beauty"},
                {"category": "transport"}
            ]
        ]
        
        diversity = await evaluator._evaluate_cross_domain_transfer(recommendations)
        
        assert isinstance(diversity, float)
        assert 0 <= diversity <= 1
    
    @pytest.mark.asyncio
    async def test_evaluate_contextual_relevance(self, evaluator):
        """Test contextual relevance evaluation"""
        recommendations = [
            [
                {"context_score": 0.9},
                {"context_score": 0.8},
                {"context_score": 0.7},
                {"context_score": 0.6},
                {"context_score": 0.5}
            ],
            [
                {"context_score": 0.85},
                {"context_score": 0.75},
                {"context_score": 0.65}
            ]
        ]
        
        relevance = await evaluator._evaluate_contextual_relevance(recommendations)
        
        assert isinstance(relevance, float)
        assert 0 <= relevance <= 1
    
    def test_calculate_task_a_score(self, evaluator):
        """Test Task A score calculation"""
        metrics = {
            "bertscore_f1": 0.85,
            "rouge_l": 0.42,
            "rmse": 0.68,
            "cvi_hit_rate": 0.75,
            "behavioral_fidelity": 0.82
        }
        
        score = evaluator._calculate_task_a_score(metrics)
        
        assert isinstance(score, float)
        assert 0 <= score <= 1
        # Should be high with good metrics
        assert score > 0.7
    
    def test_calculate_task_a_score_low(self, evaluator):
        """Test Task A score calculation with low metrics"""
        metrics = {
            "bertscore_f1": 0.6,
            "rouge_l": 0.2,
            "rmse": 1.2,
            "cvi_hit_rate": 0.3,
            "behavioral_fidelity": 0.4
        }
        
        score = evaluator._calculate_task_a_score(metrics)
        
        assert isinstance(score, float)
        assert 0 <= score <= 1
        # Should be low with poor metrics
        assert score < 0.5
    
    def test_calculate_task_b_score(self, evaluator):
        """Test Task B score calculation"""
        metrics = {
            "ndcg_at_10": 0.89,
            "hit_rate_at_5": 0.82,
            "cold_start_ndcg": 0.76,
            "cross_domain_hit_rate": 0.71,
            "contextual_relevance": 0.85
        }
        
        score = evaluator._calculate_task_b_score(metrics)
        
        assert isinstance(score, float)
        assert 0 <= score <= 1
        # Should be high with good metrics
        assert score > 0.7
    
    def test_calculate_task_b_score_low(self, evaluator):
        """Test Task B score calculation with low metrics"""
        metrics = {
            "ndcg_at_10": 0.6,
            "hit_rate_at_5": 0.5,
            "cold_start_ndcg": 0.4,
            "cross_domain_hit_rate": 0.3,
            "contextual_relevance": 0.4
        }
        
        score = evaluator._calculate_task_b_score(metrics)
        
        assert isinstance(score, float)
        assert 0 <= score <= 1
        # Should be low with poor metrics
        assert score < 0.5
    
    @pytest.mark.asyncio
    async def test_run_full_evaluation(self, evaluator):
        """Test full evaluation pipeline"""
        task_a_predictions = ["This place sweet me die!"]
        task_a_references = ["This place is excellent!"]
        task_a_ratings = [4.5]
        task_a_true_ratings = [4.0]
        
        task_b_recommendations = [
            [
                {"relevance_score": 1.0, "item_id": "item_1"},
                {"relevance_score": 0.8, "item_id": "item_2"}
            ]
        ]
        task_b_ground_truth = [
            [
                {"relevance_score": 1.0, "item_id": "item_1"},
                {"relevance_score": 0.9, "item_id": "item_2"}
            ]
        ]
        
        with patch('app.ml.evaluator.bert_score') as mock_bert, \
             patch('app.ml.evaluator.rouge_scorer') as mock_rouge, \
             patch('app.ml.evaluator.ndcg_score') as mock_ndcg:
            
            # Mock external dependencies
            mock_bert.score.return_value = (
                np.array([0.85]),
                np.array([0.82]),
                np.array([0.83])
            )
            
            mock_rouge_instance = Mock()
            mock_rouge_instance.score.return_value = Mock(fmeasure=0.42)
            mock_rouge.RougeScorer.return_value = mock_rouge_instance
            
            mock_ndcg.return_value = 0.89
            
            results = await evaluator.run_full_evaluation(
                task_a_predictions=task_a_predictions,
                task_a_references=task_a_references,
                task_a_ratings=task_a_ratings,
                task_a_true_ratings=task_a_true_ratings,
                task_b_recommendations=task_b_recommendations,
                task_b_ground_truth=task_b_ground_truth
            )
            
            assert "timestamp" in results
            assert "targets" in results
            assert "task_a" in results
            assert "task_b" in results
            assert "overall_score" in results
            assert "targets_met" in results
            
            # Check targets
            assert "bertscore_target" in results["targets"]
            assert "rouge_l_target" in results["targets"]
            assert "rmse_target" in results["targets"]
            assert "ndcg_target" in results["targets"]
            
            # Check target achievements
            assert "bertscore" in results["targets_met"]
            assert "rouge_l" in results["targets_met"]
            assert "rmse" in results["targets_met"]
            assert "ndcg" in results["targets_met"]
    
    @pytest.mark.asyncio
    async def test_run_full_evaluation_partial(self, evaluator):
        """Test full evaluation with partial data"""
        # Only Task A data
        results = await evaluator.run_full_evaluation(
            task_a_predictions=["Test prediction"],
            task_a_references=["Test reference"],
            task_a_ratings=[4.0],
            task_a_true_ratings=[4.0]
        )
        
        assert "task_a" in results
        assert "task_b" not in results
        assert "overall_score" in results
    
    @pytest.mark.asyncio
    async def test_run_full_evaluation_empty(self, evaluator):
        """Test full evaluation with no data"""
        results = await evaluator.run_full_evaluation()
        
        assert "timestamp" in results
        assert "targets" in results
        assert "task_a" not in results
        assert "task_b" not in results
        assert "overall_score" in results
        assert "targets_met" in results
        
        # Overall score should be 0 with no data
        assert results["overall_score"] == 0.0
    
    def test_evaluator_initialization(self):
        """Test evaluator initialization"""
        evaluator = NaijaOracleEvaluator()
        
        assert evaluator.rouge_scorer is not None
        assert hasattr(evaluator, 'rouge_scorer')
    
    def test_evaluator_experiment_name(self, evaluator):
        """Test experiment name setting"""
        assert evaluator.experiment_name == "naija_oracle"


class TestEvaluationMetrics:
    """Test individual evaluation metrics"""
    
    @pytest.fixture
    def evaluator(self):
        """Evaluator fixture"""
        return NaijaOracleEvaluator()
    
    def test_bertscore_calculation(self, evaluator):
        """Test BERTScore calculation integration"""
        # This is tested indirectly through evaluate_task_a
        # but we can test the integration here
        pass
    
    def test_rouge_calculation(self, evaluator):
        """Test ROUGE calculation integration"""
        # This is tested indirectly through evaluate_task_a
        pass
    
    def test_ndcg_calculation_edge_cases(self, evaluator):
        """Test NDCG calculation edge cases"""
        # Empty recommendations
        ndcg = evaluator._calculate_ndcg([], [], k=5)
        assert ndcg == 0.0
        
        # Single item
        recommendations = [{"relevance_score": 1.0}]
        true_relevances = [1.0]
        ndcg = evaluator._calculate_ndcg(recommendations, true_relevances, k=5)
        assert ndcg == 1.0
        
        # Zero relevance
        recommendations = [{"relevance_score": 0.0}]
        true_relevances = [0.0]
        ndcg = evaluator._calculate_ndcg(recommendations, true_relevances, k=5)
        assert ndcg == 0.0
    
    def test_hit_rate_edge_cases(self, evaluator):
        """Test hit rate calculation edge cases"""
        # Empty recommendations
        hit_rate = evaluator._calculate_hit_rate([], {"item_1"}, k=5)
        assert hit_rate == 0.0
        
        # Empty true items
        recommendations = [{"item_id": "item_1"}]
        hit_rate = evaluator._calculate_hit_rate(recommendations, set(), k=5)
        assert hit_rate == 0.0
        
        # k larger than recommendations
        recommendations = [{"item_id": "item_1"}]
        hit_rate = evaluator._calculate_hit_rate(recommendations, {"item_1"}, k=10)
        assert hit_rate == 1.0
    
    def test_score_calculation_edge_cases(self, evaluator):
        """Test score calculation edge cases"""
        # Empty metrics
        score = evaluator._calculate_task_a_score({})
        assert score == 0.0
        
        score = evaluator._calculate_task_b_score({})
        assert score == 0.0
        
        # Missing metrics
        metrics_a = {"bertscore_f1": 0.8}  # Missing other metrics
        score = evaluator._calculate_task_a_score(metrics_a)
        assert score > 0.0  # Should handle missing gracefully
        
        metrics_b = {"ndcg_at_10": 0.8}  # Missing other metrics
        score = evaluator._calculate_task_b_score(metrics_b)
        assert score > 0.0  # Should handle missing gracefully


class TestEvaluationIntegration:
    """Test evaluation integration scenarios"""
    
    @pytest.fixture
    def evaluator(self):
        """Evaluator fixture"""
        return NaijaOracleEvaluator()
    
    @pytest.mark.asyncio
    async def test_realistic_evaluation_scenario(self, evaluator):
        """Test realistic evaluation scenario with Nigerian cultural content"""
        task_a_predictions = [
            "This jollof rice sweet me die! The service correct well well.",
            "Wahala be like bicycle for this place. Dem cheat me for price.",
            "The suya e dey manage, but portion small.",
            "Gbam! This place correct, I go come back for sure.",
            "The vibe no catch me, music too loud."
        ]
        
        task_a_references = [
            "The jollof rice was excellent! Great service.",
            "Very expensive and poor service.",
            "Average portion size, decent taste.",
            "Great experience, will return.",
            "Too loud, not comfortable."
        ]
        
        task_a_ratings = [4.5, 1.5, 2.5, 4.0, 2.0]
        task_a_true_ratings = [4.0, 2.0, 3.0, 4.5, 2.5]
        
        task_b_recommendations = [
            [
                {"relevance_score": 0.95, "item_id": "restaurant_1"},
                {"relevance_score": 0.85, "item_id": "restaurant_2"},
                {"relevance_score": 0.75, "item_id": "restaurant_3"},
                {"relevance_score": 0.65, "item_id": "restaurant_4"},
                {"relevance_score": 0.55, "item_id": "restaurant_5"}
            ]
        ]
        
        task_b_ground_truth = [
            [
                {"relevance_score": 1.0, "item_id": "restaurant_1"},
                {"relevance_score": 0.9, "item_id": "restaurant_2"},
                {"relevance_score": 0.8, "item_id": "restaurant_3"},
                {"relevance_score": 0.7, "item_id": "restaurant_4"},
                {"relevance_score": 0.6, "item_id": "restaurant_5"}
            ]
        ]
        
        with patch('app.ml.evaluator.bert_score') as mock_bert, \
             patch('app.ml.evaluator.rouge_scorer') as mock_rouge, \
             patch('app.ml.evaluator.ndcg_score') as mock_ndcg:
            
            # Mock realistic scores
            mock_bert.score.return_value = (
                np.array([0.88, 0.82, 0.85, 0.90, 0.78]),
                np.array([0.85, 0.79, 0.82, 0.87, 0.75]),
                np.array([0.86, 0.80, 0.83, 0.88, 0.76])
            )
            
            mock_rouge_instance = Mock()
            mock_rouge_instance.score.side_effect = [
                Mock(fmeasure=0.45),
                Mock(fmeasure=0.38),
                Mock(fmeasure=0.41),
                Mock(fmeasure=0.48),
                Mock(fmeasure=0.35)
            ]
            mock_rouge.RougeScorer.return_value = mock_rouge_instance
            
            mock_ndcg.return_value = 0.91
            
            results = await evaluator.run_full_evaluation(
                task_a_predictions=task_a_predictions,
                task_a_references=task_a_references,
                task_a_ratings=task_a_ratings,
                task_a_true_ratings=task_a_true_ratings,
                task_b_recommendations=task_b_recommendations,
                task_b_ground_truth=task_b_ground_truth
            )
            
            # Should achieve good scores with realistic Nigerian content
            assert results["task_a"]["bertscore_f1"] > 0.8
            assert results["task_a"]["rouge_l"] > 0.3
            assert results["task_a"]["cvi_hit_rate"] > 0.6  # Should detect CVI phrases
            assert results["task_a"]["task_a_score"] > 0.7
            
            assert results["task_b"]["ndcg_at_10"] > 0.8
            assert results["task_b"]["hit_rate_at_5"] > 0.7
            assert results["task_b"]["task_b_score"] > 0.7
            
            # Overall should be good
            assert results["overall_score"] > 0.7
            
            # Should meet most targets
            targets_met = results["targets_met"]
            assert targets_met["bertscore"] is True
            assert targets_met["rouge_l"] is True
            assert targets_met["ndcg"] is True
