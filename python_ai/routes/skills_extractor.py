import re
import json

def extract_skills(resume_text):
    """
    Extract skills from resume text using pattern matching and keyword recognition.
    In production, this would use an LLM API (OpenAI, Ollama, etc.)
    """
    
    # Common programming and technical skills
    common_skills = {
        'Python': r'\bpython\b',
        'Java': r'\bjava\b',
        'JavaScript': r'\bjavascript\b|\bjs\b',
        'C++': r'\bc\+\+\b',
        'C#': r'\bc#\b',
        'Go': r'\bgo\b',
        'Rust': r'\brust\b',
        'TypeScript': r'\btypescript\b',
        'React': r'\breact\b',
        'Vue': r'\bvue\b',
        'Angular': r'\bangular\b',
        'Node.js': r'\bnode\.?js\b',
        'Django': r'\bdjango\b',
        'Flask': r'\bflask\b',
        'Spring': r'\bspring\b',
        'Spring Boot': r'\bspring\s+boot\b',
        'Express': r'\bexpress\b',
        'FastAPI': r'\bfastapi\b',
        'SQL': r'\bsql\b',
        'MySQL': r'\bmysql\b',
        'PostgreSQL': r'\bpostgresql\b|\bpostgres\b',
        'MongoDB': r'\bmongodb\b',
        'Redis': r'\bredis\b',
        'Docker': r'\bdocker\b',
        'Kubernetes': r'\bkubernetes\b|\bk8s\b',
        'AWS': r'\baws\b|amazon\s+web\s+services',
        'Azure': r'\bazure\b',
        'GCP': r'\bgcp\b|google\s+cloud',
        'Git': r'\bgit\b',
        'REST API': r'\brest\s+api\b|\brestful\b',
        'GraphQL': r'\bgraphql\b',
        'HTML': r'\bhtml\b|\bhtml5\b',
        'CSS': r'\bcss\b|\bcss3\b',
        'Linux': r'\blinux\b',
        'Windows': r'\bwindows\b',
        'Agile': r'\bagile\b',
        'Scrum': r'\bscrum\b',
        'Machine Learning': r'\bmachine\s+learning\b|\bml\b',
        'Data Science': r'\bdata\s+science\b',
        'AI': r'\bartificial\s+intelligence\b|\bai\b',
        'TensorFlow': r'\btensorflow\b',
        'PyTorch': r'\bpytorch\b',
        'Pandas': r'\bpandas\b',
        'NumPy': r'\bnumpy\b',
    }
    
    text_lower = resume_text.lower()
    found_skills = []
    
    for skill, pattern in common_skills.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            found_skills.append(skill)
    
    return found_skills if found_skills else ['General', 'Problem Solving']
