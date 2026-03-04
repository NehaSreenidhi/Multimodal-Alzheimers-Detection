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

@app.route("/report", methods=["POST"])
def generate_report():
    data = request.get_json()

    patient_info = data.get("patient_info", {})
    model_results = data.get("model_results", {})
    clinical_inputs = data.get("clinical_inputs", {})

    # -------------------------
    # Patient Info
    # -------------------------
    patient_name = patient_info.get("patient_name", "N/A")
    age = patient_info.get("age", "N/A")
    gender = patient_info.get("gender", "N/A")
    mobile_number = patient_info.get("mobile_number", "N/A")
    clinical_history = patient_info.get("clinical_history", "Not Provided")

    # -------------------------
    # Model Results
    # -------------------------
    predicted_class = model_results.get("predicted_class", "Unknown")
    confidence = round(model_results.get("confidence", 0) * 100, 2)

    fused_probs = model_results.get("fused_probabilities", [])
    mri_probs = model_results.get("mri_probabilities", [])
    clinical_prob = model_results.get("clinical_probability", 0)

    # -------------------------
    # Explainability
    # -------------------------
    gradcam = model_results.get("gradcam", {})
    shap_plot = model_results.get("shap_plot", "")

    original_img = gradcam.get("original_image_url", "")
    heatmap_img = gradcam.get("heatmap_url", "")

    from datetime import datetime
    report_date = datetime.now().strftime("%d %B %Y")

    # -------------------------
    # HTML REPORT
    # -------------------------
    html_content = f"""
    <div style="font-family: Arial; padding: 40px; max-width: 900px; margin:auto;">

        <h1 style="text-align:center;">AI-Based Alzheimer’s Diagnostic Report</h1>
        <p style="text-align:center;"><strong>Date:</strong> {report_date}</p>
        <hr/>

        <h2>1. Patient Information</h2>
        <p><strong>Name:</strong> {patient_name}</p>
        <p><strong>Age:</strong> {age}</p>
        <p><strong>Gender:</strong> {gender}</p>
        <p><strong>Mobile:</strong> {mobile_number}</p>

        <hr/>

        <h2>2. Clinical Inputs</h2>
        <ul>
            {''.join([f"<li><strong>{k}:</strong> {v}</li>" for k, v in clinical_inputs.items()])}
        </ul>

        <hr/>

        <h2>3. Model Assessment</h2>
        <p><strong>Final Predicted Class:</strong> {predicted_class}</p>
        <p><strong>Confidence:</strong> {confidence}%</p>
        <p><strong>Clinical Probability:</strong> {round(clinical_prob * 100, 2)}%</p>

        <h3>Fused Probabilities</h3>
        <p>{fused_probs}</p>

        <h3>MRI Model Probabilities</h3>
        <p>{mri_probs}</p>

        <hr/>

        <h2>4. MRI Explainability (Grad-CAM)</h2>
        <div style="display:flex; gap:20px;">
            <div>
                <p><strong>Original MRI</strong></p>
                <img src="{original_img}" width="300"/>
            </div>
            <div>
                <p><strong>Grad-CAM Heatmap</strong></p>
                <img src="{heatmap_img}" width="300"/>
            </div>
        </div>

        <hr/>

        <h2>5. Clinical Feature Contribution (SHAP)</h2>
        <img src="{shap_plot}" width="500"/>

        <hr/>

        <h2>6. Conclusion</h2>
        <p>
        Based on multimodal fusion of MRI imaging and structured clinical data,
        the AI system predicts <strong>{predicted_class}</strong> with
        <strong>{confidence}% confidence</strong>.
        </p>

        <p style="margin-top:40px; font-size:12px;">
        Disclaimer: This AI-generated report is intended for academic and research purposes only.
        It does not replace professional medical diagnosis.
        </p>

    </div>
    """

    return jsonify({"html_content": html_content})

if __name__ == '__main__':
    app.run(debug=True)