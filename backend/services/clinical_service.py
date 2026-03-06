import numpy as np
import pandas as pd
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

    feature_names = scaler.feature_names_in_
    features_df = pd.DataFrame([features], columns=feature_names)
    scaled = scaler.transform(features_df)

    prob = model.predict_proba(scaled)[0][1]  # dementia probability

    return float(prob)