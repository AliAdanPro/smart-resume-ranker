from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

class CosineSimilarity:
    def __init__(self, ngram_range=(1, 2), max_features=5000):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=ngram_range,
            max_features=max_features
        )

    def preprocess_text(self, text):
        """
        Preprocesses the input text by lowercasing, removing special characters, and extra spaces.
        """
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def calculate_similarity(self, job_description, resume_text):
        """
        Calculates cosine similarity between job description and resume text.
        Returns a score between 0 and 100.
        """
        job_description = self.preprocess_text(job_description)
        resume_text = self.preprocess_text(resume_text)

        if not job_description or not resume_text:
            return 0.0

        try:
            tfidf_matrix = self.vectorizer.fit_transform([job_description, resume_text])
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            score = similarity_matrix[0][0] * 100
            return round(score, 2)
        except Exception as e:
            print(f"Error in Cosine Similarity: {e}")
            return 0.0

    def calculate_batch_similarity(self, job_description, resumes):
        """
        Calculates cosine similarity between a job description and multiple resumes.
        Returns a list of scores.
        """
        job_description = self.preprocess_text(job_description)
        resumes = [self.preprocess_text(resume) for resume in resumes]

        if not job_description or not resumes:
            return [0.0] * len(resumes)

        try:
            documents = [job_description] + resumes
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
            scores = similarity_matrix[0] * 100
            return [round(score, 2) for score in scores]
        except Exception as e:
            print(f"Error in Batch Cosine Similarity: {e}")
            return [0.0] * len(resumes)
