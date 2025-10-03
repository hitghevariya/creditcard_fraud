@echo off
title Credit Card Default Prediction - Install and Start
color 0B

echo ================================================================
echo    Credit Card Default Prediction System
echo    Windows Installation and Startup Script
echo ================================================================
echo.

REM Check if Python is available
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✅ Python is available

REM Check if dataset exists
echo.
echo [2/6] Checking dataset...
if not exist "UCI_Credit_Card.csv" (
    echo ERROR: UCI_Credit_Card.csv not found!
    echo Please place the dataset in this directory.
    pause
    exit /b 1
)
echo ✅ Dataset found: UCI_Credit_Card.csv

REM Install packages
echo.
echo [3/6] Installing required packages...
echo Installing Flask and dependencies...
python -m pip install --target=Lib\site-packages flask flask-cors requests
if %errorlevel% neq 0 (
    echo WARNING: Some packages may not have installed correctly
)

echo Installing Streamlit and Plotly...
python -m pip install --target=Lib\site-packages streamlit plotly
if %errorlevel% neq 0 (
    echo WARNING: Some packages may not have installed correctly
)

echo Installing ML libraries...
python -m pip install --target=Lib\site-packages pandas numpy scikit-learn xgboost matplotlib seaborn
if %errorlevel% neq 0 (
    echo WARNING: Some packages may not have installed correctly
)

REM Test imports
echo.
echo [4/6] Testing package imports...
python -c "import flask, pandas, numpy, sklearn; print('✅ Core packages imported successfully')"
if %errorlevel% neq 0 (
    echo WARNING: Some packages may not be properly installed
)

REM Start Flask API
echo.
echo [5/6] Starting Flask API Server...
echo Starting Flask on http://localhost:5000...
start "Flask API" cmd /k "python start_flask_windows.py"

REM Wait for Flask to start
echo Waiting 8 seconds for Flask to initialize...
timeout /t 8 /nobreak > nul

REM Start Streamlit
echo.
echo [6/6] Starting Streamlit Web Application...
echo Starting Streamlit on http://localhost:8501...
start "Streamlit App" cmd /k "python -m streamlit run streamlit_app.py"

echo.
echo ================================================================
echo                    🎉 SETUP COMPLETE!
echo ================================================================
echo.
echo Both applications are starting up...
echo.
echo 📍 Flask API:      http://localhost:5000
echo 📍 Streamlit App:  http://localhost:8501
echo.
echo 📋 Next Steps:
echo    1. Wait 10-15 seconds for applications to fully load
echo    2. Open browser and go to: http://localhost:8501
echo    3. Click "Train Model" in the sidebar
echo    4. Start making predictions!
echo.
echo 📁 To stop applications: Close the command windows that opened
echo.
echo Press any key to continue...
pause > nul
