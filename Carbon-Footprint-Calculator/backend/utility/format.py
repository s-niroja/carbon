import pandas as pd
from pathlib import Path

BASE_DIR = Path(
    r"C:\Users\Anandhu\OneDrive\Desktop\Carbon-Footprint-Calculator\Carbon-Footprint-Calculator"
)

INPUT_FILE = BASE_DIR / "datasets/row/Carbon FootPrint - Regression .csv"
OUTPUT_FILE = BASE_DIR / "datasets/processed/vehicle_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

# Fix negative values
df["Personal_Vehicle_Km"] = df["Personal_Vehicle_Km"].abs()
df["Public_Vehicle_Km"] = df["Public_Vehicle_Km"].abs()
df["Train_Journey_Count"] = df["Train_Journey_Count"].abs()
df["Plane_Journey_Count"] = df["Plane_Journey_Count"].abs()

df.to_csv(OUTPUT_FILE, index=False)
print("✅ Vehicle data cleaned successfully")
