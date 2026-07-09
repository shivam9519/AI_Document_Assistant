from fastapi import APIRouter, UploadFile, File

import backend.services.store as store

from backend.services.hash_service import calculate_file_hash

from backend.services.embedding_services import generate_embeddings

from backend.services.faiss_service import (
    create_faiss_index,
    save_faiss_index,
    index_exists,
    load_faiss_index
)

from backend.services.metadata_service import (
    save_metadata,
    load_metadata
)

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

    # Calculate document hash
    document_hash = calculate_file_hash(saved_path)

    # -----------------------------
    # Document already processed
    # -----------------------------
    if index_exists(document_hash):

        index = load_faiss_index(document_hash)

        chunks = load_metadata(document_hash)

        store.faiss_index = index
        store.chunks = chunks

        return {
            "message": "Document loaded from cache",
            "filename": file.filename
        }

    # -----------------------------
    # New document
    # -----------------------------

    # Extract text page by page
    pages = extract_text_from_pdf(saved_path)

    # Create chunks
    chunks = chunk_text(pages)

    # Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Create FAISS index
    index = create_faiss_index(embeddings)

    # Save FAISS index
    save_faiss_index(index, document_hash)

    # Save metadata
    save_metadata(chunks, document_hash)

    # Store in RAM
    store.faiss_index = index
    store.chunks = chunks

    return {
        "message": "New document processed",
        "filename": file.filename,
        "document_hash": document_hash,
        "total_chunks": len(chunks),
        "embedding_shape": list(embeddings.shape),
        "vectors_in_faiss": index.ntotal
    }