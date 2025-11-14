from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from database import init_db
from models.user_model import bcrypt  # Import bcrypt from user_model

# Import routes
from routes.user_routes import init_user_routes
from routes.resume_routes import init_resume_routes
# We are ignoring interview_routes for now

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    init_db(app)
    bcrypt.init_app(app) # Initialize bcrypt here
    jwt.init_app(app)
    CORS(app, 
        resources={r"/api/*": {"origins": "http://localhost:5173"}},
        supports_credentials=True # Crucial for handling cookies/Authorization headers
    )
    app.config["JWT_DECODE_STRATEGIES"] = [
        {
            "type": "header",
            "extractors": [
                {"type": "Authorization", "location": "headers"}
            ]
        }
    ]
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config['JWT_SUPPRESS_BODY_PARSING'] = True
    api = Api(app, prefix="/api")

    # Register API routes
    init_user_routes(api)
    init_resume_routes(api)
    # init_interview_routes(api) # Leave this commented out

    @app.route('/')
    def index():
        return "Welcome to the AI Resume Shortlister API (Resume Module)"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)