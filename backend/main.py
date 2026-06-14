from fastapi import FastAPI
from backend.api import routes_ingest

app = FastAPI(title = "Second Brain AI")

app.include_router(routes_ingest.router)

@app.get("/")
def root():
    return {"message": "Second Brain AI is alive!"}

@app.get("/health")
def health():
    return {"status": "ok"}

            