async function postJSON(url, payload) {
  const res = await fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });
  return await res.json();
}

document.getElementById("predict-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const payload = Object.fromEntries(new FormData(form).entries());
  // Cast numbers
  for (const k in payload) payload[k] = Number(payload[k]);
  const data = await postJSON("/api/predict", payload);
  const box = document.getElementById("result");
  box.classList.remove("hidden");
  box.innerHTML = `<h3>Prediction</h3>
    <p><strong>Risk:</strong> ${data.label} (p=${data.proba.toFixed(3)})</p>`;
});

document.getElementById("diet-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const payload = Object.fromEntries(new FormData(form).entries());
  payload.glucose = Number(payload.glucose);
  payload.bmi = Number(payload.bmi);
  payload.veg = payload.veg === "true";
  const data = await postJSON("/api/diet-plan", payload);
  const box = document.getElementById("diet");
  box.classList.remove("hidden");
  const tips = data.tips.map(t => `<li>${t}</li>`).join("");
  const meals = data.sample_meals.map(t => `<li>${t}</li>`).join("");
  box.innerHTML = `<h3>${data.title}</h3>
    <p><strong>Category:</strong> ${data.category}</p>
    <h4>Tips</h4><ul>${tips}</ul>
    <h4>Sample Meals</h4><ul>${meals}</ul>`;
});
