from fastapi import APIRouter
from backend.models.schemas import QuestionRequest
from backend.services.embedding_services import generate_question_embedding
from backend.services.faiss_service import (
    search_index,
    retrieve_chunks
)
from backend.services.llm_service import generate_answer
import backend.services.store as store

router = APIRouter()


@router.post("/chat")
async def chat(data: QuestionRequest):

    # Generate embedding for the user's question
    question_embedding = generate_question_embedding(data.question)

    # Search the FAISS index
    indices = search_index(
        store.faiss_index,
        question_embedding
    )

    # Retrieve the most relevant chunks
    top_chunks = retrieve_chunks(
        store.chunks,
        indices
    )

    # Combine retrieved chunks into one context
    context = "\n\n".join(top_chunks)

    # Create prompt for Gemini
    prompt = f"""
You are an AI Document Assistant.

Answer ONLY using the provided context.

If the answer is not available in the context, reply exactly:

"I couldn't find this information in the uploaded document."

Context:
{context}

Question:
{data.question}

Answer:
"""

    # Generate answer using Gemini
    answer = generate_answer(prompt)

    # Return response
    return {
        "question": data.question,
        "answer": answer,
        "retrieved_chunks": top_chunks
    }