from fastapi import APIRouter, UploadFile, File

from backend.services.embedding_services import generate_embeddings
from backend.services.faiss_service import create_faiss_index
import backend.services.store as store
from backend.services.hash_service import calculate_file_hash
from backend.services.faiss_service import save_faiss_index
from backend.services.metadata_service import save_metadata

from backend.services.pdf_service import (
    save_file,
    extract_text_from_pdf,
    chunk_text
)

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Save uploaded PDF
    saved_path = save_file(file)

    document_hash = calculate_file_hash(saved_path)

    # Extract text page by page
    pages = extract_text_from_pdf(saved_path)

    # Create chunks while keeping page numbers
    chunks = chunk_text(pages)

    # Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Create FAISS index
    index = create_faiss_index(embeddings)

    save_faiss_index(index, document_hash)

    save_metadata(chunks, document_hash)

    # Store for chat endpoint
    store.faiss_index = index
    store.chunks = chunks

    return {
        "filename": file.filename,
        "total_chunks": len(chunks),
        "embedding_shape": list(embeddings.shape),
        "vectors_in_faiss": index.ntotal
    }