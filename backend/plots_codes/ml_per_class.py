import numpy as np
import matplotlib.pyplot as plt
import re

# Load confusion matrix from txt file
file_path = r"E:\MAJOR PROJECT\Multimodal Alzheimers Detection\backend\metrics\clinical_confusion_matrix.txt"

with open(file_path, "r") as f:
    data = f.read()

# Extract the array part using regex
array_text = re.search(r"\[\[.*\]\]", data, re.DOTALL).group()

# Remove outer brackets and split into lines
lines = array_text.strip("[]").split("\n")

# Convert each line into a list of integers (remove any '[' or ']' from line)
cm_clinical = np.array([
    [int(x) for x in re.findall(r'\d+', line)]
    for line in lines
])

classes = ["Non-Demented", "Demented"]

# Calculate per-class accuracy
per_class_accuracy = cm_clinical.diagonal() / cm_clinical.sum(axis=1)

# Print per-class accuracy
print("Clinical ML Model Per-Class Accuracy:")
for c, acc in zip(classes, per_class_accuracy):
    print(f"{c}: {acc:.3f}")

# Plot per-class accuracy
plt.figure(figsize=(6,5))
plt.bar(classes, per_class_accuracy, color='lightgreen')
plt.ylabel("Accuracy")
plt.xlabel("Class")
plt.title("Per-Class Accuracy (Clinical ML Model)")
plt.ylim(0,1)
plt.savefig(r"E:\MAJOR PROJECT\Multimodal Alzheimers Detection\backend\metrics\plots\ml_per_class_accuracy.png", dpi=300, bbox_inches="tight")
plt.show()