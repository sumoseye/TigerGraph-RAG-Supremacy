// frontend/src/components/MetricsTable.jsx
import React from 'react';

const MetricsTable = ({ results }) => {
  if (!results) return null;

  const getJudgeStatus = (value) => {
    if (value === null || value === undefined) return 'N/A';
    return value ? '✓ PASS' : '✗ FAIL';
  };

  const formatBertScore = (value) => {
    if (value === null || value === undefined) return 'N/A';
    const score = parseFloat(value);
    if (isNaN(score)) return 'N/A';
    return score.toFixed(4);
  };

  const metrics = [
    {
      name: 'Latency',
      p1: `${results.llm_only?.latency_ms?.toFixed(0)}ms`,
      p2: `${results.basic_rag?.latency_ms?.toFixed(0)}ms`,
      p3: `${results.tigergraph?.latency_ms?.toFixed(0)}ms`,
    },
    {
      name: 'Total Tokens',
      p1: results.llm_only?.tokens_total || 0,
      p2: results.basic_rag?.tokens_total || 0,
      p3: results.tigergraph?.tokens_total || 0,
    },
    {
      name: 'Cost',
      p1: `$${results.llm_only?.cost?.toFixed(6)}`,
      p2: `$${results.basic_rag?.cost?.toFixed(6)}`,
      p3: `$${results.tigergraph?.cost?.toFixed(6)}`,
    },
    {
      name: 'LLM Judge (Llama 3.1)',
      p1: getJudgeStatus(results.llm_only?.accuracy_judge),
      p2: getJudgeStatus(results.basic_rag?.accuracy_judge),
      p3: getJudgeStatus(results.tigergraph?.accuracy_judge),
      isAccuracy: true,
    },
    {
      name: 'BERTScore F1',
      p1: formatBertScore(results.llm_only?.accuracy_bertscore),
      p2: formatBertScore(results.basic_rag?.accuracy_bertscore),
      p3: formatBertScore(results.tigergraph?.accuracy_bertscore),
      isAccuracy: true,
    },
  ];

  return (
    <div 
      className="neoborder-thick border-black bg-white overflow-hidden rounded-2xl"
      style={{
        marginLeft: '2rem',
        marginRight: '2rem',
        marginTop: '3rem',
        marginBottom: '3rem',
      }}
    >
      {/* Header */}
      <div className="bg-black text-white">
        <div 
          className="grid grid-cols-4 gap-6"
          style={{ padding: '1.5rem' }}
        >
          <div>
            <p className="label text-orange" style={{ fontSize: '0.875rem', fontWeight: 'bold' }}>Metric</p>
          </div>
          <div>
            <p className="label text-orange" style={{ fontSize: '0.875rem', fontWeight: 'bold' }}>Pipeline 1</p>
            <p style={{ fontSize: '0.75rem', color: '#d1d5db', marginTop: '0.25rem' }}>LLM Only</p>
          </div>
          <div>
            <p className="label text-orange" style={{ fontSize: '0.875rem', fontWeight: 'bold' }}>Pipeline 2</p>
            <p style={{ fontSize: '0.75rem', color: '#d1d5db', marginTop: '0.25rem' }}>Basic RAG</p>
          </div>
          <div>
            <p className="label text-orange" style={{ fontSize: '0.875rem', fontWeight: 'bold' }}>Pipeline 3</p>
            <p style={{ fontSize: '0.75rem', color: '#d1d5db', marginTop: '0.25rem' }}>GraphRAG</p>
          </div>
        </div>
      </div>

      {/* Rows */}
      <div className="divide-y-4 divide-black">
        {metrics.map((metric, idx) => (
          <div
            key={idx}
            className={`grid grid-cols-4 gap-6 transition ${
              metric.isAccuracy ? 'bg-orange/10 hover:bg-orange/20' : 'hover:bg-gray-50'
            }`}
            style={{ padding: '1.5rem' }}
          >
            <div>
              <p style={{ fontWeight: 'bold', fontSize: '1.125rem', color: '#000' }}>
                {metric.name}
              </p>
            </div>
            <div>
              <p 
                className={`heading-sm ${metric.isAccuracy ? 'text-orange font-bold' : 'text-teal'}`}
                style={{ fontSize: '1rem' }}
              >
                {metric.p1}
              </p>
            </div>
            <div>
              <p 
                className={`heading-sm ${metric.isAccuracy ? 'text-orange font-bold' : 'text-mustard'}`}
                style={{ fontSize: '1rem' }}
              >
                {metric.p2}
              </p>
            </div>
            <div>
              <p 
                className={`heading-sm ${metric.isAccuracy ? 'text-orange font-bold' : 'text-sage'}`}
                style={{ fontSize: '1rem' }}
              >
                {metric.p3}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
     
    </div>
  );
};

export default MetricsTable;