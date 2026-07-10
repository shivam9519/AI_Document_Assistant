from fastapi import APIRouter, HTTPException
import logging

import backend.services.store as store

from backend.config import SIMILARITY_THRESHOLD
from backend.models.schemas import QuestionRequest

from backend.services.embedding_services import (
    generate_question_embedding
)

from backend.services.faiss_service import (
    search_index,
    retrieve_chunks
)

from backend.services.llm_service import generate_answer

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/chat",
    summary="Chat with a PDF",
    description="Ask questions about a previously uploaded PDF."
)
async def chat(data: QuestionRequest):


    # Check document exists
    if data.document_id not in store.documents:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    # Get selected document
    document = store.documents[data.document_id]

    index = document["faiss_index"]
    chunks = document["chunks"]


    # Generate question embedding
    question_embedding = generate_question_embedding(
        data.question
    )


    # Search FAISS
    distances, indices = search_index(
        index,
        question_embedding
    )


    # Similarity threshold
    if distances[0] > SIMILARITY_THRESHOLD:
        return {
            "answer": "I couldn't find this information in the uploaded document."
        }

    # Retrieve chunks
    top_chunks = retrieve_chunks(
        chunks,
        indices
    )

    # Build context
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

    logger.info(
        f"Question answered for document {data.document_id}"
    )

    # Remove duplicate pages
    sources = sorted(
        set(
            chunk["page"] for chunk in top_chunks
        )
    )


    response = {
        "document_id": data.document_id,
        "question": data.question,
        "answer": answer,
        "sources": sources
    }

    return response