import pandas as pd
import joblib
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
MODEL_PATH = os.path.join(BASE_DIR, "models", "co2_pipeline.pkl")
TEST_DATA_PATH = os.path.join(
    BASE_DIR, "datasets", "processed", "test_data.csv"
)

model = joblib.load(MODEL_PATH)
test_df = pd.read_csv(TEST_DATA_PATH)

predictions = model.predict(test_df)

for i, value in enumerate(predictions, 1):
    print(f"Sample {i}: {value:.2f} kg CO₂")
