// frontend/src/components/PipelineCard.jsx
import React from 'react';

const PipelineCard = ({ data, title, subtitle, accentColor }) => {
  return (
    <div className="neoborder-thick border-black bg-white animate-in h-full flex flex-col">
      {/* Color Header */}
      <div style={{ backgroundColor: accentColor }} className="h-4"></div>

      {/* Title Section - Compact */}
      <div className="border-b-4 border-black p-6 bg-gray-50">
        <h3 className="heading-md text-black mb-1">{title}</h3>
        <p className="label text-gray-600">{subtitle}</p>
        
        <div className="mt-3">
          {data.status === 'success' ? (
            <span className="inline-block px-3 py-1 bg-sage/25 border-2 border-sage text-sage font-bold text-xs uppercase">
              ✓ Success
            </span>
          ) : (
            <span className="inline-block px-3 py-1 bg-rust/25 border-2 border-rust text-rust font-bold text-xs uppercase">
              ⏳ Pending
            </span>
          )}
        </div>
      </div>

      {/* Content - Flex Grow */}
      <div className="flex-1 p-6 space-y-5 flex flex-col overflow-y-auto">
        {/* Answer Box */}
        <div className="neoborder border-black bg-gray-50 p-5">
          <p className="label text-gray-600 mb-3">RESPONSE</p>
          <p className="text-sm font-medium text-black leading-relaxed line-clamp-6">
            {data.answer || 'No answer available'}
          </p>
        </div>

        {/* Metrics - Stacked */}
        <div className="space-y-3">
          <p className="label text-gray-600">KEY METRICS</p>
          
          <div style={{ borderColor: accentColor }} className="border-4 p-4 bg-white">
            <p className="label text-gray-600 mb-2">Latency</p>
            <p className="heading-sm text-black">
              {data.latency_ms ? `${data.latency_ms.toFixed(0)}ms` : 'N/A'}
            </p>
          </div>

          <div style={{ borderColor: accentColor }} className="border-4 p-4 bg-white">
            <p className="label text-gray-600 mb-2">Total Tokens</p>
            <p className="heading-sm text-black">{data.tokens_total || 0}</p>
          </div>

          <div style={{ borderColor: accentColor }} className="border-4 p-4 bg-white">
            <p className="label text-gray-600 mb-2">Cost</p>
            <p className="heading-sm text-black">${data.cost?.toFixed(6) || '0'}</p>
          </div>
        </div>
      </div>

      {/* Sources - Sticky Bottom */}
      {data.sources && data.sources.length > 0 && (
        <div className="border-t-4 border-black p-4 bg-gray-50 mt-auto">
          <p className="label text-gray-600 mb-2">SOURCES ({data.sources.length})</p>
          <div className="text-xs font-semibold text-black truncate">
            {data.sources.slice(0, 2).map(s => s.substring(0, 20)).join(', ')}...
          </div>
        </div>
      )}
    </div>
  );
};

export default PipelineCard;