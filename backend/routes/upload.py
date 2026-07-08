from fastapi import APIRouter, UploadFile, File
from backend.services.pdf_service import (
    save_file,
    extract_text_from_pdf,
    chunk_text
)

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    saved_path = save_file(file)

    text = extract_text_from_pdf(saved_path)

    chunks = chunk_text(text)

    return {
        "filename": file.filename,
        "total_chunks": len(chunks),
        "first_chunk": chunks[0]
    }