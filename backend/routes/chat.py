from fastapi import APIRouter
from backend.models.schemas import QuestionRequest
from backend.services.embedding_services import generate_question_embedding
from backend.config import SIMILARITY_THRESHOLD
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
    distances,indices = search_index(
        store.faiss_index,
        question_embedding
    )


    if distances[0] > SIMILARITY_THRESHOLD:
        return {
        "answer": "I couldn't find this information in the uploaded document."
    }


    # Retrieve the most relevant chunks
    top_chunks = retrieve_chunks(
        store.chunks,
        indices
    )

    context = ""
    for chunk in top_chunks:
        context+=f"Page{chunk['page']}:\n{chunk['text']}\n\n"

    answer = generate_answer(
    data.question,
    context
    )

    # Return response
    return {
        "question": data.question,
        "answer": answer,
        "sources":[
            chunk["page"] for chunk in top_chunks
        ]
    }