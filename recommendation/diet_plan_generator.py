import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

def load_rules():
    with open(BASE / "recommendation" / "rules" / "diabetic_diet_rules.json", "r", encoding="utf-8") as f:
        return json.load(f)

def recommend(glucose: float, bmi: float, veg: bool = True):
    rules = load_rules()
    thr = rules["glucose_thresholds"]
    if glucose <= thr["normal"]:
        plan_key = "normal"
    elif glucose <= thr["prediabetes"]:
        plan_key = "prediabetes"
    else:
        plan_key = "diabetes"

    plan = rules["plans"][plan_key].copy()
    tips = list(plan["tips"])
    if veg:
        tips += rules.get("veg_substitutions", [])
    # Simple BMI-based advice
    if bmi >= 30:
        tips.append("Aim for a 300–500 kcal/day deficit if overweight (consult clinician).")
    elif bmi < 18.5:
        tips.append("Increase nutrient-dense calories to reach a healthy BMI (consult clinician).")

    return {
        "category": plan_key,
        "title": plan["title"],
        "tips": tips,
        "sample_meals": [
            "Breakfast: Vegetable omelette/tofu bhurji + multigrain toast",
            "Lunch: Brown rice + dal + mixed veg + salad",
            "Snack: Unsweetened yogurt/curd + nuts",
            "Dinner: Grilled chicken/paneer + sautéed veggies + small roti"
        ]
    }
