import pandas as pd

df = pd.read_csv(
    r"C:\Users\Anandhu\OneDrive\Desktop\Carbon-Footprint-Calculator\Carbon-Footprint-Calculator\datasets\processed\vehicle_cleaned.csv"
)

print(df.columns)
print(df.head())
