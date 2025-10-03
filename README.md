# Credit Card Default Prediction System

A comprehensive machine learning pipeline for predicting credit card default risk, deployed with Flask API and Streamlit frontend.

## 🚀 Features

- **Machine Learning Pipeline**: Random Forest classifier trained on UCI Credit Card dataset
- **RESTful API**: Flask-based API for predictions and model management
- **Web Interface**: Streamlit dashboard for interactive predictions
- **Batch Processing**: Upload CSV files for bulk predictions
- **Model Persistence**: Save and load trained models
- **Real-time Analytics**: Data visualization and insights

## 📋 Prerequisites

- Python 3.8+
- pip package manager

## 🛠️ Installation

1. **Clone or download the project files**

2. **Create and activate virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure you have the dataset**:
   - Place `UCI_Credit_Card.csv` in the project root directory

## 🚀 Usage

### 1. Start the Flask API Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### 2. Start the Streamlit Web Application

```bash
streamlit run streamlit_app_fixed.py
```

The web interface will be available at `http://localhost:8501`

### 3. Train the Model

#### Via Web Interface:
1. Open the Streamlit app
2. Click "Train Model" in the sidebar

#### Via API:
```bash
curl -X POST http://localhost:5000/api/train
```

### 4. Make Predictions

#### Via Web Interface:
1. Navigate to "Single Prediction" tab
2. Fill in customer information
3. Click "Predict Default Risk"

#### Via API:
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

## 📊 API Endpoints

### Health Check
- **GET** `/api/health` - Check API status and model loading status

### Model Management
- **POST** `/api/train` - Train the machine learning model

### Predictions
- **POST** `/api/predict` - Single prediction
- **POST** `/api/batch_predict` - Batch predictions for multiple records

### Information
- **GET** `/api/features` - Get feature information and descriptions

## 📁 Project Structure

```
creditcard/
├── app.py                 # Flask API server
├── streamlit_app.py      # Streamlit web application
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── UCI_Credit_Card.csv  # Dataset (required)
└── credit_card_model.pkl # Trained model (generated after training)
```

## 🔧 Configuration

### Feature Descriptions

The model uses 23 features:

- **LIMIT_BAL**: Credit limit amount
- **SEX**: Gender (1=male, 2=female)
- **EDUCATION**: Education level (1=graduate school, 2=university, 3=high school, 4=others)
- **MARRIAGE**: Marital status (1=married, 2=single, 3=others)
- **AGE**: Age in years
- **PAY_0 to PAY_6**: Repayment status for the last 6 months
- **BILL_AMT1 to BILL_AMT6**: Bill statement amounts for the last 6 months
- **PAY_AMT1 to PAY_AMT6**: Previous payment amounts for the last 6 months

### Model Information

- **Algorithm**: Random Forest Classifier
- **Training Data**: 30,000 credit card records
- **Features**: 23 customer and payment history features
- **Target**: Binary classification (0=No Default, 1=Default)

## 🧪 Testing with Postman

1. **Import the API collection** (create a new collection in Postman)
2. **Set base URL**: `http://localhost:5000/api`
3. **Test endpoints**:
   - Health check: `GET /health`
   - Train model: `POST /train`
   - Single prediction: `POST /predict`
   - Batch prediction: `POST /batch_predict`
   - Get features: `GET /features`

### Sample Request Body for Prediction

```json
{
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
```

## 🔍 Troubleshooting

### Common Issues

1. **API not responding**: Ensure Flask server is running on port 5000
2. **Model not loaded**: Train the model first using `/api/train` endpoint
3. **Missing features**: Ensure all 23 features are provided in prediction requests
4. **CSV upload issues**: Verify CSV has all required columns

### Port Conflicts

If ports 5000 or 8501 are in use, modify the startup commands:

```bash
# Flask on different port
python app.py  # Edit app.py to change port

# Streamlit on different port
streamlit run streamlit_app.py --server.port 8502
```

## 📈 Performance

- **Training Time**: ~30-60 seconds for 30K records
- **Prediction Time**: ~100ms per record
- **Model Accuracy**: ~82% on test set
- **Memory Usage**: ~200MB for model and dependencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- UCI Machine Learning Repository for the credit card dataset
- scikit-learn for machine learning algorithms
- Flask and Streamlit for web frameworks
