import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/DiagnosisResult.css";
import {
  ShieldCheck,
  AlertCircle,
  TrendingUp,
  Brain,
} from "lucide-react";

/* ================= UI MAP ================= */
const CLASS_UI = {

  NonDemented: {
    label: "Non-Demented",
    description:
      "Multimodal indicators show no significant brain atrophy or cognitive deficits consistent with neurodegeneration.",
    color: "#16a34a",
    icon: ShieldCheck,
  },

  VeryMildDemented: {
    label: "Very Mild Demented",
    description:
      "Subtle structural changes and minor clinical variances suggest the onset of early-stage cognitive impairment.",
    color: "#f59e0b",
    icon: AlertCircle,
  },

  MildDemented: {
    label: "Mild Demented",
    description:
      "Identifiable patterns of cortical thinning and functional scores indicate a transition into mild dementia.",
    color: "#ea580c",
    icon: TrendingUp,
  },

  ModerateDemented: {
    label: "Moderate Demented",
    description:
      "Pronounced global atrophy and significant deficits in daily living activities confirm a moderate dementia profile.",
    color: "#dc2626",
    icon: Brain,
  },
};
export default function DiagnosisResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = React.useState("gradcam");
  

  /* ✅ SAFE READ */
  const prediction = location.state?.prediction;
  const clinicalInputs = location.state?.clinicalInputs;
  const patientDetails = location.state?.patientDetails;  

  if (!prediction || !clinicalInputs || !patientDetails) {
    return (
      <div className="result-page">
        <div className="result-card">
          <h2>No diagnosis data received</h2>
          <button className="primary-btn" onClick={() => navigate(-1)}>
            Go Back
          </button>
        </div>
      </div>
    );
  }

  const {
    fused_probabilities,
    confidence,
    predicted_class,
    mri_probabilities,
    clinical_probability
  } = prediction;
  const ui = CLASS_UI[predicted_class];
  const Icon = ui.icon;

  // ================= BACKEND CLASS ORDER =================
  const CLASS_NAMES = [
    "MildDemented",
    "ModerateDemented",
    "NonDemented",
    "VeryMildDemented",
  ];

  if (!ui || !Array.isArray(fused_probabilities)) {
    return (
      <div className="result-page">
        <div className="result-card">
          <h2>Unsupported diagnosis</h2>
          <p>{predicted_class}</p>
        </div>
      </div>
    );
  }

  /* ================= DYNAMIC VALUES ================= */

  // Final probability & confidence
  const confidencePercent = Math.round(confidence * 100);
  const probabilityPercent = confidencePercent;
  // Predicted class index
  const predictedIndex = fused_probabilities.indexOf(confidence);

  // MRI confidence for predicted class
  const mriConfidencePercent = mri_probabilities
    ? Math.round(mri_probabilities[predictedIndex] * 100)
    : 0;

  // Clinical dementia probability (binary)
  const clinicalConfidencePercent = clinical_probability
  ? Math.round(clinical_probability * 100)
  : 0;

  const now = new Date().toLocaleString();

  return (
    <div className="result-page">
      <div className="result-card">

        {/* HEADER */}
        <div className="top-header">
          <div>
            <h1>Diagnosis Results</h1>
            <p className="date-text">Analysis completed on {now}</p>
          </div>

          <div className="top-actions">
            
          <button
            className="secondary-btn"
            onClick={() => navigate("/")}>
          Home </button>
          <button
            className="secondary-btn"
            onClick={() => navigate("/new_diagnosis")}>
          New Diagnosis </button>
            
          <button
            className="view-btn"
            onClick={() =>
              navigate("/generate_report", {
                state: {
                  prediction,
                  clinicalInputs, 
                  patientDetails
                }
              })
            }>
          View Report </button>
          </div>
        </div>
    
        

      {/* SUMMARY */}
      <div className="final-summary-card">
        <div
          className="summary-icon"
          style={{ backgroundColor: `${ui.color}20`, color: ui.color }}
        >
          <Icon size={28} strokeWidth={2.2} />
        </div>

        <div className="summary-text">
          <h3>{ui.label}</h3>
          <span className="summary-subtitle">{ui.subtitle}</span>
          <p>{ui.description}</p>
        </div>
      </div>

        {/* METRICS */}
        <div className="metrics-card">
          <div className="metrics-header">
            <div>
              <h2>Diagnosis Prediction</h2>
              <p>Multimodal fusion model result</p>
            </div>
            <span className="metrics-badge">{ui.label}</span>
          </div>

          <div className="metrics-grid">
            <Metric
              label="Final Prediction Probability"
              value={probabilityPercent}
              color={ui.color}
            />
          </div>
        </div>

        {/* ================= MRI & CLINICAL ANALYSIS ================= */}
<div className="analysis-grid">

  {/* MRI ANALYSIS */}
  <div className="analysis-card">
    <div className="analysis-header">
      <span className="analysis-icon">🧠</span>
      <div>
        <h3>MRI Analysis (CNN)</h3>
        <p>Deep learning image analysis results</p>
      </div>
    </div>

    {CLASS_NAMES.map((className, idx) => {
      const prob = mri_probabilities ? Math.round(mri_probabilities[idx] * 100) : 0;
      return (
        <div key={className}>
          <div className="analysis-metric">
            <span>{CLASS_UI[className].label} Probability</span>
            <strong>{prob}%</strong>
          </div>
          <div className="analysis-bar">
            <div
              className="analysis-fill dark"
              style={{ width: `${prob}%` }}
            />
          </div>
        </div>
      );
    })}
  </div>

  {/* CLINICAL ANALYSIS */}
  <div className="analysis-card">
    <div className="analysis-header">
      <span className="analysis-icon purple">📈</span>
      <div>
        <h3>Clinical Analysis (ML)</h3>
        <p>Machine learning clinical assessment</p>
      </div>
    </div>

    <div className="analysis-metric">
      <span>Dementia Probability</span>
      <strong>{clinicalConfidencePercent}%</strong>
    </div>

    <div className="analysis-bar">
      <div
        className="analysis-fill dark"
        style={{ width: `${clinicalConfidencePercent}%` }}
      />
    </div>

    <div className="analysis-metric">
      <span>No Dementia Probability</span>
      <strong>{100 - clinicalConfidencePercent}%</strong>
    </div>

    <div className="analysis-bar">
      <div
        className="analysis-fill dark"
        style={{ width: `${100 - clinicalConfidencePercent}%` }}
      />
    </div>
  </div>
</div>
{/* ================= EXPLAINABILITY ================= */}
<div className="explain-card">
  <div className="explain-header">
    <span className="explain-icon">🧠</span>
    <div>
      <h2>Explainability Analysis</h2>
      <p>Visual explanations for transparent AI decision-making</p>
    </div>
  </div>

  {/* TABS */}
  <div className="explain-tabs">
    <button
      className={activeTab === "gradcam" ? "active" : ""}
      onClick={() => setActiveTab("gradcam")}
    >
      Grad-CAM (MRI)
    </button>
    <button
      className={activeTab === "shap" ? "active" : ""}
      onClick={() => setActiveTab("shap")}
    >
      SHAP (Clinical)
    </button>
  </div>

  {/* ================= GRAD-CAM ================= */}
  {activeTab === "gradcam" && prediction.gradcam && (
    <>
      <p className="explain-text">
        Gradient-weighted Class Activation Mapping highlights regions
        of the MRI that influenced the CNN prediction.
      </p>

      <div className="gradcam-grid">
        <div className="gradcam-item">
          <h4>Original MRI Scan</h4>
          <img 
            className="gradcam-image" 
            src={prediction.gradcam.original_image_url} 
            alt="Original MRI" 
          />
          <p className="gradcam-label">Input brain MRI scan</p>
        </div>

        <div className="gradcam-item">
          <h4>Grad-CAM Heatmap</h4>
          <img 
            className="gradcam-image"
            src={prediction.gradcam.heatmap_url} 
            alt="GradCAM Heatmap"
          />
          <p className="gradcam-label">
            CNN attention regions overlaid on MRI
          </p>
        </div>
      </div>
      <div className="gradcam-legend">
        <p><strong>Key Findings:</strong></p>
        <ul>
          <li><span className="legend-red"/> High Attention (Red): Hippocampal region showing potential atrophy</li>
          <li><span className="legend-orange"/> Moderate Attention (Orange): Temporal lobe areas with structural changes</li>
          <li><span className="legend-yellow"/> Low Attention (Yellow): Cortical regions with mild changes</li>
          <li><span className="legend-blue"/> Minimal Attention (Blue): Areas with normal appearance</li>
        </ul>
      </div>
    </>
  )}

  {/* ================= SHAP ================= */}
  {activeTab === "shap" && prediction.shap_plot && (
    <>
      <p className="explain-text">
        The SHAP waterfall plot illustrates how each clinical feature contributed to 
        the final dementia probability.
      </p>

      <div className="shap-plot-container">
        <img 
          src={prediction.shap_plot} 
          alt="Clinical SHAP Waterfall Plot" 
          style={{ 
            width: '100%', 
            height: 'auto', 
            borderRadius: '8px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)' 
          }} 
        />
        <div className="gradcam-legend">
          <p><strong>How to read this plot:</strong></p>
          <ul>
            <li><span className="legend-red"/> <b>Red bars:</b> Factors that increased the risk of Alzheimer's.</li>
            <li><span className="legend-blue"/> <b>Blue bars:</b> Factors that decreased the risk of Alzheimer's.</li>
            <li><b>f(x):</b> The model's final prediction for this patient.</li>
          </ul>
        </div>
      </div>
    </>
    
  )}
  </div>
  
  
  {/* ================= PATIENT SUMMARY ================= */}
<div className="patient-summary-card">
  <h3 className="patient-title">Patient Information Summary</h3>
  <p className="patient-subtitle">Clinical data used for analysis</p>
 <div className="patient-grid">
    {/* Dynamic values from clinicalInputs */}
    <Info label="MMSE Score" value={`${clinicalInputs.MMSE} / 30`} />
    <Info label="Functional Score" value={`${clinicalInputs.FunctionalAssessment} / 10`} />
    <Info label="ADL Score" value={`${clinicalInputs.ADL} / 10`} />
    <Info label="Age" value={clinicalInputs.Age} />
    <Info label="Sleep Quality" value={`${clinicalInputs.SleepQuality} / 5`} />
    <Info label="HDL Cholesterol" value={`${clinicalInputs.CholesterolHDL} mg/dL`} />
    <Info label="LDL Cholesterol" value={`${clinicalInputs.CholesterolLDL} mg/dL`} />
    
    {/* Symptoms (converted from Yes/No) */}
    <Info label="Memory Complaints" value={clinicalInputs.MemoryComplaints} />
    <Info label="Behavioral Problems" value={clinicalInputs.BehavioralProblems} />
    <Info label="Family History Of Alzheimers" value={clinicalInputs.FamilyHistoryAlzheimers} />
  </div>
  {/* CENTER BUTTON */}
  {/* <div className="download-center">
    <button className="primary-btn" onClick={() => navigate("/generate_report")} >Download Report</button>
  </div> */}
</div>
  </div>
  </div>
  );
}


/* ================= SUB COMPONENTS ================= */

function Metric({ label, value, color, gradient }) {
  return (
    <div className="metric">
      <span className="metric-label">{label}</span>
      <span className="metric-value" style={{ color }}>
        {value}%
      </span>
      <div className="metric-bar">
        <div
          className="metric-fill"
          style={{
            width: `${value}%`,
            background: gradient
              ? "linear-gradient(90deg, #2563eb, #60a5fa)"
              : color,
          }}
        />
      </div>
    </div>
  );
}
function Info({ label, value }) {
  return (
    <div className="patient-item">
      <span className="patient-label">{label}</span>
      <span className="patient-value">{value ?? "—"}</span>
    </div>
  );
}

function SplitBar({ label, value, type }) {
  return (
    <div className="split-block">
      <div className="split-row">
        <span>{label}</span>
        <strong>{value}%</strong>
      </div>
      <div className="split-bar">
        <div className={`split-fill ${type}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}