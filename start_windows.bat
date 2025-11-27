@echo off
echo ============================================
echo AI Interview System - Setup Script
echo ============================================
echo.

echo Step 1: Starting Python AI Service...
start cmd /k "cd python_ai && pip install -r requirements.txt && python app.py"
echo.

timeout /t 3 /nobreak

echo Step 2: Building Java Backend...
cd backend_java\src
echo Please ensure mysql-connector-java-8.0.x.jar is in this directory
echo Compiling Java files...
javac -cp mysql-connector-java-8.0.x.jar MainServer.java DBConnection.java
if %errorlevel% neq 0 (
    echo Failed to compile Java files. Check if JAR is present.
    pause
    exit /b 1
)
echo.

echo Step 3: Starting Java Backend...
echo Java Server will run on http://localhost:8080
start cmd /k "java -cp .;mysql-connector-java-8.0.x.jar MainServer"
echo.

echo Step 4: Database Setup
echo Please:
echo 1. Start XAMPP (Apache + MySQL)
echo 2. Open phpMyAdmin: http://localhost/phpmyadmin
echo 3. Import database/create_tables.sql
echo.

echo ============================================
echo All services starting...
echo Frontend: http://localhost:8080
echo Python Service: http://localhost:5000
echo ============================================
echo.
pause
