# Diabetes Detection & Diet Plan — CN Project (Cloud + IoT + Ensemble)

This is a complete **Computer Networks-flavoured** project that implements:
- A Flask **backend API** (client–server over HTTP/JSON)
- **Model training** for Decision Tree, SVM, and MLP, plus a **Voting ensemble**
- A simple **patient web UI** and **provider dashboard**
- A rule-based **diet plan recommendation** module
- Sample **data** and a fully automated setup

> Designed so you can run it locally in minutes. No external downloads required.

---

## 🗂 Project Structure
```
diabetes_networks_project/
├── app/
│   ├── templates/
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   └── diet_plan.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── cloud/
│   ├── storage_config.yaml
│   └── api_integration.py
├── data/
│   └── diabetes_sample.csv
├── models/           # populated after training
├── preprocessing/
│   └── feature_pipeline.py
├── recommendation/
│   ├── diet_plan_generator.py
│   └── rules/diabetic_diet_rules.json
├── tests/
│   └── run_smoke_test.py
├── training/
│   └── train_models.py
├── main.py           # Flask API server
├── requirements.txt
└── README.md
```

---

## ▶️ Quickstart (Local)

1) **Create venv & install deps**
```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2) **Train models (creates /models)**
```bash
python training/train_models.py
```

3) **Run the server**
```bash
python main.py
```
- Open **http://127.0.0.1:5000/** for the patient UI
- Open **http://127.0.0.1:5000/dashboard** for the provider dashboard

---

## 🧪 Try the API (Examples)

**Prediction**
```bash
curl -X POST http://127.0.0.1:5000/api/predict   -H "Content-Type: application/json"   -d '{"Pregnancies":2,"Glucose":140,"BloodPressure":80,"SkinThickness":25,"Insulin":100,"BMI":30.5,"DiabetesPedigreeFunction":0.45,"Age":35}'
```

**Diet plan**
```bash
curl -X POST http://127.0.0.1:5000/api/diet-plan   -H "Content-Type: application/json"   -d '{"glucose": 155, "bmi": 31.2, "veg": true}'
```

---

## 🔐 CN Angle (What to Say in Viva)
- Client–Server over HTTP (Flask API)
- JSON payloads using REST
- Secure transport (recommend HTTPS in production)
- Layered design & logical topology (UI ⇄ API ⇄ ML Models ⇄ Storage)
- Placeholder cloud config + APIs for extensibility (cloud/ folder)
- Could use **MQTT/WebSockets** for CGM devices (left as an extension)

---

## 📦 Notes
- Dataset is a small sample similar in shape to Pima Indians Diabetes data.
- Models are lightweight for quick demos.
- No external internet access required.
- Extend rules in `recommendation/rules/diabetic_diet_rules.json`.
