# Model Regeneration Script
# Run this if you encounter model loading errors

import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import warnings
warnings.filterwarnings('ignore')

print("🔄 Regenerating model with current environment...")
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")

# Load the clean data
try:
    df = pd.read_csv('dataset/clean_data.csv')
    print(f"✅ Data loaded: {df.shape}")
    
    # Prepare features and target
    # Assuming 'Time_taken(min)' is the target variable
    target_col = 'Time_taken(min)'  # Adjust if different
    
    # Drop the target from features
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    print(f"Features: {X.columns.tolist()}")
    print(f"Target: {target_col}")
    
    # Load the original model to get its parameters
    try:
        old_model = joblib.load('model/final_eta_model.joblib')
        print("✅ Old model loaded for reference")
        
        # Get model type
        print(f"Model type: {type(old_model).__name__}")
        
        # Try to recreate with same or similar parameters
        if hasattr(old_model, 'get_params'):
            params = old_model.get_params()
            print(f"Model parameters: {params}")
            
           # Create new model with same type
            if isinstance(old_model, GradientBoostingRegressor):
                new_model = GradientBoostingRegressor(**params)
            else:
                print("⚠️  Unknown model type, using default GradientBoostingRegressor")
                new_model = GradientBoostingRegressor()
            
            # Fit the new model
            print("🔄 Training new model...")
            new_model.fit(X, y)
            
            # Save with current numpy version
            joblib.dump(new_model, 'model/final_eta_model_new.joblib')
            print("✅ New model saved as 'model/final_eta_model_new.joblib'")
            print("➡️  Rename it to 'final_eta_model.joblib' to use it")
            
    except Exception as e:
        print(f"❌ Could not load old model: {e}")
        print("Please manually retrain the model using the training notebook")
        
except FileNotFoundError:
    print("❌ clean_data.csv not found")
    print("Please ensure the dataset is available at 'dataset/clean_data.csv'")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
