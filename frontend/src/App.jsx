import { useState } from "react";
import PDFUpload from "./components/PDFUpload";
import NoteInput from "./components/NoteInput";
import QueryBox from "./components/QueryBox";
import DocList from "./components/DocList";

export default function App() {
  const [activeTab, setActiveTab] = useState("pdf");
  const [refreshKey, setRefreshKey] = useState(0);

  function handleIngestSuccess() {
    setRefreshKey((k) => k + 1);
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
        <div className="max-w-screen-xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">🧠 Second Brain AI</h1>
            <p className="text-sm text-gray-500">Your personal AI knowledge base</p>
          </div>
          <span className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
            ● Live
          </span>
        </div>
      </header>

      <div className="max-w-screen-xl mx-auto px-6 py-6 flex gap-6">

        {/* Sidebar */}
        <aside className="w-96 shrink-0 space-y-4">
          {/* Ingest card */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
            <h2 className="text-sm font-semibold text-gray-800 mb-4">📥 Add to Your Brain</h2>
            {/* Tabs */}
            <div className="flex gap-1 mb-4 bg-gray-100 rounded-lg p-1">
              {["pdf", "note"].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`flex-1 py-1.5 text-sm font-medium rounded-md transition
                    ${activeTab === tab
                      ? "bg-white text-blue-600 shadow-sm"
                      : "text-gray-500 hover:text-gray-700"
                    }`}
                >
                  {tab === "pdf" ? "📄 PDF" : "📝 Note"}
                </button>
              ))}
            </div>
            {activeTab === "pdf"
              ? <PDFUpload onSuccess={handleIngestSuccess} />
              : <NoteInput onSuccess={handleIngestSuccess} />
            }
          </div>

          {/* Doc list card */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
            <h2 className="text-sm font-semibold text-gray-800 mb-3">📚 Your Documents</h2>
            <DocList refreshTrigger={refreshKey} />
          </div>
        </aside>

        {/* Main content */}
        <main className="flex-1 bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">💬 Ask Your Brain</h2>
          <QueryBox />
        </main>

      </div>
    </div>
  );
}