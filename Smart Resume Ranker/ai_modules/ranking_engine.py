from .cosine_similarity import CosineSimilarity
from .fuzzy_logic import FuzzyResumeScorer
from .genetic_algorithm import GAOptimizer
from .persona_matching import PersonaMatcher
from .career_predictor import CareerPredictor
from .skill_gap_analyzer import SkillGapAnalyzer
from .experience_transfer import ExperienceTransfer
from .innovation_scorer import InnovationScorer
from .neural_embeddings import NeuralEmbeddingRanker
from .knowledge_graph import KnowledgeGraphMatcher
from .ensemble_super_accuracy import SuperAccuracyEnsemble
from evaluation.metrics_calculator import MetricsCalculator
import numpy as np

class RankingEngine:
    def __init__(self):
        self.cosine_model = CosineSimilarity()
        self.fuzzy_model = FuzzyResumeScorer()
        self.ga_optimizer = GAOptimizer()
        
        # New Modules
        self.persona_matcher = PersonaMatcher()
        self.career_predictor = CareerPredictor()
        self.skill_gap_analyzer = SkillGapAnalyzer()
        self.experience_transfer = ExperienceTransfer()
        self.innovation_scorer = InnovationScorer()
        
        # Neural and Graph Models
        self.neural_ranker = NeuralEmbeddingRanker()
        self.knowledge_graph = KnowledgeGraphMatcher()
        
        # Ensemble
        self.ensemble_system = SuperAccuracyEnsemble()
        self.metrics_calculator = MetricsCalculator()

    def _normalize_scores(self, scores):
        """
        Normalizes a list of scores using Min-Max scaling to 0-100 range.
        If variance is 0, returns original scores.
        """
        scores = np.array(scores)
        if np.std(scores) == 0:
            return scores
        return (scores - np.min(scores)) / (np.max(scores) - np.min(scores)) * 100

    def rank_resumes(self, job_description, resumes_data, weights, algorithm='all'):
        """
        Orchestrates the ranking process.
        """
        # Store convergence data for metrics
        self.convergence_data = None
        
        # Optimize weights if GA is selected or run GA for convergence data
        if algorithm == 'ga' or algorithm == 'all':
            optimized_weights, convergence_data = self.ga_optimizer.optimize()
            self.convergence_data = convergence_data
            if algorithm == 'ga':
                weights['skills'] = optimized_weights[0]
                weights['education'] = optimized_weights[1]

        # Calculate raw scores for all resumes
        raw_scores = {
            'skills': [], 'education': [],
            'persona': [], 'career': [], 'gap': [], 'transfer': [], 'innovation': [],
            'neural': [], 'knowledge': []
        }
        
        # Store intermediate results to avoid re-calculation
        intermediate_results = []

        for resume in resumes_data:
            text = resume.get('text', '')
            
            # --- Super Ensemble Logic ---
            if algorithm == 'ensemble':
                try:
                    ensemble_result = self.ensemble_system.get_super_accuracy_score(job_description, text)
                    # Use the super score as the base skills score
                    skills_score = ensemble_result['final_score']
                    # We can store the detailed ensemble breakdown in intermediate results
                    intermediate_results.append({
                        'missing_skills': [], # Ensemble doesn't explicitly return missing skills list in this version
                        'ensemble_details': ensemble_result
                    })
                    print(f"✅ Ensemble Score: {skills_score:.1f}% | Neural: {ensemble_result['neural_score']:.1f} | Graph: {ensemble_result['graph_score']:.1f}")
                except Exception as e:
                    print(f"❌ Ensemble Error: {str(e)}")
                    # Fallback to standard scoring
                    cosine_score = self.cosine_model.calculate_similarity(job_description, text)
                    fuzzy_score = self.fuzzy_model.calculate_fuzzy_score(job_description, text)
                    skills_score = (cosine_score + fuzzy_score) / 2
                    _, missing_skills = self.fuzzy_model.match_skills(
                        ['python', 'java', 'flask', 'sql', 'react', 'machine learning', 'ai'], 
                        text
                    )
                    intermediate_results.append({
                        'missing_skills': missing_skills,
                        'ensemble_details': None
                    })
            else:
                # Standard Logic
                cosine_score = self.cosine_model.calculate_similarity(job_description, text)
                fuzzy_score = self.fuzzy_model.calculate_fuzzy_score(job_description, text)
                skills_score = (cosine_score + fuzzy_score) / 2
                
                # Extract skills for display (Standard)
                _, missing_skills = self.fuzzy_model.match_skills(
                    ['python', 'java', 'flask', 'sql', 'react', 'machine learning', 'ai'], 
                    text
                )
                intermediate_results.append({
                    'missing_skills': missing_skills,
                    'ensemble_details': None
                })

            raw_scores['skills'].append(skills_score)
            
            # 2. Education Score (Placeholder)
            edu_score = min(len(text) / 60, 100)
            raw_scores['education'].append(edu_score)
            
            # --- New Modules ---
            # 4. Persona Match
            persona_score = self.persona_matcher.match_persona(job_description, text)
            raw_scores['persona'].append(persona_score)
            
            # 5. Career Trajectory
            career_score = self.career_predictor.analyze_trajectory(text)
            raw_scores['career'].append(career_score)
            
            # 6. Skill Gap
            gap_result = self.skill_gap_analyzer.analyze_gap(job_description, text)
            gap_score = gap_result['score'] if isinstance(gap_result, dict) else gap_result
            missing_skills_gap = gap_result.get('missing_skills', []) if isinstance(gap_result, dict) else []
            raw_scores['gap'].append(gap_score)
            if algorithm != 'ensemble': # Update missing skills if not ensemble (or merge)
                 intermediate_results[-1]['missing_skills'] = missing_skills_gap
            
            # 7. Experience Transfer
            transfer_score = self.experience_transfer.calculate_transfer_score(job_description, text)
            raw_scores['transfer'].append(transfer_score)
            
            # 8. Innovation Potential
            innovation_score = self.innovation_scorer.calculate_innovation_score(text)
            raw_scores['innovation'].append(innovation_score)
            
            # 9. Neural Embeddings (if not ensemble)
            if algorithm != 'ensemble':
                neural_score = self.neural_ranker.get_semantic_score(job_description, text)
                raw_scores['neural'].append(neural_score)
                
                # 10. Knowledge Graph
                knowledge_score = self.knowledge_graph.graph_similarity(job_description, text)
                raw_scores['knowledge'].append(knowledge_score)
            else:
                # For ensemble, neural and knowledge are handled internally
                raw_scores['neural'].append(0)
                raw_scores['knowledge'].append(0)

        # Normalize scores across the batch
        # Note: For ensemble, we might NOT want to normalize skills if we want to show the raw >100% score
        if algorithm == 'ensemble':
            norm_skills = raw_scores['skills'] # Keep raw super scores
        else:
            norm_skills = self._normalize_scores(raw_scores['skills'])
            
        norm_edu = self._normalize_scores(raw_scores['education'])
        # Normalize new metrics too (optional, but good for consistency)
        norm_persona = self._normalize_scores(raw_scores['persona'])
        norm_career = self._normalize_scores(raw_scores['career'])
        norm_gap = self._normalize_scores(raw_scores['gap'])
        norm_transfer = self._normalize_scores(raw_scores['transfer'])
        norm_innovation = self._normalize_scores(raw_scores['innovation'])
        norm_neural = self._normalize_scores(raw_scores['neural'])
        norm_knowledge = self._normalize_scores(raw_scores['knowledge'])

        ranked_results = []
        for i, resume in enumerate(resumes_data):
            # Calculate final weighted score
            
            if algorithm == 'ensemble':
                # For ensemble, the skills score IS the final score (mostly)
                # But we can still add the other factors as minor adjustments or just display them
                final_score = norm_skills[i] # The super score
            else:
                base_score = (
                    (norm_skills[i] * weights['skills']) + 
                    (norm_edu[i] * weights['education'])
                )
                
                # Average of ALL advanced metrics (now including neural and knowledge)
                if algorithm == 'all':
                    advanced_score = (
                        norm_persona[i] + norm_career[i] + norm_gap[i] + 
                        norm_transfer[i] + norm_innovation[i] + norm_neural[i] + norm_knowledge[i]
                    ) / 7  # Now 7 metrics
                else:
                    # For specific algorithms, use subset
                    advanced_score = (
                        norm_persona[i] + norm_career[i] + norm_gap[i] + 
                        norm_transfer[i] + norm_innovation[i]
                    ) / 5
                
                # Final Score = 60% Base + 40% Advanced (increased weight for AI models)
                final_score = (base_score * 0.6) + (advanced_score * 0.4)
            
            # Extract skills for display
            matched_skills, _ = self.fuzzy_model.match_skills(
                ['python', 'java', 'flask', 'sql', 'react', 'machine learning', 'ai'], 
                resume.get('text', '')
            )

            ranked_results.append({
                'filename': resume['filename'],
                'score': float(round(final_score, 1)),
                'matched_skills': matched_skills,
                'missing_skills': intermediate_results[i]['missing_skills'],
                'email': resume.get('email', 'N/A'),
                'phone': resume.get('phone', 'N/A'),
                'education': 'Extracted',
                'ensemble_details': intermediate_results[i]['ensemble_details'],
                # Add detailed scores for UI
                'scores': {
                    'persona': float(round(norm_persona[i], 1)),
                    'career': float(round(norm_career[i], 1)),
                    'gap': float(round(norm_gap[i], 1)),
                    'transfer': float(round(norm_transfer[i], 1)),
                    'innovation': float(round(norm_innovation[i], 1)),
                    'neural': float(round(norm_neural[i], 1)),
                    'knowledge': float(round(norm_knowledge[i], 1))
                }
            })

        # Sort by score descending
        ranked_results.sort(key=lambda x: x['score'], reverse=True)
        
        # Attach convergence data if available
        if self.convergence_data:
            for result in ranked_results:
                result['convergence_data'] = self.convergence_data
        
        return ranked_results
    
    def calculate_final_accuracy(self, job_description, resumes_data, ranked_results):
        """
        Calculate the unified accuracy score using the MetricsCalculator.
        """
        if not ranked_results:
            return 0.0

        # Assuming resumes_data contains resume text
        resume_text = resumes_data[0]['text'] if resumes_data else ""
        return self.metrics_calculator.calculate_unified_accuracy(ranked_results, job_description, resume_text)
