import { useState } from "react";
import { ingestNote } from "../api";

export default function NoteInput({ onSuccess }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  async function handleIngest() {
    if (!title || !content) return;
    setLoading(true);
    setMessage(null);
    try {
      const data = await ingestNote(title, content);
      setMessage({ type: "success", text: `✅ Ingested "${data.title}" as ${data.num_chunks} chunks` });
      setTitle("");
      setContent("");
      onSuccess?.();
    } catch {
      setMessage({ type: "error", text: "❌ Failed. Is the backend running?" });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-gray-700">Add a Note</label>
      <input
        type="text"
        placeholder="Note title..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm
          focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <textarea
        placeholder="Note content..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
        rows={5}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm
          focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
      />
      <button
        onClick={handleIngest}
        disabled={!title || !content || loading}
        className="w-full py-2 px-4 bg-blue-600 text-white rounded-lg font-medium
          hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        {loading ? "Ingesting..." : "Ingest Note"}
      </button>
      {message && (
        <p className={`text-sm ${message.type === "success" ? "text-green-600" : "text-red-500"}`}>
          {message.text}
        </p>
      )}
    </div>
  );
}