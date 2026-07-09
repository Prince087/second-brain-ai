import os
import chromadb
from typing import List

# Use persistent disk path on Render, local path in development
CHROMA_PATH = os.getenv("CHROMA_PATH", "backend/chroma_db")

client = chromadb.PersistentClient(path=CHROMA_PATH)

def get_or_create_collection(collection_name: str = "second_brain"):
    collection = client.get_or_create_collection(
        name = collection_name,
        metadata = {"hnsw:space" : "cosine"}

    )
    return collection

def store_chunks(chunks: List[str], embeddings: List[List[float]], doc_id: str, collection_name: str = "second_brain"):
    collection = get_or_create_collection(collection_name)
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

     # Build metadata for each chunk (so we know which doc it came from)
    metadatas = [{"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )

    return {"stored": len(chunks), "doc_id": doc_id}

def query_collection(
    query_embedding: List[float],
    n_results: int = 5,
    collection_name: str = "second_brain"
):
    """
    Takes a query vector, returns the top-n most similar chunks.
    """
    collection = get_or_create_collection(collection_name)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    return results

def delete_document(doc_id: str, collection_name: str = "second_brain") -> dict:

    
    #Deletes all chunks belonging to a specific document.
    
    collection = get_or_create_collection(collection_name)

    # Get all chunk IDs that belong to this doc
    results = collection.get(where={"doc_id": doc_id})

    if not results["ids"]:
        return {"deleted": 0, "doc_id": doc_id, "message": "Document not found"}

    # Delete them all
    collection.delete(ids=results["ids"])

    return {
        "deleted": len(results["ids"]),
        "doc_id": doc_id,
        "message": f"Deleted {len(results['ids'])} chunks for '{doc_id}'"
}
