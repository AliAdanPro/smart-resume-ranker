import re

class TextProcessor:
    @staticmethod
    def clean_text(text):
        """
        Cleans and normalizes text.
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep basic punctuation for context if needed
        # For pure keyword matching, removing most is fine
        text = re.sub(r'[^a-zA-Z0-9\s\+\#\.]', ' ', text) # Keep +, #, . for C++, C#, Node.js
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    @staticmethod
    def extract_email(text):
        # Improved regex for email
        match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        return match.group(0) if match else "N/A"

    @staticmethod
    def extract_phone(text):
        # Improved regex for phone numbers (supports various formats)
        match = re.search(r'(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        return match.group(0) if match else "N/A"

    @staticmethod
    def extract_skills(text, skill_db=None):
        """
        Extracts skills based on a provided list or common tech keywords.
        """
        if not skill_db:
            skill_db = ['python', 'java', 'c++', 'javascript', 'html', 'css', 'sql', 'react', 'flask', 'django', 'aws', 'docker', 'kubernetes', 'machine learning', 'ai']
        
        found_skills = []
        text_lower = text.lower()
        for skill in skill_db:
            # Use word boundary to avoid partial matches (e.g., 'java' in 'javascript')
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.append(skill)
        return found_skills
