import re

class InnovationScorer:
    def __init__(self):
        self.innovation_keywords = {
            'patent': 10, 'invent': 9, 'create': 8, 'design': 7, 'novel': 8, 'unique': 7,
            'transform': 9, 'revolutionize': 10, 'spearhead': 9, 'found': 8, 'startup': 8,
            'hackathon': 7, 'research': 8, 'publish': 9, 'award': 8
        }

    def calculate_innovation_score(self, resume_text):
        """
        Scores innovation potential based on weighted keywords and vocabulary diversity.
        """
        text_lower = resume_text.lower()
        
        # Weighted keyword score
        keyword_score = sum(self.innovation_keywords[k] for k in self.innovation_keywords if re.search(r'\b' + k + r'\b', text_lower))
        
        # Vocabulary diversity score
        words = text_lower.split()
        if not words:
            return 0.0
            
        unique_ratio = len(set(words)) / len(words)
        
        # Combine metrics
        k_score = min(keyword_score, 50)
        d_score = unique_ratio * 50
        
        return min(round(k_score + d_score, 1), 100.0)
