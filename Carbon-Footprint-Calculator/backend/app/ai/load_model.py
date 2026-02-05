import os
import pandas as pd
import joblib

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_FILENAME = "co2_rf_model.pkl"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)

# -----------------------------
# Load pipeline
# -----------------------------
def load_pipeline(model_path=MODEL_PATH):
    """Load the saved RandomForest CO2 prediction pipeline."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Pipeline not found at: {model_path}")
    
    pipeline = joblib.load(model_path)
    print(f"✅ Pipeline loaded from {model_path}")
    return pipeline

# -----------------------------
# Make prediction
# -----------------------------
def predict_co2(pipeline, data):
    """Predict CO2 for new input data (DataFrame)."""
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame")
    return pipeline.predict(data)

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    # Load model
    pipeline = load_pipeline()
    
    # Example new data
    new_data = pd.DataFrame([
        {
            'Personal_Vehicle_Km': 1500,
            'Public_Vehicle_Km': 1000,
            'Plane_Journey_Count': 500,
            'Train_Km': 1500,
            'Electricity_Kwh': 15000,
            'Water_Usage_Liters': 22000,
            'Waste_Kg': 10000,
            'Diet_Type': 'NonVeg'
        }
    ])
    
    # Predict
    predicted_co2 = predict_co2(pipeline, new_data)
    print(f"Predicted CO₂: {predicted_co2[0]:.2f} kg")
