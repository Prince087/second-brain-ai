import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import routes_ingest, routes_query

app = FastAPI(title="Second Brain AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://second-brain-ai.vercel.app",
        os.getenv("FRONTEND_URL", "") 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_ingest.router)
app.include_router(routes_query.router)

@app.get("/")
def root():
    return {"message": "Second Brain is alive 🧠"}

@app.get("/health")
def health():
    return {"status": "ok"}