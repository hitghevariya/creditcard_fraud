#!/bin/bash

echo "Starting Credit Card Default Prediction System..."
echo

echo "Step 1: Installing dependencies..."
pip install -r requirements.txt

echo
echo "Step 2: Starting Flask API Server..."
python app.py &
FLASK_PID=$!

echo
echo "Waiting 5 seconds for Flask to start..."
sleep 5

echo
echo "Step 3: Starting Streamlit Web Application..."
streamlit run streamlit_app.py &
STREAMLIT_PID=$!

echo
echo "========================================"
echo "Applications started successfully!"
echo
echo "Flask API: http://localhost:5000"
echo "Streamlit App: http://localhost:8501"
echo
echo "Press Ctrl+C to stop both applications"

# Function to cleanup background processes
cleanup() {
    echo
    echo "Stopping applications..."
    kill $FLASK_PID 2>/dev/null
    kill $STREAMLIT_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for background processes
wait