// function App() {
//   return (
//     <div>
//       <h1>Multimodal Alzheimer’s Detection</h1>
//       <p>MRI + Clinical Data | Early Diagnosis</p>
//     </div>
//   );
// }

// export default App;

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import NewDiagnosis from "./pages/NewDiagnosis";
import DiagnosisResult from "./pages/DiagnosisResult";
import GenerateReport from "./pages/GenerateReport";
import TakeDetails from "./pages/TakeDetails";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/new_diagnosis" element={<NewDiagnosis />} /> 
        <Route path="/diagnosis_result" element={<DiagnosisResult />} />
        <Route path="/generate_report" element={<GenerateReport />}/>
        <Route path="/take_details" element={<TakeDetails />}/>
      </Routes>
    </Router>
  );
}

export default App;
