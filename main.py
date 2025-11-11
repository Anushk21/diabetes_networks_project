from flask import Flask, request, jsonify, render_template
from pathlib import Path
from joblib import load
import numpy as np
import csv
from datetime import datetime

from recommendation.diet_plan_generator import recommend

BASE = Path(__file__).resolve().parent
MODELS = BASE / "models"

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

NUMERIC_COLS = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
    "BMI", "DiabetesPedigreeFunction", "Age"
]

# ----------------------- MODEL LOADING -----------------------
def _load_models():
    pipe = load(MODELS / "feature_pipeline.joblib")
    ensemble = load(MODELS / "ensemble_voting.joblib")
    return pipe, ensemble

def _ensure_models():
    if not (MODELS / "ensemble_voting.joblib").exists():
        # Lazy train if models missing
        import subprocess, sys
        subprocess.check_call([sys.executable, str(BASE / "training" / "train_models.py")])

pipe_cache = None
ensemble_cache = None

# ----------------------- ROUTES -----------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    # Optional: Display total records on dashboard
    data_file = BASE / "data" / "prediction_log.csv"
    total_records = 0
    if data_file.exists():
        with open(data_file, "r") as f:
            total_records = sum(1 for _ in f) - 1  # exclude header
    return render_template("dashboard.html", total_records=total_records)


@app.post("/api/predict")
def api_predict():
    global pipe_cache, ensemble_cache
    _ensure_models()
    if pipe_cache is None or ensemble_cache is None:
        pipe_cache, ensemble_cache = _load_models()

    # Accept both JSON and form submissions
    payload = request.get_json(silent=True)
    if not payload:
        payload = request.form.to_dict()

    try:
        import pandas as pd
        x = {k: [float(payload.get(k, 0.0))] for k in NUMERIC_COLS}
        X = pd.DataFrame(x)
        Xt = pipe_cache.transform(X)
        proba = float(ensemble_cache.predict_proba(Xt)[0, 1])
        label = "diabetes" if proba >= 0.5 else "no-diabetes"

        # === DATA LAYER: Store Prediction Records ===
        data_folder = BASE / "data"
        data_folder.mkdir(exist_ok=True)
        data_file = data_folder / "prediction_log.csv"

        # If file doesn't exist, create header first
        if not data_file.exists():
            with open(data_file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp", "Pregnancies", "Glucose", "BloodPressure",
                    "SkinThickness", "Insulin", "BMI",
                    "DiabetesPedigreeFunction", "Age", "Prediction", "Probability"
                ])

        # Append each new prediction
        with open(data_file, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                payload.get("Pregnancies"),
                payload.get("Glucose"),
                payload.get("BloodPressure"),
                payload.get("SkinThickness"),
                payload.get("Insulin"),
                payload.get("BMI"),
                payload.get("DiabetesPedigreeFunction"),
                payload.get("Age"),
                label,
                round(proba, 3)
            ])

        return jsonify({"label": label, "proba": round(proba, 3)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.post("/api/diet-plan")
def api_diet():
    payload = request.get_json(force=True)
    glucose = float(payload.get("glucose", 110))
    bmi = float(payload.get("bmi", 24.0))
    veg = bool(payload.get("veg", True))
    plan = recommend(glucose=glucose, bmi=bmi, veg=veg)
    return jsonify(plan)


@app.route("/data")
def data_layer():
    import pandas as pd
    data_file = BASE / "data" / "prediction_log.csv"
    if not data_file.exists():
        return render_template("data.html", tables=[], message="No data available yet.")
    df = pd.read_csv(data_file)
    return render_template(
        "data.html",
        tables=[df.to_html(classes="data", index=False)],
        titles=df.columns.values
    )


if __name__ == "__main__":
    app.run
