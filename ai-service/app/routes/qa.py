from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag import retrieve_relevant_chunks
from app.services.qa_model import generate_answer

router = APIRouter()


class QARequest(BaseModel):
    document_text: str
    question: str


@router.post("/qa")
async def document_question_answer(request: QARequest):

    relevant_chunks = retrieve_relevant_chunks(
        request.document_text,
        request.question,
        top_k=3
    )

    if not relevant_chunks:
        return {
            "success": False,
            "message": "No relevant information found"
        }

    answer = generate_answer(
        request.question,
        relevant_chunks
    )

    return {
        "success": True,
        "question": request.question,
        "answer": answer,
        "relevant_chunks": relevant_chunks
    }