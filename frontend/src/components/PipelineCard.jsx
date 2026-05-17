// frontend/src/components/PipelineCard.jsx
import React from 'react';

const PipelineCard = ({ data, title, subtitle, accentColor }) => {
  return (
    <div className="pipeline-card-container">
      {/* Title Section */}
      <div className="mb-4">
        <h3 className="heading-md text-black mb-1">{title}</h3>
        <p className="label text-gray-600">{subtitle}</p>
      </div>

      {/* Scrollable Content Box */}
      <div className="pipeline-scrollable-box">
        {/* Answer */}
        <div className="mb-6">
          <p className="label text-gray-600 mb-3">RESPONSE</p>
          <p className="text-sm font-medium text-black leading-relaxed">
            {data.answer || 'No answer available'}
          </p>
        </div>

        {/* Metrics */}
        <div className="space-y-4">
          <p className="label text-gray-600">KEY METRICS</p>
          
          <div className="metric-item">
            <p className="label text-gray-600 mb-1">Latency</p>
            <p className="heading-sm text-black">
              {data.latency_ms ? `${data.latency_ms.toFixed(0)}ms` : 'N/A'}
            </p>
          </div>

          <div className="metric-item">
            <p className="label text-gray-600 mb-1">Total Tokens</p>
            <p className="heading-sm text-black">{data.tokens_total || 0}</p>
          </div>

          <div className="metric-item">
            <p className="label text-gray-600 mb-1">Cost</p>
            <p className="heading-sm text-black">${data.cost?.toFixed(6) || '0'}</p>
          </div>
        </div>

        {/* Sources */}
        {data.sources && data.sources.length > 0 && (
          <div className="mt-6 pt-4 border-t-2 border-gray-200">
            <p className="label text-gray-600 mb-2">SOURCES ({data.sources.length})</p>
            <div className="text-xs font-semibold text-black">
              {data.sources.slice(0, 3).map((s, idx) => (
                <div key={idx} className="mb-1">{s.substring(0, 40)}...</div>
              ))}
            </div>
          </div>
        )}

        {/* Status */}
        <div className="mt-6">
          {data.status === 'success' ? (
            <span className="inline-block px-3 py-1 bg-sage/25 border-2 border-sage text-sage font-bold text-xs uppercase">
              Success
            </span>
          ) : (
            <span className="inline-block px-3 py-1 bg-rust/25 border-2 border-rust text-rust font-bold text-xs uppercase">
              Pending
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default PipelineCard;