# 🍔 Food Delivery Time Prediction

A full-stack web application that predicts food delivery time using machine learning. Built with FastAPI backend and React frontend.

## 🎯 Features

- **ML-Powered Predictions**: Uses trained scikit-learn model to predict delivery times
- **Real-time Distance Calculation**: Haversine formula for accurate distance computation
- **Modern UI**: Beautiful, responsive React interface with Tailwind CSS
- **Production Ready**: CORS-enabled API, input validation, comprehensive error handling
- **Easy Deployment**: Ready for Render, Railway, HuggingFace, or any cloud platform

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **scikit-learn**: Machine learning model
- **Pydantic**: Data validation
- **Pandas & NumPy**: Data processing

### Frontend
- **React**: UI framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Vite**: Build tool

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## 🚀 Quick Start

### Backend Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the server:**
```bash
uvicorn app:app --reload --port 8000
```

3. **Visit API docs:**
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/health (Health check)

### Frontend Setup

1. **Install dependencies:**
```bash
npm install
```

2. **Configure API URL (optional):**
```bash
cp .env.example .env
# Edit .env to set VITE_API_URL if needed
```

3. **Start development server:**
```bash
npm run dev
```

4. **Visit application:**
- http://localhost:5173

## 📡 API Usage

### POST /predict

**Request:**
```json
{
  "Delivery_person_Age": 25,
  "Delivery_person_Ratings": 4.5,
  "Restaurant_latitude": 12.9352,
  "Restaurant_longitude": 77.6245,
  "Delivery_location_latitude": 12.9698,
  "Delivery_location_longitude": 77.7499,
  "Type_of_order": "Meal",
  "Type_of_vehicle": "motorcycle"
}
```

**Response:**
```json
{
  "predicted_delivery_time_minutes": 28.45,
  "distance_km": 15.32,
  "success": true
}
```

### Test with curl

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

## 📁 Project Structure

```
.
├── app.py                  # FastAPI backend
├── requirements.txt        # Python dependencies
├── model/
│   └── final_eta_model.joblib  # Trained ML model
├── src/
│   ├── pages/
│   │   └── Index.tsx       # Main prediction page
│   └── components/         # UI components
├── DEPLOYMENT.md           # Detailed deployment guide
└── README.md               # This file
```

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for:
- Render
- Railway
- HuggingFace Spaces
- AWS/GCP/Azure (Docker)
- Vercel/Netlify (Frontend)

## 🔧 Configuration

### Environment Variables

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000/predict
```

**Backend:**
No environment variables required for basic setup. For production, consider adding:
- `MODEL_PATH`: Custom model file path
- `CORS_ORIGINS`: Specific allowed origins

## 📊 Model Information

The ML model predicts delivery time based on:
- Delivery person age and ratings
- Restaurant and delivery location coordinates (calculates distance)
- Type of order (Snack, Meal, Drinks, Buffet)
- Type of vehicle (motorcycle, scooter, bicycle)

## 🧪 Testing

**Backend health check:**
```bash
curl http://localhost:8000/health
```

**Run tests (if available):**
```bash
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
2. Review API documentation at `/docs`
3. Check browser console and backend logs for errors

---

**Made with ❤️ using FastAPI and React**
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

