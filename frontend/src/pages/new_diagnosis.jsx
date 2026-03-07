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
  const [loading, setLoading] = useState(false);

  // clinical data state
  const [formData, setFormData] = useState({
    MMSE: 26,
    FunctionalAssessment: 8,
    ADL: 8,
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

  const validTypes = ["image/png", "image/jpeg", "image/jpg"];

  if (!validTypes.includes(file.type)) {
    alert("Invalid file format. Please upload MRI images in PNG or JPG format.");
    return;
  }

  setMriFile(file);
  setPreview(URL.createObjectURL(file));
};

  const handleChange = (key, value) => {
    setFormData({ ...formData, [key]: value });
  };
  const validateClinicalInputs = () => {

  if (formData.MMSE < 0 || formData.MMSE > 30) {
    alert("MMSE must be between 0 and 30");
    return false;
  }

  if (formData.SleepQuality < 1 || formData.SleepQuality > 5) {
    alert("Sleep Quality must be between 1 and 5");
    return false;
  }

  if (formData.FunctionalAssessment < 0 || formData.FunctionalAssessment > 10) {
    alert("Functional Assessment must be between 0 and 10");
    return false;
  }

  if (formData.ADL < 0 || formData.ADL > 10) {
    alert("ADL must be between 0 and 10");
    return false;
  }

  return true;
};

  // ✅ ACTUAL SUBMIT
  const handleSubmit = async () => {

  if (!validateClinicalInputs()) return;

  try {
    setLoading(true);

    const normalizedData = {
      ...formData,
      FunctionalAssessment: formData.FunctionalAssessment / 10,
      ADL: formData.ADL / 10
    };

    const payload = new FormData();
    payload.append("mri", mriFile);
    payload.append("data", JSON.stringify(normalizedData));

    const result = await predictDiagnosis(payload);

    navigate("/diagnosis_result", {
      state: {
        prediction: result,
        clinicalInputs: formData
      }
    });

  } catch (error) {
    console.error("Prediction failed", error);
    setLoading(false);
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

            <input
  type="file"
  hidden
  accept=".png,.jpg,.jpeg"
  onChange={handleFileUpload}
/>
          </label>
        <div className="step-actions">
  <button
    className="secondary-btn"
    onClick={() => navigate("/")}
  >
    Back
  </button>

  <button
    className={`continue-btn ${mriFile ? "active" : ""}`}
    disabled={!mriFile}
    onClick={() => setStep(2)}
  >
    Continue
    <img src={arrowRight} alt="arrow" className="continue-icon" />
  </button>
</div>
        </div>
      )}

      {/* STEP 2 */}
      {step === 2 && (
        <div className="card">
          <h3>Cognitive Assessment</h3>
          <div className="grid">
            <Input label="MMSE (0–30)" value={formData.MMSE} onChange={(v) => handleChange("MMSE", v)} />
            <Input label="Functional Assessment (0–10)" value={formData.FunctionalAssessment} onChange={(v) => handleChange("FunctionalAssessment", v)} />
            <Input label="ADL (0–10)" value={formData.ADL} onChange={(v) => handleChange("ADL", v)} />
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
            <button className="generate-btn" onClick={handleSubmit} disabled={loading}>
  {loading ? <span className="spinner" /> : "Generate Diagnosis"}
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

