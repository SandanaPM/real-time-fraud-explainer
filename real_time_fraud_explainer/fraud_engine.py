def _number(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def assess_transaction(data):
    amount = _number(data.get("amount"))
    beneficiary_new = bool(data.get("beneficiary_new", False))
    hour = int(_number(data.get("hour"), 12))
    tx_count = int(_number(data.get("transactions_last_10_min"), 0))
    device_changed = bool(data.get("device_changed", False))
    location_changed = bool(data.get("location_changed", False))
    merchant_risk = str(data.get("merchant_risk", "low")).lower()
    collect_request = bool(data.get("collect_request", False))

    score = 0
    reasons = []

    if amount >= 50000:
        score += 25
        reasons.append("Large amount: ₹50,000 or more is being moved.")
    elif amount >= 10000:
        score += 12
        reasons.append("Amount is higher than a typical small UPI payment.")

    if beneficiary_new:
        score += 22
        reasons.append("The beneficiary is new or has not been paid before.")

    if hour < 5 or hour >= 23:
        score += 12
        reasons.append("Transaction is happening at an unusual hour.")

    if tx_count >= 6:
        score += 22
        reasons.append("Many transactions were attempted in the last 10 minutes.")
    elif tx_count >= 3:
        score += 10
        reasons.append("Transaction frequency is higher than normal.")

    if device_changed:
        score += 12
        reasons.append("The payment is coming from a recently changed device.")

    if location_changed:
        score += 10
        reasons.append("The location differs from the user's recent payment pattern.")

    if merchant_risk == "high":
        score += 20
        reasons.append("The destination has a higher-risk merchant profile.")
    elif merchant_risk == "medium":
        score += 8
        reasons.append("The destination has a medium-risk merchant profile.")

    if collect_request:
        score += 10
        reasons.append("This is a collect/payment-request flow; the user should verify who initiated it.")

    score = min(score, 100)

    if score >= 60:
        level = "HIGH"
        action = "HOLD & VERIFY"
        explanation = (
            "This payment looks unusual because multiple risk signals appeared together. "
            "Pause the transaction and verify the beneficiary through a trusted channel."
        )
    elif score >= 30:
        level = "REVIEW"
        action = "STEP-UP VERIFY"
        explanation = (
            "The payment has some unusual signals. Ask the user to verify the beneficiary "
            "and transaction details before continuing."
        )
    else:
        level = "LOW"
        action = "ALLOW"
        explanation = (
            "No strong anomaly was detected by the prototype rules. "
            "Continue normal payment checks."
        )

    if not reasons:
        reasons.append("No major anomaly signal was triggered.")

    return {
        "risk_score": score,
        "risk_level": level,
        "action": action,
        "reasons": reasons,
        "explanation": explanation,
    }
