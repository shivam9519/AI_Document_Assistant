import logging
from fastapi import APIRouter, UploadFile, File
import backend.services.store as store

from backend.services.hash_service import calculate_file_hash
from backend.services.embedding_services import generate_embeddings
from backend.services.faiss_service import create_faiss_index
from backend.services.pdf_service import (
    save_file,
    extract_text_from_pdf,
    chunk_text
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", summary="Upload a PDF document")
async def upload_pdf(file: UploadFile = File(...)):

    saved_path = save_file(file)
    document_hash = calculate_file_hash(saved_path)

    # ---------------------------------
    # Document already exists in memory? (loaded at startup)
    # ---------------------------------
    if document_hash in store.documents:
        logger.info(f"Document already loaded: {document_hash}")
        return {
            "message": "Document loaded from cache",
            "document_id": document_hash,
            "filename": file.filename
        }

    # ---------------------------------
    # New document
    # ---------------------------------
    pages = extract_text_from_pdf(saved_path)
    chunks = chunk_text(pages)
    embeddings = generate_embeddings(chunks)
    index = create_faiss_index(embeddings)

    # 👇 ONE call handles disk save + memory storage
    store.save_document(document_hash, index, chunks)

    logger.info(f"Created new document: {document_hash}")

    return {
        "message": "New document processed",
        "document_id": document_hash,
        "filename": file.filename,
        "total_chunks": len(chunks),
        "embedding_shape": list(embeddings.shape),
        "vectors_in_faiss": index.ntotal
    }