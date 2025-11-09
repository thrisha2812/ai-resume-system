import spacy
import re

# Load the small English model
try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    print("Spacy model 'en_core_web_sm' not found. Please run:")
    print("python -m spacy download en_core_web_sm")
    nlp = spacy.blank("en") 

# TODO (Thrisha/Kavya): Expand this list significantly!
SKILLS_LIST = [
    'python', 'java', 'c++', 'javascript', 'react', 'node.js', 'flask',
    'mongodb', 'sql', 'aws', 'docker', 'git', 'machine learning'
]

def parse_resume(text):
    doc = nlp(text.lower())
    
    # 1. Extract Name (simple heuristic)
    name = "Not Found"
    for ent in doc.ents:
        if ent.label_ == 'PERSON' and len(ent.text.split()) < 4:
            name = ent.text.title()
            break
    
    # 2. Extract Email
    email = "Not Found"
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if email_match:
        email = email_match.group(0)

    # 3. Extract Skills (using keyword matching)
    skills = []
    text_lower = text.lower()
    for skill in SKILLS_LIST:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            skills.append(skill)
    
    # TODO (Thrisha/Kavya): Improve this to find education details
    education = []
    edu_keywords = ['education', 'university', 'college', 'b.tech', 'm.tech']
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in edu_keywords):
            education.append(sent.text.strip())

    return {
        'name': name,
        'email': email,
        'skills': list(set(skills)), # Unique skills
        'education': education,
        'full_text': text
    }