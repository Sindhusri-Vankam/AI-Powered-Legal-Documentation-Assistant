import re
import spacy

nlp = spacy.blank("en")


def clean_text(text):
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove leading and trailing spaces
    text = text.strip()

    # Process text using spaCy
    doc = nlp(text)

    # Reconstruct normalized text
    cleaned_text = " ".join(token.text for token in doc)

    return cleaned_text