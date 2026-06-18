from fastapi import FastAPI
from backend.api import routes_ingest , routes_query

app = FastAPI(title = "Second Brain AI")

app.include_router(routes_ingest.router)
app.include_router(routes_query.router)

@app.get("/")
def root():
    return {"message": "Second Brain AI is alive!"}

@app.get("/health")
def health():
    return {"status": "ok"}

            