// frontend/src/components/QueryInput.jsx
import React, { useState } from 'react';

const QueryInput = ({ onSubmit, loading, hideOptions }) => {
  const [query, setQuery] = useState('');

  const sampleQueries = [
    "Latest quantum computing breakthroughs?",
    "AI advances in healthcare",
    "Neural network architectures",
    "Machine learning trends 2024",
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query);
    }
  };

  const handleSample = (sample) => {
    setQuery(sample);
    setTimeout(() => onSubmit(sample), 50);
  };

  return (
    <div className="w-full">
      {/* Main Search Bar */}
      <div className="pb-16">
        <form onSubmit={handleSubmit} className="w-full flex justify-center">
          <div className="search-wrapper-big">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter your research question..."
              className="search-input-big"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="search-button-big"
            >
              {loading ? 'Running...' : 'Search'}
            </button>
          </div>
        </form>
      </div>

      {/* Sample Queries with explicit spacing */}
      {!hideOptions && (
        <div className="flex flex-wrap justify-center items-center query-bubbles-container px-4" style={{ gap: '0.9rem' }}>
          {sampleQueries.map((sample, idx) => (
            <button
              key={idx}
              onClick={() => handleSample(sample)}
              disabled={loading}
              className="query-bubble-neo"
              style={{ margin: 0 }}
            >
              {sample}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default QueryInput;