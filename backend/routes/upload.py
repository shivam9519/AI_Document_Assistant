from fastapi import APIRouter, UploadFile, File
from backend.services.embedding_services import generate_embeddings
from backend.services.faiss_service import create_faiss_index
import backend.services.store as store

from backend.services.pdf_service import (
    save_file,
    extract_text_from_pdf,
    chunk_text
)

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    saved_path = save_file(file)

    text = extract_text_from_pdf(saved_path)

    chunks = chunk_text(text)

    embeddings= generate_embeddings(chunks)

    index=create_faiss_index(embeddings)
    store.faiss_index=index
    store.chunks=chunks

    return {
        "filename": file.filename,
        "total_chunks": len(chunks),
        "embedding_shape":list(embeddings.shape),
        "vector_in_faiss":index.ntotal
    }