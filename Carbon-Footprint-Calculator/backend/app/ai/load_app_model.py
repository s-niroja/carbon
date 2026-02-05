import joblib
from pathlib import Path
import pandas as pd

# -----------------------------
# Base directory (project root)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[3]
# → Carbon-Footprint-Calculator/

# -----------------------------
# Model path
# -----------------------------
MODEL_PATH = BASE_DIR / "models" / "app_usage_co2_model.pkl"

# -----------------------------
# Load model
# -----------------------------
def load_model():
    #print(f"🔍 Looking for model at:\n{MODEL_PATH}")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"❌ Model file not found.\nExpected at: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)
    #print("✅ Model loaded successfully")
    return model


# -----------------------------
# Test loading
# -----------------------------
if __name__ == "__main__":
    model = load_model()

    
    print("📦 Model object:", model)
