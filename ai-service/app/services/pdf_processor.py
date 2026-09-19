from pdf2image import convert_from_path
from app.services.ocr_service import extract_text_from_image
from pypdf import PdfReader
from docx import Document
import pytesseract

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    # If no text was extracted, use OCR
    if not text.strip():
        images = convert_from_path(
            
            file_path,
            poppler_path=r"C:\Users\sindh\Downloads\Release-26.07.0-0\poppler-26.07.0\Library\bin"
)

        for image in images:
            text += pytesseract.image_to_string(image) + "\n"

    return text.strip()


def extract_text_from_docx(file_path):
    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        if paragraph.text:
            text += paragraph.text + "\n"

    return text.strip()