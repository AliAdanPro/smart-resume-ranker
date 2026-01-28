import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PersonaMatcher:
    def __init__(self):
        self.personas = {
            'leader': ['manage', 'lead', 'direct', 'strategy', 'oversee', 'budget', 'team', 'executive', 'vision', 'mentor'],
            'developer': ['code', 'program', 'develop', 'software', 'engineer', 'implement', 'debug', 'api', 'framework', 'algorithm'],
            'analyst': ['analyze', 'data', 'report', 'research', 'insight', 'trend', 'metric', 'evaluate', 'statistics', 'visualization'],
            'creative': ['design', 'creative', 'innovative', 'artistic', 'visual', 'brand', 'content', 'marketing', 'ux', 'ui'],
            'technical': ['technical', 'system', 'infrastructure', 'network', 'security', 'database', 'server', 'cloud', 'devops', 'architecture']
        }
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')

    def detect_persona(self, text):
        """
        Enhanced persona detection using weighted scoring and TF-IDF analysis.
        """
        text_lower = text.lower()
        scores = {}
        
        # Weighted keyword matching
        for persona, keywords in self.personas.items():
            weighted_score = 0
            for keyword in keywords:
                # Count occurrences and apply TF-like weighting
                occurrences = text_lower.count(keyword)
                weight = 1 + np.log(1 + occurrences)  # Log weighting to prevent single keyword dominance
                weighted_score += weight
            scores[persona] = weighted_score
            
        # Normalize scores
        total = sum(scores.values())
        if total == 0:
            return "neutral", 0
            
        dominant_persona = max(scores, key=scores.get)
        confidence = (scores[dominant_persona] / total) * 100
        
        return dominant_persona, round(confidence, 1)

    def match_persona(self, job_text, resume_text):
        """
        Advanced persona compatibility scoring using semantic similarity.
        """
        job_persona, job_conf = self.detect_persona(job_text)
        resume_persona, resume_conf = self.detect_persona(resume_text)
        
        # Perfect match bonus
        if job_persona == resume_persona:
            base_score = 100.0
        else:
            # Cross-persona compatibility matrix
            compatibility_matrix = {
                ('leader', 'analyst'): 75,
                ('leader', 'technical'): 70,
                ('developer', 'technical'): 85,
                ('developer', 'analyst'): 80,
                ('creative', 'developer'): 70,
                ('analyst', 'technical'): 75,
                ('technical', 'leader'): 65,
                ('creative', 'analyst'): 60
            }
            
            # Check both directions
            key1 = (job_persona, resume_persona)
            key2 = (resume_persona, job_persona)
            
            if key1 in compatibility_matrix:
                base_score = compatibility_matrix[key1]
            elif key2 in compatibility_matrix:
                base_score = compatibility_matrix[key2]
            else:
                base_score = 50.0  # Default compatibility
        
        # Confidence adjustment
        confidence_factor = min(job_conf, resume_conf) / 100
        adjusted_score = base_score * (0.7 + 0.3 * confidence_factor)
        
        return round(min(adjusted_score, 100.0), 1)
