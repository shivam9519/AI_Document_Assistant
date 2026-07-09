from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks: list):

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts)

    return embeddings


def generate_question_embedding(question: str):

    embedding = model.encode([question])

    return embedding