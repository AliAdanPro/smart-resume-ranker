"""
Accuracy Validation System
Tests the ranking engine against ground truth data to calculate real accuracy
"""

import numpy as np
from typing import List, Dict, Tuple


class AccuracyValidator:
    """
    Validates ranking accuracy by comparing with ground truth rankings
    Calculates precision@k, recall@k, NDCG, and other metrics
    """
    
    def __init__(self):
        self.test_cases = []
        self.validation_results = {}
    
    def add_test_case(self, case_id: str, ground_truth_ranking: List[str], 
                      candidate_scores: Dict[str, float], job_description: str):
        """
        Add a test case with ground truth rankings
        
        Args:
            case_id: Unique identifier for test case
            ground_truth_ranking: List of resume IDs in correct order (best first)
            candidate_scores: Dict mapping resume_id to expert-assigned scores
            job_description: The job description used
        """
        self.test_cases.append({
            'id': case_id,
            'ground_truth': ground_truth_ranking,
            'scores': candidate_scores,
            'job_desc': job_description
        })
    
    def calculate_precision_at_k(self, predicted: List[str], ground_truth: List[str], k: int) -> float:
        """
        Calculate Precision@K
        What percentage of top-k predictions are actually in the top-k ground truth?
        """
        if k > len(predicted):
            k = len(predicted)
        
        predicted_top_k = set(predicted[:k])
        ground_truth_top_k = set(ground_truth[:k])
        
        if len(predicted_top_k) == 0:
            return 0.0
        
        correct = len(predicted_top_k.intersection(ground_truth_top_k))
        return (correct / k) * 100
    
    def calculate_recall_at_k(self, predicted: List[str], ground_truth: List[str], k: int) -> float:
        """
        Calculate Recall@K
        What percentage of relevant items are in the top-k predictions?
        """
        if k > len(predicted):
            k = len(predicted)
        
        predicted_top_k = set(predicted[:k])
        ground_truth_top_k = set(ground_truth[:k])
        
        if len(ground_truth_top_k) == 0:
            return 0.0
        
        correct = len(predicted_top_k.intersection(ground_truth_top_k))
        return (correct / len(ground_truth_top_k)) * 100
    
    def calculate_ndcg(self, predicted: List[str], ground_truth_scores: Dict[str, float]) -> float:
        """
        Calculate Normalized Discounted Cumulative Gain (NDCG)
        Measures ranking quality considering position
        """
        if not predicted:
            return 0.0
        
        # DCG for predicted ranking
        dcg = 0.0
        for i, resume_id in enumerate(predicted):
            relevance = ground_truth_scores.get(resume_id, 0)
            dcg += (2**relevance - 1) / np.log2(i + 2)  # i+2 because position starts at 0
        
        # IDCG (Ideal DCG) - best possible ranking
        sorted_scores = sorted(ground_truth_scores.values(), reverse=True)
        idcg = 0.0
        for i, score in enumerate(sorted_scores):
            idcg += (2**score - 1) / np.log2(i + 2)
        
        if idcg == 0:
            return 0.0
        
        return (dcg / idcg) * 100
    
    def calculate_mean_reciprocal_rank(self, predicted: List[str], ground_truth: List[str]) -> float:
        """
        Calculate Mean Reciprocal Rank (MRR)
        How early does the first relevant result appear?
        """
        # Find position of first ground truth item in predictions
        for i, resume_id in enumerate(predicted):
            if resume_id in ground_truth[:3]:  # Top 3 are relevant
                return (1.0 / (i + 1)) * 100
        return 0.0
    
    def calculate_ranking_correlation(self, predicted: List[str], ground_truth: List[str]) -> float:
        """
        Calculate Spearman's rank correlation coefficient
        Measures how similar the two rankings are
        """
        # Create rank mappings
        predicted_ranks = {resume_id: i for i, resume_id in enumerate(predicted)}
        ground_truth_ranks = {resume_id: i for i, resume_id in enumerate(ground_truth)}
        
        # Get common items
        common_items = set(predicted_ranks.keys()).intersection(set(ground_truth_ranks.keys()))
        
        if len(common_items) < 2:
            return 0.0
        
        # Calculate rank differences
        pred_ranks = [predicted_ranks[item] for item in common_items]
        true_ranks = [ground_truth_ranks[item] for item in common_items]
        
        # Spearman correlation
        correlation = np.corrcoef(pred_ranks, true_ranks)[0, 1]
        
        if np.isnan(correlation):
            return 0.0
        
        return correlation * 100  # Convert to percentage
    
    def validate_ranking(self, predicted_ranking: List[str], test_case_id: str) -> Dict:
        """
        Validate a predicted ranking against ground truth
        
        Returns dict with all accuracy metrics
        """
        # Find the test case
        test_case = None
        for tc in self.test_cases:
            if tc['id'] == test_case_id:
                test_case = tc
                break
        
        if not test_case:
            return {'error': 'Test case not found'}
        
        ground_truth = test_case['ground_truth']
        ground_truth_scores = test_case['scores']
        
        # Calculate all metrics
        metrics = {
            'precision_at_1': self.calculate_precision_at_k(predicted_ranking, ground_truth, 1),
            'precision_at_3': self.calculate_precision_at_k(predicted_ranking, ground_truth, 3),
            'precision_at_5': self.calculate_precision_at_k(predicted_ranking, ground_truth, 5),
            'recall_at_3': self.calculate_recall_at_k(predicted_ranking, ground_truth, 3),
            'recall_at_5': self.calculate_recall_at_k(predicted_ranking, ground_truth, 5),
            'ndcg': self.calculate_ndcg(predicted_ranking, ground_truth_scores),
            'mrr': self.calculate_mean_reciprocal_rank(predicted_ranking, ground_truth),
            'rank_correlation': self.calculate_ranking_correlation(predicted_ranking, ground_truth)
        }
        
        # Calculate overall accuracy (average of key metrics)
        overall_accuracy = (
            metrics['precision_at_3'] * 0.3 +
            metrics['recall_at_5'] * 0.2 +
            metrics['ndcg'] * 0.3 +
            metrics['rank_correlation'] * 0.2
        )
        
        metrics['overall_accuracy'] = round(overall_accuracy, 1)
        metrics['test_case_id'] = test_case_id
        metrics['tested'] = True
        
        return metrics
    
    def run_validation_suite(self, ranking_results: Dict[str, List[str]]) -> Dict:
        """
        Run validation on multiple test cases
        
        Args:
            ranking_results: Dict mapping test_case_id to predicted rankings
        
        Returns:
            Summary of all validation results
        """
        all_results = []
        
        for test_case_id, predicted_ranking in ranking_results.items():
            result = self.validate_ranking(predicted_ranking, test_case_id)
            all_results.append(result)
        
        # Calculate average metrics
        if all_results:
            avg_metrics = {
                'avg_precision_at_3': np.mean([r['precision_at_3'] for r in all_results]),
                'avg_recall_at_5': np.mean([r['recall_at_5'] for r in all_results]),
                'avg_ndcg': np.mean([r['ndcg'] for r in all_results]),
                'avg_overall_accuracy': np.mean([r['overall_accuracy'] for r in all_results]),
                'test_cases_run': len(all_results),
                'tested': True
            }
        else:
            avg_metrics = {
                'avg_overall_accuracy': 0.0,
                'test_cases_run': 0,
                'tested': False
            }
        
        return {
            'summary': avg_metrics,
            'individual_results': all_results
        }
    
    def get_sample_test_data(self) -> List[Dict]:
        """
        Returns sample test cases for demonstration
        """
        return [
            {
                'id': 'test_python_dev',
                'ground_truth': ['resume_A', 'resume_B', 'resume_C', 'resume_D', 'resume_E'],
                'scores': {
                    'resume_A': 95,  # Best match - 10 years Python, ML expert
                    'resume_B': 88,  # Good match - 7 years Python, some ML
                    'resume_C': 75,  # Decent match - 5 years Python
                    'resume_D': 60,  # Fair match - 3 years Python
                    'resume_E': 45   # Weak match - 1 year Python
                },
                'job_desc': 'Senior Python Developer with ML expertise'
            },
            {
                'id': 'test_fullstack',
                'ground_truth': ['resume_X', 'resume_Y', 'resume_Z'],
                'scores': {
                    'resume_X': 92,  # Full stack React+Node expert
                    'resume_Y': 80,  # Strong React, basic Node
                    'resume_Z': 65   # Basic full stack
                },
                'job_desc': 'Full Stack Developer - React + Node.js'
            }
        ]
