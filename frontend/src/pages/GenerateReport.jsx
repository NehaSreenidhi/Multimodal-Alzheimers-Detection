import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/GenerateReport.css";
import html2pdf from "html2pdf.js";

export default function GenerateReport() {
  const location = useLocation();
  const navigate = useNavigate();

  console.log("STATE:", location.state);
  const { prediction, clinicalInputs, patientDetails } = location.state || {};

  const [reportHtml, setReportHtml] = React.useState(null);
  const [loading, setLoading] = React.useState(true);

  
  if (!prediction || !clinicalInputs || !patientDetails) {
    return (
      <div className="report-page">
        <div className="report-card">
          <h2>No report data available</h2>
          <button className="primary-btn" onClick={() => navigate("/")}>
            Go Home
          </button>
        </div>
      </div>
    );
  }

  /* AUTO GENERATE REPORT ON LOAD */
  React.useEffect(() => {
    const generateReport = async () => {
      try {
        const response = await fetch("http://localhost:5000/report", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            patient_info: patientDetails,
            model_results: prediction,
            clinical_inputs: clinicalInputs
          })
        });

        const data = await response.json();
        setReportHtml(data.html_content);
      } catch (error) {
        console.error("Report generation failed:", error);
      } finally {
        setLoading(false);
      }
    };

    generateReport();
  }, []);

  /* ✅ DOWNLOAD PDF */
  const handleDownload = () => {
    const element = document.getElementById("report-content");

    const opt = {
      margin: 0.5,
      filename: `${patientDetails.patient_name}_Report.pdf`,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: "in", format: "a4", orientation: "portrait" }
    };

    html2pdf().set(opt).from(element).save();
  };

  return (
    <div className="report-page">
      <div className="report-card">

        <h2>Diagnostic Report</h2>

        {/* Loading */}
        {loading && <p className="loading-text">Generating report...</p>}

        {/* Preview */}
        {!loading && reportHtml && (
          <div className="report-preview">

            <div id="report-content">
              <div dangerouslySetInnerHTML={{ __html: reportHtml }} />
            </div>

            <div className="button-group">
              <button
                className="secondary-btn"
                onClick={() => navigate(-1)}
              >
                Back
              </button>

              <button
                className="primary-btn"
                onClick={handleDownload}
              >
                Download PDF
              </button>
            </div>

          </div>
        )}

      </div>
    </div>
  );
}