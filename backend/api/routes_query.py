from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.ingestion.embedder import embed_single
from backend.retrieval.vector_store import query_collection
from backend.generation.llm import generate_answer

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    n_results: int = 5

@router.post("/query")
def query_brain(request: QueryRequest):
    # Embed the question using the same model
    try:
        query_embedding = embed_single(request.question)

        # Find most similar chunks
        results = query_collection(query_embedding, n_results=request.n_results)

        # Format response cleanly
        chunks = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

    
        retrieved_chunks = [
                {
                    "chunk": chunks[i],
                    "doc_id": metadatas[i]["doc_id"],
                  "chunk_index": metadatas[i]["chunk_index"],
                    "similarity_score": round(1 - distances[i], 4)
                }
                for i in range(len(chunks))
            ]
    

        answer = generate_answer(request.question, retrieved_chunks)

        return {
            "question": request.question,
            "answer": answer,
            "sources": retrieved_chunks
        }

    except HTTPException:
        raise  # re-raise HTTP exceptions as-is
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

