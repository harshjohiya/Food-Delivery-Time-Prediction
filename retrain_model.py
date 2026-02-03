import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
import joblib

# Load data
df = pd.read_csv("dataset/clean_data.csv")

# Strip trailing spaces from column names
df.columns = df.columns.str.strip()

print(f"Loaded {len(df)} samples")
print(f"Columns: {df.columns.tolist()}")

# Features and target - REMOVE lat/long columns
X = df.drop(columns=[
    "Time_taken(min)",
    "Restaurant_latitude",
    "Restaurant_longitude", 
    "Delivery_location_latitude",
    "Delivery_location_longitude"
])
y = df["Time_taken(min)"]

print(f"\nFeatures (distance-only model): {X.columns.tolist()}")
print(f"Feature shape: {X.shape}")

# Train model
print("\nTraining model...")
model = HistGradientBoostingRegressor(random_state=42, max_iter=100)
model.fit(X, y)

# Save model
joblib.dump(model, "model/final_eta_model.joblib")
print("\n✓ Model saved to model/final_eta_model.joblib")
print(f"Model features: {model.feature_names_in_.tolist()}")

# Test prediction
sample = X.iloc[0:1]
pred = model.predict(sample)
print(f"\nTest prediction: {pred[0]:.2f} minutes")
print(f"Actual: {y.iloc[0]:.2f} minutes")
