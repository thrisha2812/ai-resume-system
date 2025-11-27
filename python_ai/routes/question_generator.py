import json
import random

def generate_question(skills, question_count):
    """
    Generate interview questions based on extracted skills.
    Each question focuses on one or more of the candidate's skills.
    """
    try:
        q_count = int(question_count)
    except Exception:
        q_count = 0
    
    # Parse skills if it's a string (from Java backend)
    if isinstance(skills, str):
        try:
            # Try parsing as JSON array
            if skills.startswith('['):
                skills = json.loads(skills)
            else:
                skills = [s.strip() for s in skills.split(',')]
        except:
            skills = ['General']
    
    if not skills:
        skills = ['General']
    
    # Question templates by category
    experience_questions = [
        "Tell me about your experience with {skill} and a challenging project where you used it.",
        "Describe your most significant project using {skill}. What was the impact?",
        "How have you evolved your {skill} expertise? Share an example of learning on the job.",
        "What's your approach to staying current with {skill}? Any recent projects?",
        "Tell me about a time you had to troubleshoot a complex issue with {skill}.",
    ]
    
    design_questions = [
        "How would you design a system using {skill}? Walk through your architectural approach.",
        "Explain how you'd choose {skill} over alternatives for a specific problem.",
        "Describe the trade-offs you consider when using {skill} in production systems.",
        "Tell me about optimizing performance in a {skill} application you built.",
        "How do you handle scalability challenges with {skill}?",
    ]
    
    best_practice_questions = [
        "What are the key best practices you follow when working with {skill}?",
        "How do you ensure code quality and maintainability with {skill}?",
        "Describe your testing strategy for {skill} applications.",
        "What common mistakes have you seen with {skill}, and how do you avoid them?",
        "How do you approach debugging issues in {skill} codebases?",
    ]
    
    # Select skill(s) for this question
    selected_skills = skills.copy()
    if len(selected_skills) > 2:
        selected_skills = random.sample(selected_skills, min(2, len(selected_skills)))
    
    primary_skill = selected_skills[0] if selected_skills else 'your technical skills'
    
    # Distribute questions across types
    question_type = q_count % 3
    
    if question_type == 0:
        question = random.choice(experience_questions).format(skill=primary_skill)
    elif question_type == 1:
        question = random.choice(design_questions).format(skill=primary_skill)
    else:
        question = random.choice(best_practice_questions).format(skill=primary_skill)
    
    return question
