from .load_model import load_pipeline
from .load_app_model import load_model as app_model
import pandas as pd
from .suggestion import suggest_individual, analyze_user_emissions, app_co2_emissions

# -----------------------------
# Predict individual monthly CO2
# -----------------------------
def predict_individual_co2(pvkm, puvkm, pjc, tkm, ekwh, wul, wk, dt):
    """
    Predict individual CO2 emissions.
    
    Parameters:
    pvkm: Personal Vehicle Km
    puvkm: Public Vehicle Km
    pjc: Plane Journey Count
    tkm: Train Km
    ekwh: Electricity kWh
    wul: Water Usage Liters
    wk: Waste Kg
    dt: Diet Type
    """
    pipeline = load_pipeline()

    # Prepare input DataFrame matching training features
    try:
        new_data = pd.DataFrame([{
            'Personal_Vehicle_Km': pvkm,
            'Public_Vehicle_Km': puvkm,
            'Plane_Journey_Count': pjc,
            'Train_Km': tkm,  # match training dataset column
            'Electricity_Kwh': ekwh,
            'Water_Usage_Liters': wul,
            'Waste_Kg': wk,
            'Diet_Type': dt
        }])
    except Exception as e:
        return f"Error while preparing input data: {e}"

    # Make prediction
    try:
        prediction = pipeline.predict(new_data)
        category, suggestion = suggest_individual(prediction)
        suggestion_result = analyze_user_emissions(pvkm, puvkm, pjc, tkm, ekwh, wul, wk, dt)
        return prediction[0], category, suggestion, suggestion_result
    except Exception as e:
        return f"Error during prediction: {e}"




def predict_app_co2(cpu,ram,duriation,apptype):
  model = app_model()
  input_data =pd.DataFrame([{
    "CPU_Usage": cpu,        # %
    "RAM_Usage": ram,         # GB
    "Duration_hr": duriation,       # hours
    "App_Type": apptype     # App category
}])
  prediction = model.predict(input_data)
  #simple_suggestion = app_co2_emissions(prediction[0])
  tips =app_co2_emissions(prediction[0],apptype)
  return(prediction[0],tips)

 



#comment line cheking
if __name__ == "__main__":
    """
    co2_value, category, suggestion, result = predict_individual_co2(
        pvkm=60,
        puvkm=60,
        pjc=5,
        tkm=5,      # Train Km
        ekwh=250,
        wul=20,
        wk=0.5,
        dt="Veg"
    )

    if isinstance(co2_value, str):  # error message
        print(f"❌ {co2_value}")
    else:
        print("########################################### __OUTPUT__ ############################################################")
        print(f"✅ Predicted CO2 : {co2_value:.2f} kg")
        print(f"📊 Category     : {category}")
        print(f"💡 Suggestion   : {suggestion}\n")

        print("📋 Detailed Suggestions:")
        for item in result:
            print(f"🔹 Category   : {item.get('category', 'N/A')}")
            print(f"   Value      : {item.get('value', 'N/A')}")
            print(f"   Suggestion : {item.get('suggestion', 'N/A')}")
            print("-" * 40)

        print("########################################################################################################")


predicion, result = predict_app_co2(20.0, 7.2, 2.5, "Communication")

print("Application CO₂ Emission Report")
print("-" * 35)
print(f"Application Type : {result['application_type']}")
print(f"Predicted CO₂    : {result['predicted_co2_kg']} kg")
print(f"Impact Level     : {result['impact_level']} {result['status']}")
print("Optimization Tips:")
for i, tip in enumerate(result["optimization_tips"], 1):
    print(f"{i}. {tip}")
"""