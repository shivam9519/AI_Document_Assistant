import os
import json
import pickle
import faiss

documents = {}

STORAGE_DIR = "storage/documents"
os.makedirs(STORAGE_DIR, exist_ok=True)


def save_document(document_id: str, faiss_index, chunks: list):
    """Save a document's FAISS index + chunks to disk."""
    
    doc_folder = os.path.join(STORAGE_DIR, document_id)
    os.makedirs(doc_folder, exist_ok=True)

    # Save FAISS index
    faiss.write_index(faiss_index, os.path.join(doc_folder, "index.faiss"))

    # Save chunks (text + page numbers)
    with open(os.path.join(doc_folder, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)

    # Keep in memory too (avoids re-reading disk on same session)
    documents[document_id] = {
        "faiss_index": faiss_index,
        "chunks": chunks
    }


def load_all_documents():
    """Reload all saved documents from disk into memory on server startup."""

    if not os.path.exists(STORAGE_DIR):
        return

    for document_id in os.listdir(STORAGE_DIR):
        doc_folder = os.path.join(STORAGE_DIR, document_id)

        index_path = os.path.join(doc_folder, "index.faiss")
        chunks_path = os.path.join(doc_folder, "chunks.pkl")

        if os.path.exists(index_path) and os.path.exists(chunks_path):

            faiss_index = faiss.read_index(index_path)

            with open(chunks_path, "rb") as f:
                chunks = pickle.load(f)

            documents[document_id] = {
                "faiss_index": faiss_index,
                "chunks": chunks
            }