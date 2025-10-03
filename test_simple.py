"""
Simple test script for Windows
"""

import requests
import time

def test_flask():
    """Test Flask API"""
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("SUCCESS: Flask API is running!")
            print("Response:", response.json())
            return True
        else:
            print("ERROR: Flask API returned status", response.status_code)
            return False
    except Exception as e:
        print("ERROR: Flask API not responding -", str(e))
        return False

def main():
    print("Testing Credit Card Default Prediction System...")
    print("=" * 50)
    
    # Wait a bit for services to start
    print("Waiting for services to start...")
    time.sleep(10)
    
    # Test Flask
    print("\nTesting Flask API...")
    flask_ok = test_flask()
    
    if flask_ok:
        print("\nSUCCESS: System is ready!")
        print("Open your browser and go to: http://localhost:8501")
    else:
        print("\nERROR: Flask API is not running")
        print("Try running: python start_flask_windows.py")

if __name__ == "__main__":
    main()
