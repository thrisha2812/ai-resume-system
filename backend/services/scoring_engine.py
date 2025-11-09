from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text) # Remove punctuation and numbers
    text = re.sub(r'\s+', ' ', text).strip() # Remove extra whitespace
    return text

def calculate_suitability_score(resume_text, job_description_text):
    if not resume_text or not job_description_text:
        return 0, [], []

    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description_text)
    
    documents = [cleaned_resume, cleaned_jd]
    
    try:
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = float(cosine_sim[0][0]) * 100
        
        feature_names = tfidf_vectorizer.get_feature_names_out()
        jd_vocab = set(word for word in feature_names if word in cleaned_jd.split())
        resume_vocab = set(word for word in feature_names if word in cleaned_resume.split())

        matched_skills = list(jd_vocab.intersection(resume_vocab))
        missing_skills = list(jd_vocab.difference(resume_vocab))
        
        # TODO (Thrisha/Kavya): Improve this filter
        common_words = {'and', 'or', 'the', 'a', 'in', 'of', 'for', 'with', 'to', 'is', 'as', 'on'}
        matched_skills = [s for s in matched_skills if s not in common_words and len(s) > 2]
        missing_skills = [s for s in missing_skills if s not in common_words and len(s) > 2]
        
        return round(score, 2), matched_skills, missing_skills

    except ValueError as e:
        print(f"Error in TF-IDF: {e}")
        return 0, [], []    