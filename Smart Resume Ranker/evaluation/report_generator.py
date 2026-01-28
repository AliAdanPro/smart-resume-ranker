import pandas as pd
import os

class ReportGenerator:
    @staticmethod
    def generate_csv(results, output_path):
        """
        Exports results to a CSV file.
        """
        df = pd.DataFrame(results)
        df.to_csv(output_path, index=False)
        return output_path

    @staticmethod
    def generate_summary(results):
        """
        Generates a text summary of the ranking.
        """
        if not results:
            return "No results to summarize."
            
        top_candidate = results[0]
        avg_score = sum(r['score'] for r in results) / len(results)
        
        summary = f"""
        Ranking Summary
        ---------------
        Total Candidates: {len(results)}
        Average Score: {avg_score:.2f}
        
        Top Candidate:
        Name/File: {top_candidate['filename']}
        Score: {top_candidate['score']}
        """
        return summary
