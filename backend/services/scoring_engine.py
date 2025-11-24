from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from services.resume_parser import SKILLS_LIST # <-- Import our list of tech skills
import re

def clean_text(text):
    text = text.lower()
    # Allow +, #, . for C++, C#, Node.js
    text = re.sub(r'[^a-z0-9\s\+\#\.]', '', text) 
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_suitability_score(resume_text, job_description_text):
    if not resume_text or not job_description_text:
        return 0, [], []

    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description_text)
    
    documents = [cleaned_resume, cleaned_jd]
    
    try:
        # 1. Calculate the Score using TF-IDF (keep this as is)
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = float(cosine_sim[0][0]) * 100
        
        # 2. Extract Smart Skills (The Fix)
        # We get words from the resume & JD
        jd_words = set(cleaned_jd.split())
        resume_words = set(cleaned_resume.split())
        
        # We force the system to ONLY care about words in our SKILLS_LIST
        tech_skills_set = set(SKILLS_LIST)
        
        # Intersection: Words in Resume AND JD AND Skills List
        matched_skills = list(jd_words.intersection(resume_words).intersection(tech_skills_set))
        
        # Missing: Words in JD AND Skills List (but NOT in Resume)
        missing_skills = list(jd_words.intersection(tech_skills_set).difference(resume_words))
        
        return round(score, 2), matched_skills, missing_skills

    except ValueError:
        return 0, [], []