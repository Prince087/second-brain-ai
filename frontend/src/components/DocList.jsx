import { useState } from "react";
import { listDocs, deleteDoc } from "../api";

export default function DocList({ refreshTrigger }) {
  const [docs, setDocs] = useState(null);
  const [loading, setLoading] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [error, setError] = useState(null);

  async function fetchDocs() {
    setLoading(true);
    setError(null);
    try {
      const data = await listDocs();
      setDocs(data);
    } catch {
      setError("Could not load documents. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(doc_id) {
    if (!confirm(`Delete "${doc_id}" from your brain?`)) return;
    setDeletingId(doc_id);
    try {
      await deleteDoc(doc_id);
      // Refresh the list after deletion
      const data = await listDocs();
      setDocs(data);
    } catch {
      setError(`Failed to delete "${doc_id}"`);
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <div className="space-y-2">
      <button
        onClick={fetchDocs}
        className="w-full py-1.5 px-3 text-sm border border-gray-300 rounded-lg
          hover:bg-gray-50 transition text-gray-600"
      >
        {loading ? "Loading..." : "🔄 Refresh Documents"}
      </button>

      {error && <p className="text-xs text-red-500">{error}</p>}

      {docs && (
        <div className="space-y-1">
          <p className="text-xs text-gray-400">
            {docs.total_chunks} chunks · {docs.num_documents} documents
          </p>
          {docs.documents.length === 0 && (
            <p className="text-xs text-gray-400 italic">No documents yet.</p>
          )}
          {docs.documents.map((doc) => (
            <div
              key={doc.doc_id}
              className="flex items-center justify-between bg-gray-50
                border border-gray-200 rounded-lg px-3 py-2"
            >
              <div>
                <p className="text-sm text-gray-700 font-medium">📄 {doc.doc_id}</p>
                <p className="text-xs text-gray-400">{doc.num_chunks} chunks</p>
              </div>
              <button
                onClick={() => handleDelete(doc.doc_id)}
                disabled={deletingId === doc.doc_id}
                className="text-xs text-red-400 hover:text-red-600
                  disabled:opacity-50 transition px-2 py-1 rounded
                  hover:bg-red-50"
              >
                {deletingId === doc.doc_id ? "Deleting..." : "🗑️"}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}