// frontend/src/components/MetricsTable.jsx
import React from 'react';
import { FaTrophy, FaBolt, FaDollarSign, FaDatabase } from 'react-icons/fa';

const MetricsTable = ({ results }) => {
  if (!results) return null;

  // Get values with fallback
  const getVal = (val, fallback = 'N/A') => val !== null && val !== undefined ? val : fallback;

  const data = [
    {
      metric: 'Latency (ms)',
      icon: FaBolt,
      color: 'yellow',
      llm: getVal(results.llm_only?.latency_ms?.toFixed(0)),
      rag: getVal(results.basic_rag?.latency_ms?.toFixed(0)),
      graph: getVal(results.tigergraph?.latency_ms?.toFixed(0)),
    },
    {
      metric: 'Total Tokens',
      icon: FaDatabase,
      color: 'blue',
      llm: getVal(results.llm_only?.tokens_total, 0),
      rag: getVal(results.basic_rag?.tokens_total, 0),
      graph: getVal(results.tigergraph?.tokens_total, 0),
    },
    {
      metric: 'Cost ($)',
      icon: FaDollarSign,
      color: 'green',
      llm: `$${getVal(results.llm_only?.cost?.toFixed(6), '0')}`,
      rag: `$${getVal(results.basic_rag?.cost?.toFixed(6), '0')}`,
      graph: `$${getVal(results.tigergraph?.cost?.toFixed(6), '0')}`,
    },
    {
      metric: 'Sources Used',
      icon: FaDatabase,
      color: 'purple',
      llm: getVal(results.llm_only?.sources?.length, 0),
      rag: getVal(results.basic_rag?.sources?.length, 0),
      graph: getVal(results.tigergraph?.sources?.length, 0),
    },
  ];

  // Calculate fastest latency
  const latencies = [
    results.llm_only?.latency_ms,
    results.basic_rag?.latency_ms,
    results.tigergraph?.latency_ms
  ].filter(v => v > 0);
  
  const fastestLatency = latencies.length > 0 ? Math.min(...latencies) : null;

  return (
    <div className="bg-white rounded-xl shadow-2xl p-6 border-t-4 border-indigo-500">
      <div className="flex items-center gap-3 mb-6 pb-4 border-b">
        <FaTrophy className="text-3xl text-yellow-500" />
        <h2 className="text-2xl font-bold text-gray-800">📊 Benchmark Comparison</h2>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gradient-to-r from-blue-50 to-purple-50">
              <th className="px-4 py-3 text-left font-bold text-gray-700">Metric</th>
              <th className="px-4 py-3 text-left font-bold text-blue-600">
                🤖 Pipeline 1<br /><span className="text-xs font-normal text-gray-500">LLM Only</span>
              </th>
              <th className="px-4 py-3 text-left font-bold text-green-600">
                🔍 Pipeline 2<br /><span className="text-xs font-normal text-gray-500">Basic RAG</span>
              </th>
              <th className="px-4 py-3 text-left font-bold text-purple-600">
                📊 Pipeline 3<br /><span className="text-xs font-normal text-gray-500">TigerGraph</span>
              </th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => {
              const isLatencyRow = row.metric === 'Latency (ms)';
              const isFastest = (val) => {
                if (!isLatencyRow || !fastestLatency) return false;
                return parseFloat(val) === fastestLatency;
              };
              
              return (
                <tr key={idx} className="border-b hover:bg-gray-50 transition">
                  <td className="px-4 py-3 font-semibold text-gray-700 flex items-center gap-2">
                    <span className={`text-${row.color}-500`}>●</span>
                    {row.metric}
                  </td>
                  <td className={`px-4 py-3 font-medium ${isFastest(row.llm) ? 'bg-green-100 text-green-700' : 'text-gray-600'}`}>
                    {row.llm} {isFastest(row.llm) && '🏆'}
                  </td>
                  <td className={`px-4 py-3 font-medium ${isFastest(row.rag) ? 'bg-green-100 text-green-700' : 'text-gray-600'}`}>
                    {row.rag} {isFastest(row.rag) && '🏆'}
                  </td>
                  <td className={`px-4 py-3 font-medium ${isFastest(row.graph) ? 'bg-green-100 text-green-700' : 'text-gray-600'}`}>
                    {row.graph} {isFastest(row.graph) && '🏆'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-800">
        <strong>📊 Summary:</strong> 
        <ul className="mt-2 space-y-1">
          <li>✅ <strong>Pipeline 1 (LLM):</strong> Full context, fast response</li>
          <li>✅ <strong>Pipeline 2 (RAG):</strong> Vector search, targeted results</li>
          <li>⏳ <strong>Pipeline 3 (TigerGraph):</strong> Coming soon!</li>
        </ul>
      </div>
    </div>
  );
};

export default MetricsTable;