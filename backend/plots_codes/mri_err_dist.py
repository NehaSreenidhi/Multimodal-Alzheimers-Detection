import numpy as np
import matplotlib.pyplot as plt

# Load confusion matrix
cm = np.load(r"E:\MAJOR PROJECT\Multimodal Alzheimers Detection\backend\metrics\effnet_test_confusion_matrix.npy")

# Compute errors per class
errors = cm.sum(axis=1) - np.diag(cm)

classes = ["Mild", "Moderate", "NonDemented", "VeryMild"]

plt.figure(figsize=(6,4))
plt.bar(classes, errors)
plt.xlabel("Alzheimer's Stage")
plt.ylabel("Number of Misclassifications")
plt.title("Error Distribution Across Alzheimer’s Classes (DL Model)")
plt.tight_layout()
plt.savefig("metrics/mri_error_distribuion.png")
plt.show()