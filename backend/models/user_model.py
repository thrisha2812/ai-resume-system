from database import mongo
# We will import bcrypt from app.py
from bson.objectid import ObjectId
import flask_bcrypt

bcrypt = flask_bcrypt.Bcrypt()

class User:
    def __init__(self, email, password, name, role='candidate'):
        self.email = email
        self.password = password
        self.name = name
        self.role = role  # 'candidate' or 'recruiter'

    def save(self):
        hashed_password = bcrypt.generate_password_hash(self.password).decode('utf-8')
        user_data = {
            'email': self.email,
            'password': hashed_password,
            'name': self.name,
            'role': self.role
        }
        return mongo.db.users.insert_one(user_data)

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({'email': email})

    @staticmethod
    def find_by_id(user_id):
        try:
            return mongo.db.users.find_one({'_id': ObjectId(user_id)})
        except Exception:
            return None

    @staticmethod
    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)