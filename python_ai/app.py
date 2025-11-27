from flask import Flask, request, jsonify
import json
from routes.skills_extractor import extract_skills
from routes.question_generator import generate_question
from routes.answer_evaluator import evaluate_answer

app = Flask(__name__)

@app.route('/extract-skills', methods=['POST'])
def extract_skills_route():
    try:
        data = request.json
        resume_text = data.get('resume_text', '')
        skills = extract_skills(resume_text)
        return jsonify({'skills': skills, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/generate-question', methods=['POST'])
def generate_question_route():
    try:
        data = request.json
        skills = data.get('skills', '')
        question_count = data.get('question_count', 0)
        question = generate_question(skills, question_count)
        return jsonify({'question': question, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/evaluate-answer', methods=['POST'])
def evaluate_answer_route():
    try:
        data = request.json
        question = data.get('question', '')
        answer = data.get('answer', '')
        score, feedback = evaluate_answer(question, answer)
        return jsonify({'score': score, 'feedback': feedback, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'AI Interview System'})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
