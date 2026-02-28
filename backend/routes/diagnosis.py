from flask import Blueprint, request, jsonify
from services.ml_service import predict

diagnosis_bp = Blueprint("diagnosis", __name__)

@diagnosis_bp.route("/predict", methods=["GET","POST"])
def predict_diagnosis():
    data = request.json
    result = predict(data)
    return jsonify(result)