import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

# =====================================================
# PROJECT ROOT PATH (Carbon-Footprint-Calculator)
# =====================================================
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

print(f"📁 Project root: {BASE_DIR}")

# =====================================================
# DATASET PATH
# =====================================================
DATASET_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "processed",
    "app_usage_co2_dataset.csv"
)

print(f"📄 Dataset path: {DATASET_PATH}")

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(
        f"❌ Dataset not found!\n"
        f"Expected at: {DATASET_PATH}"
    )

# =====================================================
# MODEL SAVE PATH
# =====================================================
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "app_usage_co2_model.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)
print(f"📦 Model directory: {MODEL_DIR}")

# =====================================================
# LOAD DATASET
# =====================================================
df = pd.read_csv(DATASET_PATH)
print("✅ Dataset loaded successfully")
print(df.head())

# =====================================================
# FEATURES & TARGET
# =====================================================
X = df[
    ["CPU_Usage", "RAM_Usage", "Duration_hr", "App_Type"]
]
y = df["CO2_Kg"]

# =====================================================
# PREPROCESSING
# =====================================================
numeric_features = ["CPU_Usage", "RAM_Usage", "Duration_hr"]
categorical_features = ["App_Type"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(drop="first"), categorical_features)
    ]
)

# =====================================================
# PIPELINE
# =====================================================
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ]
)

# =====================================================
# TRAIN / TEST SPLIT
# =====================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =====================================================
# TRAIN MODEL
# =====================================================
pipeline.fit(X_train, y_train)

# =====================================================
# EVALUATION
# =====================================================
y_pred = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"📊 MAE: {mae:.3f}")
print(f"📈 R² Score: {r2:.3f}")

# =====================================================
# SAVE MODEL
# =====================================================
joblib.dump(pipeline, MODEL_PATH)

print("🎉 MODEL TRAINED SUCCESSFULLY!")
print(f"✅ Saved at: {MODEL_PATH}")
