import os
import PyPDF2
import docx

class FileParser:
    @staticmethod
    def extract_text(file_path):
        """
        Extracts text from PDF, DOCX, or TXT files.
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        try:
            if ext == '.pdf':
                return FileParser._read_pdf(file_path)
            elif ext == '.docx':
                return FileParser._read_docx(file_path)
            elif ext == '.txt':
                return FileParser._read_txt(file_path)
            else:
                return ""
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""

    @staticmethod
    def _read_pdf(file_path):
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    @staticmethod
    def _read_docx(file_path):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    @staticmethod
    def _read_txt(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
