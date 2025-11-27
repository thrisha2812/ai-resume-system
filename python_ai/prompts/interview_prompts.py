import random

INTERVIEW_QUESTIONS = {
    'Python': [
        'Explain the difference between a list and a tuple in Python. When would you use each?',
        'What are decorators in Python and how do you use them?',
        'Describe how Python handles memory management and garbage collection.',
        'What is the GIL (Global Interpreter Lock) and how does it affect multi-threading?',
        'How do you handle exceptions in Python? Explain try-except-finally.',
        'What are list comprehensions and provide an example of how you would use one.',
        'Explain the difference between *args and **kwargs in Python functions.',
        'What is a generator in Python and how is it different from a regular function?',
    ],
    'Java': [
        'Explain the concept of inheritance in Java and how it differs from composition.',
        'What are the four access modifiers in Java? Explain each one.',
        'Describe the difference between abstract classes and interfaces.',
        'What is the purpose of the static keyword in Java?',
        'Explain the concept of polymorphism with a real-world example.',
        'What is exception handling in Java? How do you use try-catch-finally?',
        'Describe the difference between checked and unchecked exceptions.',
        'What are the benefits of using generics in Java?',
    ],
    'JavaScript': [
        'Explain the difference between var, let, and const in JavaScript.',
        'What is hoisting in JavaScript? Provide examples.',
        'Describe the event loop and how asynchronous code works in JavaScript.',
        'What is a closure in JavaScript? Provide a practical example.',
        'Explain the this keyword in JavaScript and its different contexts.',
        'What is the difference between === and == in JavaScript?',
        'Describe how promises and async/await work in JavaScript.',
        'What is the spread operator and how would you use it?',
    ],
    'React': [
        'What are React hooks? Name a few and explain their purpose.',
        'Explain the difference between controlled and uncontrolled components.',
        'What is the virtual DOM and why is it important?',
        'How do you handle state management in React applications?',
        'Describe the lifecycle methods of a React class component.',
        'What are keys in React and why are they important in lists?',
        'Explain the concept of lifting state up in React.',
        'How do you optimize performance in React applications?',
    ],
    'SQL': [
        'Explain the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN.',
        'What is normalization and why is it important in database design?',
        'Describe the different types of SQL keys: PRIMARY, FOREIGN, UNIQUE, and COMPOSITE.',
        'What is an index in a database and why is it used?',
        'Explain the difference between WHERE and HAVING clauses.',
        'What are aggregate functions in SQL? Name a few examples.',
        'Describe the difference between GROUP BY and ORDER BY.',
        'What is a stored procedure and when would you use one?',
    ],
    'General': [
        'Tell me about a challenging project you worked on and how you overcame the obstacles.',
        'How do you approach learning a new technology or framework?',
        'Describe a time when you had to debug a complex issue. What was your approach?',
        'How do you handle conflicts or disagreements with team members?',
        'What is your experience with version control systems like Git?',
        'Tell me about your experience with Agile development methodologies.',
        'How do you ensure code quality in your projects?',
        'Describe your approach to writing unit tests and why they are important.',
    ],
    'Problem Solving': [
        'Walk me through how you would approach solving an unknown problem you encounter.',
        'Describe a time when you optimized a process or solution. What was the result?',
        'How do you break down a complex problem into manageable parts?',
        'Tell me about a time when you had to learn something new quickly.',
        'Describe your experience with performance optimization.',
        'How do you approach code review and providing constructive feedback?',
        'Tell me about a time when you had to balance speed with quality.',
        'How do you stay updated with industry trends and new technologies?',
    ]
}

def get_random_questions(skill, question_count):
    """
    Get random interview questions for the given skill.
    """
    
    # Normalize skill name
    skill_key = skill.strip().title()
    
    # Get questions for the skill, fallback to General
    if skill_key in INTERVIEW_QUESTIONS:
        questions = INTERVIEW_QUESTIONS[skill_key]
    else:
        # Try to find partial match
        found = False
        for key in INTERVIEW_QUESTIONS.keys():
            if skill_key.lower() in key.lower() or key.lower() in skill_key.lower():
                questions = INTERVIEW_QUESTIONS[key]
                found = True
                break
        if not found:
            questions = INTERVIEW_QUESTIONS['General']
    
    # Shuffle and avoid repetition
    shuffled = random.sample(questions, min(len(questions), max(3, 5 - question_count)))
    return shuffled

def get_question_prompt(skill, question_count):
    """
    Get a full prompt for generating questions via LLM.
    """
    
    prompt = f"""Generate a technical interview question for someone with {skill} skills.

    This is question number {question_count + 1} out of 5.
    
    Requirements:
    - The question should be appropriate for assessing {skill} knowledge
    - It should be open-ended and allow for detailed answers
    - It should test both knowledge and practical experience
    
    Return ONLY the question text, nothing else."""
    
    return prompt
