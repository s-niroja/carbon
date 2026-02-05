import pandas as pd
import numpy as np

# Seed for reproducibility
np.random.seed(42)

# Define app types and corresponding app names
app_types = ['Browser', 'IDE', 'Meeting', 'Media', 'Communication']
app_names = {
    'Browser': ['Chrome', 'Firefox', 'Edge', 'Opera'],
    'IDE': ['VSCode', 'PyCharm', 'Sublime', 'Atom'],
    'Meeting': ['Zoom', 'Teams', 'Google Meet', 'Skype'],
    'Media': ['Spotify', 'YouTube', 'VLC', 'Netflix'],
    'Communication': ['Slack', 'Discord', 'WhatsApp', 'Telegram']
}

# Generate 1000 rows of data
rows = []
for _ in range(1000):
    app_type = np.random.choice(app_types)
    app_name = np.random.choice(app_names[app_type])
    cpu_usage = round(np.random.uniform(5, 60), 2)      # CPU % usage
    ram_usage = round(np.random.uniform(0.5, 4.0), 2)   # RAM in GB
    duration = round(np.random.uniform(0.5, 8), 2)      # Duration in hours
    # Synthetic CO2 formula (simplified)
    co2 = round((cpu_usage*0.02 + ram_usage*0.05)*duration, 2)
    rows.append([app_name, cpu_usage, ram_usage, duration, app_type, co2])

# Create DataFrame
df = pd.DataFrame(rows, columns=['App_Name', 'CPU_Usage', 'RAM_Usage', 'Duration_hr', 'App_Type', 'CO2_Kg'])

# Save to CSV
df.to_csv('app_usage_co2_dataset.csv', index=False)
print("✅ 1000-row synthetic dataset saved as app_usage_co2_dataset.csv")
