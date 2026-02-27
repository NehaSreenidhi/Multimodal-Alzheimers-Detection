import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import joblib

# -------------------------------
# 1. Load data
# -------------------------------
csv_path = r"E:\MAJOR PROJECT\Clinical features ML workflow\Processed_Alzheimers_data.csv"
df = pd.read_csv(csv_path)

# -------------------------------
# 2. Select features & target
# -------------------------------
FEATURES = [
    "FunctionalAssessment", "ADL", "MMSE", "MemoryComplaints",
    "BehavioralProblems", "SleepQuality", "BMI",
    "CholesterolHDL", "CholesterolLDL"
]
X = df[FEATURES]
y = df["Diagnosis"]

# -------------------------------
# 3. Split dataset
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------
# 4. Scale features
# -------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------------
# 5. Train XGBoost
# -------------------------------
model = XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    use_label_encoder=False
)
model.fit(X_train_scaled, y_train)

# -------------------------------
# 6. Evaluate
# -------------------------------
y_pred = model.predict(X_test_scaled)
report = classification_report(y_test, y_pred)
print("✅ Classification Report:\n", report)

# Save classification report
with open("../metrics/classification_report.txt", "w") as f:
    f.write(report)
print("✅ Classification report saved in metrics/")

# -------------------------------
# 7. Save model & scaler
# -------------------------------
joblib.dump(model, "../models/clinical_model.pkl")
joblib.dump(scaler, "../models/clinical_scaler.pkl")
print("✅ Model and scaler saved in models/")