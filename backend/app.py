from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
import pandas as pd
import joblib

# Import your services
from services.mri_service import model as mri_model, preprocess_image
from services.clinical_service import predict_clinical, model as clinical_model
from services.fusion_service import soft_late_fusion
from services.gradcam_service import generate_gradcam
from services.shap_service import get_shap_waterfall_plot

app = Flask(__name__)
CORS(app)

MODEL_FEATURES = [
    "MMSE", "FunctionalAssessment", "ADL", 
    "MemoryComplaints", "BehavioralProblems",
    "SleepQuality", "Age",
    "CholesterolHDL", "CholesterolLDL", 
    "FamilyHistoryAlzheimers"
]

CLASS_NAMES = [
    "MildDemented",
    "ModerateDemented",
    "NonDemented",
    "VeryMildDemented",
]
clinical_scaler = joblib.load("models/clinical_scaler.pkl")

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

        input_dict = {
            "MMSE": float(clinical_data["MMSE"]),
            "FunctionalAssessment": float(clinical_data["FunctionalAssessment"]),
            "ADL": float(clinical_data["ADL"]),
            "MemoryComplaints": 1 if clinical_data["MemoryComplaints"] == "Yes" else 0,
            "BehavioralProblems": 1 if clinical_data["BehavioralProblems"] == "Yes" else 0,
            "SleepQuality": float(clinical_data["SleepQuality"]),
            "Age": int(clinical_data["Age"]),
            "CholesterolHDL": float(clinical_data["CholesterolHDL"]),
            "CholesterolLDL": float(clinical_data["CholesterolLDL"]),
            "FamilyHistoryAlzheimers": 1 if clinical_data["FamilyHistoryAlzheimers"] == "Yes" else 0
        }
        # Create dataframe using UI order
        input_df = pd.DataFrame([input_dict])

        # Reorder columns to match training order
        input_df = input_df[MODEL_FEATURES]
        scaled_values = clinical_scaler.transform(input_df)

        scaled_df = pd.DataFrame(scaled_values, columns=MODEL_FEATURES)
            
        shap_plot_url = get_shap_waterfall_plot(clinical_model, scaled_df)

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

   
    # Patient Info
    patient_name = patient_info.get("patient_name", "N/A")
    Age=clinical_inputs.get("Age","N/A")
    gender = patient_info.get("gender", "N/A")
    mobile_number = patient_info.get("mobile_number", "N/A")

    # Model Results
    predicted_class = model_results.get("predicted_class", "Unknown")
    confidence = round(model_results.get("confidence", 0) * 100, 2)

    fused_probs = model_results.get("fused_probabilities", [])
    mri_probs = model_results.get("mri_probabilities", [])
    clinical_prob = model_results.get("clinical_probability", 0)

    mri_prob_dict = {
        CLASS_NAMES[i]: round(float(mri_probs[i]) * 100, 2)
        for i in range(len(CLASS_NAMES))
    }

    fused_prob_dict = {
        CLASS_NAMES[i]: round(float(fused_probs[i]) * 100, 2)
        for i in range(len(CLASS_NAMES))
    }

    # Explainability
    gradcam = model_results.get("gradcam", {})
    shap_plot = model_results.get("shap_plot", "")

    original_img = gradcam.get("original_image_url", "")
    heatmap_img = gradcam.get("heatmap_url", "")

    from datetime import datetime
    report_date = datetime.now().strftime("%d %B %Y")

    # HTML REPORT

    html_content = f"""
<div style="font-family: 'Segoe UI', Arial; max-width:900px; margin:auto; padding:40px; background:white; color:#333;">

<!-- HEADER -->
<div style="text-align:center; margin-bottom:30px;">
    <h1 style="color:#2c3e50; margin-bottom:5px;">
        Alzheimer's Diagnostic Report
    </h1>
    <p style="font-size:14px; color:#666;">
        Multimodal AI System
    </p>
    <p style="font-size:13px;">
        <strong>Date:</strong> {report_date}
    </p>
</div>

<hr style="border:none; height:1px; background:#e5e7eb;"/>

<!-- PATIENT INFO -->
<h2 style="color:#1f3c88;">Patient Information</h2>

<div style="display:grid; grid-template-columns:repeat(2,1fr); gap:10px; margin-top:10px;">
    <div><strong>Name:</strong> {patient_name}</div>
    <div><strong>Age:</strong> {Age}</div>
    <div><strong>Gender:</strong> {gender}</div>
    <div><strong>Mobile:</strong> {mobile_number}</div>
</div>

<hr style="margin-top:25px; border:none; height:1px; background:#e5e7eb;"/>

<!-- CLINICAL INPUTS -->
<h2 style="color:#1f3c88;">Clinical Features</h2>

<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-top:15px;">

{''.join([
    f'''
    <div style="background:#f8fafc; padding:10px; border-radius:6px;">
        <div style="font-size:12px; color:#666;">{k}</div>
        <div style="font-weight:600; color:#1f2937;">{v}</div>
    </div>
    '''
    for k, v in clinical_inputs.items()
])}

</div>

<hr style="margin-top:25px; border:none; height:1px; background:#e5e7eb;"/>

<!-- DIAGNOSIS -->
<h2 style="color:#1f3c88;">Diagnosis</h2>

<div style="margin-top:10px;">
    <p><strong>Final Prediction:</strong> {predicted_class}</p>
    <p><strong>Confidence:</strong> {confidence}%</p>
    <p><strong>Clinical Probability:</strong> {round(clinical_prob * 100, 2)}%</p>
</div>

<!-- PROBABILITIES -->
<div style="margin-top:20px;">

<h3 style="margin-bottom:10px;">MRI Probabilities</h3>

<table style="width:100%; border-collapse:collapse; margin-bottom:20px;">
    <tr style="background:#f3f4f6;">
        <th style="padding:10px; border:1px solid #d1d5db;">Class</th>
        <th style="padding:10px; border:1px solid #d1d5db;">Probability (%)</th>
    </tr>

    {''.join([
        f"<tr><td style='padding:10px; border:1px solid #d1d5db;'>{k}</td>"
        f"<td style='padding:10px; border:1px solid #d1d5db;'>{v}%</td></tr>"
        for k,v in mri_prob_dict.items()
    ])}
</table>


<h3 style="margin-bottom:10px;">Fused Multimodal Probabilities</h3>

<table style="width:100%; border-collapse:collapse;">
    <tr style="background:#f3f4f6;">
        <th style="padding:10px; border:1px solid #d1d5db;">Class</th>
        <th style="padding:10px; border:1px solid #d1d5db;">Probability (%)</th>
    </tr>

    {''.join([
        f"<tr><td style='padding:10px; border:1px solid #d1d5db;'>{k}</td>"
        f"<td style='padding:10px; border:1px solid #d1d5db;'>{v}%</td></tr>"
        for k,v in fused_prob_dict.items()
    ])}
</table>

</div>
<!-- MRI IMAGES -->
<h2 style="color:#1f3c88;">MRI Explainability</h2>

<div style="display:flex; justify-content:center; gap:40px; margin-top:15px;">
    <div style="text-align:center;">
        <p><strong>Original</strong></p>
        <img src="{original_img}" style="width:250px; border-radius:6px;"/>
    </div>

    <div style="text-align:center;">
        <p><strong>Grad-CAM</strong></p>
        <img src="{heatmap_img}" style="width:250px; border-radius:6px;"/>
    </div>
</div>

<hr style="margin-top:25px; border:none; height:1px; background:#e5e7eb;"/>

<!-- SHAP -->
<h2 style="color:#1f3c88;">Feature Contribution</h2>

<div style="text-align:center;">
    <img src="{shap_plot}" style="width:450px; border-radius:6px;"/>
</div>

<hr style="margin-top:25px; border:none; height:1px; background:#e5e7eb;"/>

<!-- CONCLUSION -->
<h2 style="color:#1f3c88;">Conclusion</h2>

<p style="line-height:1.6;">
The system predicts <strong>{predicted_class}</strong> with confidence
<strong>{confidence}%</strong> based on multimodal analysis.
</p>

</div>
"""

    return jsonify({"html_content": html_content})

if __name__ == '__main__':
    app.run(debug=True)