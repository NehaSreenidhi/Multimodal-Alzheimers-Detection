import numpy as np

CLASS_NAMES = [
    "MildDemented",
    "ModerateDemented",
    "NonDemented",
    "VeryMildDemented"
]


def binary_to_4class(p_dementia):
    p_non_demented = 1.0 - p_dementia
    p_stage = p_dementia / 3.0

    return np.array([
        p_stage,
        p_stage,
        p_non_demented,
        p_stage
    ])


def soft_late_fusion(mri_probs, clinical_prob, alpha=0.5):
    clinical_4 = binary_to_4class(clinical_prob)

    fused = alpha * mri_probs + (1 - alpha) * clinical_4
    fused = np.clip(fused, 1e-6, None)
    fused /= fused.sum()

    idx = int(np.argmax(fused))

    return {
        "fused_probabilities": fused.tolist(),
        "predicted_class": CLASS_NAMES[idx],
        "confidence": float(np.max(fused))
    }