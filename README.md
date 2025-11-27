# 🤖 AI Interview System

A complete AI-powered interview preparation system with resume parsing, dynamic question generation, and intelligent answer evaluation.

## Features

### 🎓 Interview Preparation
- **Resume Analysis**: Upload and parse resumes to extract technical skills
- **Dynamic Questions**: Get AI-generated interview questions based on your skills
- **Smart Scoring**: Receive detailed feedback and scores for your answers
- **Progress Tracking**: Monitor your interview performance over time

### 🛠️ Tech Stack

**Frontend**
- HTML5, CSS3, JavaScript (Vanilla - no frameworks)
- Responsive design
- Interactive interview UI

**Backend**
- **Java HTTP Server** (no frameworks, no Maven)
- Plain Java with built-in httpserver library
- MySQL database integration
- RESTful API endpoints

**AI Microservice**
- **Python Flask** microservice
- Resume text extraction
- Question generation engine
- Answer evaluation system

**Database**
- **MySQL** with XAMPP
- User management
- Interview history
- Progress tracking

## 🚀 Quick Start

### Prerequisites
```
- Java 11+
- Python 3.7+
- MySQL (XAMPP)
```

### 1. Database Setup
```bash
# Start XAMPP - MySQL and Apache
# Open phpMyAdmin: http://localhost/phpmyadmin
# Import database/create_tables.sql
```

### 2. Start Python Service
```bash
cd python_ai
pip install flask requests
python app.py
# Runs on http://localhost:5000
```

### 3. Start Java Backend
```bash
cd backend_java/src
# Download mysql-connector-java-8.0.x.jar
javac -cp mysql-connector-java-8.0.x.jar *.java
java -cp .:mysql-connector-java-8.0.x.jar MainServer
# Runs on http://localhost:8080
```

### 4. Access Application
```
Open browser: http://localhost:8080
Login with: john@example.com / password123
Or create new account
```

## 📋 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/login` | POST | User authentication |
| `/api/signup` | POST | Create new account |
| `/api/uploadResume` | POST | Upload and parse resume |
| `/api/getSkills` | GET | Retrieve extracted skills |
| `/api/startInterview` | POST | Begin interview session |
| `/api/nextQuestion` | POST | Get next question |
| `/api/evaluateAnswer` | POST | Score and evaluate answer |
| `/api/saveProgress` | POST | Save session results |
| `/api/history` | GET | View interview history |

## 📁 Project Structure

```
interview_system/
├── backend_java/src/
│   ├── MainServer.java          # HTTP Server & Routes
│   ├── DBConnection.java        # MySQL Connection
│   └── handlers/                # Request handlers
├── python_ai/
│   ├── app.py                   # Flask app
│   ├── routes/
│   │   ├── skills_extractor.py  # Resume parsing
│   │   ├── question_generator.py # Question generation
│   │   └── answer_evaluator.py  # Answer scoring
│   ├── utils/
│   └── prompts/
├── frontend/
│   ├── index.html               # Home page
│   ├── upload.html              # Resume upload
│   ├── interview.html           # Interview session
│   ├── dashboard.html           # Progress tracking
│   ├── css/style.css            # Styling
│   └── js/                      # JavaScript files
└── database/
    └── create_tables.sql        # Database schema
```

## 🎯 Workflow

```
1. Register/Login
   ↓
2. Upload Resume
   ↓
3. Skills Extracted
   ↓
4. Start Interview (5 Questions)
   ↓
5. Answer Each Question
   ↓
6. Get Score & Feedback
   ↓
7. View Progress Dashboard
```

## 💾 Database Schema

### Tables
- **users** - User accounts
- **resumes** - Stored resume content
- **skills** - Extracted skills
- **interview_sessions** - Interview sessions
- **answers** - Question-answer pairs with scores
- **progress_history** - Interview results

## 🔧 Configuration

### Java Backend
```java
// MainServer.java
private static int PORT = 8080;
private static String PYTHON_SERVICE_URL = "http://localhost:5000";
```

### Python Service
```python
# app.py
app.run(debug=True, host='localhost', port=5000)
```

### Database
```java
// DBConnection.java
private String url = "jdbc:mysql://localhost:3306/interview_system";
private String user = "root";
private String password = "";
```

## 🎨 Features Explained

### Resume Skill Extraction
- Pattern-based skill recognition
- Supports 40+ common technical skills
- Fallback to general categories

### Question Generation
- Skill-specific question database
- Adaptive difficulty levels
- Varied question types (technical, behavioral, practical)

### Answer Evaluation
- Length-based initial scoring
- Keyword detection for specificity
- Constructive feedback generation
- Score scale: 0-100

### Progress Tracking
- Interview history with timestamps
- Score statistics (average, best)
- Session-based organization
- Detailed answer review

## 🚀 Enhancement Ideas

### Short Term
- Add more skill categories
- Improve LLM integration
- Add difficulty levels
- Create question templates

### Medium Term
- Implement OpenAI/Claude API
- Add voice recording
- Create PDF reports
- Add peer benchmarking

### Long Term
- Real-time WebSocket feedback
- Video interview recording
- Advanced NLP analysis
- Interview preparation paths

## 📝 Development Notes

### Without Maven
- Uses only Java built-in libraries for HTTP server
- Manual classpath management
- Simple, lightweight deployment

### Database Connection
- Direct JDBC connection
- No ORM framework
- Raw SQL with PreparedStatements
- Connection pooling ready

### API Communication
- Java calls Python service via HTTP POST
- JSON serialization/deserialization
- Error handling and retry logic

## 🐛 Troubleshooting

### Common Issues

**Java Port Already in Use**
```bash
# Change PORT in MainServer.java or kill process
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

**MySQL Connection Failed**
```bash
# Ensure XAMPP MySQL is running
# Check credentials in DBConnection.java
# Verify database exists: interview_system
```

**Python Module Missing**
```bash
pip install flask requests
```

**API Calls Returning 404**
```
- Check server is running on correct port
- Verify URL endpoints match API routes
- Check CORS headers in MainServer.java
```

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Built as a comprehensive AI Interview System with all components integrated locally.

---

**Happy Interviewing! 🎯**
