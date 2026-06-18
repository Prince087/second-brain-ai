from fastapi import UploadFile , File, APIRouter
from pydantic import BaseModel
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

class NoteRequest(BaseModel):
    title: str
    content: str

@router.post("/ingest/notes")
def ingest_notes(note: NoteRequest):

    chunks = chunk_text(note.content)
    embeddings = embed_chunks(chunks)

    doc_id = note.title.replace(" ","_")
    result = store_chunks(chunks, embeddings, doc_id)

    return{
        "title": note.title,
        "num_chunks": len(chunks),
        "embedding_dim": len(embeddings[0]),
        "stored": result["stored"],
        "doc_id": result["doc_id"],
        "message": "Note successfully ingested into Second Brain!"
    }

from backend.retrieval.vector_store import get_or_create_collection

@router.get("/docs")
def list_docs():
    """
    Returns all unique documents stored in ChromaDB.
    """
    collection = get_or_create_collection()
    results = collection.get(include=["metadatas"])

    # Extract unique doc_ids
    doc_ids = list(set(
        meta["doc_id"] for meta in results["metadatas"]
    ))

    return {
        "total_chunks": len(results["metadatas"]),
        "documents": doc_ids,
        "num_documents": len(doc_ids)
    }


