import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load confusion matrix
cm = np.load("E:/MAJOR PROJECT/Multimodal Alzheimers Detection/backend/metrics/effnet_test_confusion_matrix.npy")

# Class labels
classes = ["Mild", "Moderate", "NonDemented", "VeryMild"]

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=classes,
            yticklabels=classes)

plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")

# Save to metrics folder
plt.savefig("metrics/effnet_confusionmatrix.png", dpi=300, bbox_inches="tight")

plt.show()