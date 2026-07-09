from fastapi import APIRouter

from backend.models.schemas import QuestionRequest
from backend.services.embedding_services import generate_question_embedding
from backend.services.faiss_service import (
    search_index,
    retrieve_chunks
)
from backend.services.llm_service import generate_answer
from backend.config import SIMILARITY_THRESHOLD

import backend.services.store as store

router = APIRouter()


@router.post("/chat")
async def chat(data: QuestionRequest):

    # Check whether a PDF has been uploaded
    if store.faiss_index is None:
        return {
            "error": "Please upload a PDF before asking questions."
        }

    if not store.chunks:
        return {
            "error": "No document content available."
        }

    # Generate question embedding
    question_embedding = generate_question_embedding(
        data.question
    )

    # Search FAISS
    distances, indices = search_index(
        store.faiss_index,
        question_embedding
    )

    # Similarity threshold check
    if distances[0] > SIMILARITY_THRESHOLD:
        return {
            "answer": "I couldn't find this information in the uploaded document."
        }

    # Retrieve chunks
    top_chunks = retrieve_chunks(
        store.chunks,
        indices
    )

    # Build context with page numbers
    context = ""

    for chunk in top_chunks:
        context += f"""
Page {chunk['page']}:

{chunk['text']}

"""

    # Generate answer using Gemini
    answer = generate_answer(
        data.question,
        context
    )

    # Remove duplicate page numbers
    sources = sorted(
        set(
            chunk["page"] for chunk in top_chunks
        )
    )

    return {
        "question": data.question,
        "answer": answer,
        "sources": sources
    }