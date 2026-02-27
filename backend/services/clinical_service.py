import numpy as np
import joblib

model = joblib.load("models/clinical_model.pkl")
scaler = joblib.load("models/clinical_scaler.pkl")


def predict_clinical(data):
    features = [
        float(data["MMSE"]),
        float(data["FunctionalAssessment"]),
        float(data["ADL"]),
        1 if data["MemoryComplaints"] == "Yes" else 0,
        1 if data["BehavioralProblems"] == "Yes" else 0,
        float(data["SleepQuality"]),
        float(data["BMI"]),
        float(data["CholesterolHDL"]),
        float(data["CholesterolLDL"]),
    ]

    features = np.array(features).reshape(1, -1)
    scaled = scaler.transform(features)

    prob = model.predict_proba(scaled)[0][1]  # dementia probability

    return float(prob)