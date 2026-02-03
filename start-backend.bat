@echo off
REM Food Delivery Time Prediction - Startup Script for Windows

echo 🍔 Starting Food Delivery Time Prediction Application
echo ==================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

echo ✅ Python is installed
echo.

REM Install backend dependencies
echo 📦 Installing backend dependencies...
pip install -r requirements.txt

echo.
echo 🚀 Starting FastAPI backend on http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo ❤️  Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo ==================================================
echo.

REM Start the backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
