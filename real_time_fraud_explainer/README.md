# Real-Time Fraud Explainer

A hackathon-ready prototype for flagging suspicious UPI-style transactions in real time and explaining the risk in plain language.

## What it does
- Accepts a simulated UPI transaction.
- Calculates a 0–100 risk score using explainable signals.
- Classifies the transaction as LOW, REVIEW, or HIGH risk.
- Produces human-readable reasons instead of only saying "fraud detected".
- Recommends an immediate action: allow, verify, or hold.
- Stores recent transactions in memory for the demo dashboard.

> This is a prototype. It does not connect to NPCI/bank rails and must not be presented as a production fraud engine.

## Run
Python 3.10+ recommended.

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Demo examples
1. Normal transaction: ₹250 to a known merchant -> low risk.
2. New beneficiary + high amount + unusual hour -> high risk.
3. Many transactions in a short period -> review/high risk.

## API
POST `/api/check-transaction`

Example:
```json
{
  "amount": 85000,
  "beneficiary_new": true,
  "hour": 2,
  "transactions_last_10_min": 7,
  "device_changed": true,
  "location_changed": true,
  "merchant_risk": "medium",
  "collect_request": true
}
```

The response contains `risk_score`, `risk_level`, `reasons`, `action`, and `explanation`.
