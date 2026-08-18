from flask import Flask, jsonify, render_template, request
from fraud_engine import assess_transaction

app = Flask(__name__)

recent_transactions = []

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/check-transaction")
def check_transaction():
    data = request.get_json(silent=True) or {}
    result = assess_transaction(data)

    record = {
        "amount": data.get("amount", 0),
        "risk_score": result["risk_score"],
        "risk_level": result["risk_level"],
        "action": result["action"],
    }
    recent_transactions.insert(0, record)
    del recent_transactions[20:]

    return jsonify(result)

@app.get("/api/recent")
def recent():
    return jsonify(recent_transactions)

if __name__ == "__main__":
    app.run(debug=True)
