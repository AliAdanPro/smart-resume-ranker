TRANSFORMERS_AVAILABLE = False
SentenceTransformer = None

# Disable transformers to avoid loading issues
# try:
#     from sentence_transformers import SentenceTransformer
#     TRANSFORMERS_AVAILABLE = True
# except ImportError:
#     TRANSFORMERS_AVAILABLE = False

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class NeuralEmbeddingRanker:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the ranker with a pre-trained SentenceTransformer model.
        """
        # Temporarily disable to avoid download issues
        print("Neural embeddings using fallback mode (model download disabled)")
        self.model = None
        return
        
        if not TRANSFORMERS_AVAILABLE:
            print("Warning: sentence_transformers not available")
            self.model = None
            return
            
        try:
            # Try to load model in offline mode first
            self.model = SentenceTransformer(model_name, device='cpu', cache_folder='./models')
            print(f"Successfully loaded {model_name}")
        except Exception as e:
            print(f"Warning: Could not load model '{model_name}': {e}")
            print("Neural embeddings will use fallback scoring")
            self.model = None

    def get_semantic_score(self, job_desc, resume_text):
        """
        Calculates semantic similarity score using embeddings.
        """
        if not self.model or not job_desc or not resume_text:
            return 0.0

        try:
            embeddings = self.model.encode([job_desc, resume_text])
            score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0] * 100
            return round(score, 2)
        except Exception as e:
            print(f"Error in Semantic Scoring: {e}")
            return 0.0

    def get_batch_semantic_scores(self, job_desc, resumes):
        """
        Calculates semantic similarity scores for a job description against multiple resumes.
        Returns a list of scores.
        """
        if not self.model or not job_desc or not resumes:
            return [0.0] * len(resumes)

        try:
            documents = [job_desc] + resumes
            embeddings = self.model.encode(documents)
            job_desc_embedding = embeddings[0]
            resume_embeddings = embeddings[1:]

            scores = cosine_similarity([job_desc_embedding], resume_embeddings)[0] * 100
            return [round(score, 2) for score in scores]
        except Exception as e:
            print(f"Error in Batch Semantic Scoring: {e}")
            return [0.0] * len(resumes)
