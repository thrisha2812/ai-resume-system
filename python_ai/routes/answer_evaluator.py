import re

def evaluate_answer(question, answer):
    """
    Dynamically evaluate interview answers based on content quality indicators.
    Scores range from 0-100 based on multiple criteria.
    """
    if not answer or len(answer.strip()) < 10:
        return 20, "Your answer is too brief. Please provide more detail about your experience and approach."
    
    answer_lower = answer.lower()
    question_lower = question.lower()
    
    # Start with base score
    score = 50
    feedback_parts = []
    
    # Scoring criteria
    
    # 1. Length and detail (0-15 points)
    words = len(answer.split())
    if words < 30:
        feedback_parts.append("Consider providing more detail")
    elif words < 50:
        score += 8
    elif words < 100:
        score += 12
    else:
        score += 15
    
    # 2. Specific examples (0-15 points)
    if re.search(r'(project|example|instance|case|built|created|developed|implemented)', answer_lower):
        score += 15
        feedback_parts.append("Great use of concrete examples")
    elif re.search(r'(did|made|worked|experience)', answer_lower):
        score += 8
    else:
        feedback_parts.append("Add specific examples of what you built or accomplished")
    
    # 3. Technical depth (0-20 points)
    technical_terms = [
        'architecture', 'algorithm', 'optimization', 'performance', 'scalability',
        'database', 'framework', 'api', 'deployment', 'testing', 'debugging',
        'pattern', 'best practice', 'refactor', 'integration', 'pipeline'
    ]
    tech_count = sum(1 for term in technical_terms if term in answer_lower)
    if tech_count >= 3:
        score += 20
        feedback_parts.append("Excellent technical depth")
    elif tech_count >= 2:
        score += 15
        feedback_parts.append("Good technical terminology")
    elif tech_count >= 1:
        score += 10
    else:
        feedback_parts.append("Use more technical terminology to demonstrate expertise")
    
    # 4. Problem-solving mindset (0-15 points)
    problem_indicators = [
        'challenge', 'obstacle', 'solved', 'fix', 'improved', 'optimized',
        'issue', 'bug', 'error', 'resolved', 'overcame', 'learned'
    ]
    problem_count = sum(1 for term in problem_indicators if term in answer_lower)
    if problem_count >= 3:
        score += 15
        feedback_parts.append("Strong problem-solving approach")
    elif problem_count >= 2:
        score += 10
        feedback_parts.append("Good mention of challenges overcome")
    elif problem_count >= 1:
        score += 5
    else:
        feedback_parts.append("Discuss challenges and how you overcame them")
    
    # 5. Results and impact (0-15 points)
    result_indicators = [
        'result', 'outcome', 'impact', 'improved', 'reduced', 'increased',
        'faster', 'efficient', 'user', 'customers', 'metric', 'performance'
    ]
    result_count = sum(1 for term in result_indicators if term in answer_lower)
    if result_count >= 3:
        score += 15
        feedback_parts.append("Excellent - you quantified the impact")
    elif result_count >= 2:
        score += 10
        feedback_parts.append("Good mention of results and outcomes")
    elif result_count >= 1:
        score += 5
    else:
        feedback_parts.append("Include measurable outcomes and impact")
    
    # 6. Relevance to question (0-10 points)
    # Extract key skill from question
    skill_match = False
    common_skills = ['python', 'java', 'javascript', 'react', 'angular', 'node', 
                     'django', 'flask', 'spring', 'sql', 'database', 'cloud',
                     'docker', 'kubernetes', 'aws', 'azure', 'git']
    for skill in common_skills:
        if skill in question_lower and skill in answer_lower:
            skill_match = True
            break
    
    if skill_match or 'skill' in question_lower:
        score += 10
        feedback_parts.append("You directly addressed the skill mentioned")
    else:
        feedback_parts.append("Ensure your answer directly addresses the skill in the question")
    
    # 7. Collaboration and learning (0-5 points)
    collaboration_terms = ['team', 'collaborated', 'feedback', 'mentor', 'learned', 'helped']
    if any(term in answer_lower for term in collaboration_terms):
        score += 5
        feedback_parts.append("Nice mention of teamwork and learning")
    
    # Cap score at 100
    score = min(100, score)
    
    # Build feedback message
    if score >= 85:
        base_feedback = "Excellent answer with strong technical depth and clear examples."
    elif score >= 75:
        base_feedback = "Good answer demonstrating solid experience."
    elif score >= 65:
        base_feedback = "Acceptable answer, but could use more specific examples."
    elif score >= 50:
        base_feedback = "Your answer shows understanding, but needs more detail."
    else:
        base_feedback = "Your answer is too brief or lacks specific examples."
    
    # Combine base feedback with suggestions
    if feedback_parts:
        feedback = base_feedback + " " + " - ".join(feedback_parts[:2]) + "."
    else:
        feedback = base_feedback
    
    return score, feedback
