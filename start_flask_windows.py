"""
Windows-optimized Flask startup script
"""

import os
import sys
import time

def main():
    print("=" * 60)
    print("🚀 Credit Card Default Prediction Flask API - Windows")
    print("=" * 60)
    print()
    
    # Check if dataset exists
    if not os.path.exists('UCI_Credit_Card.csv'):
        print("❌ ERROR: UCI_Credit_Card.csv not found!")
        print("Please make sure the dataset is in the current directory.")
        input("Press Enter to exit...")
        return
    
    print("✅ Dataset found: UCI_Credit_Card.csv")
    
    try:
        # Import and start Flask app
        from app import app
        
        print("✅ Flask app loaded successfully")
        print()
        print("🌐 Starting Flask API Server...")
        print("📍 API will be available at: http://localhost:5000")
        print("📍 API Documentation: http://localhost:5000/api/health")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Start the Flask app
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=False  # Disable reloader for Windows stability
        )
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please install required packages:")
        print("python -m pip install flask flask-cors pandas numpy scikit-learn")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error starting Flask: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
