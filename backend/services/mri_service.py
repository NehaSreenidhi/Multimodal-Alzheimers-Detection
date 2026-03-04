import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.models import load_model

IMG_SIZE = (224, 224)

model = load_model("models/mri_effnet_best.h5", compile=False)


def preprocess_image(file):
    image = Image.open(file).convert("RGB")
    image = image.resize(IMG_SIZE)
    image = np.array(image)

    # SAME preprocessing as training
    image = preprocess_input(image)

    image = np.expand_dims(image, axis=0)
    return image


def predict_mri(file):
    image = preprocess_image(file)
    preds = model.predict({"input_layer": image})[0]   # shape (4,)
    return preds