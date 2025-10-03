"""
Simple test script for the Credit Card Default Prediction API
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        print(f"Health Check - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_train():
    """Test model training"""
    try:
        response = requests.post(f"{API_BASE_URL}/train", timeout=60)
        print(f"Train Model - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Train model failed: {e}")
        return False

def test_features():
    """Test features endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/features")
        print(f"Get Features - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total features: {data.get('total_features', 'Unknown')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Get features failed: {e}")
        return False

def test_prediction():
    """Test single prediction"""
    sample_data = {
        "LIMIT_BAL": 20000,
        "SEX": 1,
        "EDUCATION": 1,
        "MARRIAGE": 1,
        "AGE": 30,
        "PAY_0": 0,
        "PAY_2": 0,
        "PAY_3": 0,
        "PAY_4": 0,
        "PAY_5": 0,
        "PAY_6": 0,
        "BILL_AMT1": 1000,
        "BILL_AMT2": 1000,
        "BILL_AMT3": 1000,
        "BILL_AMT4": 1000,
        "BILL_AMT5": 1000,
        "BILL_AMT6": 1000,
        "PAY_AMT1": 1000,
        "PAY_AMT2": 1000,
        "PAY_AMT3": 1000,
        "PAY_AMT4": 1000,
        "PAY_AMT5": 1000,
        "PAY_AMT6": 1000
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/predict", json=sample_data, timeout=10)
        print(f"Single Prediction - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Prediction: {data.get('prediction')}")
            print(f"Probability: {data.get('probability')}")
        else:
            print(f"Error: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Prediction failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Credit Card Default Prediction API Tests")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    health_ok = test_health()
    
    if not health_ok:
        print("❌ API is not running. Please start the Flask server first.")
        print("Run: python app.py")
        return
    
    # Test 2: Train Model
    print("\n2. Testing Model Training...")
    train_ok = test_train()
    
    if not train_ok:
        print("❌ Model training failed")
        return
    
    # Test 3: Get Features
    print("\n3. Testing Get Features...")
    features_ok = test_features()
    
    # Test 4: Single Prediction
    print("\n4. Testing Single Prediction...")
    prediction_ok = test_prediction()
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Model Training: {'✅ PASS' if train_ok else '❌ FAIL'}")
    print(f"Get Features: {'✅ PASS' if features_ok else '❌ FAIL'}")
    print(f"Prediction: {'✅ PASS' if prediction_ok else '❌ FAIL'}")
    print("=" * 50)

if __name__ == "__main__":
    main()