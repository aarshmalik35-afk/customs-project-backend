# risk_scoring.py

def calculate_risk(data):

    risk_score = 0
    reasons = []

    # =========================
    # CRITICAL FIELDS
    # =========================

    if data.get("Air Waybill") == "Not Found":
        risk_score += 25
        reasons.append("Missing Air Waybill")

    if data.get("Invoice Number") == "Not Found":
        risk_score += 25
        reasons.append("Missing Invoice Number")

    if data.get("Country") == "Not Found":
        risk_score += 15
        reasons.append("Missing Country")

    if data.get("Total Value") == "Not Found":
        risk_score += 20
        reasons.append("Missing Total Value")

    # =========================
    # IMPORTANT FIELDS
    # =========================

    if data.get("Shipper") == "Not Found":
        risk_score += 10
        reasons.append("Missing Shipper Information")

    if data.get("Consignee") == "Not Found":
        risk_score += 10
        reasons.append("Missing Consignee Information")

    if data.get("Invoice Date") == "Not Found":
        risk_score += 10
        reasons.append("Missing Invoice Date")

    # =========================
    # COUNTRY RISK
    # =========================

    country = str(
        data.get("Country", "Not Found")
    ).strip()

    HIGH_RISK_COUNTRIES = [
        "Iran",
        "North Korea",
        "Afghanistan"
    ]

    MEDIUM_RISK_COUNTRIES = [
        "Pakistan",
        "Russia"
    ]

    country_risk_level = "UNKNOWN"

    if country == "Not Found" or country == "":

        reasons.append("Country Information Missing")

    elif country in HIGH_RISK_COUNTRIES:

        risk_score += 30
        country_risk_level = "HIGH"
        reasons.append("High-Risk Origin Country")

    elif country in MEDIUM_RISK_COUNTRIES:

        risk_score += 15
        country_risk_level = "MEDIUM"
        reasons.append("Medium-Risk Origin Country")

    else:

        country_risk_level = "LOW"

    # =========================
    # SHIPMENT VALUE RISK
    # =========================

    high_value_shipment = False

    value = data.get("Total Value")

    try:

        if value != "Not Found":

            value = float(
                str(value)
                .replace("$", "")
                .replace(",", "")
            )

            if value >= 50000:

                risk_score += 40
                high_value_shipment = True
                reasons.append(
                    "Very High Shipment Value"
                )

            elif value >= 10000:

                risk_score += 20
                reasons.append(
                    "High Shipment Value"
                )

            elif value >= 5000:

                risk_score += 10
                reasons.append(
                    "Moderately High Shipment Value"
                )

    except:

        reasons.append(
            "Unable to Validate Shipment Value"
        )

    # =========================
    # WEIGHT VALIDATION
    # =========================

    gross = data.get("Gross Weight")
    net = data.get("Net Weight")

    try:

        if (
            gross != "Not Found"
            and
            net != "Not Found"
        ):

            gross = float(
                str(gross).replace(",", "")
            )

            net = float(
                str(net).replace(",", "")
            )

            if net > gross:

                risk_score += 30
                reasons.append(
                    "Net Weight exceeds Gross Weight"
                )

            if gross <= 0:

                risk_score += 20
                reasons.append(
                    "Invalid Gross Weight"
                )

            if net <= 0:

                risk_score += 20
                reasons.append(
                    "Invalid Net Weight"
                )

    except:

        risk_score += 10
        reasons.append(
            "Weight Validation Failed"
        )

    # =========================
    # CONFIDENCE SCORE
    # =========================

    total_fields = len(data)

    found_fields = sum(
        1
        for value in data.values()
        if value != "Not Found"
    )

    confidence_score = round(
        (found_fields / total_fields) * 100
    )

    # =========================
    # LIMIT SCORE
    # =========================

    risk_score = min(risk_score, 100)

    # =========================
    # RISK LEVEL
    # =========================

    if risk_score < 30:

        risk_level = "LOW"

    elif risk_score < 60:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    # =========================
    # DECISION ENGINE
    # =========================

    if risk_score >= 60:

        decision = "MANUAL REVIEW"

    elif high_value_shipment:

        decision = "MANUAL REVIEW"

    elif confidence_score < 70:

        decision = "REVIEW RECOMMENDED"

    else:

        decision = "AUTO APPROVE"

    # =========================
    # RISK REASONS
    # =========================

    if len(reasons) == 0:

        risk_reason = (
            "No Risk Indicators Detected"
        )

    else:

        risk_reason = " | ".join(reasons)

    # =========================
    # RETURN
    # =========================

    return (
        risk_score,
        confidence_score,
        risk_level,
        decision,
        risk_reason,
        country_risk_level
    )