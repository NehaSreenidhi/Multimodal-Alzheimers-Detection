import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ================= PATHS =================
MODEL_PATH = "models/mri_effnet_best.h5"
TEST_CSV = "data/test_mri.csv"

ASSETS_DIR = "assets"     
METRICS_DIR = "metrics"    

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(METRICS_DIR, exist_ok=True)

# ================= CONFIG =================
IMG_SIZE = (224, 224)
BATCH_SIZE = 16

# ================= LOAD CLASS INDICES =================
with open(f"{ASSETS_DIR}/effnet_class_indices.json") as f:
    class_indices = json.load(f)

# Ensure consistent ordering
class_names = [
    k for k, v in sorted(class_indices.items(), key=lambda item: item[1])
]

# ================= LOAD MODEL =================
model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

# ================= LOAD TEST DATA =================
test_df = pd.read_csv(TEST_CSV)

test_gen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

test_data = test_gen.flow_from_dataframe(
    test_df,
    x_col="filepath",
    y_col="label",
    target_size=IMG_SIZE,
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    shuffle=False
)
print("Class indices (TEST):", test_data.class_indices)
print("Expected order:", class_names)

# ================= PREDICTIONS =================
y_probs = model.predict(test_data, verbose=1)
y_pred = np.argmax(y_probs, axis=1)
y_true = test_data.classes

print("Prediction distribution:", np.bincount(y_pred))

# ================= SAVE PROBABILITIES (FOR FUSION) =================
np.save(f"{ASSETS_DIR}/effnet_test_probabilities.npy", y_probs)
np.save(f"{ASSETS_DIR}/effnet_test_labels.npy", y_true)

# ================= METRICS =================
acc = accuracy_score(y_true, y_pred)
print(f"\n✅ Test Accuracy: {acc:.4f}")

report = classification_report(
    y_true,
    y_pred,
    target_names=class_names,
    digits=4
)

print("\nClassification Report:\n", report)

with open(f"{METRICS_DIR}/effnet_test_classification_report.txt", "w") as f:
    f.write(report)

# ================= CONFUSION MATRIX =================
cm = confusion_matrix(y_true, y_pred)

# Primary (machine-readable)
np.save(f"{METRICS_DIR}/effnet_test_confusion_matrix.npy", cm)

# Secondary (human-readable)
with open(f"{METRICS_DIR}/effnet_test_confusion_matrix.txt", "w") as f:
    f.write("Confusion Matrix\n")
    f.write("Rows: True labels | Columns: Predicted labels\n\n")
    f.write(np.array2string(cm))

# ================= PER-CLASS ACCURACY =================
per_class_acc = cm.diagonal() / cm.sum(axis=1)

per_class_results = {
    class_names[i]: float(per_class_acc[i])
    for i in range(len(class_names))
}

with open(f"{METRICS_DIR}/effnet_per_class_accuracy.json", "w") as f:
    json.dump(per_class_results, f, indent=4)

print("\nPer-class accuracy:")
for cls, acc in per_class_results.items():
    print(f"{cls}: {acc:.4f}")

print("\n✅ EfficientNet testing completed successfully")
