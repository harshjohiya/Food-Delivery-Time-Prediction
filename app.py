from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import joblib
import pandas as pd
import numpy as np
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model
MODEL_PATH = "model/final_eta_model.joblib"
model = None
try:
    model = joblib.load(MODEL_PATH)
    logger.info(f"Model loaded successfully from {MODEL_PATH}")
    logger.info(f"Model features: {list(model.feature_names_in_)}")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    logger.error("Please ensure the model was saved with compatible scikit-learn and numpy versions")
    logger.error("Try regenerating the model or adjust numpy/scikit-learn versions")
    # Don't raise - allow API to start for health checks

app = FastAPI(
    title="Food Delivery Time Prediction API",
    description="API for predicting food delivery time based on delivery details",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------- Input Schema --------
class DeliveryInput(BaseModel):
    Delivery_person_Age: int = Field(..., ge=18, le=70, description="Age of delivery person")
    Delivery_person_Ratings: float = Field(..., ge=1.0, le=5.0, description="Rating of delivery person")
    Restaurant_latitude: float = Field(..., ge=-90, le=90, description="Restaurant latitude")
    Restaurant_longitude: float = Field(..., ge=-180, le=180, description="Restaurant longitude")
    Delivery_location_latitude: float = Field(..., ge=-90, le=90, description="Delivery location latitude")
    Delivery_location_longitude: float = Field(..., ge=-180, le=180, description="Delivery location longitude")
    Type_of_order: str = Field(..., description="Type of order (e.g., Snack, Meal, Drinks, Buffet)")
    Type_of_vehicle: str = Field(..., description="Type of vehicle (e.g., motorcycle, scooter, bicycle)")

    @validator('Type_of_order')
    def validate_order_type(cls, v):
        valid_types = ['Snack', 'Meal', 'Drinks', 'Buffet']
        if v not in valid_types:
            raise ValueError(f'Type_of_order must be one of {valid_types}')
        return v
    
    @validator('Type_of_vehicle')
    def validate_vehicle_type(cls, v):
        valid_vehicles = ['motorcycle', 'scooter', 'bicycle']
        if v not in valid_vehicles:
            raise ValueError(f'Type_of_vehicle must be one of {valid_vehicles}')
        return v


class PredictionResponse(BaseModel):
    predicted_delivery_time_minutes: float = Field(..., description="Predicted delivery time in minutes")
    distance_km: Optional[float] = Field(None, description="Calculated distance in kilometers")
    success: bool = Field(True, description="Prediction success status")



# -------- Distance Function --------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))



# -------- Health Check Endpoint --------
@app.get("/")
def root():
    return {
        "message": "Food Delivery Time Prediction API",
        "status": "active",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict (POST)",
            "health": "/health (GET)",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_features": len(model.feature_names_in_) if model else 0
    }


# -------- Prediction Endpoint --------
@app.post("/predict", response_model=PredictionResponse)
def predict_delivery_time(data: DeliveryInput):
    try:
        logger.info(f"Received prediction request: {data.dict()}")
        
        # Convert to dict
        input_data = data.dict()

        # Compute distance
        distance_km = haversine(
            input_data["Restaurant_latitude"],
            input_data["Restaurant_longitude"],
            input_data["Delivery_location_latitude"],
            input_data["Delivery_location_longitude"]
        )
        
        logger.info(f"Calculated distance: {distance_km:.2f} km")

        # Base dataframe
        row = {
            "Delivery_person_Age": input_data["Delivery_person_Age"],
            "Delivery_person_Ratings": input_data["Delivery_person_Ratings"],
            "Restaurant_latitude": input_data["Restaurant_latitude"],
            "Restaurant_longitude": input_data["Restaurant_longitude"],
            "Delivery_location_latitude": input_data["Delivery_location_latitude"],
            "Delivery_location_longitude": input_data["Delivery_location_longitude"],
            "distance_km": distance_km,
        }

        df = pd.DataFrame([row])

        # One-hot encoding (must match training)
        for col in model.feature_names_in_:
            if col.startswith("Type_of_order_") or col.startswith("Type_of_vehicle_"):
                df[col] = 0

        order_col = f"Type_of_order_{input_data['Type_of_order']}"
        vehicle_col = f"Type_of_vehicle_{input_data['Type_of_vehicle']}"

        if order_col in model.feature_names_in_:
            df[order_col] = 1
        else:
            logger.warning(f"Order type '{input_data['Type_of_order']}' not found in model features")

        if vehicle_col in model.feature_names_in_:
            df[vehicle_col] = 1
        else:
            logger.warning(f"Vehicle type '{input_data['Type_of_vehicle']}' not found in model features")

        # Ensure all model features are present and in correct order
        df = df[model.feature_names_in_]

        # Make prediction
        prediction = model.predict(df)[0]
        
        logger.info(f"Prediction: {prediction:.2f} minutes")

        return {
            "predicted_delivery_time_minutes": round(float(prediction), 2),
            "distance_km": round(float(distance_km), 2),
            "success": True
        }
    
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
