import matplotlib.pyplot as plt
import io
import base64

class Visualization:
    @staticmethod
    def plot_ga_convergence(history):
        """
        Plots the convergence of the Genetic Algorithm.
        """
        plt.figure(figsize=(8, 5))
        plt.plot(range(len(history)), history, marker='o')
        plt.title('GA Convergence: Fitness over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness Score')
        plt.grid(True)
        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()

    @staticmethod
    def plot_score_distribution(scores):
        """
        Plots the distribution of resume scores.
        """
        plt.figure(figsize=(8, 5))
        plt.hist(scores, bins=10, color='skyblue', edgecolor='black')
        plt.title('Resume Score Distribution')
        plt.xlabel('Score')
        plt.ylabel('Count')
        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()
