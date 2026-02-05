import pandas as pd
from backend.app.ai.load_app_model import load_model

model =load_model()
sample_input = pd.DataFrame([{
    "CPU_Usage": 20.0,        # %
    "RAM_Usage": 7.2,         # GB
    "Duration_hr": 2.5,       # hours
    "App_Type": "IDE"     # App category
}])
prediction = model.predict(sample_input)
print(prediction[0])