@echo off
echo Starting Credit Card Default Prediction System...
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Starting Flask API Server...
start "Flask API" cmd /k "python app.py"

echo.
echo Waiting 5 seconds for Flask to start...
timeout /t 5 /nobreak > nul

echo.
echo Step 3: Starting Streamlit Web Application...
start "Streamlit App" cmd /k "streamlit run streamlit_app.py"

echo.
echo ========================================
echo Applications started successfully!
echo.
echo Flask API: http://localhost:5000
echo Streamlit App: http://localhost:8501
echo.
echo Press any key to exit...
pause > nul