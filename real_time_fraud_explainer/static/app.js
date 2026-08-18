const form = document.getElementById("fraudForm");
const result = document.getElementById("result");
const recent = document.getElementById("recent");

const boolValue = (id) => document.getElementById(id).value === "true";

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    amount: Number(document.getElementById("amount").value),
    beneficiary_new: boolValue("beneficiary_new"),
    hour: Number(document.getElementById("hour").value),
    transactions_last_10_min: Number(document.getElementById("tx_count").value),
    device_changed: boolValue("device_changed"),
    location_changed: boolValue("location_changed"),
    merchant_risk: document.getElementById("merchant_risk").value,
    collect_request: boolValue("collect_request")
  };

  result.innerHTML = "<h2>Checking...</h2><p>Evaluating transaction signals.</p>";

  try {
    const response = await fetch("/api/check-transaction", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error("Request failed");
    const data = await response.json();

    const cssClass = data.risk_level.toLowerCase();

    result.innerHTML = `
      <p class="eyebrow">REAL-TIME DECISION</p>
      <span class="badge ${cssClass}">${data.risk_level} RISK</span>
      <div class="score">${data.risk_score}/100</div>
      <div class="action">${data.action}</div>
      <h3>Why was it flagged?</h3>
      ${data.reasons.map(r => `<div class="reason">• ${r}</div>`).join("")}
      <h3>What should the user do?</h3>
      <p class="explanation">${data.explanation}</p>
    `;

    loadRecent();
  } catch (error) {
    result.innerHTML = "<h2>Something went wrong</h2><p>Could not reach the fraud engine. Check that Flask is running.</p>";
  }
});

async function loadRecent() {
  const response = await fetch("/api/recent");
  const data = await response.json();

  if (!data.length) {
    recent.textContent = "No checks yet.";
    return;
  }

  recent.innerHTML = `
    <table>
      <thead><tr><th>Amount</th><th>Score</th><th>Risk</th><th>Action</th></tr></thead>
      <tbody>
        ${data.map(x => `
          <tr>
            <td>₹${Number(x.amount).toLocaleString("en-IN")}</td>
            <td>${x.risk_score}/100</td>
            <td>${x.risk_level}</td>
            <td>${x.action}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
}
