// frontend/src/components/MetricsTable.jsx
import React from 'react';
import { FaTrophy, FaBolt, FaDollarSign, FaDatabase } from 'react-icons/fa';

const MetricsTable = ({ results }) => {
  if (!results) return null;

  const data = [
    {
      metric: 'Latency (ms)',
      icon: FaBolt,
      color: 'yellow',
      llm: results.llm_only?.latency_ms?.toFixed(0) || 'N/A',
      rag: 'Coming Soon',
      graph: 'Coming Soon',
    },
    {
      metric: 'Total Tokens',
      icon: FaDatabase,
      color: 'blue',
      llm: results.llm_only?.tokens_total || 0,
      rag: '-',
      graph: '-',
    },
    {
      metric: 'Cost ($)',
      icon: FaDollarSign,
      color: 'green',
      llm: `$${results.llm_only?.cost?.toFixed(6) || '0'}`,
      rag: '$0.00',
      graph: '$0.00',
    },
  ];

  return (
    <div className="bg-white rounded-xl shadow-2xl p-6 border-t-4 border-indigo-500">
      <div className="flex items-center gap-3 mb-6 pb-4 border-b">
        <FaTrophy className="text-3xl text-yellow-500" />
        <h2 className="text-2xl font-bold text-gray-800">Benchmark Comparison</h2>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gradient-to-r from-blue-50 to-purple-50">
              <th className="px-4 py-3 text-left font-bold text-gray-700">Metric</th>
              <th className="px-4 py-3 text-left font-bold text-blue-600">
                🤖 Pipeline 1<br /><span className="text-xs font-normal text-gray-500">LLM (Groq)</span>
              </th>
              <th className="px-4 py-3 text-left font-bold text-green-600">
                🔍 Pipeline 2<br /><span className="text-xs font-normal text-gray-500">RAG</span>
              </th>
              <th className="px-4 py-3 text-left font-bold text-purple-600">
                📊 Pipeline 3<br /><span className="text-xs font-normal text-gray-500">TigerGraph</span>
              </th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => {
              const Icon = row.icon;
              return (
                <tr key={idx} className="border-b hover:bg-gray-50 transition">
                  <td className="px-4 py-3 font-semibold text-gray-700 flex items-center gap-2">
                    <Icon className={`text-${row.color}-500`} />
                    {row.metric}
                  </td>
                  <td className="px-4 py-3 text-gray-600 font-medium">{row.llm}</td>
                  <td className="px-4 py-3 text-gray-500 text-xs">{row.rag}</td>
                  <td className="px-4 py-3 text-gray-500 text-xs">{row.graph}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-800">
        <strong>ℹ️ Info:</strong> Pipeline 1 is currently operational with Groq API. Pipelines 2 & 3 coming soon!
      </div>
    </div>
  );
};

export default MetricsTable;