from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class FuzzyResumeScorer:
    def __init__(self, skill_database=None, match_threshold=80):
        """
        Initialize with an optional skill database and match threshold.
        """
        self.skill_database = skill_database if skill_database else []
        self.match_threshold = match_threshold

    def extract_skills(self, text):
        """
        Extracts skills from text using a predefined skill database.
        """
        if not self.skill_database:
            # Fallback to simple keyword extraction if no database is provided
            return set(text.lower().split())

        extracted_skills = set()
        for skill in self.skill_database:
            if fuzz.partial_ratio(skill.lower(), text.lower()) > self.match_threshold:
                extracted_skills.add(skill)
        return extracted_skills

    def calculate_fuzzy_score(self, job_desc_text, resume_text):
        """
        Calculates a score based on fuzzy matching of content.
        """
        if not job_desc_text or not resume_text:
            return 0.0

        try:
            # Token set ratio for better overlap comparison
            score = fuzz.token_set_ratio(job_desc_text, resume_text)
            return score
        except Exception as e:
            print(f"Error in Fuzzy Score Calculation: {e}")
            return 0.0

    def match_skills(self, job_skills, resume_text):
        """
        Matches specific skills from job description against resume text.
        """
        matched = []
        missing = []
        resume_lower = resume_text.lower()

        for skill in job_skills:
            try:
                # Use partial ratio to find skill in text
                if fuzz.partial_ratio(skill.lower(), resume_lower) > self.match_threshold:
                    matched.append(skill)
                else:
                    missing.append(skill)
            except Exception as e:
                print(f"Error matching skill '{skill}': {e}")

        return matched, missing

    def calculate_batch_fuzzy_scores(self, job_desc_text, resumes):
        """
        Calculates fuzzy scores for a job description against multiple resumes.
        Returns a list of scores.
        """
        if not job_desc_text or not resumes:
            return [0.0] * len(resumes)

        try:
            scores = [self.calculate_fuzzy_score(job_desc_text, resume) for resume in resumes]
            return scores
        except Exception as e:
            print(f"Error in Batch Fuzzy Score Calculation: {e}")
            return [0.0] * len(resumes)
