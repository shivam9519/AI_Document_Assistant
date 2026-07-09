import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question: str, context: str) -> str:

    prompt = f"""
You are an AI Document Assistant.

Answer ONLY using the provided context.

Rules:
1. Give a clear and concise answer.
2. Do not use outside knowledge.
3. If the answer is not found in the context, reply exactly:
"I couldn't find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text