import random
from services.scoring_engine import model, util

# 1. ROBUST QUESTION BANK
INTERVIEW_DATA = {
    "python": [
        {"q": "Difference between list and tuple?", "a": "Lists are mutable, tuples are immutable."},
        {"q": "Explain decorators.", "a": "Functions that modify other functions."},
        {"q": "How is memory managed?", "a": "Private heap and garbage collection."}
    ],
    "react": [
        {"q": "What is Virtual DOM?", "a": "Lightweight copy of real DOM for optimization."},
        {"q": "useState vs useEffect?", "a": "State management vs side effects."},
        {"q": "What are Props?", "a": "Read-only data passed to components."}
    ],
    "javascript": [
        {"q": "What is a Closure?", "a": "Function remembering outer scope."},
        {"q": "Explain 'this'.", "a": "Refers to the object executing code."},
        {"q": "Let vs Const?", "a": "Const cannot be reassigned."}
    ],
    "sql": [
        {"q": "WHERE vs HAVING?", "a": "Filter rows vs Filter groups."},
        {"q": "What is Primary Key?", "a": "Unique record identifier."}
    ],
    # FALLBACKS
    "general": [
        {"q": "What is an API?", "a": "Interface for software communication."},
        {"q": "Explain Git.", "a": "Version control system."},
        {"q": "What is Agile?", "a": "Iterative development methodology."}
    ],
    "hr": [
        {"q": "Tell me about yourself.", "a": "I am a passionate engineer..."},
        {"q": "Biggest strength?", "a": "Quick learner and adaptable."},
        {"q": "Why this company?", "a": "Aligns with my career goals."}
    ]
}

def get_interview_questions(skills):
    selected_questions = []
    skills_lower = [s.lower() for s in skills]
    
    print(f"DEBUG: Generating for skills: {skills_lower}")

    # 1. Tech Questions
    for skill_key in INTERVIEW_DATA:
        if skill_key in skills_lower and skill_key not in ['hr', 'general']:
            questions = INTERVIEW_DATA[skill_key]
            # Safely pick 1
            if questions:
                q_data = random.choice(questions)
                selected_questions.append({
                    "type": "Technical",
                    "skill": skill_key.title(),
                    "question": q_data['q'],
                    "ideal_answer": q_data['a']
                })

    # 2. General Fallback (If < 2 technical questions found)
    if len(selected_questions) < 2:
        print("DEBUG: Not enough tech matches. Adding General questions.")
        gen_qs = INTERVIEW_DATA['general']
        # Safely pick up to 2
        count = min(len(gen_qs), 2)
        random_gen = random.sample(gen_qs, count)
        
        for q in random_gen:
            # Avoid duplicates
            if not any(existing['question'] == q['q'] for existing in selected_questions):
                selected_questions.append({
                    "type": "Technical",
                    "skill": "General Computing",
                    "question": q['q'],
                    "ideal_answer": q['a']
                })

    # 3. HR Questions (Fill up to 5)
    hr_qs = INTERVIEW_DATA['hr']
    attempts = 0
    while len(selected_questions) < 5 and attempts < 10:
        q_data = random.choice(hr_qs)
        if not any(existing['question'] == q_data['q'] for existing in selected_questions):
            selected_questions.append({
                "type": "HR",
                "skill": "Behavioral",
                "question": q_data['q'],
                "ideal_answer": q_data['a']
            })
        attempts += 1
            
    print(f"DEBUG: Final generated list has {len(selected_questions)} questions.")
    return selected_questions

def evaluate_response(user_answer, ideal_answer):
    if not user_answer or len(user_answer) < 2: return 0, "Too short."
    
    emb1 = model.encode(user_answer, convert_to_tensor=True)
    emb2 = model.encode(ideal_answer, convert_to_tensor=True)
    score = util.cos_sim(emb1, emb2).item() * 100
    
    feedback = "Good attempt."
    if score > 70: feedback = "Excellent answer!"
    elif score < 40: feedback = "Try to be more specific."
    
    return round(score, 1), feedback