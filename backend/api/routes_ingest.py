from fastapi import UploadFile , File, APIRouter
import shutil
import os

from backend.ingestion.pdf_parser import extract_text_from_pdf
from backend.ingestion.chunker import chunk_text
from backend.ingestion.embedder import embed_chunks
from backend.retrieval.vector_store import store_chunks

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

    # Store in ChromaDB
    doc_id = os.path.splitext(file.filename)[0]  # "Unit 1.pdf" → "Unit 1"
    result = store_chunks(chunks, embeddings, doc_id)


    return {
        "filename": file.filename,
        "num_chunks": len(chunks),
        "embedding_dim": len(embeddings[0]),
        "stored": result["stored"],
        "doc_id": result["doc_id"],
        "message": "PDF successfully ingested into Second Brain!"
    }


