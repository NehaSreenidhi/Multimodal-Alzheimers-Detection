import numpy as np

CLASS_NAMES = [
    "MildDemented",
    "ModerateDemented",
    "NonDemented",
    "VeryMildDemented"
]


def soft_late_fusion(mri_probs, clinical_prob, alpha=0.5):
    """
    Hierarchical Soft Late Fusion

    MRI model: 4-class probability vector
    Clinical model: Binary probability P(Dementia)

    Strategy:
    - Clinical model controls dementia vs non-dementia belief
    - MRI model controls stage distribution
    """

    mri_probs = np.array(mri_probs, dtype=float)

    p_dementia = float(clinical_prob)
    p_non_demented = 1.0 - p_dementia

    fused = np.copy(mri_probs)

    # ===============================
    # 1️⃣ Adjust NonDemented class
    # ===============================
    NON_INDEX = 2

    fused[NON_INDEX] = (
        alpha * mri_probs[NON_INDEX] +
        (1 - alpha) * p_non_demented
    )

    # ===============================
    # 2️⃣ Redistribute dementia belief
    # ===============================
    dementia_indices = [0, 1, 3]
    dementia_sum = mri_probs[dementia_indices].sum()

    if dementia_sum > 0:
        for i in dementia_indices:
            # Preserve MRI stage proportions
            stage_ratio = mri_probs[i] / dementia_sum

            fused[i] = (
                alpha * mri_probs[i] +
                (1 - alpha) * p_dementia * stage_ratio
            )
    else:
        # Edge case: MRI predicts 100% NonDemented
        # In this case distribute dementia evenly
        equal_share = p_dementia / len(dementia_indices)
        for i in dementia_indices:
            fused[i] = equal_share

    # ===============================
    # 3️⃣ Normalize for safety
    # ===============================
    fused = np.clip(fused, 1e-6, None)
    fused = fused / fused.sum()

    # ===============================
    # 4️⃣ Final prediction
    # ===============================
    idx = int(np.argmax(fused))

    return {
        "fused_probabilities": fused.tolist(),
        "predicted_class": CLASS_NAMES[idx],
        "confidence": float(fused[idx]),
        "mri_probabilities": mri_probs.tolist(),
        "clinical_probability": p_dementia
    }