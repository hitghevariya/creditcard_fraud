"""
Flask API for Credit Card Default Prediction
"""

import streamlit as st
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# Global variables for model and scaler
model = None
scaler = None
feature_columns = None

def load_model():
    """Load the trained model and scaler"""
    global model, scaler, feature_columns
    
    try:
        # Check if model file exists
        if os.path.exists('credit_card_model.pkl'):
            with open('credit_card_model.pkl', 'rb') as f:
                model_data = pickle.load(f)
            
            model = model_data['model']
            scaler = model_data['scaler']
            feature_columns = model_data['feature_columns']
            
            print("Model loaded successfully!")
            return True
        else:
            print("Model file not found. Please train the model first.")
            return False
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def train_model_from_notebook():
    """Train model using the same pipeline as in the notebook"""
    global model, scaler, feature_columns
    
    try:
        # Read the dataset (same as notebook)
        df = pd.read_csv('UCI_Credit_Card.csv')
        
        # Drop ID column
        df = df.drop('ID', axis=1)
        
        # Separate features and target variable
        X = df.drop('default.payment.next.month', axis=1)
        y = df['default.payment.next.month']
        
        # Split data into training and testing sets
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Standardize numerical features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Create and train Random Forest model (best performing from notebook)
        model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        model.fit(X_train_scaled, y_train)
        
        # Store feature columns
        feature_columns = X.columns.tolist()
        
        # Evaluate model
        from sklearn.metrics import accuracy_score, classification_report
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model trained successfully! Accuracy: {accuracy:.4f}")
        
        # Save the model
        model_data = {
            'model': model,
            'scaler': scaler,
            'feature_columns': feature_columns
        }
        
        with open('credit_card_model.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        
        print("Model saved successfully!")
        return True
        
    except Exception as e:
        print(f"Error training model: {e}")
        return False

@app.route('/')
def home():
    """Home page"""
    return jsonify({
        'message': 'Credit Card Default Prediction API',
        'version': '1.0.0',
        'endpoints': {
            'health': 'GET /api/health',
            'train': 'POST /api/train',
            'predict': 'POST /api/predict',
            'batch_predict': 'POST /api/batch_predict',
            'features': 'GET /api/features'
        },
        'documentation': 'See README.md for detailed API documentation'
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'message': 'Credit Card Default Prediction API is running'
    })

@app.route('/api/train', methods=['POST'])
def train_model():
    """Train the model endpoint"""
    try:
        success = train_model_from_notebook()
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Model trained and saved successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to train model'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error training model: {str(e)}'
        }), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict credit card default endpoint"""
    global model, scaler, feature_columns
    
    if model is None or scaler is None:
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded. Please train the model first.'
        }), 400
    
    try:
        # Get data from request
        data = request.get_json()
        
        # Validate input data
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400
        
        # Convert to DataFrame
        input_data = pd.DataFrame([data])
        
        # Ensure all required features are present
        missing_features = set(feature_columns) - set(input_data.columns)
        if missing_features:
            return jsonify({
                'status': 'error',
                'message': f'Missing features: {list(missing_features)}'
            }), 400
        
        # Reorder columns to match training data
        input_data = input_data[feature_columns]
        
        # Scale the features
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0]
        
        # Get feature importance
        feature_importance = dict(zip(feature_columns, model.feature_importances_))
        
        return jsonify({
            'status': 'success',
            'prediction': int(prediction),
            'probability': {
                'no_default': float(probability[0]),
                'default': float(probability[1])
            },
            'feature_importance': feature_importance,
            'interpretation': {
                'prediction_text': 'High risk of default' if prediction == 1 else 'Low risk of default',
                'confidence': float(max(probability))
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Prediction error: {str(e)}'
        }), 500

@app.route('/api/features', methods=['GET'])
def get_features():
    """Get feature information endpoint"""
    if feature_columns is None:
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded'
        }), 400
    
    # Feature descriptions based on the dataset
    feature_descriptions = {
        'LIMIT_BAL': 'Credit limit amount',
        'SEX': 'Gender (1=male, 2=female)',
        'EDUCATION': 'Education level (1=graduate school, 2=university, 3=high school, 4=others)',
        'MARRIAGE': 'Marital status (1=married, 2=single, 3=others)',
        'AGE': 'Age in years',
        'PAY_0': 'Repayment status in September',
        'PAY_2': 'Repayment status in August',
        'PAY_3': 'Repayment status in July',
        'PAY_4': 'Repayment status in June',
        'PAY_5': 'Repayment status in May',
        'PAY_6': 'Repayment status in April',
        'BILL_AMT1': 'Bill statement amount in September',
        'BILL_AMT2': 'Bill statement amount in August',
        'BILL_AMT3': 'Bill statement amount in July',
        'BILL_AMT4': 'Bill statement amount in June',
        'BILL_AMT5': 'Bill statement amount in May',
        'BILL_AMT6': 'Bill statement amount in April',
        'PAY_AMT1': 'Previous payment amount in September',
        'PAY_AMT2': 'Previous payment amount in August',
        'PAY_AMT3': 'Previous payment amount in July',
        'PAY_AMT4': 'Previous payment amount in June',
        'PAY_AMT5': 'Previous payment amount in May',
        'PAY_AMT6': 'Previous payment amount in April'
    }
    
    features_info = []
    for feature in feature_columns:
        features_info.append({
            'name': feature,
            'description': feature_descriptions.get(feature, 'Feature description not available')
        })
    
    return jsonify({
        'status': 'success',
        'features': features_info,
        'total_features': len(feature_columns)
    })

@app.route('/api/batch_predict', methods=['POST'])
def batch_predict():
    """Batch prediction endpoint for multiple records"""
    global model, scaler, feature_columns
    
    if model is None or scaler is None:
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded. Please train the model first.'
        }), 400
    
    try:
        # Get data from request
        data = request.get_json()
        
        if 'records' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No records provided. Expected format: {"records": [...]}'
            }), 400
        
        records = data['records']
        
        if not isinstance(records, list):
            return jsonify({
                'status': 'error',
                'message': 'Records must be a list'
            }), 400
        
        # Convert to DataFrame
        input_data = pd.DataFrame(records)
        
        # Validate features
        missing_features = set(feature_columns) - set(input_data.columns)
        if missing_features:
            return jsonify({
                'status': 'error',
                'message': f'Missing features: {list(missing_features)}'
            }), 400
        
        # Reorder columns
        input_data = input_data[feature_columns]
        
        # Scale features
        input_scaled = scaler.transform(input_data)
        
        # Make predictions
        predictions = model.predict(input_scaled)
        probabilities = model.predict_proba(input_scaled)
        
        # Format results
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            results.append({
                'record_id': i,
                'prediction': int(pred),
                'probability': {
                    'no_default': float(prob[0]),
                    'default': float(prob[1])
                },
                'confidence': float(max(prob))
            })
        
        return jsonify({
            'status': 'success',
            'predictions': results,
            'total_records': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Batch prediction error: {str(e)}'
        }), 500

# if __name__ == '__main__':
#     # Try to load existing model on startup
#     load_model()
    
#     # Run the Flask app
#     app.run(debug=True, host='0.0.0.0', port=5000)