import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/GenerateReport.css";

export default function GenerateReport() {
  const navigate = useNavigate();

  const [formData, setFormData] = React.useState({
    patient_name: "",
    mobile_number: "",
    gender: ""
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleNext = () => {
    if (
      !formData.patient_name ||
      !formData.mobile_number ||
      !formData.gender
    ) {
      alert("Please fill all required fields.");
      return;
    }

    navigate("/new_diagnosis", { state: formData });
  };

  return (
    <div className="report-page">
      <div className="report-card">

        

        <h2>Enter Patient Details</h2>

        <div className="report-form">

          <input
            type="text"
            name="patient_name"
            placeholder="Patient Name"
            onChange={handleChange}
          />

          <input
            type="tel"
            name="mobile_number"
            placeholder="Mobile Number"
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



          <div className="button-group">
  <button
    className="secondary-btn"
    onClick={() => navigate("/")}
  >
    Back
  </button>

  <button
    className="primary-btn"
    onClick={handleNext}
  >
    Next
  </button>
</div>

        </div>
      </div>
    </div>
  );
}