// frontend/src/components/MetricsTable.jsx
import React from 'react';
import { FaTrophy } from 'react-icons/fa';

const MetricsTable = ({ results }) => {
  if (!results) return null;

  const data = [
    {
      metric: 'Latency (ms)',
      llm: results.llm_only?.latency_ms?.toFixed(0) || 'N/A',
      rag: results.basic_rag?.latency_ms?.toFixed(0) || 'N/A',
      graph: results.tigergraph?.latency_ms?.toFixed(0) || 'N/A',
    },
    {
      metric: 'Total Tokens',
      llm: results.llm_only?.tokens_total || 0,
      rag: results.basic_rag?.tokens_total || 0,
      graph: results.tigergraph?.tokens_total || 0,
    },
    {
      metric: 'Cost ($)',
      llm: `$${results.llm_only?.cost?.toFixed(6) || '0'}`,
      rag: `$${results.basic_rag?.cost?.toFixed(6) || '0'}`,
      graph: `$${results.tigergraph?.cost?.toFixed(6) || '0'}`,
    },
  ];

  return (
    <div className="bg-card rounded-xl border border-[#2a2a2a] overflow-hidden">
      {/* Header */}
      <div className="p-6 border-b border-[#2a2a2a] flex items-center gap-3">
        <FaTrophy className="text-[#5a9c6f] text-xl" />
        <h2 className="text-xl font-bold text-white">Performance Metrics</h2>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-[#2a2a2a] bg-[#1f1f1f]/50">
              <th className="px-6 py-4 text-left text-xs font-semibold text-[#999999] uppercase tracking-wider">Metric</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-[#5a9c6f] uppercase tracking-wider">Pipeline 1</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-[#5a9c6f] uppercase tracking-wider">Pipeline 2</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-[#5a9c6f] uppercase tracking-wider">Pipeline 3</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={idx} className="border-b border-[#2a2a2a] hover:bg-[#1f1f1f]/50 transition-colors">
                <td className="px-6 py-4 text-sm font-medium text-white">{row.metric}</td>
                <td className="px-6 py-4 text-sm text-[#e0e0e0]">{row.llm}</td>
                <td className="px-6 py-4 text-sm text-[#e0e0e0]">{row.rag}</td>
                <td className="px-6 py-4 text-sm text-[#e0e0e0]">{row.graph}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MetricsTable;