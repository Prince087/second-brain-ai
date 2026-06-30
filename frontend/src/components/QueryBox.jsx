import { useState } from "react";
import { queryBrain } from "../api";

export default function QueryBox() {
  const [question, setQuestion] = useState("");
  const [nResults, setNResults] = useState(3);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleQuery() {
    if (!question.trim()) return;
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const data = await queryBrain(question, nResults);
      setResult(data);
    } catch {
      setError("❌ Query failed. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-3">
        <input
          type="text"
          placeholder="Ask anything across your documents..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleQuery()}
          className="flex-1 px-4 py-3 border border-gray-300 rounded-xl text-sm
            focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
        />
        <button
          onClick={handleQuery}
          disabled={!question.trim() || loading}
          className="px-6 py-3 bg-blue-600 text-white rounded-xl font-medium
            hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-sm"
        >
          {loading ? "Thinking..." : "Ask 🔍"}
        </button>
      </div>

      <div className="flex items-center gap-3">
        <label className="text-sm text-gray-500">Sources to retrieve:</label>
        <input
          type="range" min={1} max={10} value={nResults}
          onChange={(e) => setNResults(Number(e.target.value))}
          className="w-32"
        />
        <span className="text-sm font-medium text-blue-600">{nResults}</span>
      </div>

      {error && <p className="text-red-500 text-sm">{error}</p>}

      {result && (
        <div className="space-y-4">
          {/* Answer card */}
          <div className="bg-blue-50 border border-blue-200 rounded-xl p-5">
            <h3 className="text-sm font-semibold text-blue-700 mb-2">🤖 Answer</h3>
            <p className="text-gray-800 leading-relaxed">{result.answer}</p>
          </div>

          {/* Sources */}
          <div>
            <h3 className="text-sm font-semibold text-gray-600 mb-2">📎 Sources</h3>
            <div className="space-y-2">
              {result.sources.map((source, i) => (
                <details key={i} className="bg-gray-50 border border-gray-200 rounded-lg">
                  <summary className="px-4 py-2 cursor-pointer text-sm font-medium
                    text-gray-700 hover:bg-gray-100 rounded-lg">
                    Source {i + 1} — <span className="text-blue-600">{source.doc_id}</span>
                    {" "}· chunk #{source.chunk_index}
                    {" "}· score: <span className="text-green-600">{source.similarity_score}</span>
                  </summary>
                  <div className="px-4 py-3 text-sm text-gray-600 border-t border-gray-200">
                    {source.chunk}
                  </div>
                </details>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}