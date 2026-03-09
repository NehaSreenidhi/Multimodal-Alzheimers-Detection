import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import entropy

# Setup
SAVE_DIR = "metrics"
os.makedirs(SAVE_DIR, exist_ok=True)
CLASSES = ['Mild', 'Moderate', 'Non-Demented', 'Very Mild']

# Load only probabilities
probs = np.load(r'E:\MAJOR PROJECT\Multimodal Alzheimers Detection\backend\assets\effnet_test_probabilities.npy')

# --- PLOT 1: Max Confidence Distribution ---
plt.figure(figsize=(10, 6))
max_probs = np.max(probs, axis=1)
sns.histplot(max_probs, bins=25, kde=True, color='skyblue')
plt.title('Distribution of Model Prediction Confidence')
plt.xlabel('Confidence Score (0.0 to 1.0)')
plt.ylabel('Number of Samples')
plt.savefig(os.path.join(SAVE_DIR, "model_confidence_dist.png"))
plt.close()

# --- PLOT 2: Prediction Entropy (Uncertainty) ---
plt.figure(figsize=(10, 6))
uncertainty = entropy(probs.T)
sns.kdeplot(uncertainty, fill=True, color='orange')
plt.title('Model Uncertainty (Entropy) Distribution')
plt.xlabel('Entropy Score (Higher = More Uncertain)')
plt.savefig(os.path.join(SAVE_DIR, "model_uncertainty_entropy.png"))
plt.close()

# --- PLOT 3: Class Probability Correlations ---
plt.figure(figsize=(8, 6))
corr = np.corrcoef(probs.T)
sns.heatmap(corr, annot=True, xticklabels=CLASSES, yticklabels=CLASSES, cmap='coolwarm')
plt.title('Correlation Between Disease Stage Probabilities')
plt.savefig(os.path.join(SAVE_DIR, "class_correlation_heatmap.png"))
plt.close()

print("Confidence and Uncertainty plots saved to metrics/ folder.")