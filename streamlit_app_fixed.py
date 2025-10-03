"""
Fixed Streamlit Web Application for Credit Card Default Prediction
"""

import streamlit as st
import requests
import pandas as pd
import numpy as np
import json
import os
import pickle

# Page configuration
st.set_page_config(
    page_title="Credit Card Default Prediction",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL (configurable via secrets or env)
DEFAULT_API_BASE_URL = st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", ""))

def check_api_health(api_base_url: str):
    """Check if the API is running"""
    try:
        if not api_base_url:
            return False, None
        response = requests.get(f"{api_base_url}/health", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except:
        return False, None

def train_model(api_base_url: str):
    """Train the model via API"""
    try:
        if not api_base_url:
            return False, {"error": "API base URL not set"}
        response = requests.post(f"{api_base_url}/train", timeout=60)
        return response.status_code == 200, response.json() if response.status_code == 200 else response.json()
    except Exception as e:
        return False, {"error": str(e)}

def predict_single_api(api_base_url: str, data):
    """Make single prediction via API"""
    try:
        if not api_base_url:
            return False, {"error": "API base URL not set"}
        response = requests.post(f"{api_base_url}/predict", json=data, timeout=10)
        return response.status_code == 200, response.json() if response.status_code == 200 else response.json()
    except Exception as e:
        return False, {"error": str(e)}

@st.cache_resource
def load_local_model():
    """Load local model artifact for offline predictions"""
    model_path = "credit_card_model.pkl"
    if not os.path.exists(model_path):
        return None
    with open(model_path, "rb") as f:
        model_data = pickle.load(f)
    # Expecting keys: model, scaler, feature_columns
    if not all(k in model_data for k in ["model", "scaler", "feature_columns"]):
        return None
    return model_data

def predict_single_local(model_data, data):
    """Predict locally using loaded model data"""
    try:
        feature_columns = model_data["feature_columns"]
        scaler = model_data["scaler"]
        model = model_data["model"]
        df = pd.DataFrame([data])
        missing = set(feature_columns) - set(df.columns)
        if missing:
            return False, {"message": f"Missing features: {sorted(list(missing))}"}
        df = df[feature_columns]
        X = scaler.transform(df)
        pred = int(model.predict(X)[0])
        proba = model.predict_proba(X)[0]
        return True, {
            "prediction": pred,
            "probability": {"no_default": float(proba[0]), "default": float(proba[1])}
        }
    except Exception as e:
        return False, {"message": str(e)}

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("💳 Credit Card Default Prediction")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        api_base_url = st.text_input("API Base URL", value=DEFAULT_API_BASE_URL, placeholder="https://your-api-host/api")
        use_local_fallback = st.toggle("Use local model if API unavailable", value=True)
        st.caption("Tip: On Streamlit Cloud, leave API empty to use local model.")
        uploaded_model = None
        if use_local_fallback and not api_base_url:
            uploaded_model = st.file_uploader("Upload credit_card_model.pkl", type=["pkl"], help="Upload the trained model bundle with keys: model, scaler, feature_columns")

    # Check API health (non-blocking)
    api_healthy, health_data = check_api_health(api_base_url)

    if api_healthy:
        st.info("API connected")
    else:
        if api_base_url:
            st.warning("API not reachable. The app will use local model if available.")
        else:
            st.warning("No API configured. The app will use local model if available.")

    # Load local model if needed
    local_model_data = None
    if use_local_fallback and not api_healthy:
        # Prefer uploaded model if provided
        if uploaded_model is not None:
            try:
                model_data = pickle.load(uploaded_model)
                if all(k in model_data for k in ["model", "scaler", "feature_columns"]):
                    local_model_data = model_data
                else:
                    st.error("Uploaded file is missing required keys: model, scaler, feature_columns")
            except Exception as e:
                st.error(f"Failed to read uploaded model: {e}")
        if local_model_data is None:
            local_model_data = load_local_model()
        if local_model_data is None:
            st.error("Local model not found or invalid. Upload/run training to create `credit_card_model.pkl`.")

    # Sidebar
    with st.sidebar:
        # Model status
        if api_healthy and health_data and health_data.get('model_loaded'):
            st.success("✅ API Model Loaded")
        elif local_model_data is not None:
            st.success("✅ Local Model Loaded")
        else:
            st.warning("⚠️ No model loaded")
        if api_healthy and st.button("🚀 Train Model via API", type="primary"):
            with st.spinner("Training model..."):
                success, result = train_model(api_base_url)
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
                if api_healthy:
                    success, result = predict_single_api(api_base_url, input_data)
                elif local_model_data is not None:
                    success, result = predict_single_local(local_model_data, input_data)
                else:
                    success, result = False, {"message": "No prediction backend available"}
                
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
        success, result = check_api_health(api_base_url)
        if success:
            st.success("✅ API is healthy!")
            st.json(result)
        else:
            st.error("❌ API is not responding")
    
    if st.button("Train Model via API"):
        with st.spinner("Training model..."):
            success, result = train_model(api_base_url)
            if success:
                st.success("✅ Model trained successfully!")
            else:
                st.error(f"❌ Training failed: {result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    main()
