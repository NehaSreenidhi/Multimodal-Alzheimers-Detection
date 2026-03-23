import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/TakeDetails.css";

export default function TakeDetails() {
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

    navigate("/new_diagnosis", {
      state: {
        patientDetails: formData
      }
    });
  };

  return (
    <div className="take-page">
      <div className="take-card">

        <h2>Enter Patient Details</h2>

        <div className="take-form">

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
    className="back-btn"
    onClick={() => navigate("/")}
  >
    Back
  </button>

  <button
    className="next-btn"
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