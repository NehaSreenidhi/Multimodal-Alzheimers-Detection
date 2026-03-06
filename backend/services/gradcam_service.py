import numpy as np
import tensorflow as tf
import cv2
import io
import base64
from PIL import Image

# ================= CONFIG =================
LAST_CONV_LAYER = "top_conv"  # EfficientNetB0 last conv layer

# ================= HELPERS =================
def array_to_base64(img_array):
    """Convert numpy array image to base64 string"""
    img_pil = Image.fromarray(np.uint8(img_array))
    buffer = io.BytesIO()
    img_pil.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def make_gradcam_heatmap(img_batch, model, last_conv_layer_name, pred_index=None):
    """Generate Grad-CAM heatmap using GradientTape"""
    # Use model.inputs (plural) for better compatibility with Keras functional models
    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model({"input_layer": img_batch})
        if pred_index is None:
            pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]

    # Calculate gradients of the predicted class with respect to the last conv layer
    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # Weight the channels of the feature map by the gradient importance
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # ReLU and Normalize
    heatmap = tf.maximum(heatmap, 0)
    heatmap /= (tf.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy()

def overlay_gradcam(original_img, heatmap, alpha=0.4):
    """Overlay Grad-CAM heatmap on original image"""
    heatmap = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # Ensure original_img is uint8 for OpenCV overlay
    if original_img.dtype != np.uint8:
        original_img = np.uint8(original_img)
        
    overlay = cv2.addWeighted(original_img, 1 - alpha, heatmap, alpha, 0)
    return overlay

# ================= MAIN FUNCTION =================
def generate_gradcam(img_batch, mri_model, pred_index):
    """
    img_batch: The preprocessed numpy array (1, 224, 224, 3) from mri_service
    mri_model: The shared model instance loaded in app.py or mri_service
    pred_index: The class index determined in app.py
    """
    # 1. Generate Heatmap
    heatmap = make_gradcam_heatmap(img_batch, mri_model, LAST_CONV_LAYER, pred_index)

    # 2. Reconstruct original image for display (undoing preprocessing scaling)
    # We normalize to 0-255 range for the base64 conversion
    img_to_show = img_batch[0]
    low, high = img_to_show.min(), img_to_show.max()
    display_img = ((img_to_show - low) * (255 / (high - low + 1e-8))).astype(np.uint8)

    # 3. Generate Overlay
    overlay = overlay_gradcam(original_img=display_img, heatmap=heatmap)

    # 4. Convert to base64 using keys expected by DiagnosisResult.jsx
    return {
        "original_image_url": f"data:image/png;base64,{array_to_base64(display_img)}",
        "heatmap_url": f"data:image/png;base64,{array_to_base64(overlay)}"
    }