import matplotlib.pyplot as plt

# File path
report_file = "E:/MAJOR PROJECT/Multimodal Alzheimers Detection/backend/metrics/effnet_test_classification_report.txt"

classes = []
precision = []
recall = []
f1_score = []

with open(report_file, "r") as f:
    lines = f.readlines()

# Skip first line (header)
for line in lines[1:]:
    parts = line.strip().split()
    if len(parts) == 5:  # class rows
        cls, p, r, f1, support = parts
        classes.append(cls)
        precision.append(float(p))
        recall.append(float(r))
        f1_score.append(float(f1))
    else:
        # skip lines like accuracy, macro avg, weighted avg
        continue

# Plot Precision, Recall, F1-score
import pandas as pd

metrics_df = pd.DataFrame({
    "Class": classes,
    "Precision": precision,
    "Recall": recall,
    "F1-score": f1_score
})

metrics_df.set_index("Class", inplace=True)
metrics_df.plot(kind="bar", figsize=(7,5))

plt.title("Class-wise Precision, Recall, and F1-score")
plt.xlabel("Class")
plt.ylabel("Score")
plt.ylim(0,1)
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("metrics/class_metrics.png", dpi=300)
plt.show()