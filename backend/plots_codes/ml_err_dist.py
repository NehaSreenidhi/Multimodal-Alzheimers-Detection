import numpy as np
import matplotlib.pyplot as plt
import re
import os

# Use an absolute path or ensure the script knows where to look
file_path = r"E:\MAJOR PROJECT\Multimodal Alzheimers Detection\backend\metrics\clinical_confusion_matrix.txt"

with open(file_path, "r") as f:
    text = f.read()

# Extract all numbers as integers
nums = list(map(int, re.findall(r'\d+', text)))

# Take only the LAST 4 numbers (which represent the [[TN, FP], [FN, TP]] raw array)
if len(nums) >= 4:
    matrix_vals = nums[-4:] 
    cm = np.array(matrix_vals).reshape(2, 2)
else:
    raise ValueError("Could not find enough numerical data in the text file.")

TN, FP = cm[0]
FN, TP = cm[1]

errors = [FP, FN]
labels = ["False Positives (Type I)", "False Negatives (Type II)"]
colors = ['#ff9999', '#66b3ff'] # Soft red and blue for clear distinction

plt.figure(figsize=(8, 5))
bars = plt.bar(labels, errors, color=colors, edgecolor='black', width=0.6)

# Add value labels on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, yval, ha='center', va='bottom', fontweight='bold')

plt.ylabel("Number of Cases")
plt.title("Error Analysis: Clinical ML Model (False Predictions)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Ensure metrics directory exists before saving
os.makedirs("metrics", exist_ok=True)
plt.savefig("metrics/ml_error_distribution.png")
plt.show()

print(f"✅ Error distribution plot saved with FP: {FP} and FN: {FN}")