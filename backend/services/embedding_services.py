from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks: list):
    embeddings = model.encode(chunks)

    return embeddings
def generate_question_embedding(question: str):
    embedding = model.encode([question])

    return embedding