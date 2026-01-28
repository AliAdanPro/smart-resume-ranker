from .fuzzy_logic import FuzzyResumeScorer
import re
from collections import defaultdict

class SkillGapAnalyzer:
    def __init__(self):
        self.fuzzy_scorer = FuzzyResumeScorer()
        self.skill_hierarchy = {
            'critical': ['python', 'java', 'sql', 'aws', 'machine learning', 'leadership', 'communication'],
            'important': ['react', 'node.js', 'docker', 'kubernetes', 'git', 'problem solving', 'teamwork'],
            'useful': ['html', 'css', 'javascript', 'excel', 'powerpoint', 'project management', 'agile']
        }
        self.skill_synonyms = {
            'python': ['python', 'py', 'python3'],
            'javascript': ['javascript', 'js', 'ecmascript'],
            'machine learning': ['machine learning', 'ml', 'artificial intelligence', 'ai'],
            'communication': ['communication', 'interpersonal', 'verbal', 'written']
        }

    def _normalize_skill(self, skill):
        """Normalize skill variations to standard form"""
        skill_lower = skill.lower()
        for standard, variations in self.skill_synonyms.items():
            if skill_lower in variations:
                return standard
        return skill_lower

    def _extract_skills_advanced(self, text):
        """Enhanced skill extraction with pattern matching and normalization"""
        extracted_skills = set()
        text_lower = text.lower()
        
        # Extract from all skill categories
        for category, skills in self.skill_hierarchy.items():
            for skill in skills:
                # Use word boundaries for exact matching
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    extracted_skills.add(self._normalize_skill(skill))
                    
                # Check synonyms
                if skill in self.skill_synonyms:
                    for synonym in self.skill_synonyms[skill]:
                        pattern = r'\b' + re.escape(synonym.lower()) + r'\b'
                        if re.search(pattern, text_lower):
                            extracted_skills.add(self._normalize_skill(skill))
        
        return extracted_skills

    def analyze_gap(self, job_description, resume_text):
        """
        Advanced gap analysis with weighted scoring and detailed insights.
        """
        # Extract skills using enhanced method
        required_skills = self._extract_skills_advanced(job_description)
        resume_skills = self._extract_skills_advanced(resume_text)
        
        # Fallback if no skills detected in job description
        if not required_skills:
            required_skills = {'python', 'communication', 'problem solving', 'teamwork'}
            
        # Categorize missing skills
        missing_skills = required_skills - resume_skills
        present_skills = required_skills & resume_skills
        
        # Calculate weighted score
        total_penalty = 0
        skill_gaps = defaultdict(list)
        
        for skill in missing_skills:
            penalty = self._get_skill_penalty(skill)
            total_penalty += penalty
            
            # Categorize the gap
            category = self._get_skill_category(skill)
            skill_gaps[category].append(skill)
        
        # Calculate final score with bonus for having skills
        base_score = max(0, 100 - total_penalty)
        skill_coverage = len(present_skills) / len(required_skills) if required_skills else 1
        adjusted_score = base_score * (0.7 + 0.3 * skill_coverage)
        
        return {
            'score': round(min(adjusted_score, 100), 1),
            'missing_skills': list(missing_skills),
            'present_skills': list(present_skills),
            'skill_coverage': round(skill_coverage * 100, 1),
            'gaps_by_category': dict(skill_gaps)
        }
    
    def _get_skill_penalty(self, skill):
        """Get penalty weight for missing skill"""
        if skill in self.skill_hierarchy['critical']:
            return 20
        elif skill in self.skill_hierarchy['important']:
            return 10
        elif skill in self.skill_hierarchy['useful']:
            return 5
        else:
            return 8  # Default penalty
    
    def _get_skill_category(self, skill):
        """Determine skill category"""
        for category, skills in self.skill_hierarchy.items():
            if skill in skills:
                return category
        return 'other'
