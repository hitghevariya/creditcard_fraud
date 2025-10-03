@echo off
title Credit Card Default Prediction System
color 0A

echo ================================================================
echo    Credit Card Default Prediction System - Windows Startup
echo ================================================================
echo.

echo Step 1: Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo.
echo Step 2: Installing required packages...
echo Installing Flask and Flask-CORS...
python -m pip install --target=Lib\site-packages flask flask-cors

echo Installing Streamlit and Plotly...
python -m pip install --target=Lib\site-packages streamlit plotly

echo Installing ML packages...
python -m pip install --target=Lib\site-packages scikit-learn xgboost

echo.
echo Step 3: Checking if dataset exists...
if not exist "UCI_Credit_Card.csv" (
    echo ERROR: UCI_Credit_Card.csv not found!
    echo Please make sure the dataset is in the current directory.
    pause
    exit /b 1
)
echo Dataset found: UCI_Credit_Card.csv

echo.
echo Step 4: Starting Flask API Server...
echo Starting Flask on port 5000...
start "Flask API Server" cmd /k "python start_flask.py"

echo.
echo Step 5: Waiting for Flask to start...
timeout /t 5 /nobreak > nul

echo.
echo Step 6: Starting Streamlit Web Application...
echo Starting Streamlit on port 8501...
start "Streamlit Web App" cmd /k "python -m streamlit run streamlit_app.py"

echo.
echo ================================================================
echo                    STARTUP COMPLETE!
echo ================================================================
echo.
echo Applications are starting up...
echo.
echo Flask API Server: http://localhost:5000
echo Streamlit Web App: http://localhost:8501
echo.
echo Wait about 10-15 seconds for both applications to fully load.
echo Then open your browser and go to: http://localhost:8501
echo.
echo To stop the applications, close the command windows that opened.
echo.
echo Press any key to continue...
pause > nul
