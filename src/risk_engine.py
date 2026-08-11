def calculate_risk(
    xgb_probability,
    anomaly_score
):
    risk_score = (
        0.7 * xgb_probability +
        0.3 * anomaly_score
    ) * 100

    if risk_score < 25:
        level = "Low"
        action = "Monitor"

    elif risk_score < 50:
        level = "Medium"
        action = "Rate Limit"

    elif risk_score < 75:
        level = "High"
        action = "Block Traffic"

    else:
        level = "Critical"
        action = "Block + Alert"

    return risk_score, level, action