import { useState } from "react";
import { listDocs } from "../api";

export default function DocList({ refreshTrigger }) {
  const [docs, setDocs] = useState(null);
  const [loading, setLoading] = useState(false);

  async function fetchDocs() {
    setLoading(true);
    try {
      const data = await listDocs();
      setDocs(data);
    } finally {
      setLoading(false);
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
      {docs && (
        <div className="space-y-1">
          <p className="text-xs text-gray-400">{docs.total_chunks} total chunks · {docs.num_documents} documents</p>
          {docs.documents.map((doc) => (
            <div key={doc} className="text-sm text-gray-600 bg-gray-50 rounded px-3 py-1.5">
              📄 {doc}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}