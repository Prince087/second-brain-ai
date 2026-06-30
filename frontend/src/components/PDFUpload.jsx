import { useState } from "react";
import { ingestPDF } from "../api";

export default function PDFUpload({ onSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  async function handleUpload() {
    if (!file) return;
    setLoading(true);
    setMessage(null);
    try {
      const data = await ingestPDF(file);
      setMessage({ type: "success", text: `✅ Ingested ${data.num_chunks} chunks from "${data.filename}"` });
      onSuccess?.();
    } catch {
      setMessage({ type: "error", text: "❌ Upload failed. Is the backend running?" });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-gray-700">Upload PDF</label>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
        className="block w-full text-sm text-gray-500 file:mr-3 file:py-2 file:px-4
          file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-700
          hover:file:bg-blue-100 cursor-pointer"
      />
      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="w-full py-2 px-4 bg-blue-600 text-white rounded-lg font-medium
          hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        {loading ? "Ingesting..." : "Ingest PDF"}
      </button>
      {message && (
        <p className={`text-sm ${message.type === "success" ? "text-green-600" : "text-red-500"}`}>
          {message.text}
        </p>
      )}
    </div>
  );
}