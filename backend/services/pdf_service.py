from pathlib import Path
from fastapi import UploadFile
import shutil
import fitz

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_file(file: UploadFile) -> str:
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)

def extract_text_from_pdf(file_path: str):

    document = fitz.open(file_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        page_text = page.get_text("text")
        page_text = page_text.replace("\n", " ")
        page_text = " ".join(page_text.split())

        pages.append({
            "page": page_number,
            "text": page_text
        })

    document.close()

    return pages

def chunk_text(pages, chunk_size=500, overlap=100):

    if overlap >= chunk_size:
        raise ValueError(
        "overlap must be smaller than chunk_size"
    )

    chunks = []

    step = chunk_size - overlap

    for page in pages:

        page_number = page["page"]
        text = page["text"]

        for i in range(0, len(text), step):

            chunk = text[i:i + chunk_size]

            if chunk.strip():

                chunks.append({
                    "page": page_number,
                    "text": chunk
                })

    return chunks
