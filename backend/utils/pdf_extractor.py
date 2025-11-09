import pdfplumber
import docx2txt
import os
import re

def extract_text_from_file(file_path):
    text = ""
    extension = os.path.splitext(file_path)[1].lower()

    try:
        if extension == '.pdf':
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        elif extension == '.docx':
            text = docx2txt.process(file_path)
        else:
            return None  # Unsupported file type
        
        # Basic text cleaning
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None