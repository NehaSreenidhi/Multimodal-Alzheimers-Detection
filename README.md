# A multimodal learning framework for early Alzheimer’s disease detection using MRI images and clinical data.

## Tech Stack
- React (Vite) – Frontend
- Python (Flask) – Backend 
- Machine Learning & Deep Learning for Clinical Data & MRI Imaging
- Explainable AI

## System Overview
The system analyzes two sources of patient information:

1. **MRI Brain Images**
   - CNN model predicts dementia stage from MRI scans.
   - Classes:
     - NonDemented
     - VeryMildDemented
     - MildDemented
     - ModerateDemented

2. **Clinical Data**
   - Structured medical parameters (age, cognitive scores, etc.)
   - Machine learning model predicts dementia probability.

3. **Multimodal Fusion**
   - A hierarchical **soft late fusion strategy** combines MRI and clinical predictions to improve diagnostic reliability.

---

### Explainability Features
To improve transparency and trust in predictions:

- **Grad-CAM**
  - Highlights important brain regions influencing the MRI model decision.

- **SHAP Waterfall Plot**
  - Shows how each clinical feature contributes to the final prediction.

---

## Project Structure
- frontend/ – React UI
- backend/ – Flask API endpoints,
           - models/ – ML/DL models,
           - fusion algorithm

---

## Workflow

1. User uploads MRI scan and enters clinical information.
2. MRI image is processed by the CNN model.
3. Clinical features are processed by the ML model.
4. Predictions are combined using the multimodal fusion algorithm.
5. Explainability modules generate:
   - Grad-CAM heatmap
   - SHAP plot
6. A medical-style interpretation report can be generated and downloaded further.

---

