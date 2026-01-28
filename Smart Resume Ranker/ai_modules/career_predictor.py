import re

class CareerPredictor:
    def __init__(self):
        self.seniority_keywords = {
            'intern': 1,
            'junior': 2, 'associate': 2,
            'engineer': 3, 'developer': 3, 'analyst': 3,
            'senior': 4, 'lead': 5,
            'manager': 6, 'architect': 7,
            'director': 8, 'vp': 9, 'head': 9, 'chief': 10
        }

    def analyze_trajectory(self, resume_text):
        """
        Analyzes the career trajectory based on job titles found in the text.
        Returns a trajectory score (0-100) indicating growth.
        """
        found_levels = []
        text_lower = resume_text.lower()
        
        # Use regex to find job titles
        for title, level in self.seniority_keywords.items():
            if re.search(r'\b' + title + r'\b', text_lower):
                found_levels.append(level)
        
        if not found_levels:
            return 50.0 # Neutral start
            
        # Calculate weighted average level
        avg_level = sum(found_levels) / len(found_levels)
        
        # Calculate max level achieved
        max_level = max(found_levels)
        
        # Trajectory score: Combination of max level and average level
        score = ((max_level * 0.7) + (avg_level * 0.3)) * 10
        
        return min(round(score, 1), 100.0)
