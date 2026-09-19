import re


def detect_risks(text):
    risks = []

    risk_patterns = {
        "early_termination": r"(?i)([^.]*\b(?:terminate|termination|terminated)\b[^.]*\b(?:without notice|immediately|at any time)\b[^.]*)\.",
        "late_payment": r"(?i)([^.]*\b(?:payment|pay|paid)\b[^.]*\b(?:late|delay|penalty|interest)\b[^.]*)\.",
        "unlimited_liability": r"(?i)([^.]*\b(?:unlimited liability|liable for all damages)\b[^.]*)\.",
        "confidentiality_breach": r"(?i)([^.]*\bconfidentiality\b[^.]*\b(?:breach|violation|penalty)\b[^.]*)\.",
        "dispute_risk": r"(?i)([^.]*\b(?:any dispute|disputes? shall|disputes? will|arbitration shall|mediation shall)\b[^.]*)\.",
    }

    for risk_name, pattern in risk_patterns.items():
        match = re.search(pattern, text)

        if match:
            risks.append({
                "type": risk_name,
                "description": match.group(1).strip()
            })

    return risks