import pandas as pd
import numpy as np
import random

# -----------------------------
# Configuration
# -----------------------------
NUM_SAMPLES = 1000
OUTPUT_PATH = "final_co2_dataset_realistic.csv"

# Emission factors (kg CO2)
VEHICLE_CO2_PER_KM = 0.21
PUBLIC_CO2_PER_KM = 0.05
PLANE_CO2_PER_TRIP = 90
TRAIN_CO2_PER_KM = 0.015
ELECTRICITY_CO2_PER_KWH = 0.82
WATER_CO2_PER_LITER = 0.0003
WASTE_CO2_PER_KG = 1.9

DIET_CO2 = {
    "Veg": 1.7,
    "MostlyVeg": 2.5,
    "Both": 3.3,
    "MostlyNonVeg": 4.2,
    "NonVeg": 5.0
}

# -----------------------------
# Dataset generation
# -----------------------------
data = []

for _ in range(NUM_SAMPLES):

    # Generate travel distances with some realistic correlations
    personal_km = round(np.random.normal(40, 25), 2)  # avg 40 km, std 25
    personal_km = np.clip(personal_km, 0, 100)

    public_km = round(np.random.normal(25, 15), 2)
    public_km = np.clip(public_km, 0, 70)

    plane_trips = np.random.choice([0, 1, 2, 3], p=[0.6, 0.25, 0.1, 0.05])  # most people 0-1

    train_km = round(np.random.normal(100, 80), 2)
    train_km = np.clip(train_km, 0, 300)

    # Utilities correlated with travel: more travel → more electricity likely
    electricity_kwh = round(np.random.normal(200 + 0.5*plane_trips*100, 80), 2)
    electricity_kwh = np.clip(electricity_kwh, 50, 400)

    water_liters = round(np.random.normal(120, 50), 2)
    water_liters = np.clip(water_liters, 50, 200)

    waste_kg = round(np.random.normal(0.8, 0.3), 2)
    waste_kg = np.clip(waste_kg, 0.3, 1.5)

    # Diet chosen randomly but with weighted probabilities
    diet = random.choices(
        population=list(DIET_CO2.keys()),
        weights=[0.2, 0.25, 0.2, 0.2, 0.15],
        k=1
    )[0]

    # -----------------------------
    # CO2 Calculations
    # -----------------------------
    vehicle_co2 = personal_km * VEHICLE_CO2_PER_KM
    public_co2 = public_km * PUBLIC_CO2_PER_KM
    plane_co2 = plane_trips * PLANE_CO2_PER_TRIP
    train_co2 = train_km * TRAIN_CO2_PER_KM
    electricity_co2 = electricity_kwh * ELECTRICITY_CO2_PER_KWH
    water_co2 = water_liters * WATER_CO2_PER_LITER
    waste_co2 = waste_kg * WASTE_CO2_PER_KG
    diet_co2 = DIET_CO2[diet]

    total_co2 = (
        vehicle_co2 +
        public_co2 +
        plane_co2 +
        train_co2 +
        electricity_co2 +
        water_co2 +
        waste_co2 +
        diet_co2
    )

    data.append([
        personal_km,
        public_km,
        plane_trips,
        train_km,
        electricity_kwh,
        water_liters,
        diet,
        waste_kg,
        round(vehicle_co2, 2),
        round(public_co2, 2),
        round(plane_co2, 2),
        round(train_co2, 2),
        round(electricity_co2, 2),
        round(water_co2, 4),
        round(waste_co2, 2),
        diet_co2,
        round(total_co2, 2)
    ])

# -----------------------------
# Create DataFrame
# -----------------------------
columns = [
    "Personal_Vehicle_Km",
    "Public_Vehicle_Km",
    "Plane_Journey_Count",
    "Train_Km",
    "Electricity_Kwh",
    "Water_Usage_Liters",
    "Diet_Type",
    "Waste_Kg",
    "Vehicle_CO2",
    "Public_CO2",
    "Plane_CO2",
    "Train_CO2",
    "Electricity_CO2",
    "Water_CO2",
    "Waste_CO2",
    "Diet_CO2",
    "Calculated_Total_CO2"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv(OUTPUT_PATH, index=False)
print(f"✅ Realistic and consistent dataset generated: {OUTPUT_PATH}")
