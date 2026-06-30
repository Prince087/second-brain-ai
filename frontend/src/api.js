const API_URL = "http://127.0.0.1:8000";

export async function ingestPDF(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_URL}/ingest/pdf`, {
    method: "POST",
    body: formData,
  });
  return res.json();
}

export async function ingestNote(title, content) {
  const res = await fetch(`${API_URL}/ingest/notes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content }),
  });
  return res.json();
}

export async function queryBrain(question, n_results = 3) {
  const res = await fetch(`${API_URL}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, n_results }),
  });
  return res.json();
}

export async function listDocs() {
  const res = await fetch(`${API_URL}/docs`);
  return res.json();
}