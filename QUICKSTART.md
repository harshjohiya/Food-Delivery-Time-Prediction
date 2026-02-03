# Quick Start Guide

## ✅ System Status

Your Food Delivery Time Prediction application is now ready!

### What Has Been Built:

1. **Backend API (FastAPI)**
   - ✅ Production-ready with CORS enabled
   - ✅ Input validation with Pydantic
   - ✅ Error handling and logging
   - ✅ Health check endpoints
   - ✅ Haversine distance calculation
   - ✅ ML model inference with one-hot encoding

2. **Frontend (React + TypeScript)**
   - ✅ Beautiful, responsive UI with Tailwind CSS
   - ✅ Form validation
   - ✅ Loading states and error handling
   - ✅ Environment-based API URL configuration
   - ✅ Distance display in results

3. **Documentation**
   - ✅ Comprehensive deployment guide (DEPLOYMENT.md)
   - ✅ Updated README with examples
   - ✅ Environment variable templates

---

## 🚀 How to Run

### Start Backend:
```bash
# Windows:
start-backend.bat

# Linux/Mac:
bash start-backend.sh

# Or manually:
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Backend will run at: **http://localhost:8000**
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Start Frontend:
```bash
npm install    # Already done!
npm run dev
```

Frontend will run at: **http://localhost:5173** (or similar)

---

## 🧪 Test the API

### Quick Test:
```bash
curl http://localhost:8000/health
```

### Full Prediction Test:
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

---

## 📋 What's Included:

### Backend Files:
- `app.py` - FastAPI application with all endpoints
- `requirements.txt` - Python dependencies
- `start-backend.bat` / `start-backend.sh` - Startup scripts
- `model/final_eta_model.joblib` - Trained ML model

### Frontend Files:
- `src/pages/Index.tsx` - Main prediction page with enhanced error handling
- `.env.example` - Environment variable template

### Documentation:
- `DEPLOYMENT.md` - Complete deployment guide
- `README.md` - Project overview and API reference
- `QUICKSTART.md` - This file!

---

## 🔧 Configuration

### Backend:
No configuration needed for local development.

For production, update CORS origins in `app.py`:
```python
allow_origins=["https://your-frontend-domain.com"]
```

### Frontend:
Create `.env` file (copy from `.env.example`):
```env
VITE_API_URL=http://localhost:8000/predict
```

For production:
```env
VITE_API_URL=https://your-backend.com/predict
```

---

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions for:
- **Backend:** Render, Railway, HuggingFace Spaces, Docker
- **Frontend:** Vercel, Netlify, GitHub Pages

---

## ⚠️ Troubleshooting

### Backend won't start?
1. Check Python version: `python --version` (need 3.8+)
2. Install dependencies: `pip install -r requirements.txt`
3. Check model file exists: `model/final_eta_model.joblib`

### Model loading error?
If you see NumPy/PCG64 errors, the model needs to be regenerated with compatible versions.
The API will still start but predictions will return 503 errors.

### Frontend can't connect?
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check console for CORS errors
3. Verify API URL in `.env` file

### TypeScript errors?
Run: `npm install` to ensure all dependencies are installed.

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/predict` | POST | Predict delivery time |
| `/docs` | GET | Interactive API docs |

---

## 🎯 Next Steps

1. **Test locally:**
   - Start backend
   - Start frontend
   - Make a prediction

2. **Deploy:**
   - Follow DEPLOYMENT.md
   - Update frontend .env with production backend URL

3. **Customize:**
   - Update CORS origins for production
   - Add rate limiting if needed
   - Configure monitoring/logging

---

## 💡 Tips

- Use `/docs` endpoint for interactive API testing
- Check browser console for frontend errors
- Check terminal for backend logs
- Test with curl before testing with frontend

---

**Need help? Check DEPLOYMENT.md for detailed troubleshooting!**
