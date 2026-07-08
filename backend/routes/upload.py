from fastapi import APIRouter, UploadFile, File
from backend.services.pdf_service import save_file

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    saved_path = save_file(file)

    return {
        "message": "PDF uploaded successfully",
        "path": saved_path,
        "filename": file.filename
    }