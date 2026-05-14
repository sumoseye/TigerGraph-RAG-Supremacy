// frontend/src/App.jsx
import React, { useState, useEffect } from 'react';
import QueryInput from './components/QueryInput';
import PipelineCard from './components/PipelineCard';
import MetricsTable from './components/MetricsTable';
import LoadingSpinner from './components/LoadingSpinner';
import { runAllPipelines, checkHealth } from './services/api';
import { FaTrophy, FaRocket, FaCheckCircle } from 'react-icons/fa';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [health, setHealth] = useState(null);

  useEffect(() => {
    // Check backend health on mount
    const checkBackend = async () => {
      try {
        const data = await checkHealth();
        setHealth(data);
        console.log('✅ Backend is healthy:', data);
      } catch (err) {
        console.error('❌ Backend health check failed:', err);
        setHealth({ status: 'unhealthy' });
      }
    };

    checkBackend();
  }, []);

  const handleQuery = async (query) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      console.log('🚀 Submitting query:', query);
      const data = await runAllPipelines(query);
      console.log('✅ Results received:', data);
      setResults(data.results);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Unknown error';
      setError(errorMsg);
      console.error('❌ Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-4 md:p-8">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center gap-3 mb-4">
          <FaRocket className="text-5xl md:text-6xl text-white animate-bounce" />
          <h1 className="text-4xl md:text-5xl font-bold text-white">
            ⚔️ Research Pipeline Battle
          </h1>
        </div>
        <p className="text-lg text-white/90 mb-2">
          Compare AI Pipeline Approaches with Groq
        </p>
        <div className="flex items-center justify-center gap-3 text-white/80 text-sm flex-wrap justify-center">
          <span className="flex items-center gap-1">
            <FaCheckCircle className="text-green-400" /> 100% Free
          </span>
          <span>•</span>
          <span className="flex items-center gap-1">
            <FaCheckCircle className="text-green-400" /> Cloud API
          </span>
          <span>•</span>
          <span className="flex items-center gap-1">
            <FaCheckCircle className="text-green-400" /> Ultra-Fast
          </span>
        </div>
      </div>

      {/* Backend Status */}
      {health && (
        <div className={`max-w-4xl mx-auto mb-6 rounded-lg p-4 text-sm border ${
          health.status === 'healthy' 
            ? 'bg-green-50/20 border-green-300/50 text-green-100' 
            : 'bg-red-50/20 border-red-300/50 text-red-100'
        }`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${health.status === 'healthy' ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`}></div>
              <span className="font-semibold">
                {health.status === 'healthy' ? '✅ Backend Ready' : '❌ Backend Offline'}
              </span>
            </div>
            <div className="text-xs">
              {health.api && `API: ${health.api}`}
            </div>
          </div>
        </div>
      )}

      {/* Query Input */}
      <QueryInput onSubmit={handleQuery} loading={loading} />

      {/* Error Display */}
      {error && (
        <div className="max-w-4xl mx-auto mb-8 bg-red-100/20 border border-red-400/50 text-red-100 px-6 py-4 rounded-xl backdrop-blur-sm">
          <strong>❌ Error:</strong> {error}
        </div>
      )}

      {/* Loading State */}
      {loading && <LoadingSpinner message="Calling Groq API..." />}

      {/* Results */}
      {results && !loading && (
        <>
          {/* Pipeline Cards */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-7xl mx-auto mb-8">
            <PipelineCard
              data={results.llm_only}
              title="Pipeline 1: LLM Only"
              icon="brain"
              color="border-blue-500"
            />
            <PipelineCard
              data={results.basic_rag}
              title="Pipeline 2: Basic RAG"
              icon="database"
              color="border-green-500"
            />
            <PipelineCard
              data={results.tigergraph}
              title="Pipeline 3: TigerGraph"
              icon="graph"
              color="border-purple-500"
            />
          </div>

          {/* Metrics Table */}
          <div className="max-w-7xl mx-auto mb-8">
            <MetricsTable results={results} />
          </div>

          {/* Winner Badge */}
          <div className="max-w-4xl mx-auto bg-gradient-to-r from-yellow-400 via-orange-500 to-pink-500 rounded-xl p-6 text-center shadow-2xl">
            <div className="flex items-center justify-center gap-3 text-white mb-2">
              <FaTrophy className="text-4xl animate-bounce" />
              <h2 className="text-2xl md:text-3xl font-bold">Pipeline 1 is Ready!</h2>
            </div>
            <p className="text-white/90">
              Powered by Groq Llama 3.1 • Free • Fast • Professional Demo Ready
            </p>
          </div>
        </>
      )}

      {/* Empty State */}
      {!results && !loading && (
        <div className="max-w-4xl mx-auto text-center mt-12 bg-white/10 backdrop-blur-md rounded-xl p-12 border border-white/20">
          <FaRocket className="text-6xl text-white/50 mx-auto mb-4" />
          <h3 className="text-2xl font-bold text-white mb-2">Ready to Compare Pipelines!</h3>
          <p className="text-white/80">Enter your research question above and watch the magic happen.</p>
        </div>
      )}

      {/* Footer */}
      <div className="max-w-7xl mx-auto mt-12 text-center text-white/60 text-sm border-t border-white/10 pt-6">
        <p>Research Pipeline Battle • Powered by Groq API • Built with React + FastAPI</p>
        <p className="text-xs text-white/40 mt-2">💡 Judges: Just visit this URL and start testing!</p>
      </div>
    </div>
  );
}

export default App;