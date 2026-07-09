import faiss
import os
import numpy as np
from backend.config import TOP_K


def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings).astype("float32"))

    return index



def search_index(index, question_embedding):

    distances, indices = index.search(
        question_embedding.astype("float32"),
        TOP_K
    )

    return distances[0], indices[0]

def retrieve_chunks(chunks, indices):
    return [chunks[i] for i in indices]


def save_faiss_index(index, document_hash):

    folder = "backend/storage/indexes"

    os.makedirs(folder, exist_ok=True)

    path = os.path.join(
        folder,
        f"{document_hash}.index"
    )

    faiss.write_index(index, path)

def index_exists(document_hash):

    import os

    path = os.path.join(
        "backend",
        "storage",
        "indexes",
        f"{document_hash}.index"
    )

    return os.path.exists(path)

def load_faiss_index(document_hash):

    path = os.path.join(
        "backend",
        "storage",
        "indexes",
        f"{document_hash}.index"
    )

    index = faiss.read_index(path)

    return index    