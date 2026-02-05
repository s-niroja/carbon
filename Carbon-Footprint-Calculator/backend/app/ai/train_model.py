# train_model.py
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# -----------------------------
# Dataset path
# -----------------------------
DATASET_PATH = Path(
    r"C:\Users\Anandhu\OneDrive\Desktop\Carbon-Footprint-Calculator\Carbon-Footprint-Calculator\datasets\processed\final_co2_dataset_clean.csv"
)

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(DATASET_PATH)
print("✅ Dataset loaded")
print("Columns:", df.columns.tolist())

# -----------------------------
# Feature engineering
# -----------------------------
# Create Train_Journey_Count from Train_Km (assuming average train journey = 50 km)
df['Train_Journey_Count'] = df['Train_Km'] / 50.0

# -----------------------------
# Compute realistic Total_CO2 with small random noise
# -----------------------------
# Using emission formulas for each activity
# CO2 factors (kg CO2 per unit)
CO2_FACTORS = {
    'Vehicle_CO2': 0.21,        # per km
    'Public_CO2': 0.1,          # per km
    'Plane_CO2': 90.0,          # per journey
    'Train_CO2': 0.05,          # per km
    'Electricity_CO2': 0.45,    # per kWh
    'Water_CO2': 0.0003,        # per liter
    'Waste_CO2': 1.0,           # per kg
    'Diet_CO2': {'Veg': 2.0, 'MostlyVeg': 3.0, 'Both': 4.0, 'MostlyNonVeg': 5.0, 'NonVeg': 6.0}
}

# Compute each CO2 component
df['Vehicle_CO2'] = df['Personal_Vehicle_Km'] * CO2_FACTORS['Vehicle_CO2']
df['Public_CO2'] = df['Public_Vehicle_Km'] * CO2_FACTORS['Public_CO2']
df['Plane_CO2'] = df['Plane_Journey_Count'] * CO2_FACTORS['Plane_CO2']
df['Train_CO2'] = df['Train_Km'] * CO2_FACTORS['Train_CO2']
df['Electricity_CO2'] = df['Electricity_Kwh'] * CO2_FACTORS['Electricity_CO2']
df['Water_CO2'] = df['Water_Usage_Liters'] * CO2_FACTORS['Water_CO2']
df['Waste_CO2'] = df['Waste_Kg'] * CO2_FACTORS['Waste_CO2']
df['Diet_CO2'] = df['Diet_Type'].map(CO2_FACTORS['Diet_CO2'])

# Total CO2 with small random noise
np.random.seed(42)
df['Calculated_Total_CO2'] = (
    df['Vehicle_CO2'] + df['Public_CO2'] + df['Plane_CO2'] + df['Train_CO2'] +
    df['Electricity_CO2'] + df['Water_CO2'] + df['Waste_CO2'] + df['Diet_CO2']
)
df['Calculated_Total_CO2'] += np.random.normal(0, 5, size=len(df))  # ±5 kg CO2 noise

print("✅ Total_CO2 computed with realistic noise")

# -----------------------------
# Features and target
# -----------------------------
FEATURES = [
    'Personal_Vehicle_Km', 'Public_Vehicle_Km', 'Plane_Journey_Count', 'Train_Km',
    'Electricity_Kwh', 'Water_Usage_Liters', 'Diet_Type', 'Waste_Kg'
]
TARGET = 'Calculated_Total_CO2'

X = df[FEATURES]
y = df[TARGET]

# -----------------------------
# Preprocessing
# -----------------------------
categorical_features = ['Diet_Type']
numerical_features = [f for f in FEATURES if f not in categorical_features]

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), categorical_features),
    ],
    remainder='passthrough'  # leave numerical features as-is
)

# -----------------------------
# RandomForest Regressor Pipeline
# -----------------------------
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=42))
])

# -----------------------------
# Hyperparameter tuning
# -----------------------------
param_grid = {
    'regressor__n_estimators': [100, 200],
    'regressor__max_depth': [None, 10, 20],
    'regressor__min_samples_split': [2, 5],
    'regressor__min_samples_leaf': [1, 2],
    'regressor__max_features': ['sqrt', 'log2']
}

grid_search = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring='r2',
    n_jobs=-1,
    verbose=1
)

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -----------------------------
# Fit model
# -----------------------------
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

print("✅ Best hyperparameters:")
print(grid_search.best_params_)

# -----------------------------
# Evaluate model
# -----------------------------
from sklearn.metrics import mean_absolute_error, r2_score

y_pred = best_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n📈 Model Evaluation on Test Set")
print(f"MAE : {mae:.2f} kg CO₂")
print(f"R²  : {r2:.3f}")

# -----------------------------
# Cross-validated R²
# -----------------------------
cv_scores = cross_val_score(best_model, X, y, cv=5, scoring='r2')
print(f"\n📊 Cross-validated R²: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# -----------------------------
# Save model
# -----------------------------
MODEL_PATH = Path(r"C:\Users\Anandhu\OneDrive\Desktop\Carbon-Footprint-Calculator\Carbon-Footprint-Calculator\models\co2_rf_model.pkl")
joblib.dump(best_model, MODEL_PATH)
print(f"\n✅ Model pipeline saved at: {MODEL_PATH}")
