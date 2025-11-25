import spacy
import re

# Load model
try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    nlp = spacy.blank("en")

SKILLS_LIST = [
    'python', 'java', 'c++', 'c', 'c#', 'javascript', 'typescript', 'html', 'css', 'sql', 'nosql', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin',
    'react', 'react.js', 'angular', 'vue', 'next.js', 'node.js', 'express', 'flask', 'django', 'fastapi', 'spring', 'spring boot', 'hibernate', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'tailwind', 'tailwindcss', 'bootstrap', 'material-ui',
    'mongodb', 'postgresql', 'mysql', 'sqlite', 'redis', 'cassandra', 'oracle', 'firebase', 'dynamodb',
    'git', 'github', 'gitlab', 'docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'gcp', 'terraform', 'ansible', 'circleci', 'linux', 'bash', 'nginx',
    'rest api', 'restful api', 'graphql', 'microservices', 'agile', 'scrum', 'machine learning', 'deep learning', 'nlp', 'data science', 'artificial intelligence', 'system design', 'oop', 'dsa', 'seo', 'sem', 'marketing', 'excel', 'tally'
]

def clean_text_for_name(text):
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\+?\d[\d -]{8,12}\d', '', text)
    text = re.sub(r'[^a-zA-Z\s\.]', '', text)
    return text.strip()

def extract_experience(text):
    # Pattern: Looks for a number (like 5, 2.5) followed by "years", "year", "yrs"
    # \d+       = one or more digits
    # (?:\.\d+)? = optional decimal part (like .5)
    # \+?       = optional plus sign (like 5+)
    # \s* = optional space
    pattern = r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?|yoe)'
    
    matches = re.findall(pattern, text.lower())
    
    if matches:
        print(f"DEBUG: Found experience numbers: {matches}") # <-- Watch your terminal for this!
        try:
            # Convert to floats and get the biggest number found
            years = [float(m) for m in matches]
            return max(years)
        except ValueError:
            return 0
    return 0

def parse_resume(text):
    doc = nlp(text[:5000]) # Limit to first 5000 chars for speed
    
    # 1. Extract Email
    email = "No Email Found"
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    if email_match:
        email = email_match.group(0)

    # 2. Extract Name
    name = "Unknown Candidate"
    doc_name = nlp(text[:500])
    for ent in doc_name.ents:
        if ent.label_ == 'PERSON':
            clean_ent = clean_text_for_name(ent.text)
            if 2 <= len(clean_ent.split()) <= 4:
                name = clean_ent.title()
                break
    
    if name == "Unknown Candidate":
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            cleaned_line = clean_text_for_name(lines[0])
            if 2 <= len(cleaned_line.split()) <= 5:
                name = cleaned_line.title()

    # 3. Extract Experience (New Function)
    years_exp = extract_experience(text)

    # 4. Extract Skills
    skills = []
    text_lower = text.lower()
    for skill in SKILLS_LIST:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            skills.append(skill)
    
    return {
        'name': name,
        'email': email,
        'years_of_experience': years_exp, # This sends the number to the database
        'skills': list(set(skills)), 
        'education': [], 
        'full_text': text
    }