// frontend/src/components/QueryInput.jsx
import React, { useState } from 'react';

const QueryInput = ({ onSubmit, loading }) => {
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
    <div className="space-y-6 w-full">
      {/* Main Search Bar - Centered, Rounded */}
      <form onSubmit={handleSubmit} className="w-full">
        <div className="search-wrapper">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your research question..."
            className="search-input"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="search-button"
          >
            {loading ? 'Running...' : 'Search'}
          </button>
        </div>
      </form>

      {/* Sample Queries - Rounded Black Boxes */}
      <div className="flex flex-wrap gap-3 justify-center">
        {sampleQueries.map((sample, idx) => (
          <button
            key={idx}
            onClick={() => handleSample(sample)}
            disabled={loading}
            className="query-bubble"
          >
            {sample}
          </button>
        ))}
      </div>
    </div>
  );
};

export default QueryInput;