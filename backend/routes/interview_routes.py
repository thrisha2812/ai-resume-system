from flask_restful import Resource
from flask import request
import traceback
from database import mongo
from services.interview_service import get_interview_questions, evaluate_response

class StartInterview(Resource):
    def get(self):
        try:
            # 1. Fetch the latest resume
            resume = mongo.db.resumes.find_one(sort=[('_id', -1)])

            skills = []
            if resume and 'parsed' in resume:
                skills = resume['parsed'].get('skills', [])
                print(f"DEBUG: Found skills: {skills}")
            else:
                print("DEBUG: No resume found, using default HR questions.")

            # 2. Generate Questions
            print("DEBUG: Calling get_interview_questions")
            questions = get_interview_questions(skills)

            return {'questions': questions}, 200

        except Exception as e:
            print(f"❌ SERVER ERROR in StartInterview: {e}")
            return {'message': f"Server Error: {str(e)}"}, 500


class SubmitAnswer(Resource):
    def post(self):
        try:
            data = request.get_json()
            user_answer = data.get('user_answer', '')
            ideal_answer = data.get('ideal_answer', '')
            
            # 3. AI Evaluation
            score, feedback = evaluate_response(user_answer, ideal_answer)
            
            return {'score': score, 'feedback': feedback}, 200
            
        except Exception as e:
            traceback.print_exc()
            return {'message': str(e)}, 500

def init_interview_routes(api):
    api.add_resource(StartInterview, '/interview/start')
    api.add_resource(SubmitAnswer, '/interview/submit')