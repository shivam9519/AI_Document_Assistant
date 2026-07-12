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

    try:

        # -----------------------------
        # Check document exists
        # -----------------------------
        if data.document_id not in store.documents:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        document = store.documents[data.document_id]

        index = document["faiss_index"]
        chunks = document["chunks"]

        # -----------------------------
        # Generate embedding
        # -----------------------------
        question_embedding = generate_question_embedding(
            data.question
        )

        # -----------------------------
        # Search FAISS
        # -----------------------------
        distances, indices = search_index(
            index,
            question_embedding
        )

        if len(distances) == 0:
            return {
                "answer": "I couldn't find this information in the uploaded document.",
                "sources": []
            }

        # -----------------------------
        # Similarity check
        # -----------------------------
        if distances[0] > SIMILARITY_THRESHOLD:
            return {
                "answer": "I couldn't find this information in the uploaded document.",
                "sources": []
            }

        # -----------------------------
        # Retrieve chunks
        # -----------------------------
        top_chunks = retrieve_chunks(
            chunks,
            indices
        )

        if len(top_chunks) == 0:
            return {
                "answer": "I couldn't find this information in the uploaded document.",
                "sources": []
            }

        # -----------------------------
        # Build context
        # -----------------------------
        context = ""

        for chunk in top_chunks:

            context += f"""
Page {chunk['page']}:

{chunk['text']}

"""

        # -----------------------------
        # Gemini
        # -----------------------------
        answer = generate_answer(
            data.question,
            context
        )

        sources = sorted(
            set(chunk["page"] for chunk in top_chunks)
        )

        logger.info(
            f"Question answered for document {data.document_id}"
        )

        return {
            "document_id": data.document_id,
            "question": data.question,
            "answer": answer,
            "sources": sources
        }

    except HTTPException:
        raise

    except Exception as e:

        logger.exception(e)

        return {
            "answer": "The AI service is temporarily unavailable. Please try again in a few minutes.",
            "sources": []
        }