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

from backend.retrieval.vector_store import store_chunks, get_or_create_collection, delete_document
from fastapi import HTTPException

@router.get("/docs")
def list_docs():
    """Returns all unique documents stored in ChromaDB."""
    collection = get_or_create_collection()
    results = collection.get(include=["metadatas"])

    if not results["metadatas"]:
        return {"total_chunks": 0, "documents": [], "num_documents": 0}

    # Count chunks per document
    doc_chunk_counts = {}
    for meta in results["metadatas"]:
        doc_id = meta["doc_id"]
        doc_chunk_counts[doc_id] = doc_chunk_counts.get(doc_id, 0) + 1

    return {
        "total_chunks": len(results["metadatas"]),
        "num_documents": len(doc_chunk_counts),
        "documents": [
            {"doc_id": doc_id, "num_chunks": count}
            for doc_id, count in doc_chunk_counts.items()
        ]
    }

@router.delete("/docs/{doc_id}")
def delete_doc(doc_id: str):
    """Deletes all chunks for a specific document."""
    result = delete_document(doc_id)
    if result["deleted"] == 0:
        raise HTTPException(status_code=404, detail=f"Document '{doc_id}' not found")
    return result


