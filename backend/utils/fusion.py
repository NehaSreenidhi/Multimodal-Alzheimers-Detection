# fusion.py
import numpy as np

CLASS_NAMES = [
    "MildDemented",      # index 0
    "ModerateDemented",  # index 1
    "NonDemented",       # index 2
    "VeryMildDemented"   # index 3
]


def binary_to_4class(p_dementia):
    p_non_demented = 1.0 - p_dementia
    p_stage = p_dementia / 3.0
    
    return np.array([
        p_stage,          # MildDemented (0)
        p_stage,          # ModerateDemented (1)
        p_non_demented,   # NonDemented (2)
        p_stage           # VeryMildDemented (3)
    ])

def soft_late_fusion(mri_probs, clinical_prob, alpha=0.5):
    clinical_4 = binary_to_4class(clinical_prob)

    fused = alpha * mri_probs + (1.0 - alpha) * clinical_4
    fused = np.clip(fused, 1e-6, None)
    fused /= fused.sum()

    return fused
