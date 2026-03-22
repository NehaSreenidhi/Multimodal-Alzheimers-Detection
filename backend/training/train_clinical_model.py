import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# 1. Load processed dataset
csv_path = r"E:\MAJOR PROJECT\Clinical features ML workflow\Processed_Alzheimers_data.csv"
df = pd.read_csv(csv_path)

# 2. Select features & target
FEATURES = [
    'MMSE',
    'FunctionalAssessment',
    'ADL',
    'MemoryComplaints',
    'BehavioralProblems',
    'SleepQuality',
    'Age',
    'CholesterolHDL',
    'CholesterolLDL',
    'FamilyHistoryAlzheimers'
]

X = df[FEATURES]
y = df["Diagnosis"]

# 3. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# Calculate class imbalance weight
scale_pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])
print("scale_pos_weight:", scale_pos_weight)

# 4. Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Train XGBoost
model = XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    scale_pos_weight=scale_pos_weight, 
    use_label_encoder=False
)
model.fit(X_train_scaled, y_train)

# 6. Evaluate
y_pred = model.predict(X_test_scaled)
report = classification_report(y_test, y_pred)
print("Classification Report:\n", report)

# Save classification report
with open("metrics/ml_classification_report.txt", "w") as f:
    f.write(report)
print("Classification report saved in metrics/")

# Generate Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

# Visualize the Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Non-Demented', 'Demented'], 
            yticklabels=['Non-Demented', 'Demented'])
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix: Clinical ML Model')

# Save the plot
plt.savefig("metrics/plots/clinical_confusion_matrix.png")
plt.show()

cm_txt_path = "metrics/clinical_confusion_matrix.txt"

# Save as a more descriptive text summary
with open(cm_txt_path, "w") as f:
    f.write("Confusion Matrix: Clinical ML Model\n")
    f.write("-" * 35 + "\n")
    f.write(f"True Non-Demented: {cm[0][0]} (Correct) | {cm[0][1]} (Misclassified)\n")
    f.write(f"True Demented:     {cm[1][0]} (Misclassified) | {cm[1][1]} (Correct)\n")
    f.write("-" * 35 + "\n")
    f.write(f"Raw Array:\n{cm}")

print(f"✅ Confusion matrix text file saved in {cm_txt_path}")

# 7. Save model & scaler
joblib.dump(model, "models/clinical_model.pkl")
joblib.dump(scaler, "models/clinical_scaler.pkl")
print("✅ Model and scaler saved in models/")