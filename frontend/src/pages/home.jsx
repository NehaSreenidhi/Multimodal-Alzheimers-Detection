import React from "react";
import { useNavigate } from "react-router-dom";
import { Brain, Zap, Shield, Target } from "lucide-react";
import { ArrowUpRight } from "lucide-react";
import "../styles/home.css";

const Home = () => {
  const navigate = useNavigate();

  return (
    <>
      {/* ---------------- HERO SECTION ---------------- */}
      <div className="hero2-container">
        <div className="hero2-icon">
          <Brain size={40} color="white" />
        </div>

        <h1 className="hero2-title">
          Multimodal Early Detection of <br /> Alzheimer's Disease
        </h1>

        <p className="hero2-subtitle">
          Advanced multimodal fusion system combining deep learning analysis of MRI scans with
          machine learning assessment of clinical features for early Alzheimer's detection.
        </p>

        <div className="hero2-btn-group">
          
<button className="hero2-btn-primary" onClick={() => navigate("/new_diagnosis")}>
  <ArrowUpRight size={18} strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round" />
  Start Diagnosis
</button>
        </div>
      </div>

      {/* ---------------- FEATURES SECTION ---------------- */}
      <div className="features2-container">

        <div className="feature2-item">
          <div className="feature2-icon icon-skyblue">
            <Zap size={30} color="#3b82f6" />
          </div>
          <div>
            <h3 className="feature2-title">Early Detection</h3>
            <p className="feature2-text">
              Identify Alzheimer’s at early stages enabling timely intervention and treatment.
            </p>
          </div>
        </div>

        <div className="feature2-item">
          <div className="feature2-icon icon-purple">
            <Shield size={30} color="#8b5cf6" />
          </div>
          <div>
            <h3 className="feature2-title">Explainable AI</h3>
            <p className="feature2-text">
              Transparent predictions with Grad-CAM and SHAP visualizations for clinical trust.
            </p>
          </div>
        </div>

        <div className="feature2-item">
          <div className="feature2-icon icon-green">
            <Target size={30} color="#22c55e" />
          </div>
          <div>
            <h3 className="feature2-title">High Accuracy</h3>
            <p className="feature2-text">
              Multimodal fusion approach demonstrates superior performance over single-modality methods.
            </p>
          </div>
        </div>

      </div>

      {/* ---------------- CTA SECTION ---------------- */}
      <div className="cta2-box">
        <h2>Ready to Get Started?</h2>
        <p>
          Upload an MRI scan and provide clinical information to receive a comprehensive
          Alzheimer's disease risk assessment with Explainable AI insights.
        </p>

        <button className="cta2-btn" onClick={() => navigate("/new_diagnosis")}>
  <ArrowUpRight size={18} strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round" />
  Begin Diagnosis
</button>
      </div>
    </>
  );
};

export default Home;