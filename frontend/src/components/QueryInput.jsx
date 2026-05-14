// frontend/src/components/QueryInput.jsx
import React, { useState } from 'react';
import { FaSearch, FaRocket } from 'react-icons/fa';

const QueryInput = ({ onSubmit, loading }) => {
  const [query, setQuery] = useState('');

  const sampleQueries = [
    "What are the main findings in quantum computing?",
    "Summarize the healthcare AI research",
    "What climate impacts were discovered?"
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query);
    }
  };

  const handleSampleClick = (sample) => {
    setQuery(sample);
  };

  return (
    <div className="w-full max-w-4xl mx-auto mb-8">
      <form onSubmit={handleSubmit}>
        <div className="relative mb-4">
          <div className="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
            <FaSearch className="text-gray-400 text-lg" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about the research papers..."
            className="w-full pl-12 pr-36 py-4 text-base rounded-lg border-2 border-white/30 bg-white/10 text-white placeholder-white/60 focus:border-white focus:outline-none shadow-xl backdrop-blur-sm transition-all"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="absolute right-2 top-2 px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg font-semibold hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-all transform hover:scale-105 shadow-lg active:scale-95"
          >
            <FaRocket />
            {loading ? 'Running...' : 'Run'}
          </button>
        </div>
      </form>

      {/* Sample Queries */}
      <div className="flex flex-wrap gap-2 justify-center">
        <span className="text-white/80 text-sm">💡 Try:</span>
        {sampleQueries.map((sample, idx) => (
          <button
            key={idx}
            onClick={() => handleSampleClick(sample)}
            disabled={loading}
            className="px-3 py-1 bg-white/10 hover:bg-white/20 text-white text-xs rounded-full transition-all backdrop-blur-sm disabled:opacity-50 border border-white/20"
          >
            {sample}
          </button>
        ))}
      </div>
    </div>
  );
};

export default QueryInput;