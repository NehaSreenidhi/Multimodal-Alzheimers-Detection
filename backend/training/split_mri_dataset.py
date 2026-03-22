import os
import pandas as pd
from sklearn.model_selection import train_test_split

ROOT_DIR = "E:\MAJOR PROJECT\Multimodal Alzheimers Detection\Datasets\MRI DATA"

data = []

for label in os.listdir(ROOT_DIR):
    class_dir = os.path.join(ROOT_DIR, label)
    if not os.path.isdir(class_dir):
        continue

    for img in os.listdir(class_dir):
        data.append([os.path.join(class_dir, img), label])

df = pd.DataFrame(data, columns=["filepath", "label"])

print("Full dataset distribution:")
print(df["label"].value_counts())

# Stratified split
train_df, temp_df = train_test_split(
    df, test_size=0.30, stratify=df["label"], random_state=42
)

val_df, test_df = train_test_split(
    temp_df, test_size=0.50, stratify=temp_df["label"], random_state=42
)

# Save splits
train_df.to_csv("../Datasets/train_mri.csv", index=False)
val_df.to_csv("../Datasets/val_mri.csv", index=False)
test_df.to_csv("../Datasets/test_mri.csv", index=False)

print("\nTrain distribution:")
print(train_df["label"].value_counts())

print("\nVal distribution:")
print(val_df["label"].value_counts())

print("\nTest distribution:")
print(test_df["label"].value_counts())

print("\n✅ MRI dataset split completed")
