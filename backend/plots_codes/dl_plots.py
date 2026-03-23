import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import entropy

# Setup
SAVE_DIR = "metrics/plots"
os.makedirs(SAVE_DIR, exist_ok=True)
CLASSES = ['Mild', 'Moderate', 'Non-Demented', 'Very Mild']

# Load only probabilities
probs = np.load(r'E:\MAJOR PROJECT\Multimodal Alzheimers Detection\backend\assets\effnet_test_probabilities.npy')

# --- Class Probability Correlations ---
plt.figure(figsize=(8, 6))
corr = np.corrcoef(probs.T)
sns.heatmap(corr, annot=True, xticklabels=CLASSES, yticklabels=CLASSES, cmap='coolwarm')
plt.title('Correlation Between Disease Stage Probabilities')
plt.savefig(os.path.join(SAVE_DIR, "class_correlation_heatmap.png"))
plt.close()
