import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.utils.class_weight import compute_class_weight

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# ================== PATHS ==================
MODEL_DIR   = "models"
METRICS_DIR = "metrics"
ASSETS_DIR  = "assets"
CSV_DIR     = "../Datasets"

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(METRICS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# ================== CONFIG ==================
IMG_SIZE = (224, 224)
BATCH_SIZE = 16            # CPU safe
EPOCHS_PHASE1 = 10
EPOCHS_PHASE2 = 15
SEED = 42

# ================== LOAD CSVs ==================
train_df = pd.read_csv(f"{CSV_DIR}/train_mri.csv")
val_df   = pd.read_csv(f"{CSV_DIR}/val_mri.csv")

class_names = sorted(train_df["label"].unique())
NUM_CLASSES = len(class_names)

# ================== DATA GENERATORS ==================
train_gen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

val_gen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

train_data = train_gen.flow_from_dataframe(
    train_df,
    x_col="filepath",
    y_col="label",
    target_size=IMG_SIZE,
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=SEED
)

val_data = val_gen.flow_from_dataframe(
    val_df,
    x_col="filepath",
    y_col="label",
    target_size=IMG_SIZE,
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    shuffle=False
)

# ================== SAVE CLASS INDICES ==================
with open(f"{ASSETS_DIR}/effnet_class_indices.json", "w") as f:
    json.dump(train_data.class_indices, f, indent=4)

# ================== CLASS WEIGHTS ==================
y_train = train_df["label"].map(train_data.class_indices).values

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(y_train),
    y=y_train
)

class_weights = {i: float(w) for i, w in enumerate(class_weights)}

# Save for reference (JSON only, not for training reuse)
with open(f"{ASSETS_DIR}/effnet_class_weights.json", "w") as f:
    json.dump({str(k): v for k, v in class_weights.items()}, f, indent=4)

# ================== MODEL ==================
base_model = EfficientNetB0(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

base_model.trainable = False  # Phase 1

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation="relu")(x)
x = Dropout(0.4)(x)
output = Dense(NUM_CLASSES, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-3),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ================== SAVE MODEL SUMMARY ==================
with open(f"{ASSETS_DIR}/effnet_model_summary.txt", "w", encoding="utf-8") as f:
    model.summary(print_fn=lambda x: f.write(x + "\n"))


# ================== CALLBACKS ==================
callbacks = [
    ModelCheckpoint(
        f"{MODEL_DIR}/mri_effnet_best.h5",
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1
    ),
    EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    ),
    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.3,
        patience=3,
        min_lr=1e-6
    )
]

steps_per_epoch = train_data.samples // BATCH_SIZE
val_steps = val_data.samples // BATCH_SIZE

# ================== TRAIN PHASE 1 ==================
model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_PHASE1,
    steps_per_epoch=steps_per_epoch,
    validation_steps=val_steps,
    class_weight=class_weights,
    callbacks=callbacks
)

# ================== FINE TUNING (PHASE 2) ==================
base_model.trainable = True

for layer in base_model.layers[:-40]:  # safe unfreeze depth
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-4),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_PHASE2,
    steps_per_epoch=steps_per_epoch,
    validation_steps=val_steps,
    class_weight=class_weights,
    callbacks=callbacks
)

print("\n EfficientNet MRI training completed successfully")
print("Best model saved at: models/mri_effnet_best.h5")
