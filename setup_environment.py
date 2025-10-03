"""
Environment Setup Script for Credit Card Default Prediction System
This script will install all required packages and verify the setup.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def check_package(package_name):
    """Check if a package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def main():
    """Main setup function"""
    print("🚀 Credit Card Default Prediction System - Environment Setup")
    print("="*70)
    
    # Check if we're in the right directory
    if not os.path.exists('UCI_Credit_Card.csv'):
        print("❌ UCI_Credit_Card.csv not found in current directory")
        print("Please make sure you're in the correct project directory")
        return False
    
    # Install packages using system Python
    packages_to_install = [
        "flask",
        "flask-cors", 
        "streamlit",
        "plotly",
        "pandas",
        "numpy",
        "scikit-learn",
        "xgboost",
        "matplotlib",
        "seaborn",
        "requests"
    ]
    
    print(f"\n📦 Installing {len(packages_to_install)} packages...")
    
    # Install each package
    failed_packages = []
    for package in packages_to_install:
        cmd = f'& "C:\\Program Files\\Python312\\python.exe" -m pip install --target=Lib\\site-packages {package}'
        success = run_command(cmd, f"Installing {package}")
        if not success:
            failed_packages.append(package)
    
    # Check installation
    print(f"\n🔍 Verifying installations...")
    verification_results = {}
    
    packages_to_check = [
        ("flask", "Flask"),
        ("flask_cors", "Flask-CORS"),
        ("streamlit", "Streamlit"),
        ("plotly", "Plotly"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("sklearn", "Scikit-learn"),
        ("xgboost", "XGBoost"),
        ("matplotlib", "Matplotlib"),
        ("seaborn", "Seaborn"),
        ("requests", "Requests")
    ]
    
    for package, display_name in packages_to_check:
        is_installed = check_package(package)
        verification_results[package] = is_installed
        status = "✅" if is_installed else "❌"
        print(f"{status} {display_name}: {'Installed' if is_installed else 'Not Found'}")
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 SETUP SUMMARY")
    print(f"{'='*70}")
    
    installed_count = sum(verification_results.values())
    total_count = len(verification_results)
    
    print(f"Packages Installed: {installed_count}/{total_count}")
    
    if installed_count == total_count:
        print("🎉 All packages installed successfully!")
        print("\n🚀 Ready to start the application:")
        print("   1. Flask API: python start_flask.py")
        print("   2. Streamlit App: python -m streamlit run streamlit_app.py")
        print("\n📱 Access URLs:")
        print("   - Flask API: http://localhost:5000")
        print("   - Streamlit App: http://localhost:8501")
        return True
    else:
        print("⚠️  Some packages failed to install:")
        for package, is_installed in verification_results.items():
            if not is_installed:
                print(f"   - {package}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Next Steps:")
        print("   1. Start Flask API: python start_flask.py")
        print("   2. Start Streamlit: python -m streamlit run streamlit_app.py")
        print("   3. Open browser to http://localhost:8501")
    else:
        print("\n❌ Setup incomplete. Please check the errors above.")
    
    input("\nPress Enter to continue...")
