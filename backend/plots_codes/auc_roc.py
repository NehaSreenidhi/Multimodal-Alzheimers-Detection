import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
import joblib

# -------------------------------
# Load model and scaler
# -------------------------------
model = joblib.load("models/clinical_model.pkl")
scaler = joblib.load("models/clinical_scaler.pkl")

# -------------------------------
# Load test data
# -------------------------------
csv_path = r"E:\MAJOR PROJECT\Clinical features ML workflow\Processed_Alzheimers_data.csv"
df = pd.read_csv(csv_path)

FEATURES = [
    "FunctionalAssessment", "ADL", "MMSE", "MemoryComplaints",
    "BehavioralProblems", "SleepQuality", "BMI",
    "CholesterolHDL", "CholesterolLDL"
]
X = df[FEATURES]
y = df["Diagnosis"]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

X_test_scaled = scaler.transform(X_test)

# -------------------------------
# Binary ROC/AUC
# -------------------------------
# Binarize labels
classes_list = sorted(y.unique())
y_test_bin = label_binarize(y_test, classes=classes_list)  # shape = (n_samples,1)

# Predicted probabilities (probability of positive class)
y_score = model.predict_proba(X_test_scaled)[:,1]  # only positive class

fpr, tpr, _ = roc_curve(y_test_bin[:,0], y_score)
roc_auc = auc(fpr, tpr)

# Plot ROC
plt.figure(figsize=(7,6))
plt.plot(fpr, tpr, lw=2, label=f"{classes_list[1]} vs {classes_list[0]} (AUC = {roc_auc:.2f})")
plt.plot([0,1],[0,1],'k--', lw=1)  # random classifier
plt.xlim([0,1])
plt.ylim([0,1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Clinical Model: ROC Curve (Binary)")
plt.legend(loc="lower right")
plt.grid(alpha=0.3)

# Save figure
plt.savefig("metrics/clinical_roc_auc.png", dpi=300, bbox_inches="tight")
plt.show()