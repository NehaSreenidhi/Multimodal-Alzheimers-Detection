import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

const DiagnosisResult = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Get prediction result passed via state
  const { prediction } = location.state || { prediction: "No result found" };

  return (
    <div className="diagnosis-result-page p-4">
      <h1 className="text-2xl font-bold mb-4">Diagnosis Result</h1>
      <div className="result-box border p-4 rounded shadow">
        <p className="text-lg">
          Prediction: <strong>{prediction}</strong>
        </p>
      </div>
      <button
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
        onClick={() => navigate(-1)}
      >
        Go Back
      </button>
    </div>
  );
};

export default DiagnosisResult;