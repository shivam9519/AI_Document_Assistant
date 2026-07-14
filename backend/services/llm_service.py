import os
import logging

from dotenv import load_dotenv
from google import genai

load_dotenv()

logger = logging.getLogger(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question: str, context: str):

    prompt = f"""
You are an AI Document Assistant.

Answer ONLY using the provided context.

Rules:
1. Give a clear and concise answer.
2. Do not use outside knowledge.
3. Mention the page number(s) whenever possible.
4. If the answer is not found in the context, reply exactly:

"I couldn't find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    try:

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text

    except Exception as error:

        logger.exception("Gemini API Error")
        print("REAL ERROR:", error) 
        error_message = str(error)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

            return (
                "⚠️ Gemini API quota exceeded.\n\n"
                "Please try again later or use another API key."
            )

        return (
            "⚠️ Something went wrong while generating the answer.\n\n"
            "Please try again."
        )