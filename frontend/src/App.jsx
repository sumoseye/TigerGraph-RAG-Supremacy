// frontend/src/App.jsx
import React, { useState, useEffect } from 'react';
import QueryInput from './components/QueryInput';
import PipelineCard from './components/PipelineCard';
import MetricsTable from './components/MetricsTable';
import LoadingSpinner from './components/LoadingSpinner';
import { runAllPipelines, checkHealth } from './services/api';
import { FaTrophy, FaCheckCircle, FaRocket } from 'react-icons/fa';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [health, setHealth] = useState(null);

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const data = await checkHealth();
        setHealth(data);
      } catch (err) {
        console.error('Backend health check failed:', err);
      }
    };
    checkBackend();
  }, []);

  const handleQuery = async (query) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await runAllPipelines(query);
      setResults(data.results);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Unknown error';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f0f0f] via-[#1a1a1a] to-[#0f0f0f]">
      {/* Background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-[#4a7c59] rounded-full mix-blend-screen filter blur-3xl opacity-5"></div>
        <div className="absolute bottom-40 right-20 w-96 h-96 bg-[#4a7c59] rounded-full mix-blend-screen filter blur-3xl opacity-5"></div>
      </div>

      {/* Content */}
      <div className="relative z-10">
        {/* Header */}
        <header className="border-b border-[#2a2a2a] backdrop-blur-sm bg-[#0f0f0f]/50 sticky top-0 z-20">
          <div className="max-w-7xl mx-auto px-6 py-8">
            <div className="flex items-center gap-4 mb-2">
              <div className="p-2 rounded-lg bg-[#4a7c59]/10 border border-[#4a7c59]/30">
                <FaRocket className="text-2xl text-[#5a9c6f]" />
              </div>
              <h1 className="text-4xl font-bold text-white tracking-tight">
                Research Pipeline <span className="text-[#5a9c6f]">Battle</span>
              </h1>
            </div>
            <p className="text-[#999999] text-sm">Compare three AI research approaches in real-time</p>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-6 py-12">
          {/* Health Status */}
          {health && (
            <div className="mb-8 p-4 rounded-lg bg-card border border-[#2a2a2a] backdrop-blur">
              <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${health.status === 'healthy' ? 'bg-[#5a9c6f]' : 'bg-red-600'}`}></div>
                <span className="text-sm text-[#999999]">
                  {health.status === 'healthy' ? '✅ All systems operational' : '⚠️ System status check needed'}
                </span>
              </div>
            </div>
          )}

          {/* Query Input */}
          <div className="mb-12">
            <QueryInput onSubmit={handleQuery} loading={loading} />
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-8 p-4 rounded-lg bg-red-950/20 border border-red-900/30 backdrop-blur">
              <p className="text-red-400 text-sm">❌ {error}</p>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="flex justify-center">
              <LoadingSpinner />
            </div>
          )}

          {/* Results */}
          {results && !loading && (
            <>
              {/* Pipeline Cards Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12">
                <PipelineCard
                  data={results.llm_only}
                  title="Pipeline 1"
                  subtitle="LLM Only"
                  icon="⚡"
                  accentColor="from-[#4a7c59] to-[#5a9c6f]"
                />
                <PipelineCard
                  data={results.basic_rag}
                  title="Pipeline 2"
                  subtitle="Basic RAG"
                  icon="🔍"
                  accentColor="from-[#5a9c6f] to-[#6aac7f]"
                />
                <PipelineCard
                  data={results.tigergraph}
                  title="Pipeline 3"
                  subtitle="Multi-Agent"
                  icon="🤖"
                  accentColor="from-[#3a6c49] to-[#4a7c59]"
                />
              </div>

              {/* Metrics Table */}
              <MetricsTable results={results} />

              {/* Winner Badge */}
              <div className="mt-12 p-8 rounded-xl bg-gradient-to-r from-[#4a7c59]/20 to-[#5a9c6f]/20 border border-[#5a9c6f]/30 backdrop-blur-sm text-center">
                <div className="flex items-center justify-center gap-3 mb-3">
                  <FaTrophy className="text-2xl text-[#5a9c6f]" />
                  <h2 className="text-2xl font-bold text-white">Comparison Complete</h2>
                </div>
                <p className="text-[#999999] text-sm">Review the metrics above to see which pipeline works best for your use case</p>
              </div>
            </>
          )}

          {/* Empty State */}
          {!results && !loading && (
            <div className="text-center py-20">
              <div className="inline-block p-4 rounded-lg bg-[#4a7c59]/10 border border-[#4a7c59]/30 mb-4">
                <FaRocket className="text-5xl text-[#5a9c6f]" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">Ready to Compare</h3>
              <p className="text-[#999999] max-w-md mx-auto">
                Enter a research question above to see how different AI pipeline approaches handle the same query
              </p>
            </div>
          )}
        </main>

        {/* Footer */}
        <footer className="border-t border-[#2a2a2a] mt-20 py-8 backdrop-blur-sm bg-[#0f0f0f]/50">
          <div className="max-w-7xl mx-auto px-6 text-center text-sm text-[#666666]">
            <p>Research Pipeline Battle • Powered by Groq, ChromaDB & TigerGraph</p>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;