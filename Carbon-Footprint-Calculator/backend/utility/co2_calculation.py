import pandas as pd
from pathlib import Path

DATA_DIR = Path(
    r"C:\Users\Anandhu\OneDrive\Desktop\Carbon-Footprint-Calculator\Carbon-Footprint-Calculator\datasets\processed"
)

# Emission factors (kg CO₂)
EF_PERSONAL = 0.192
EF_PUBLIC = 0.089
EF_TRAIN = 0.041
EF_PLANE = 90


def calculate_vehicle_co2():
    df = pd.read_csv(DATA_DIR / "vehicle_cleaned.csv")

    df["Personal_Vehicle_CO2"] = df["Personal_Vehicle_Km"] * EF_PERSONAL
    df["Public_Vehicle_CO2"] = df["Public_Vehicle_Km"] * EF_PUBLIC
    df["Train_CO2"] = df["Train_Journey_Count"] * EF_TRAIN
    df["Plane_CO2"] = df["Plane_Journey_Count"] * EF_PLANE

    df["Total_Vehicle_CO2"] = (
        df["Personal_Vehicle_CO2"]
        + df["Public_Vehicle_CO2"]
        + df["Train_CO2"]
        + df["Plane_CO2"]
    )

    df.to_csv(DATA_DIR / "vehicle_co2.csv", index=False)
    print("✅ Vehicle CO₂ calculation completed successfully")


if __name__ == "__main__":
    calculate_vehicle_co2()
