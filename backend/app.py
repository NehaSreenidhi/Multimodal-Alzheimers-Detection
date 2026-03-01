from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
import pandas as pd

# Import your services
from services.mri_service import model as mri_model, preprocess_image
from services.clinical_service import predict_clinical, model as clinical_model
from services.fusion_service import soft_late_fusion
from services.gradcam_service import generate_gradcam
from services.shap_service import get_shap_waterfall_plot

app = Flask(__name__)
CORS(app)

CLINICAL_FEATURES = [
    "MMSE", "FunctionalAssessment", "ADL", 
    "MemoryComplaints", "BehavioralProblems", 
    "SleepQuality", "BMI", "CholesterolHDL", "CholesterolLDL"
]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Get Data
        mri_file = request.files['mri']
        clinical_data = json.loads(request.form['data'])

        # 2. MRI Prediction
        # We preprocess here so we have the array for both prediction and Grad-CAM
        img_batch = preprocess_image(mri_file) 
        mri_preds = mri_model.predict(img_batch)[0]
        mri_pred_index = int(np.argmax(mri_preds))

        # 3. Clinical Prediction
        clinical_prob = predict_clinical(clinical_data)

        # 4. Multimodal Fusion
        fusion_result = soft_late_fusion(mri_preds, clinical_prob)

        # 5. Generate Grad-CAM (Passing the already loaded mri_model)
        # Pass the preprocessed batch and the shared model instance
        gradcam_data = generate_gradcam(img_batch, mri_model, mri_pred_index)

        raw_values = [
            float(clinical_data["MMSE"]),
            float(clinical_data["FunctionalAssessment"]),
            float(clinical_data["ADL"]),
            1 if clinical_data["MemoryComplaints"] == "Yes" else 0,
            1 if clinical_data["BehavioralProblems"] == "Yes" else 0,
            float(clinical_data["SleepQuality"]),
            float(clinical_data["BMI"]),
            float(clinical_data["CholesterolHDL"]),
            float(clinical_data["CholesterolLDL"]),
        ]
        # Ensure column order matches FEATURE_NAMES from clinical_service
        input_df = pd.DataFrame([raw_values], columns=CLINICAL_FEATURES)
        shap_plot_url = get_shap_waterfall_plot(clinical_model, input_df)

        # 6. Combine Results
        # Your React UI expects the 'gradcam' key inside the response
        response = {
            **fusion_result,
            "gradcam": gradcam_data,
            "shap_plot": shap_plot_url
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)