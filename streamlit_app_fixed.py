"""
Fixed Streamlit Web Application for Credit Card Default Prediction
"""

import streamlit as st
import requests
import pandas as pd
import numpy as np
import json

# Page configuration
st.set_page_config(
    page_title="Credit Card Default Prediction",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
API_BASE_URL = "http://localhost:5000/api"

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except:
        return False, None

def train_model():
    """Train the model via API"""
    try:
        response = requests.post(f"{API_BASE_URL}/train", timeout=60)
        return response.status_code == 200, response.json() if response.status_code == 200 else response.json()
    except Exception as e:
        return False, {"error": str(e)}

def predict_single(data):
    """Make single prediction via API"""
    try:
        response = requests.post(f"{API_BASE_URL}/predict", json=data, timeout=10)
        return response.status_code == 200, response.json() if response.status_code == 200 else response.json()
    except Exception as e:
        return False, {"error": str(e)}

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("💳 Credit Card Default Prediction")
    st.markdown("---")
    
    # Check API health
    api_healthy, health_data = check_api_health()
    
    if not api_healthy:
        st.error("🚨 API is not running! Please start the Flask API server first.")
        st.code("python app.py", language="bash")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Model status
        if health_data and health_data.get('model_loaded'):
            st.success("✅ Model Loaded")
        else:
            st.warning("⚠️ Model Not Loaded")
            if st.button("🚀 Train Model", type="primary"):
                with st.spinner("Training model..."):
                    success, result = train_model()
                    if success:
                        st.success("✅ Model trained successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Training failed: {result.get('message', 'Unknown error')}")
    
    # Main content
    st.header("Single Credit Card Default Prediction")
    
    # Create input form
    with st.form("prediction_form"):
        st.subheader("Customer Information")
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            limit_bal = st.number_input("Credit Limit", min_value=0, value=20000, step=1000)
            sex = st.selectbox("Gender", [1, 2], format_func=lambda x: "Male" if x == 1 else "Female")
            education = st.selectbox("Education", [1, 2, 3, 4], 
                                   format_func=lambda x: {1: "Graduate School", 2: "University", 3: "High School", 4: "Others"}[x])
            marriage = st.selectbox("Marital Status", [1, 2, 3], 
                                  format_func=lambda x: {1: "Married", 2: "Single", 3: "Others"}[x])
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
        
        with col2:
            st.subheader("Payment History (Repayment Status)")
            st.caption("Repayment status: -1=pay duly, 1=delay 1 month, 2=delay 2 months, etc.")
            
            pay_0 = st.selectbox("September", [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8], index=2)
            pay_2 = st.selectbox("August", [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8], index=2)
            pay_3 = st.selectbox("July", [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8], index=2)
            pay_4 = st.selectbox("June", [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8], index=2)
            pay_5 = st.selectbox("May", [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8], index=2)
            pay_6 = st.selectbox("April", [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8], index=2)
        
        st.subheader("Bill Statement Amounts")
        col3, col4 = st.columns(2)
        
        with col3:
            bill_amt1 = st.number_input("September Bill Amount", value=0, step=100)
            bill_amt2 = st.number_input("August Bill Amount", value=0, step=100)
            bill_amt3 = st.number_input("July Bill Amount", value=0, step=100)
        
        with col4:
            bill_amt4 = st.number_input("June Bill Amount", value=0, step=100)
            bill_amt5 = st.number_input("May Bill Amount", value=0, step=100)
            bill_amt6 = st.number_input("April Bill Amount", value=0, step=100)
        
        st.subheader("Previous Payment Amounts")
        col5, col6 = st.columns(2)
        
        with col5:
            pay_amt1 = st.number_input("September Payment", value=0, step=100)
            pay_amt2 = st.number_input("August Payment", value=0, step=100)
            pay_amt3 = st.number_input("July Payment", value=0, step=100)
        
        with col6:
            pay_amt4 = st.number_input("June Payment", value=0, step=100)
            pay_amt5 = st.number_input("May Payment", value=0, step=100)
            pay_amt6 = st.number_input("April Payment", value=0, step=100)
        
        # Submit button
        submitted = st.form_submit_button("🔮 Predict Default Risk", type="primary")
        
        if submitted:
            # Prepare input data
            input_data = {
                'LIMIT_BAL': limit_bal,
                'SEX': sex,
                'EDUCATION': education,
                'MARRIAGE': marriage,
                'AGE': age,
                'PAY_0': pay_0,
                'PAY_2': pay_2,
                'PAY_3': pay_3,
                'PAY_4': pay_4,
                'PAY_5': pay_5,
                'PAY_6': pay_6,
                'BILL_AMT1': bill_amt1,
                'BILL_AMT2': bill_amt2,
                'BILL_AMT3': bill_amt3,
                'BILL_AMT4': bill_amt4,
                'BILL_AMT5': bill_amt5,
                'BILL_AMT6': bill_amt6,
                'PAY_AMT1': pay_amt1,
                'PAY_AMT2': pay_amt2,
                'PAY_AMT3': pay_amt3,
                'PAY_AMT4': pay_amt4,
                'PAY_AMT5': pay_amt5,
                'PAY_AMT6': pay_amt6
            }
            
            # Make prediction
            with st.spinner("Making prediction..."):
                success, result = predict_single(input_data)
                
                if success:
                    st.success("✅ Prediction completed!")
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        prediction = result['prediction']
                        if prediction == 1:
                            st.error("🚨 HIGH RISK - Default Likely")
                        else:
                            st.success("✅ LOW RISK - No Default Expected")
                    
                    with col2:
                        prob_no_default = result['probability']['no_default']
                        st.metric("No Default Probability", f"{prob_no_default:.2%}")
                    
                    with col3:
                        prob_default = result['probability']['default']
                        st.metric("Default Probability", f"{prob_default:.2%}")
                    
                    # Show detailed results
                    st.subheader("Detailed Results")
                    st.json(result)
                
                else:
                    st.error(f"❌ Prediction failed: {result.get('message', 'Unknown error')}")
    
    # API Testing Section
    st.markdown("---")
    st.header("🧪 API Testing")
    
    if st.button("Test API Health"):
        success, result = check_api_health()
        if success:
            st.success("✅ API is healthy!")
            st.json(result)
        else:
            st.error("❌ API is not responding")
    
    if st.button("Train Model"):
        with st.spinner("Training model..."):
            success, result = train_model()
            if success:
                st.success("✅ Model trained successfully!")
            else:
                st.error(f"❌ Training failed: {result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    main()
