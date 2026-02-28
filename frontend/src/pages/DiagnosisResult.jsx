import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/DiagnosisResult.css";

/* ================= UI MAP ================= */
const CLASS_UI = {
  NonDemented: {
    label: "Non-Demented",
    description:
      "Multimodal indicators show no significant brain atrophy or cognitive deficits consistent with neurodegeneration.",
    color: "#16a34a",
    icon: "🧠",
  },
  VeryMildDemented: {
    label: "Very Mild Demented",
    description:
      "Subtle structural changes and minor clinical variances suggest early-stage cognitive impairment.",
    color: "#f59e0b",
    icon: "🌱",
  },
  MildDemented: {
    label: "Mild Demented",
    description:
      "Identifiable patterns of cortical thinning indicate mild dementia progression.",
    color: "#ea580c",
    icon: "⚠️",
  },
  ModerateDemented: {
    label: "Moderate Demented",
    description:
      "Pronounced global atrophy and daily activity impairment detected.",
    color: "#dc2626",
    icon: "🧩",
  },
};

export default function DiagnosisResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = React.useState("gradcam");

  /* ✅ SAFE READ */
  const prediction = location.state?.prediction;

  if (!prediction) {
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

  const { fused_probabilities, confidence, predicted_class } = prediction;
  const ui = CLASS_UI[predicted_class];

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

  // MRI vs Clinical (derived from fusion)
  const maxFused = Math.max(...fused_probabilities);
  const mriContribution = Math.round(maxFused * 100);
  const clinicalContribution = 100 - mriContribution;

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
              onClick={() => navigate("/new_diagnosis")}
            >
              New Diagnosis
            </button>
            <button className="primary-btn">View Full Report</button>
          </div>
        </div>

        {/* SUMMARY */}
        <div className="final-summary-card">
          <div
            className="summary-icon"
            style={{ backgroundColor: `${ui.color}20`, color: ui.color }}
          >
            {ui.icon}
          </div>
          <div className="summary-text">
            <h3>{ui.label}</h3>
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
              label="Final Probability"
              value={probabilityPercent}
              color={ui.color}
            />
            <Metric
              label="Confidence Score"
              value={confidencePercent}
              color="#2563eb"
              gradient
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

    <div className="analysis-metric">
      <span>CNN Confidence</span>
      <strong>{Math.round(Math.max(...fused_probabilities) * 100)}%</strong>
    </div>

    <div className="analysis-bar">
      <div
        className="analysis-fill dark"
        style={{
          width: `${Math.round(Math.max(...fused_probabilities) * 100)}%`,
        }}
      />
    </div>
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
      <span>ML Confidence</span>
      <strong>{confidencePercent}%</strong>
    </div>

    <div className="analysis-bar">
      <div
        className="analysis-fill dark"
        style={{ width: `${confidencePercent}%` }}
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
        <div>
          <h4>Original MRI Scan</h4>
          <img src={prediction.gradcam.original_image_url} alt="MRI" />
        </div>

        <div>
          <h4>Grad-CAM Heatmap</h4>
          <img src={prediction.gradcam.heatmap_url} alt="GradCAM" />
        </div>
      </div>
    </>
  )}

  {/* ================= SHAP ================= */}
  {activeTab === "shap" && prediction.shap && (
    <>
      <p className="explain-text">
        SHAP values show how each clinical feature influenced the
        prediction.
      </p>

      <div className="shap-bars">
        {prediction.shap.features.map((f) => {
          const isPositive = f.value > 0;
          const width = Math.min(Math.abs(f.value) * 100, 100);

          return (
            <div key={f.name} className="shap-row">
              <span>{f.name}</span>

              <div className="shap-bar">
                <div
                  className={`shap-fill ${isPositive ? "red" : "blue"}`}
                  style={{ width: `${width}%` }}
                />
              </div>

              <small className={isPositive ? "red-text" : "blue-text"}>
                {f.value > 0 ? "+" : ""}
                {f.value.toFixed(2)}
              </small>
            </div>
          );
        })}
      </div>
    </>
  )}
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