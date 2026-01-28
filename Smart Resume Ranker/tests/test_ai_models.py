import unittest
from ai_modules.genetic_algorithm import GAOptimizer
from ai_modules.cosine_similarity import CosineSimilarity
from ai_modules.fuzzy_logic import FuzzyResumeScorer
from ai_modules.neural_embeddings import NeuralEmbeddingRanker

class TestAIModels(unittest.TestCase):

    def test_genetic_algorithm(self):
        optimizer = GAOptimizer(population_size=10, generations=5, mutation_rate=0.2)
        best_weights, history = optimizer.optimize()
        self.assertTrue(len(best_weights) == 3)
        self.assertAlmostEqual(sum(best_weights), 1.0, places=2)

    def test_cosine_similarity(self):
        cosine = CosineSimilarity()
        score = cosine.calculate_similarity("Data Scientist", "Experienced Data Scientist with Python skills")
        self.assertGreater(score, 0)

    def test_fuzzy_logic(self):
        fuzzy = FuzzyResumeScorer(skill_database=["Python", "Machine Learning", "Data Analysis"])
        matched, missing = fuzzy.match_skills(["Python", "Data Analysis"], "Expert in Python and Data Analysis")
        self.assertIn("Python", matched)
        self.assertIn("Data Analysis", matched)
        self.assertEqual(len(missing), 0)

    def test_neural_embeddings(self):
        ranker = NeuralEmbeddingRanker()
        score = ranker.get_semantic_score("Software Engineer", "Experienced Software Engineer with Java expertise")
        self.assertGreater(score, 0)

if __name__ == "__main__":
    unittest.main()