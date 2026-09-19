from app.services.risk_detector import detect_risks
from app.services.clause_extractor import extract_clauses
from app.services.summarizer import summarize_text
from app.services.embeddings import generate_embedding
from fastapi import APIRouter, UploadFile, File
import tempfile
import os

from app.services.pdf_processor import (
    extract_text_from_pdf,
    extract_text_from_docx
)
from app.services.text_cleaner import clean_text
router = APIRouter()


@router.post("/process")
async def process_document(file: UploadFile = File(...)):

    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in [".pdf", ".docx"]:
        return {
            "success": False,
            "message": "Only PDF and DOCX files are supported"
        }

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=file_extension
    ) as temp_file:

        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:
        if file_extension == ".pdf":
            text = clean_text(extract_text_from_pdf(temp_path))
        else:
            text = clean_text(extract_text_from_docx(temp_path))
        embedding = generate_embedding(text)
        summary = summarize_text(text)
        clauses = extract_clauses(text)
        risks = detect_risks(text)
        return {
            "success": True,
            "fileName": file.filename,
            "extractedText": text,
            "embedding": embedding,
            "summary": summary,
            "clauses": clauses,
            "risks": risks
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)