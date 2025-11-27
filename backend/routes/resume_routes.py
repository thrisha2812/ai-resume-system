from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask import request
from database import mongo
from utils.pdf_extractor import extract_text_from_file
from utils.cheater_detector import extract_text_from_file
from services.resume_parser import parse_resume
from services.scoring_engine import calculate_suitability_score
from models.user_model import User
from io import StringIO
import csv
import os
import re

# Create a directory for uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Remove the file upload parser - we'll use request.files directly
analyze_parser = reqparse.RequestParser()
analyze_parser.add_argument('job_description', type=str, required=True, help="Job description is required")

class ResumeUpload(Resource):
    #@jwt_required()
    def post(self):
        # Use Flask's request.files instead of reqparse for file uploads
        try:
            verify_jwt_in_request()
        except Exception as e:
            # If verification fails (e.g., token missing or expired)
            return {'message': f'Authorization failed: {str(e)}'}, 401
        
        if 'resume' not in request.files:
            return {'message': 'No resume file provided'}, 422
        
        resume_file = request.files['resume']
        
        if resume_file.filename == '':
            return {'message': 'No file selected'}, 422
        
        # Validate file extension
        allowed_extensions = {'.pdf', '.docx'}
        file_ext = os.path.splitext(resume_file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return {'message': 'Only PDF and DOCX files are allowed'}, 400
        
        identity = get_jwt_identity()
        user = User.find_by_email(identity)
        if not user:
            return {'message': 'User not found'}, 404
        
        filename = re.sub(r'[^a-zA-Z0-9._-]', '_', resume_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, f"{user['_id']}_{filename}")
        
        try:
            resume_file.save(file_path)
            
            # --- MODIFIED LINE: Unpack both values ---
            text, is_suspicious = extract_text_from_file(file_path)
            
            if text is None:
                return {'message': 'Unsupported file type or error reading file'}, 400
                
            parsed_data = parse_resume(text)
            
            mongo.db.resumes.update_one(
                {'user_id': user['_id']},
                {'$set': {
                    'user_id': user['_id'],
                    'filename': filename,
                    'text': parsed_data['full_text'],
                    'parsed': parsed_data,
                    'is_suspicious': is_suspicious  # --- NEW: Save the flag to DB ---
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
    def post(self):
        # Authentication removed for testing
        
        data = analyze_parser.parse_args()
        job_description = data['job_description']
        
        candidates = []
        
        # Iterate through all resumes in the database
        for resume in mongo.db.resumes.find():
            resume_text = resume.get('text', '')
            parsed_data = resume.get('parsed', {})
            
            # --- NEW: Get the flag from DB (Default to False) ---
            is_suspicious = resume.get('is_suspicious', False)
            
            score, matched, missing = calculate_suitability_score(resume_text, job_description)
            
            candidates.append({
                'name': parsed_data.get('name', 'Unknown'),
                'email': parsed_data.get('email', 'Unknown'),
                'years_of_experience': parsed_data.get('years_of_experience', 0),
                'score': score,
                'matched_skills': matched,
                'missing_skills': missing,
                'is_suspicious': is_suspicious # --- NEW: Send flag to frontend ---
            })
            
        # Sort candidates by score (highest to lowest)
        ranked_candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)
        
        return {'message': 'Analysis complete', 'results': ranked_candidates}, 200

def init_resume_routes(api):
    api.add_resource(ResumeUpload, '/resume/upload')
    api.add_resource(ResumeAnalyze, '/resume/analyze')