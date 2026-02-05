def suggest_individual(prediction):
  try:
    if prediction < 1000:
        category = "Good ✅"
        suggestion = "Keep it up! You’re living sustainably 🌱"
    elif 1000 <= prediction <= 3000:
        category = "Average ⚖️"
        suggestion = "Try reducing car usage, eat more plant-based meals, and save energy."
    else:
        category = "Bad ❌"
        suggestion = "Significant reduction needed: reduce travel, minimize waste, switch to renewable energy."
    return category, suggestion
  except:
     raise Exception("cant suggest")
  

def analyze_user_emissions(pvkm, puvkm, pjc, tjc, ekwh, wul, wk, dt):

    # -----------------------------
    # User values mapping
    # -----------------------------
    values = {
        'Personal_Vehicle_Km': pvkm,
        'Public_Vehicle_Km': puvkm,
        'Plane_Journey_Count': pjc,
        'Train_Journey_Count': tjc,
        'Electricity_Kwh': ekwh,
        'Water_Usage_Liters': wul,
        'Waste_Kg': wk
    }

    # -----------------------------
    # Rules: threshold + suggestion
    # -----------------------------
    rules = {
        'Personal_Vehicle_Km': {
            'threshold': 120,
            'suggestion': "Reduce personal vehicle usage 🚗"
        },
        'Public_Vehicle_Km': {
            'threshold': 100,
            'suggestion': "Prefer buses or trains over private vehicles 🚌"
        },
        'Plane_Journey_Count': {
            'threshold': 2,
            'suggestion': "Reduce air travel ✈️"
        },
        'Train_Journey_Count': {
            'threshold': 10,
            'suggestion': "Combine train trips or travel efficiently 🚆"
        },
        'Electricity_Kwh': {
            'threshold': 200,
            'suggestion': "Save electricity: use LED bulbs, switch off unused devices 💡"
        },
        'Water_Usage_Liters': {
            'threshold': 50,
            'suggestion': "Reduce water wastage 🚿"
        },
        'Waste_Kg': {
            'threshold': 1,
            'suggestion': "Minimize and recycle waste ♻️"
        }
    }

    # -----------------------------
    # Build matched results
    # -----------------------------
    results = []

    for category, rule in rules.items():
        value = values[category]

        if value > rule['threshold']:
            results.append({
                "category": category,
                "value": value,
                "threshold": rule['threshold'],
                "suggestion": rule['suggestion']
            })

    # -----------------------------
    # Diet-based suggestion
    # -----------------------------
    if dt == "NonVeg":
        results.append({
            "category": "Diet_Type",
            "value": dt,
            "threshold": None,
            "suggestion": "Eat more plant-based meals 🌱"
        })

    # -----------------------------
    # Sort:
    # 1️⃣ Exceeded threshold first
    # 2️⃣ Higher value first
    # -----------------------------
    results.sort(
        key=lambda x: (
            x['threshold'] is not None and x['value'] <= x['threshold'],
            -x['value'] if isinstance(x['value'], (int, float)) else 0
        )
    )

    # -----------------------------
    # Default eco-friendly message
    # -----------------------------
    if not results:
        results.append({
            "category": "Overall",
            "value": 0,
            "threshold": None,
            "suggestion": "Your lifestyle is eco-friendly! Keep it up 🌍"
        })

    return results


def app_co2_emissions(prediction,app_type):
    
    if prediction > 5.0:
      impact = "High"
      status = "🔴 Needs Reduction"
      tips = [
        "Limit long-running background usage ⏱️",
        "Close unused apps to free memory 🧠",
        "Disable unused plugins 🧩",
        "Close inactive projects"
    ]

    elif 2.0 < prediction <= 5.0:
      impact = "Medium"
      status = "🟠 Needs Reduction"
      tips = [
        "Limit long-running background usage ⏱️",
        "Close unused apps to free memory 🧠",
        "Disable unused plugins 🧩",
        "Close inactive projects"
    ]

    else:
      impact = "Low"
      status = "🟢 Optimized"
      tips = ["Application usage is efficient 👍"]


    return {
        "application_type": app_type,
        "predicted_co2_kg": round(prediction, 3),
        "impact_level": impact,
        "status": status,
        "optimization_tips": tips
    }