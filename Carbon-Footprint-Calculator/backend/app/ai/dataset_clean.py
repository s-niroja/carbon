import pandas as pd
import os

# =============================
# Paths
# =============================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "processed", "final_co2_dataset_realistic.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "datasets", "processed", "final_co2_dataset_clean.csv")

# =============================
# Load dataset
# =============================
df = pd.read_csv(DATASET_PATH)
df.columns = df.columns.str.strip()

print("✅ Original Columns:", df.columns.tolist())

# =============================
# Columns to remove (CO2 component columns)
# =============================
co2_columns = [
    "Vehicle_CO2",
    "Public_CO2",
    "Plane_CO2",
    "Train_CO2",
    "Electricity_CO2",
    "Water_CO2",
    "Waste_CO2",
    "Diet_CO2",
    "Calculated_Total_CO2"  # optional if you want to recompute later
]

# Remove CO2 columns if they exist
df_clean = df.drop(columns=[col for col in co2_columns if col in df.columns])

print("✅ Cleaned Columns:", df_clean.columns.tolist())

# =============================
# Save cleaned dataset
# =============================
df_clean.to_csv(OUTPUT_PATH, index=False)
print(f"\n✅ Cleaned dataset saved at:\n{OUTPUT_PATH}")
