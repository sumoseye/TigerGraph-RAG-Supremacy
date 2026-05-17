// frontend/src/App.jsx
import React, { useState, useEffect } from 'react';
import QueryInput from './components/QueryInput';
import PipelineCard from './components/PipelineCard';
import MetricsTable from './components/MetricsTable';
import LoadingSpinner from './components/LoadingSpinner';
import { runAllPipelines, checkHealth } from './services/api';

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
    <div className="bg-primary min-h-screen flex flex-col">
      {/* Main Content - Centered */}
      <main className="flex-1 flex flex-col items-center justify-center px-6 py-12">
        <div className="w-full max-w-7xl">
          {/* Title - Centered Above Search */}
          <h1 className="heading-xl text-black text-center mb-8">
            One Query, Three Approaches
          </h1>

          {/* Query Input Section */}
          <div className="mb-12">
            <QueryInput onSubmit={handleQuery} loading={loading} hideOptions={loading || results} />
          </div>

          {/* Error Message */}
          {error && (
            <div className="neoborder border-rust bg-rust/15 p-6 mb-8 animate-in rounded-2xl">
              <div className="flex items-start gap-4">
                <span className="text-3xl">⚠️</span>
                <div>
                  <h3 className="heading-sm text-rust mb-2">ERROR</h3>
                  <p className="text-black font-medium">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div style={{ marginTop: '80px' }}>
              <LoadingSpinner />
            </div>
          )}

          {/* Results Section - TABLE FIRST, THEN CARDS */}
          {results && !loading && (
            <div style={{ marginTop: '4rem', marginBottom: '4rem' }}>
              {/* Metrics Table - COMES FIRST */}
              <MetricsTable results={results} />

              {/* Pipeline Cards - COMES BELOW TABLE */}
              <div 
                className="grid grid-cols-1 lg:grid-cols-3 gap-8"
                style={{ 
                  paddingLeft: '2rem',
                  paddingRight: '2rem',
                  marginTop: '4rem'
                }}
              >
                <PipelineCard
                  data={results.llm_only}
                  title="LLM Only"
                  subtitle="Direct LLM Response"
                  accentColor="#4A90E2"
                />
                <PipelineCard
                  data={results.basic_rag}
                  title="RAG"
                  subtitle="Retrieval Augmented"
                  accentColor="#D4A373"
                />
                <PipelineCard
                  data={results.tigergraph}
                  title="Multi-Agent"
                  subtitle="Graph-Enhanced RAG"
                  accentColor="#6B8E23"
                />
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Black Border Above Footer */}
      <div className="border-t-8 border-black"></div>

      {/* Footer - Minimal with Pattern */}
      <footer className="bg-black text-white py-12">
        <div className="footer-pattern mb-8"></div>
        <div className="text-center">
          <h2 className="text-5xl font-bold mb-3 text-orange tracking-tight">PAPERCUT</h2>
          <p className="text-lg text-orange">Slash through messy research.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;