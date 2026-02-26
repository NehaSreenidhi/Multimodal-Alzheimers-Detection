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
import Home from "./pages/home";
import NewDiagnosis from "./pages/new_diagnosis";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/new_diagnosis" element={<NewDiagnosis />} /> {/* route for new page */}
      </Routes>
    </Router>
  );
}

export default App;
