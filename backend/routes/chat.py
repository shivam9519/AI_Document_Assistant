from fastapi import APIRouter
from backend.models.schemas import QuestionRequest
from backend.services.embedding_service import generate_question_embedding
from backend.services.faiss_service import (
    search_index,
    retrieve_chunks
)
import backend.services.store as store

router = APIRouter()


@router.post("/chat")
async def chat(data: QuestionRequest):

    question_embedding = generate_question_embedding(
        data.question
    )

    indices = search_index(
        store.faiss_index,
        question_embedding
    )

    top_chunks = retrieve_chunks(
        store.chunks,
        indices
    )

    return {
        "question": data.question,
        "retrieved_chunks": top_chunks
    }