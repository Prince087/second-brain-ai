from fastapi import UploadFile , File, APIRouter
import shutil
import os

from backend.ingestion.pdf_parser import extract_text_from_pdf
from backend.ingestion.chunker import chunk_text
from backend.ingestion.embedder import embed_chunks

router = APIRouter()

UPLOAD_DIR = r"backend\uploads"

@router.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)

    chunks = chunk_text(extracted_text)

    embeddings = embed_chunks(chunks)

    return {
        "filename": file.filename,
        "num_chunks": len(chunks),
        "embedding_dim": len(embeddings[0]),
        "sample_chunk": chunks[0],
        "sample_vector_preview": embeddings[0][:5]
    }


