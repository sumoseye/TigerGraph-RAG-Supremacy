// frontend/src/components/MetricsTable.jsx
import React from 'react';

const MetricsTable = ({ results }) => {
  if (!results) return null;

  const metrics = [
    {
      name: 'Latency',
      icon: '⏱️',
      p1: `${results.llm_only?.latency_ms?.toFixed(0)}ms`,
      p2: `${results.basic_rag?.latency_ms?.toFixed(0)}ms`,
      p3: `${results.tigergraph?.latency_ms?.toFixed(0)}ms`,
    },
    {
      name: 'Total Tokens',
      icon: '📊',
      p1: results.llm_only?.tokens_total || 0,
      p2: results.basic_rag?.tokens_total || 0,
      p3: results.tigergraph?.tokens_total || 0,
    },
    {
      name: 'Cost',
      icon: '💰',
      p1: `$${results.llm_only?.cost?.toFixed(6)}`,
      p2: `$${results.basic_rag?.cost?.toFixed(6)}`,
      p3: `$${results.tigergraph?.cost?.toFixed(6)}`,
    },
  ];

  return (
    <div className="neoborder-thick border-black bg-white overflow-hidden">
      {/* Header */}
      <div className="bg-black text-white">
        <div className="grid grid-cols-5 gap-6 p-6">
          <div>
            <p className="label text-orange">Metric</p>
          </div>
          <div>
            <p className="label text-orange">Pipeline 1</p>
            <p className="text-xs text-gray-300">LLM Only</p>
          </div>
          <div>
            <p className="label text-orange">Pipeline 2</p>
            <p className="text-xs text-gray-300">Basic RAG</p>
          </div>
          <div>
            <p className="label text-orange">Pipeline 3</p>
            <p className="text-xs text-gray-300">GraphRAG</p>
          </div>
          <div></div>
        </div>
      </div>

      {/* Rows */}
      <div className="divide-y-4 divide-black">
        {metrics.map((metric, idx) => (
          <div key={idx} className="grid grid-cols-5 gap-6 p-6 hover:bg-gray-50 transition">
            <div>
              <p className="font-bold text-black text-lg flex items-center gap-2">
                <span className="text-2xl">{metric.icon}</span>
                {metric.name}
              </p>
            </div>
            <div>
              <p className="heading-sm text-teal">{metric.p1}</p>
            </div>
            <div>
              <p className="heading-sm text-mustard">{metric.p2}</p>
            </div>
            <div>
              <p className="heading-sm text-sage">{metric.p3}</p>
            </div>
            <div></div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MetricsTable;