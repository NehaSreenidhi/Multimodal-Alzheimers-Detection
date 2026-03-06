export async function predictDiagnosis(formData) {
  const response = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Prediction failed");
  }

  return await response.json(); // ✅ BACKEND DATA
}