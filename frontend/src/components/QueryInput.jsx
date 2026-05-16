// frontend/src/components/QueryInput.jsx
import React, { useState } from 'react';
import { FaSearch, FaArrowRight } from 'react-icons/fa';

const QueryInput = ({ onSubmit, loading }) => {
  const [query, setQuery] = useState('');

  const sampleQueries = [
    "What papers discuss transformers?",
    "Find research on quantum computing",
    "Show papers about machine learning",
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
    <div className="w-full space-y-4">
      <form onSubmit={handleSubmit}>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
            <FaSearch className="text-[#666666]" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a research question..."
            className="w-full pl-12 pr-14 py-4 rounded-lg bg-[#1f1f1f] border border-[#2a2a2a] text-white placeholder-[#666666] focus:border-[#5a9c6f] focus:outline-none transition-colors"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-2 bg-gradient-to-r from-[#4a7c59] to-[#5a9c6f] text-white rounded-lg font-medium hover:from-[#5a9c6f] hover:to-[#6aac7f] disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2 text-sm"
          >
            {loading ? 'Running...' : <><FaArrowRight /> Run</>}
          </button>
        </div>
      </form>

      {/* Sample Queries */}
      <div className="flex flex-wrap gap-2 justify-center pt-2">
        {sampleQueries.map((sample, idx) => (
          <button
            key={idx}
            onClick={() => handleSampleClick(sample)}
            disabled={loading}
            className="px-3 py-1.5 text-xs bg-[#1f1f1f] hover:bg-[#2a2a2a] text-[#999999] rounded-full border border-[#2a2a2a] hover:border-[#4a7c59] transition-all disabled:opacity-50"
          >
            {sample}
          </button>
        ))}
      </div>
    </div>
  );
};

export default QueryInput;