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
    <div className="bg-primary min-h-screen">
      {/* Hero Header - CENTERED & COMPACT */}
      <header className="border-b-8 border-black bg-primary relative overflow-hidden">
        {/* Decorative Elements */}
        <div className="absolute top-0 right-0 w-40 h-40 bg-orange/5 border-l-4 border-b-4 border-orange"></div>
        <div className="absolute top-32 left-0 w-32 h-32 bg-sage/5 border-r-4 border-b-4 border-sage"></div>

        <div className="max-w-7xl mx-auto px-12 py-12 relative z-10 text-center">
          {/* Title - Single Line, Centered */}
          <h1 className="heading-xl text-black inline-block mb-6">
            RESEARCH PIPELINE <span className="text-orange">BATTLE</span>
          </h1>
          
          {/* Divider */}
          <div className="flex justify-center mb-6">
            <div className="divider-line-orange"></div>
          </div>

          <p className="text-lg font-semibold text-black mx-auto max-w-2xl">
            One query. Three approaches. Real-time comparison.
          </p>

          {/* Health Badge */}
          {health && (
            <div className={`neoborder inline-block mt-6 ${health.status === 'healthy' ? 'bg-sage/20 border-sage' : 'bg-rust/20 border-rust'}`}>
              <div className="px-6 py-3 flex items-center gap-3">
                <div className={`w-3 h-3 ${health.status === 'healthy' ? 'bg-sage' : 'bg-rust'}`}></div>
                <span className="font-bold text-black text-xs uppercase tracking-wider">
                  {health.status === 'healthy' ? '✓ Ready' : '⚠ Check Status'}
                </span>
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-12">
        {/* Query Section - NO TOP BORDER */}
        <section className="py-12 animate-in">
          <QueryInput onSubmit={handleQuery} loading={loading} />
        </section>

        {/* Error Message */}
        {error && (
          <div className="neoborder border-rust bg-rust/15 p-8 mb-12 animate-in">
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
          <div className="py-24">
            <LoadingSpinner />
          </div>
        )}

        {/* Results Section */}
        {results && !loading && (
          <>
            {/* Results Header */}
            <section className="py-12 border-t-4 border-black">
              <h2 className="heading-lg text-black mb-3">Results</h2>
              <div className="divider-line-sage"></div>
            </section>

            {/* Pipeline Cards - 3 Column Grid */}
            <section className="grid grid-cols-3 gap-8 pb-12">
              <PipelineCard
                data={results.llm_only}
                title="PIPELINE 1"
                subtitle="LLM ONLY"
                accentColor="#4A90E2"
              />
              <PipelineCard
                data={results.basic_rag}
                title="PIPELINE 2"
                subtitle="BASIC RAG"
                accentColor="#D4A373"
              />
              <PipelineCard
                data={results.tigergraph}
                title="PIPELINE 3"
                subtitle="MULTI-AGENT"
                accentColor="#6B8E23"
              />
            </section>

            {/* Metrics Section */}
            <section className="py-12 border-t-4 border-black">
              <h2 className="heading-lg text-black mb-6">Metrics & Benchmarks</h2>
              <div className="divider-line"></div>
              <div className="mt-8">
                <MetricsTable results={results} />
              </div>
            </section>

            {/* Winner Section */}
            <section className="neoborder-thick border-orange bg-orange/15 p-12 my-12 animate-pulse-brut">
              <div className="mb-4">
                <h2 className="heading-md text-orange mb-2">🏆 COMPARISON COMPLETE</h2>
                <div className="divider-line-orange"></div>
              </div>
              <p className="text-lg font-semibold text-black leading-relaxed">
                All three pipelines executed in parallel. Use the metrics above to choose the best approach for your research needs.
              </p>
            </section>
          </>
        )}

        {/* Empty State */}
        {!results && !loading && (
          <section className="py-32 text-center">
            <div className="inline-block neoborder-thick border-orange bg-orange/25 p-12 mb-8 animate-float">
              <span className="text-7xl">🚀</span>
            </div>
            <h2 className="heading-lg text-black mb-4">Ready to Compare</h2>
            <p className="text-lg font-semibold text-black max-w-xl mx-auto">
              Enter a research question above to benchmark all three approaches.
            </p>
          </section>
        )}

        {/* Footer Spacing */}
        <div className="pb-12"></div>
      </main>

      {/* Footer */}
      <footer className="border-t-8 border-black bg-black text-primary mt-12">
        <div className="max-w-7xl mx-auto px-12 py-12">
          <h3 className="heading-sm text-orange mb-2">RESEARCH PIPELINE BATTLE</h3>
          <p className="font-semibold text-primary text-sm">
            Powered by Groq • ChromaDB • TigerGraph Savanna
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;a// frontend/src/App.jsx
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
        <div className="w-full max-w-4xl">
          {/* Title - Centered Above Search */}
          <h1 className="heading-xl text-black text-center mb-8">
            One Query, Three Approaches
          </h1>

          {/* Query Input Section */}
          <div className="mb-12">
            <QueryInput onSubmit={handleQuery} loading={loading} />
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
            <div className="py-16">
              <LoadingSpinner />
            </div>
          )}

          {/* Results Section */}
          {results && !loading && (
            <div className="space-y-8">
              {/* Pipeline Cards - 3 Column Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <PipelineCard
                  data={results.llm_only}
                  title="PIPELINE 1"
                  subtitle="LLM ONLY"
                  accentColor="#4A90E2"
                />
                <PipelineCard
                  data={results.basic_rag}
                  title="PIPELINE 2"
                  subtitle="BASIC RAG"
                  accentColor="#D4A373"
                />
                <PipelineCard
                  data={results.tigergraph}
                  title="PIPELINE 3"
                  subtitle="MULTI-AGENT"
                  accentColor="#6B8E23"
                />
              </div>

              {/* Metrics Table */}
              <div className="mt-8">
                <MetricsTable results={results} />
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer - Black with PAPERCUT */}
      <footer className="bg-black text-white py-8 mt-auto">
        <div className="text-center">
          <h2 className="text-4xl font-bold mb-2">PAPERCUT</h2>
          <p className="text-lg text-gray-300 italic">Slash through messy research.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;