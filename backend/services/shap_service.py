# utils/shap.py
import shap
import numpy as np

def compute_shap_values(
    model,
    X_background,
    X_sample,
    feature_names
):
    """
    SHAP explanation for clinical ML model

    Args:
        model: trained sklearn model
        X_background: np.ndarray (background dataset)
        X_sample: np.ndarray (single sample or batch)
        feature_names: list of feature names

    Returns:
        shap_values, explainer
    """

    explainer = shap.Explainer(
        model,
        X_background,
        feature_names=feature_names
    )

    shap_values = explainer(X_sample)

    return shap_values, explainer
