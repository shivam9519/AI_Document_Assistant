import os
from google import genai
from dotenv import load_dotenv
import numpy as np

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

EMBEDDING_MODEL = "gemini-embedding-001"


def generate_embeddings(chunks: list):

    texts = [chunk["text"] for chunk in chunks]

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts
    )

    embeddings = np.array(
        [e.values for e in result.embeddings],
        dtype="float32"
    )

    return embeddings


def generate_question_embedding(question: str):

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[question]
    )

    embedding = np.array(
        [e.values for e in result.embeddings],
        dtype="float32"
    )

    return embedding