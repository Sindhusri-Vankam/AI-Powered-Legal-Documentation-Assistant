from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def summarize_text(text):
    if not text or not text.strip():
        return ""

    text = text[:3000]

    prompt = f"""
Provide a concise summary of the following document.
Mention the main purpose, important details, requirements, and conclusion if present.

Document:
{text}

Summary:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        min_new_tokens=30,
        do_sample=False,
        num_beams=4,
        early_stopping=True
    )

    summary = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return summary.strip()