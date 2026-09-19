import re


def extract_clauses(text):
    clauses = {}

    patterns = {
        "termination": r"(?i)([^.]*\b(?:termination|terminated|terminate)\b[^.]*)\.",
        "payment": r"(?i)([^.]*\b(?:payment|pay|paid)\b[^.]*)\.",
        "confidentiality": r"(?i)([^.]*\b(?:confidentiality|confidential)\b[^.]*)\.",
        "liability": r"(?i)([^.]*\b(?:liability|liable)\b[^.]*)\.",
        "dispute_resolution": r"(?i)([^.]*\b(?:dispute resolution|arbitration|mediation)\b[^.]*)\.",
    }

    for clause_name, pattern in patterns.items():
        matches = re.findall(pattern, text)

        if matches:
            clauses[clause_name] = matches[0].strip()

    return clauses