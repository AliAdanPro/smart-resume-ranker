# Smart Resume Ranker

A powerful AI-driven tool to screen and rank resumes against job descriptions using Cosine Similarity, Fuzzy Logic, and Genetic Algorithms.

## Features
- **Multi-Format Support**: Upload PDF, DOCX, or TXT resumes.
- **AI-Powered Ranking**: Uses TF-IDF and Cosine Similarity for content matching.
- **Fuzzy Logic**: Matches skills and experience even with slight variations.
- **Genetic Algorithm**: Optimizes ranking weights for better accuracy.
- **Visual Analytics**: View convergence graphs and score distributions.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000`.
3. Paste a job description and upload resumes.
4. Select an algorithm and click "Analyze".

## Project Structure
- `app.py`: Main Flask server.
- `ai_modules/`: Core AI logic (Cosine, Fuzzy, GA).
- `utils/`: File parsing and text processing.
- `evaluation/`: Metrics and visualization.
- `templates/`: HTML frontend.
- `static/`: CSS and JS assets.
