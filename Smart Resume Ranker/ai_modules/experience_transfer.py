import numpy as np

class ExperienceTransfer:
    def __init__(self):
        self.domains = {
            'tech': ['software', 'it', 'developer', 'engineering', 'data'],
            'finance': ['bank', 'finance', 'audit', 'accounting', 'tax'],
            'healthcare': ['medical', 'health', 'patient', 'clinical', 'care'],
            'marketing': ['sales', 'marketing', 'brand', 'content', 'social']
        }
        self.domain_vectors = self._create_domain_vectors()

    def _create_domain_vectors(self):
        """
        Creates a simple vector representation for each domain.
        """
        all_keywords = sorted(list(set(kw for kws in self.domains.values() for kw in kws)))
        vectors = {}
        for domain, keywords in self.domains.items():
            vector = np.zeros(len(all_keywords))
            for kw in keywords:
                vector[all_keywords.index(kw)] = 1
            vectors[domain] = vector
        return vectors

    def detect_domain(self, text):
        text_lower = text.lower()
        scores = {}
        for domain, keywords in self.domains.items():
            scores[domain] = sum(1 for k in keywords if k in text_lower)
            
        if sum(scores.values()) == 0:
            return 'general'
        return max(scores, key=scores.get)

    def calculate_transfer_score(self, job_text, resume_text):
        """
        Calculates how well experience transfers using domain vectors.
        """
        job_domain = self.detect_domain(job_text)
        resume_domain = self.detect_domain(resume_text)
        
        if job_domain == 'general' or resume_domain == 'general':
            return 60.0

        job_vector = self.domain_vectors.get(job_domain)
        resume_vector = self.domain_vectors.get(resume_domain)

        if job_vector is None or resume_vector is None:
            return 60.0

        # Cosine similarity between domain vectors
        similarity = np.dot(job_vector, resume_vector) / (np.linalg.norm(job_vector) * np.linalg.norm(resume_vector))
        
        return similarity * 100
