import { useState } from "react";
import uploadIcon from "../assets/upload.svg";
import arrowRight from "../assets/arrow-right.svg";
import "../styles/new_diagnosis.css";
import { predictDiagnosis } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function NewDiagnosis() {
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [mriFile, setMriFile] = useState(null);
  const [preview, setPreview] = useState(null);

  // clinical data state
  const [formData, setFormData] = useState({
    MMSE: 26,
    FunctionalAssessment: 80,
    ADL: 85,
    MemoryComplaints: "No",
    BehavioralProblems: "No",
    SleepQuality: 3,
    BMI: 23,
    CholesterolHDL: 55,
    CholesterolLDL: 120,
  });

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setMriFile(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleChange = (key, value) => {
    setFormData({ ...formData, [key]: value });
  };

  // ✅ ACTUAL SUBMIT
  const handleSubmit = async () => {
    try {
      const payload = new FormData();
      payload.append("mri", mriFile);
      payload.append("data", JSON.stringify(formData));

      const result = await predictDiagnosis(payload);

      console.log("Result:", result);
      // alert(result.predicted_class);
      // Redirect to DiagnosisResult page with prediction
      navigate("/diagnosis_result", {
        state: { prediction: result.predicted_class },
      });

    } catch (error) {
      alert("Prediction failed");
    }
  };

  return (
    <div className="diagnosis-container">
      {/* PROGRESS */}
      <div className="progress-wrapper">
        <div className="progress-header">
          <span>Step {step} of 2</span>
          <span>{step === 1 ? "MRI Upload" : "Clinical Data"}</span>
        </div>

        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: step === 1 ? "50%" : "100%" }}
          />
        </div>
      </div>

      {/* STEP 1 */}
      {step === 1 && (
        <div className="card">
          <h3>Upload Brain MRI</h3>

          <label className="upload-box">
            {preview ? (
              <img src={preview} alt="MRI Preview" className="mri-preview" />
            ) : (
              <>
                <img src={uploadIcon} alt="upload" />
                <p>Click to upload MRI</p>
              </>
            )}

            <input type="file" hidden accept="image/*" onChange={handleFileUpload} />
          </label>

          <button
            className={`continue-btn ${mriFile ? "active" : ""}`}
            disabled={!mriFile}
            onClick={() => setStep(2)}
          >
            Continue
            <img src={arrowRight} alt="arrow" className="continue-icon" />
          </button>
        </div>
      )}

      {/* STEP 2 */}
      {step === 2 && (
        <div className="card">
          <h3>Cognitive Assessment</h3>
          <div className="grid">
            <Input label="MMSE (0–30)" value={formData.MMSE} onChange={(v) => handleChange("MMSE", v)} />
            <Input label="Functional Assessment (0–100)" value={formData.FunctionalAssessment} onChange={(v) => handleChange("FunctionalAssessment", v)} />
            <Input label="ADL (0–100)" value={formData.ADL} onChange={(v) => handleChange("ADL", v)} />
          </div>

          <h3>Symptoms & Behavior</h3>
          <div className="grid">
            <Select label="Memory Complaints" value={formData.MemoryComplaints} onChange={(v) => handleChange("MemoryComplaints", v)} />
            <Select label="Behavioral Problems" value={formData.BehavioralProblems} onChange={(v) => handleChange("BehavioralProblems", v)} />
            <Input label="Sleep Quality (1–5)" value={formData.SleepQuality} onChange={(v) => handleChange("SleepQuality", v)} />
          </div>

          <h3>Metabolic & Clinical Factors</h3>
          <div className="grid">
            <Input label="BMI" value={formData.BMI} onChange={(v) => handleChange("BMI", v)} />
            <Input label="Cholesterol HDL (mg/dL)" value={formData.CholesterolHDL} onChange={(v) => handleChange("CholesterolHDL", v)} />
            <Input label="Cholesterol LDL (mg/dL)" value={formData.CholesterolLDL} onChange={(v) => handleChange("CholesterolLDL", v)} />
          </div>

          <div className="footer-buttons">
            <button className="back-btn" onClick={() => setStep(1)}>Back</button>
            <button className="generate-btn" onClick={handleSubmit}>
              Generate Diagnosis
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/* REUSABLE COMPONENTS */

function Input({ label, value, onChange }) {
  return (
    <div className="field">
      <label>{label}</label>
      <input type="number" value={value} onChange={(e) => onChange(e.target.value)} />
    </div>
  );
}

function Select({ label, value, onChange }) {
  return (
    <div className="field">
      <label>{label}</label>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        <option>No</option>
        <option>Yes</option>
      </select>
    </div>
  );
}

