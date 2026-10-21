import re
import datetime
import random

from risk_scoring import calculate_risk


def extract_fields(text):

    # =========================
    # EXTRACT FIELDS
    # =========================

    data = {
        "Invoice Date": "Not Found",
        "Air Waybill": "Not Found",
        "HTS Code": "Not Found",
        "Country": "Not Found",
        "Gross Weight": "Not Found",
        "Net Weight": "Not Found",
        "Invoice Number": "Not Found",
        "Total Value": "Not Found",
        "Shipper": "Not Found",
        "Consignee": "Not Found",
        "Fax": "Not Found"
    }

    # =========================
    # INVOICE DATE
    # =========================

    date_match = re.search(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\s+\d{1,2},\s+\d{4}",
        text,
        re.IGNORECASE
    )

    if date_match:
        data["Invoice Date"] = date_match.group()

    # =========================
    # AIR WAYBILL
    # =========================

    awb_match = re.search(
        r"(?:AIR WAYBILL|AWB)[^\d]*(\d[\d\s-]{6,})",
        text,
        re.IGNORECASE
    )

    if awb_match:
        data["Air Waybill"] = awb_match.group(1).strip()

    # =========================
    # HTS CODE
    # =========================

    hts_match = re.search(
        r"(\d{4}\.\d{2})",
        text
    )

    if hts_match:
        data["HTS Code"] = hts_match.group(1)

    # =========================
    # COUNTRY
    # =========================

    country_match = re.search(
        r"Manufactured in ([A-Za-z\s]+)",
        text,
        re.IGNORECASE
    )

    if country_match:
        data["Country"] = country_match.group(1).strip()

    # =========================
    # GROSS WEIGHT
    # =========================

    gross_match = re.search(
        r"gross weight[:\s]+([\d.]+)",
        text,
        re.IGNORECASE
    )

    if gross_match:
        data["Gross Weight"] = gross_match.group(1)

    # =========================
    # NET WEIGHT
    # =========================

    net_match = re.search(
        r"net weight[:\s]+([\d.]+)",
        text,
        re.IGNORECASE
    )

    if net_match:
        data["Net Weight"] = net_match.group(1)

    # =========================
    # INVOICE NUMBER
    # =========================

    invoice_match = re.search(
        r"invoice\s*(?:number|no\.?)[:\s]*([A-Za-z0-9-]+)",
        text,
        re.IGNORECASE
    )

    if invoice_match:
        data["Invoice Number"] = invoice_match.group(1)

    # =========================
    # TOTAL VALUE
    # =========================

    total_match = re.search(
        r"total[:\s]*usd\s*([\d,.]+)",
        text,
        re.IGNORECASE
    )

    if total_match:
        data["Total Value"] = total_match.group(1)

    # =========================
    # EMAIL → SHIPPER FALLBACK
    # =========================

    email_match = re.search(
        r"[\w\.-]+@[\w\.-]+\.\w+",
        text
    )

    if email_match:
        data["Shipper"] = email_match.group()

    # =========================
    # CONSIGNEE
    # =========================

    consignee_match = re.search(
        r"HFT Electronics",
        text,
        re.IGNORECASE
    )

    if consignee_match:
        data["Consignee"] = consignee_match.group()

    # =========================
    # FAX
    # =========================

    fax_match = re.search(
        r"fax[:\s]*([+\d\s()\-]+)",
        text,
        re.IGNORECASE
    )

    if fax_match:
        data["Fax"] = fax_match.group(1).strip()

    # =========================
    # RISK ANALYSIS
    # =========================

    (
        risk_score,
        confidence_score,
        risk_level,
        decision,
        risk_reason,
        country_risk_level
    ) = calculate_risk(data)

    # =========================
    # SHIPMENT STATUS
    # =========================

    if decision == "MANUAL REVIEW":

        shipment_status = "Manual Review"

    elif decision == "AUTO APPROVE":

        shipment_status = "Approved"

    else:

        shipment_status = "Under Review"

    # =========================
    # SHIPMENT ID
    # =========================

    shipment_id = (
        "SHIP-"
        + datetime.datetime.now().strftime(
            "%Y%m%d-%H%M%S"
        )
    )

    # =========================
    # TELEMETRY SIMULATION
    # =========================

    temperature = random.randint(20, 35)

    humidity = random.randint(40, 80)

    door_status = random.choice([
        "Closed",
        "Closed",
        "Closed",
        "Open"
    ])

    # =========================
    # ADD GENERATED DATA
    # =========================

    data["Risk Score"] = risk_score
    data["Confidence Score"] = confidence_score
    data["Risk Level"] = risk_level
    data["Decision"] = decision
    data["Risk Reason"] = risk_reason
    data["Country Risk Level"] = country_risk_level
    data["Shipment Status"] = shipment_status
    data["Shipment ID"] = shipment_id
    data["Temperature"] = f"{temperature} °C"
    data["Humidity"] = f"{humidity} %"
    data["Door Status"] = door_status

    return data