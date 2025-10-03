@echo off
title Credit Card Default Prediction
echo Starting Credit Card Default Prediction System...
echo.

echo Starting Flask API Server...
start "Flask API" cmd /k "python start_flask_windows.py"

echo Waiting 5 seconds...
timeout /t 5 /nobreak > nul

echo Starting Streamlit Web App...
start "Streamlit App" cmd /k "python -m streamlit run streamlit_app.py"

echo.
echo ================================================================
echo Applications are starting up...
echo.
echo Flask API:      http://localhost:5000
echo Streamlit App:  http://localhost:8501
echo.
echo Wait 10-15 seconds, then open: http://localhost:8501
echo ================================================================
echo.
pause
