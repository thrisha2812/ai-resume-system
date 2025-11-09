from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage
from database import mongo
from utils.pdf_extractor import extract_text_from_file
from services.resume_parser import parse_resume
from services.scoring_engine import calculate_suitability_score
from models.user_model import User
import os
import re

# Create a directory for uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('resume', type=FileStorage, location='files', required=True, help="Resume file is required")

analyze_parser = reqparse.RequestParser()
analyze_parser.add_argument('job_description', type=str, required=True, help="Job description is required")

class ResumeUpload(Resource):
    @jwt_required()
    def post(self):
        data = upload_parser.parse_args()
        resume_file = data['resume']
        
        identity = get_jwt_identity()
        user = User.find_by_email(identity['email'])
        if not user:
            return {'message': 'User not found'}, 404
        
        filename = re.sub(r'[^a-zA-Z0-9._-]', '_', resume_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, f"{user['_id']}_{filename}")
        
        try:
            resume_file.save(file_path)
            text = extract_text_from_file(file_path)
            if text is None:
                return {'message': 'Unsupported file type or error reading file'}, 400
                
            parsed_data = parse_resume(text)
            
            mongo.db.resumes.update_one(
                {'user_id': user['_id']},
                {'$set': {
                    'user_id': user['_id'],
                    'filename': filename,
                    'text': parsed_data['full_text'],
                    'parsed': parsed_data
                }},
                upsert=True
            )
        except Exception as e:
            return {'message': f"An error occurred: {str(e)}"}, 500
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        return {'message': 'Resume uploaded and parsed successfully', 'data': parsed_data}, 201

class ResumeAnalyze(Resource):
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        if identity['role'] != 'recruiter':
            return {'message': 'Access forbidden: Recruiters only'}, 403
            
        data = analyze_parser.parse_args()
        job_description = data['job_description']
        
        candidates = []
        for resume in mongo.db.resumes.find():
            resume_text = resume.get('text', '')
            parsed_data = resume.get('parsed', {})
            
            score, matched, missing = calculate_suitability_score(resume_text, job_description)
            
            candidates.append({
                'name': parsed_data.get('name', 'Unknown'),
                'email': parsed_data.get('email', 'Unknown'),
                'score': score,
                'matched_skills': matched,
                'missing_skills': missing
            })
            
        ranked_candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)
        
        return {'message': 'Analysis complete', 'results': ranked_candidates}, 200

def init_resume_routes(api):
    api.add_resource(ResumeUpload, '/resume/upload')
    api.add_resource(ResumeAnalyze, '/resume/analyze')