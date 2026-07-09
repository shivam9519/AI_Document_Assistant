import faiss
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