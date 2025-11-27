from sentence_transformers import SentenceTransformer, util
from services.resume_parser import SKILLS_LIST
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\+\#\.]', '', text) 
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_suitability_score(resume_text, job_description_text):
    if not resume_text or not job_description_text:
        return 0, [], []

    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description_text)
    
    # --- 1. AI Score (SBERT) ---
    embeddings1 = model.encode(resume_text, convert_to_tensor=True)
    embeddings2 = model.encode(job_description_text, convert_to_tensor=True)
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    ai_score = float(cosine_scores[0][0]) * 100
    
    # --- 2. Keyword Score (Hard Skills) ---
    try:
        jd_words = set(cleaned_jd.split())
        resume_words = set(cleaned_resume.split())
        tech_skills_set = set(SKILLS_LIST)
        
        # Skills found in JD
        jd_tech_skills = jd_words.intersection(tech_skills_set)
        
        # Skills found in Resume
        resume_tech_skills = resume_words.intersection(tech_skills_set)
        
        # Intersection
        matched_skills = list(jd_tech_skills.intersection(resume_tech_skills))
        missing_skills = list(jd_tech_skills.difference(resume_tech_skills))
        
        # Calculate Keyword Match %
        # If JD has 10 skills and Resume has 5 of them, score is 50%
        if len(jd_tech_skills) > 0:
            keyword_score = (len(matched_skills) / len(jd_tech_skills)) * 100
        else:
            keyword_score = ai_score # Fallback if JD has no tech keywords
            
    except Exception as e:
        print(f"Error in skills extraction: {e}")
        return 0, [], []

    # --- 3. Final Hybrid Score ---
    # Weighted Average: 60% Keywords + 40% AI Context
    # This penalizes candidates heavily if they lack specific skills
    final_score = (keyword_score * 0.6) + (ai_score * 0.4)
    
    return round(final_score, 2), matched_skills, missing_skills