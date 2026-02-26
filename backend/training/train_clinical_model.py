import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import joblib
import os

# Load data
df = pd.read_csv("E:\MAJOR PROJECT\Clinical features ML workflow\Processed_Alzheimers_data.csv")

METRICS_DIR = "metrics"

FEATURES = [
    "Age", "MMSE", "ADL", "BMI",
    "CholesterolTotal", "SleepQuality",
    "FunctionalAssessment", "DietQuality",
    "MemoryComplaints", "BehavioralProblems"
]

X = df[FEATURES]
y = df["Diagnosis"]   # 0/1

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model
model = XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss"
)

model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
report = classification_report(y_test, y_pred)
print(report)
os.makedirs("metrics", exist_ok=True)
with open("metrics/classification_report.txt", "w") as f:
    f.write(report)
print("✅ Classification report saved in metrics/classification_report.txt")

# Save model + scaler
joblib.dump(model, "models/clinical_model.pkl")
joblib.dump(scaler, "models/clinical_scaler.pkl")

print("✅ Clinical model & scaler saved")
