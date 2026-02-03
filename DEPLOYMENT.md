# Food Delivery Time Prediction - Deployment Guide

## 🚀 Production-Ready Backend & Frontend Integration

This guide will help you deploy the Food Delivery Time Prediction application.

---

## 📋 Table of Contents
- [Local Development](#local-development)
- [Backend Deployment](#backend-deployment)
- [Frontend Configuration](#frontend-configuration)
- [Testing the API](#testing-the-api)
- [Troubleshooting](#troubleshooting)

---

## 🖥️ Local Development

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed (for frontend)
- Model file: `model/final_eta_model.joblib`

### Backend Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the FastAPI server:**
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: `http://localhost:8000`

3. **Check API documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

4. **Health check:**
```bash
curl http://localhost:8000/health
```

### Frontend Setup

1. **Install Node dependencies:**
```bash
npm install
```

2. **Start development server:**
```bash
npm run dev
```

The frontend will be available at: `http://localhost:5173` (or similar)

---

## 🌐 Backend Deployment

### Option 1: Deploy to Render

1. **Create a new Web Service on [Render](https://render.com)**

2. **Configure the service:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:**
     - `PYTHON_VERSION`: `3.11.0`

3. **Upload your code:**
   - Connect your GitHub repository, or
   - Upload directly via Render dashboard

4. **Note your backend URL:** `https://your-app-name.onrender.com`

### Option 2: Deploy to Railway

1. **Create a new project on [Railway](https://railway.app)**

2. **Deploy from GitHub or local:**
```bash
railway login
railway init
railway up
```

3. **Configure:**
   - Railway will auto-detect Python and install dependencies
   - Set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Option 3: Deploy to HuggingFace Spaces

1. **Create a new Space on [HuggingFace](https://huggingface.co/spaces)**

2. **Choose "Gradio" or "Streamlit" SDK** (or use Docker)

3. **Create a `Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Option 4: Deploy to AWS/GCP/Azure

Use Docker for containerization:

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run:**
```bash
docker build -t food-delivery-api .
docker run -p 8000:8000 food-delivery-api
```

---

## 🎨 Frontend Configuration

### Update API URL

1. **For development:**
   - Default: `http://localhost:8000/predict`

2. **For production:**
   
   Create a `.env` file in the frontend directory:
   ```env
   VITE_API_URL=https://your-backend-url.com/predict
   ```

3. **Rebuild frontend:**
```bash
npm run build
```

### Deploy Frontend

#### Option 1: Vercel
```bash
npm install -g vercel
vercel
```

#### Option 2: Netlify
```bash
npm run build
# Upload the 'dist' folder to Netlify
```

#### Option 3: GitHub Pages
```bash
npm run build
# Deploy the 'dist' folder to gh-pages branch
```

---

## 🧪 Testing the API

### Test with curl

**Health check:**
```bash
curl http://localhost:8000/health
```

**Make a prediction:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Delivery_person_Age": 25,
    "Delivery_person_Ratings": 4.5,
    "Restaurant_latitude": 12.9352,
    "Restaurant_longitude": 77.6245,
    "Delivery_location_latitude": 12.9698,
    "Delivery_location_longitude": 77.7499,
    "Type_of_order": "Meal",
    "Type_of_vehicle": "motorcycle"
  }'
```

**Expected response:**
```json
{
  "predicted_delivery_time_minutes": 28.45,
  "distance_km": 15.32,
  "success": true
}
```

### Test with Python

```python
import requests

url = "http://localhost:8000/predict"
payload = {
    "Delivery_person_Age": 25,
    "Delivery_person_Ratings": 4.5,
    "Restaurant_latitude": 12.9352,
    "Restaurant_longitude": 77.6245,
    "Delivery_location_latitude": 12.9698,
    "Delivery_location_longitude": 77.7499,
    "Type_of_order": "Meal",
    "Type_of_vehicle": "motorcycle"
}

response = requests.post(url, json=payload)
print(response.json())
```

### Test with JavaScript/Frontend

```javascript
const response = await fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    Delivery_person_Age: 25,
    Delivery_person_Ratings: 4.5,
    Restaurant_latitude: 12.9352,
    Restaurant_longitude: 77.6245,
    Delivery_location_latitude: 12.9698,
    Delivery_location_longitude: 77.7499,
    Type_of_order: "Meal",
    Type_of_vehicle: "motorcycle"
  })
});

const data = await response.json();
console.log(data);
```

---

## 🔧 Troubleshooting

### Backend Issues

**1. Model not found:**
```
Error: FileNotFoundError: model/final_eta_model.joblib
```
**Solution:** Ensure the model file is in the correct path relative to `app.py`

**2. CORS errors:**
```
Access to fetch blocked by CORS policy
```
**Solution:** Backend already has CORS enabled for all origins. For production, update:
```python
allow_origins=["https://your-frontend-domain.com"]
```

**3. Port already in use:**
```bash
# Use a different port
uvicorn app:app --port 8001
```

### Frontend Issues

**1. Cannot connect to backend:**
- Verify backend is running: `curl http://localhost:8000/health`
- Check API URL in `.env` file
- Check browser console for errors

**2. Build errors:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 📊 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/predict` | Get delivery time prediction |
| GET | `/docs` | Swagger UI documentation |

### Input Validation

- **Delivery_person_Age:** 18-70
- **Delivery_person_Ratings:** 1.0-5.0
- **Latitudes:** -90 to 90
- **Longitudes:** -180 to 180
- **Type_of_order:** Snack, Meal, Drinks, Buffet
- **Type_of_vehicle:** motorcycle, scooter, bicycle

---

## 🎯 Production Checklist

- [ ] Backend runs without errors
- [ ] Model file is accessible
- [ ] CORS configured for your frontend domain
- [ ] Frontend `.env` configured with backend URL
- [ ] API tested with curl/Postman
- [ ] Frontend successfully calls backend
- [ ] Error handling works correctly
- [ ] HTTPS enabled (for production)
- [ ] Environment variables secured
- [ ] Logging configured
- [ ] Rate limiting added (optional)
- [ ] Monitoring setup (optional)

---

## 🚀 Quick Start Commands

**Backend:**
```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

**Frontend:**
```bash
npm install
npm run dev
```

**Test:**
```bash
curl http://localhost:8000/health
```

---

## 📝 Notes

- The backend uses the Haversine formula to calculate distance between coordinates
- One-hot encoding is applied to categorical variables to match the trained model
- Input validation prevents invalid data from reaching the model
- The model should be trained with the same features used in the API

---

## 🤝 Support

For issues or questions:
1. Check the logs: backend console and browser console
2. Test the API directly with curl
3. Verify all inputs match the expected format
4. Ensure model file is accessible

---

**Happy Deploying! 🎉**
