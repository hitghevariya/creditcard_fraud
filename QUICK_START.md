# 🚀 Quick Start Guide - Credit Card Default Prediction System

## 📋 What You Have

✅ **Complete ML Pipeline** - Flask API + Streamlit Web App  
✅ **Jupyter Notebook Integration** - Uses your existing notebook logic  
✅ **Postman Collection** - Ready-to-use API tests  
✅ **Model Persistence** - Save/load trained models  
✅ **Batch Processing** - Upload CSV files for bulk predictions  

## 🎯 Quick Start (3 Steps)

### Step 1: Start the Flask API
```bash
python start_flask.py
```
**API will run at:** `http://localhost:5000`

### Step 2: Start the Streamlit App (New Terminal)
```bash
streamlit run streamlit_app.py
```
**Web App will run at:** `http://localhost:8501`

### Step 3: Train the Model
- **Via Web App:** Click "Train Model" in sidebar
- **Via API:** `POST http://localhost:5000/api/train`
- **Via Postman:** Import `Credit_Card_API.postman_collection.json`

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Check API status |
| `POST` | `/api/train` | Train the model |
| `GET` | `/api/features` | Get feature info |
| `POST` | `/api/predict` | Single prediction |
| `POST` | `/api/batch_predict` | Batch predictions |

## 📊 Sample Prediction Request

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

## 🧪 Testing with Postman

1. **Import Collection:** `Credit_Card_API.postman_collection.json`
2. **Set Environment:** Base URL = `http://localhost:5000/api`
3. **Run Tests:** Start with "Health Check" → "Train Model" → "Single Prediction"

## 📈 Features

### Web Interface (Streamlit)
- **Single Prediction:** Interactive form for individual customers
- **Batch Prediction:** Upload CSV files for bulk processing
- **Analytics:** Data visualization and insights
- **Real-time Results:** Probability charts and feature importance

### API (Flask)
- **RESTful Design:** Standard HTTP methods and status codes
- **JSON Responses:** Structured data format
- **Error Handling:** Comprehensive error messages
- **CORS Enabled:** Cross-origin requests supported

## 🎨 Web App Screenshots

### Single Prediction Tab
- Customer information form
- Real-time risk assessment
- Probability visualization
- Feature importance charts

### Batch Prediction Tab
- CSV file upload
- Bulk processing results
- Download predictions
- Summary statistics

### Analytics Tab
- Data distributions
- Default rate analysis
- Model performance metrics

## 🔍 Troubleshooting

### Common Issues
1. **API not responding:** Check if Flask server is running on port 5000
2. **Model not loaded:** Train model first using `/api/train`
3. **Missing features:** Ensure all 23 features are provided
4. **Port conflicts:** Modify ports in `app.py` and `streamlit_app.py`

### Quick Fixes
```bash
# Check if ports are in use
netstat -an | findstr :5000
netstat -an | findstr :8501

# Kill processes if needed
taskkill /f /im python.exe
```

## 📁 File Structure

```
creditcard/
├── app.py                              # Flask API server
├── streamlit_app.py                    # Streamlit web app
├── start_flask.py                      # Flask startup script
├── test_api.py                         # API test script
├── requirements.txt                    # Dependencies
├── Credit_Card_API.postman_collection.json # Postman collection
├── run_app.bat                         # Windows startup script
├── run_app.sh                          # Linux/Mac startup script
├── README.md                           # Full documentation
├── QUICK_START.md                      # This file
└── UCI_Credit_Card.csv                 # Dataset (your existing file)
```

## 🎯 Next Steps

1. **Customize Model:** Modify hyperparameters in `app.py`
2. **Add Features:** Extend the API with new endpoints
3. **Deploy:** Use Docker or cloud platforms
4. **Monitor:** Add logging and monitoring
5. **Scale:** Implement caching and load balancing

## 💡 Tips

- **Model Training:** Takes ~30-60 seconds for 30K records
- **Predictions:** ~100ms per record
- **Batch Processing:** Upload CSV with all required columns
- **Feature Importance:** Shows which factors matter most
- **Confidence Scores:** Helps assess prediction reliability

## 🚀 Ready to Go!

Your complete Credit Card Default Prediction system is ready! 

**Start with:** `python start_flask.py` then `streamlit run streamlit_app.py`

**Happy Predicting! 🎉**