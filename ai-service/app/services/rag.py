import numpy as np
from app.services.embeddings import generate_embedding

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def split_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def cosine_similarity(vector1, vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)

    denominator = (
        np.linalg.norm(vector1) *
        np.linalg.norm(vector2)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(vector1, vector2) / denominator
    )


def retrieve_relevant_chunks(text, question, top_k=3):

    chunks = split_text(text)

    if not chunks:
        return []

    question_embedding = generate_embedding(question)

    chunk_scores = []

    for chunk in chunks:

        chunk_embedding = generate_embedding(chunk)

        score = cosine_similarity(
            question_embedding,
            chunk_embedding
        )

        chunk_scores.append(
            (score, chunk)
        )

    chunk_scores.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        chunk
        for score, chunk in chunk_scores[:top_k]
    ]


qa_prompt = PromptTemplate.from_template(
    """Answer the question using only the provided context.

Context:
{context}

Question:
{question}

Answer clearly and concisely:"""
)


def create_qa_prompt(context, question):
    chain = qa_prompt | StrOutputParser()

    return chain.invoke({
        "context": context,
        "question": question
    })