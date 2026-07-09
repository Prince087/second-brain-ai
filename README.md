# 🧠 Second Brain AI

> A personal knowledge management system powered by RAG (Retrieval-Augmented Generation). Upload PDFs and notes, then ask questions across all your documents — get AI-generated answers grounded in your own knowledge base.

![Second Brain AI](https://img.shields.io/badge/Built%20With-FastAPI%20%7C%20React%20%7C%20ChromaDB%20%7C%20Groq-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 What It Does

Most AI assistants answer from general training data. **Second Brain AI answers from YOUR documents.**

- 📄 Upload any PDF or paste plain text notes
- 🔍 Semantic search finds relevant passages by *meaning*, not just keywords  
- 🤖 Groq LLM synthesizes a grounded answer from retrieved context
- 📎 Every answer shows exactly which documents and chunks it came from
- 🗑️ Manage your knowledge base — add and delete documents anytime

---

## 🏗️ Architecture

```
User Question
     │
     ▼
Embed question (all-MiniLM-L6-v2)
     │
     ▼
ChromaDB semantic search → top-k relevant chunks
     │
     ▼
RAG Prompt (chunks + question) → Groq LLM (llama-3.1-8b-instant)
     │
     ▼
Grounded answer + source citations
```

**Ingestion Pipeline:**
```
PDF / Note → Extract text → Chunk (500 chars, 50 overlap) → Embed → Store in ChromaDB
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | FastAPI + Uvicorn | REST API server |
| PDF Parsing | PyMuPDF (fitz) | Extract text from PDFs |
| Text Splitting | LangChain RecursiveCharacterTextSplitter | Smart overlapping chunks |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) | Local 384-dim vector embeddings |
| Vector DB | ChromaDB | Persistent vector storage + similarity search |
| LLM | Groq API (llama-3.1-8b-instant) | Answer generation |
| Frontend | React 19 + Vite + Tailwind CSS v4 | UI |

---

## ✨ Features

- **Multi-document search** — query across all uploaded documents simultaneously
- **Semantic search** — finds relevant content by meaning, not keyword matching
- **Source citations** — every answer shows which document and chunk it came from
- **PDF ingestion** — upload any PDF, text is extracted and indexed automatically
- **Note ingestion** — paste plain text notes directly into your knowledge base
- **Document management** — view all stored documents with chunk counts, delete anytime
- **Hallucination prevention** — LLM is prompted to only answer from provided context
- **Local embeddings** — no OpenAI API needed for embeddings, runs 100% free locally

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- A free [Groq API key](https://console.groq.com)

### 1. Clone the repo

```bash
git clone https://github.com/Prince087/second-brain-ai.git
cd second-brain-ai
```

### 2. Set up the backend

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
# Create .env file in the project root
cp .env.example .env
```

Open `.env` and add your Groq API key:
```
GROQ_API_KEY=gsk_your_key_here
```

### 4. Start the backend

```bash
uvicorn backend.main:app --reload
```

Backend runs at `http://127.0.0.1:8000`  
API docs at `http://127.0.0.1:8000/docs`

### 5. Set up and start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## 📁 Project Structure

```
second-brain-ai/
│
├── backend/
│   ├── main.py                   # FastAPI app entry point + CORS
│   ├── ingestion/
│   │   ├── pdf_parser.py         # PyMuPDF text extraction
│   │   ├── chunker.py            # RecursiveCharacterTextSplitter
│   │   └── embedder.py           # sentence-transformers embeddings
│   ├── retrieval/
│   │   └── vector_store.py       # ChromaDB store/query/delete
│   ├── generation/
│   │   └── llm.py                # Groq RAG prompt + answer generation
│   └── api/
│       ├── routes_ingest.py      # POST /ingest/pdf, POST /ingest/notes
│       └── routes_query.py       # POST /query
│
├── frontend/
│   └── src/
│       ├── App.jsx               # Main layout
│       ├── api.js                # All API calls in one place
│       └── components/
│           ├── PDFUpload.jsx     # PDF file upload
│           ├── NoteInput.jsx     # Plain text note input
│           ├── QueryBox.jsx      # Question input + answer display
│           └── DocList.jsx       # Document list + delete
│
├── .env.example                  # Environment variable template
├── requirements.txt              # Python dependencies
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ingest/pdf` | Upload and index a PDF file |
| `POST` | `/ingest/notes` | Ingest a plain text note |
| `POST` | `/query` | Ask a question, get AI answer + sources |
| `GET` | `/documents` | List all indexed documents |
| `DELETE` | `/documents/{doc_id}` | Remove a document from the knowledge base |
| `GET` | `/health` | Health check |

---

## 💡 How RAG Works (in plain English)

Traditional search matches **keywords**. If you search "moral behaviour" it won't find a passage about "ethical conduct" even though they mean the same thing.

RAG (Retrieval-Augmented Generation) uses **meaning**:

1. Every chunk of your documents is converted into a vector (list of 384 numbers representing its meaning)
2. Your question is converted into a vector the same way
3. ChromaDB finds the chunks whose vectors are mathematically closest to your question's vector
4. Those chunks are passed to the LLM as context
5. The LLM generates an answer using *only* that context — grounded in your documents, not hallucinated

---

## 🔮 Future Improvements

- [ ] User authentication — personal knowledge bases per user
- [ ] Support for `.docx`, `.txt`, `.md` file formats
- [ ] Conversation history — multi-turn Q&A
- [ ] Deploy to cloud — Render / AWS EC2
- [ ] Re-ranking retrieved chunks for better precision
- [ ] Streaming responses from the LLM

---

## 👨‍💻 Author

**Prince** — B.Tech CSE (Data Science), Lovely Professional University  
Built as part of an AI Engineering portfolio project.

[GitHub](https://github.com/Prince087) · [LinkedIn](#)

---

## 📄 License

MIT License — feel free to use this project as a reference or starting point.