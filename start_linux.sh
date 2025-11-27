#!/bin/bash

echo "=========================================="
echo "AI Interview System - Setup Script"
echo "=========================================="
echo ""

echo "Step 1: Starting Python AI Service..."
cd python_ai
pip install -r requirements.txt
python app.py &
PYTHON_PID=$!

sleep 3

echo "Step 2: Building Java Backend..."
cd ../backend_java/src
echo "Compiling Java files..."
javac -cp mysql-connector-java-8.0.x.jar MainServer.java DBConnection.java

if [ $? -ne 0 ]; then
    echo "Failed to compile Java files. Check if JAR is present."
    kill $PYTHON_PID
    exit 1
fi

echo "Step 3: Starting Java Backend..."
java -cp .:mysql-connector-java-8.0.x.jar MainServer &
JAVA_PID=$!

echo ""
echo "=========================================="
echo "All services started!"
echo "Frontend: http://localhost:8080"
echo "Python Service: http://localhost:5000"
echo "Database: interview_system (localhost:3306)"
echo "=========================================="
echo ""
echo "Database Setup Instructions:"
echo "1. Start MySQL (XAMPP)"
echo "2. Open phpMyAdmin: http://localhost/phpmyadmin"
echo "3. Create new database or import database/create_tables.sql"
echo ""

# Keep the script running
wait
