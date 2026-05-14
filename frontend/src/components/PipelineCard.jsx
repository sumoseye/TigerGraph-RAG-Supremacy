// frontend/src/components/PipelineCard.jsx
import React from 'react';
import { FaBrain, FaDatabase, FaProjectDiagram, FaClock, FaCoins, FaFileAlt, FaCheckCircle, FaTimesCircle } from 'react-icons/fa';

const PipelineCard = ({ data, title, icon, color }) => {
  const icons = {
    brain: FaBrain,
    database: FaDatabase,
    graph: FaProjectDiagram
  };

  const Icon = icons[icon] || FaBrain;

  const getStatusIcon = () => {
    if (data.status === 'success') return <FaCheckCircle className="text-green-500 text-lg" />;
    if (data.status === 'error') return <FaTimesCircle className="text-red-500 text-lg" />;
    return <div className="w-5 h-5 border-2 border-yellow-500 border-t-transparent rounded-full animate-spin"></div>;
  };

  return (
    <div className={`bg-white rounded-xl shadow-2xl p-6 border-t-4 ${color} transform transition-all hover:shadow-2xl`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4 pb-4 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <Icon className={`text-3xl ${color.replace('border', 'text')}`} />
          <h2 className="text-lg font-bold text-gray-800">{title}</h2>
        </div>
        {getStatusIcon()}
      </div>

      {/* Answer */}
      <div className="mb-4">
        <h3 className="text-xs font-semibold text-gray-600 mb-2 flex items-center gap-2 uppercase tracking-wide">
          <FaFileAlt /> Answer
        </h3>
        <div className="bg-gray-50 p-4 rounded-lg max-h-64 overflow-y-auto text-sm text-gray-700 leading-relaxed border border-gray-200">
          {data.answer || 'No answer available'}
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="bg-blue-50 p-3 rounded-lg border border-blue-100">
          <div className="flex items-center gap-2 text-blue-600 mb-1">
            <FaClock className="text-sm" />
            <span className="text-xs font-semibold">Latency</span>
          </div>
          <p className="text-lg font-bold text-gray-800">
            {data.latency_ms ? `${data.latency_ms.toFixed(0)}ms` : 'N/A'}
          </p>
        </div>

        <div className="bg-green-50 p-3 rounded-lg border border-green-100">
          <div className="flex items-center gap-2 text-green-600 mb-1">
            <FaCoins className="text-sm" />
            <span className="text-xs font-semibold">Cost</span>
          </div>
          <p className="text-lg font-bold text-gray-800">
            ${data.cost?.toFixed(6) || '0'}
          </p>
        </div>

        <div className="bg-purple-50 p-3 rounded-lg col-span-2 border border-purple-100">
          <div className="text-purple-600 mb-1 text-xs font-semibold">Tokens</div>
          <p className="text-sm text-gray-700">
            <span className="font-bold">{data.tokens_total || 0}</span>
            <span className="text-gray-500 text-xs"> ({data.tokens_in || 0}↑ {data.tokens_out || 0}↓)</span>
          </p>
        </div>
      </div>

      {/* Sources */}
      {data.sources && data.sources.length > 0 && (
        <div className="mb-3 pb-3 border-t border-gray-200">
          <h4 className="text-xs font-semibold text-gray-600 mb-2">📚 Sources</h4>
          <div className="flex flex-wrap gap-2">
            {data.sources.map((source, idx) => (
              <span key={idx} className="px-2 py-1 bg-indigo-50 border border-indigo-200 rounded text-xs text-indigo-700 font-medium">
                {source}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Reasoning */}
      {data.reasoning && (
        <p className="text-xs text-gray-500 italic border-t border-gray-200 pt-3">
          ℹ️ {data.reasoning}
        </p>
      )}
    </div>
  );
};

export default PipelineCard;