# Quick Model Regeneration Script
import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

print("Loading data...")
df = pd.read_csv('dataset/clean_data.csv')

# Features and target
X = df.drop(columns=['Time_taken(min)'])
y = df['Time_taken(min)']

print(f"Training with {X.shape[0]} samples and {X.shape[1]} features")

# Train smaller model for faster regeneration
model = GradientBoostingRegressor(
    n_estimators=50,  # Reduced for speed
    learning_rate=0.1,
    max_depth=4,
    random_state=42
)

print("Training model (this may take a minute)...")
model.fit(X, y)

# Save
joblib.dump(model, 'model/final_eta_model.joblib')
print("✓ Model saved successfully to model/final_eta_model.joblib")
print("✓ Restart the backend server to use the new model")
