from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from services.mri_service import predict_mri
from services.clinical_service import predict_clinical
from services.fusion_service import soft_late_fusion

app = Flask(__name__)
CORS(app)  # Allow React to call backend


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get MRI file
        mri_file = request.files.get("mri")
        if not mri_file:
            return jsonify({"error": "MRI file missing"}), 400

        # Get clinical data
        clinical_json = request.form.get("data")
        if not clinical_json:
            return jsonify({"error": "Clinical data missing"}), 400

        clinical_data = json.loads(clinical_json)

        # Run models
        mri_probs = predict_mri(mri_file)
        clinical_prob = predict_clinical(clinical_data)

        # Fuse
        result = soft_late_fusion(mri_probs, clinical_prob)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)