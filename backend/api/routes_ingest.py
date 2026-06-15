from fastapi import UploadFile , File, APIRouter
import shutil
import os

from backend.ingestion.pdf_parser import extract_text_from_pdf
from backend.ingestion.chunker import chunk_text

router = APIRouter()

UPLOAD_DIR = r"backend\uploads"

@router.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)

    chunks = chunk_text(extracted_text)

    return {
        "filename" : file.filename,
        "num_characters" : len(extracted_text),
        "num_chunks" : len(chunks),
        "first_3_chunks" : chunks[:3]
    }


