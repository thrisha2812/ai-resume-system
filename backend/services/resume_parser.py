import spacy
import re

# Load model
try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    nlp = spacy.blank("en")

# (Keep the big SKILLS_LIST exactly as it was - I have shortened it here for brevity, 
# but YOU should keep the full list you pasted earlier)
SKILLS_LIST = [
    'python', 'java', 'c++', 'c', 'c#', 'javascript', 'typescript', 'html', 'css', 'sql', 'nosql', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin',
    'react', 'react.js', 'angular', 'vue', 'next.js', 'node.js', 'express', 'flask', 'django', 'fastapi', 'spring', 'spring boot', 'hibernate', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'tailwind', 'tailwindcss', 'bootstrap', 'material-ui',
    'mongodb', 'postgresql', 'mysql', 'sqlite', 'redis', 'cassandra', 'oracle', 'firebase', 'dynamodb',
    'git', 'github', 'gitlab', 'docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'gcp', 'terraform', 'ansible', 'circleci', 'linux', 'bash', 'nginx',
    'rest api', 'restful api', 'graphql', 'microservices', 'agile', 'scrum', 'machine learning', 'deep learning', 'nlp', 'data science', 'artificial intelligence', 'system design', 'oop', 'dsa', 'seo', 'sem', 'marketing'
]

def clean_text_for_name(text):
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    # Remove phone numbers (approximate)
    text = re.sub(r'\+?\d[\d -]{8,12}\d', '', text)
    # Remove non-name characters (keep letters, spaces, dots)
    text = re.sub(r'[^a-zA-Z\s\.]', '', text)
    # Remove extra spaces
    return text.strip()

def parse_resume(text):
    # 1. Extract Email (Do this first, it's easy and accurate)
    email = "No Email Found"
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    if email_match:
        email = email_match.group(0)

    # 2. Smart Name Extraction
    name = "Unknown Candidate"
    
    # Strategy A: Spacy Entity Recognition (Strict)
    # Only look at the first 500 chars (names are at the top)
    doc = nlp(text[:500]) 
    
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            # Clean the entity (remove punctuation/titles)
            clean_ent = clean_text_for_name(ent.text)
            # A valid name usually has 2-4 words (e.g., "Rahul Mishra", not "Rahul")
            if 2 <= len(clean_ent.split()) <= 4:
                name = clean_ent.title()
                break
    
    # Strategy B: Fallback to First Line (but cleaner)
    if name == "Unknown Candidate":
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # Take the first line
            first_line = lines[0]
            # Clean it heavily (remove emails, numbers, locations if possible)
            cleaned_line = clean_text_for_name(first_line)
            # If the remaining text is short enough to be a name, take it
            if 2 <= len(cleaned_line.split()) <= 5:
                name = cleaned_line.title()

    # 3. Extract Skills
    skills = []
    text_lower = text.lower()
    for skill in SKILLS_LIST:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            skills.append(skill)
    
    return {
        'name': name,
        'email': email,
        'skills': list(set(skills)), 
        'education': [], 
        'full_text': text
    }