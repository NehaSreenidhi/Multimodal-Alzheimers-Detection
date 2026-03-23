import numpy as np
import matplotlib.pyplot as plt

cm = np.load("E:/MAJOR PROJECT/Multimodal Alzheimers Detection/backend/metrics/effnet_test_confusion_matrix.npy")

classes = ["Mild", "Moderate", "NonDemented", "VeryMild"]

# Per-class accuracy
per_class_accuracy = cm.diagonal() / cm.sum(axis=1)

for c, acc in zip(classes, per_class_accuracy):
    print(f"{c}: {acc:.3f}")

plt.figure(figsize=(6,5))

plt.bar(classes, per_class_accuracy)

plt.ylabel("Accuracy")
plt.xlabel("Class")
plt.title("Per-Class Accuracy (EfficientNet Model)")

plt.ylim(0,1)

plt.savefig("metrics/plots/effnet_per_class_accuracy.png", dpi=300, bbox_inches="tight")

plt.show()