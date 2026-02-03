#!/bin/bash

# Food Delivery Time Prediction - Startup Script

echo "🍔 Starting Food Delivery Time Prediction Application"
echo "=================================================="
echo ""

# Check Python installation
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
fi

echo "✅ Using Python: $($PYTHON_CMD --version)"
echo ""

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

echo ""
echo "🚀 Starting FastAPI backend on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "❤️  Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================================="
echo ""

# Start the backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
