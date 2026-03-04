import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/GenerateReport.css";

export default function GenerateReport() {
  const location = useLocation();
  const navigate = useNavigate();

  const { prediction, clinicalInputs } = location.state || {};

  const [formData, setFormData] = React.useState({
    patient_name: "",
    age: "",
    gender: "",
    clinical_history: ""
  });

  const [reportHtml, setReportHtml] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  if (!prediction || !clinicalInputs) {
    return (
      <div className="report-page">
        <div className="report-card">
          <h2>No data available</h2>
          <button onClick={() => navigate("/")}>
            Go Home
          </button>
        </div>
      </div>
    );
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleGenerate = async () => {
    setLoading(true);

    const response = await fetch("http://localhost:5000/report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        patient_info: formData,
        model_results: prediction,
        clinical_inputs: clinicalInputs
      })
    });

    const data = await response.json();
    setReportHtml(data.html_content);
    setLoading(false);
  };

  return (
    <div className="report-page">
      <div className="report-card">

        <h1>Generate AI Diagnostic Report</h1>

        {/* Form Section */}
        {!reportHtml && (
          <div className="report-form">
            <input
              type="text"
              name="patient_name"
              placeholder="Patient Name"
              onChange={handleChange}
            />

            <input
              type="number"
              name="age"
              placeholder="Age"
              onChange={handleChange}
            />

            <select
              name="gender"
              onChange={handleChange}
            >
              <option value="">Select Gender</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>

            <textarea
              name="clinical_history"
              placeholder="Brief Clinical History (Optional but Recommended)"
              rows={4}
              onChange={handleChange}
            />

            <button
              className="primary-btn"
              onClick={handleGenerate}
              disabled={loading}
            >
              {loading ? "Generating Report..." : "Generate Report Preview"}
            </button>
          </div>
        )}

        {/* Preview Section */}
        {reportHtml && (
          <div className="report-preview">
            <div
              dangerouslySetInnerHTML={{ __html: reportHtml }}
            />

            <button className="primary-btn">
              Download PDF
            </button>
          </div>
        )}

      </div>
    </div>
  );
}