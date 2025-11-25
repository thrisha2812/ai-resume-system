from sentence_transformers import SentenceTransformer, util
from services.resume_parser import SKILLS_LIST
import re

# Load the model (This will download ~80MB the first time you run it)
model = SentenceTransformer('all-MiniLM-L6-v2')

def clean_text(text):
    text = text.lower()
    # Allow +, #, . for C++, C#, Node.js
    text = re.sub(r'[^a-z0-9\s\+\#\.]', '', text) 
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_suitability_score(resume_text, job_description_text):
    # 0. Validation
    if not resume_text or not job_description_text:
        return 0, [], []

    # --- PART 1: The Smart Scoring (SBERT) ---
    # This understands context (e.g., "coding" == "development")
    
    # Encode text into high-dimensional vectors
    embeddings1 = model.encode(resume_text, convert_to_tensor=True)
    embeddings2 = model.encode(job_description_text, convert_to_tensor=True)

    # Calculate cosine similarity between the meanings
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    
    # Extract the number and convert to percentage
    score = float(cosine_scores[0][0]) * 100
    
    # --- PART 2: The Visual Skills (Set Matching) ---
    # We still need this to show the recruiter WHICH skills matched
    
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description_text)
    
    try:
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

    except Exception as e:
        print(f"Error in skills extraction: {e}")
        # If skills fail, still return the SBERT score
        return round(score, 2), [], []