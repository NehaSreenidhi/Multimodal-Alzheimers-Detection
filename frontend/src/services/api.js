// frontend/src/services/api.js

export async function predictDiagnosis(formData) {
  const response = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    body: formData, // IMPORTANT: FormData (no headers!)
  });

  if (!response.ok) {
    throw new Error("Prediction request failed");
  }

  return await response.json();
}