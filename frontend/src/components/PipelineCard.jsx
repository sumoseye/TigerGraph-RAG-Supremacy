// frontend/src/components/PipelineCard.jsx
import React from 'react';
import { FaCheckCircle, FaClock, FaCoins } from 'react-icons/fa';

const PipelineCard = ({ data, title, subtitle, icon, accentColor }) => {
  return (
    <div className={`group relative bg-card rounded-xl border border-[#2a2a2a] overflow-hidden hover:border-[#4a7c59] transition-all duration-300`}>
      {/* Gradient background on hover */}
      <div className={`absolute inset-0 bg-gradient-to-br ${accentColor} opacity-0 group-hover:opacity-5 transition-opacity duration-300`}></div>

      <div className="relative p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-2xl">{icon}</span>
              <div>
                <h3 className="text-lg font-bold text-white">{title}</h3>
                <p className="text-xs text-[#666666]">{subtitle}</p>
              </div>
            </div>
          </div>
          {data.status === 'success' && <FaCheckCircle className="text-[#5a9c6f] text-lg" />}
        </div>

        {/* Answer */}
        <div className="mb-6">
          <p className="text-xs font-semibold text-[#999999] mb-2 uppercase tracking-wider">Response</p>
          <div className="bg-[#0f0f0f]/50 p-4 rounded-lg max-h-48 overflow-y-auto border border-[#2a2a2a]">
            <p className="text-sm text-[#e0e0e0] leading-relaxed">
              {data.answer || 'No answer available'}
            </p>
          </div>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-[#1f1f1f] p-3 rounded-lg border border-[#2a2a2a]">
            <div className="flex items-center gap-2 mb-1">
              <FaClock className="text-[#5a9c6f] text-sm" />
              <span className="text-xs font-semibold text-[#999999]">Latency</span>
            </div>
            <p className="text-lg font-bold text-white">
              {data.latency_ms ? `${data.latency_ms.toFixed(0)}ms` : 'N/A'}
            </p>
          </div>

          <div className="bg-[#1f1f1f] p-3 rounded-lg border border-[#2a2a2a]">
            <div className="flex items-center gap-2 mb-1">
              <FaCoins className="text-[#5a9c6f] text-sm" />
              <span className="text-xs font-semibold text-[#999999]">Cost</span>
            </div>
            <p className="text-lg font-bold text-white">
              ${data.cost?.toFixed(6) || '0'}
            </p>
          </div>

          <div className="col-span-2 bg-[#1f1f1f] p-3 rounded-lg border border-[#2a2a2a]">
            <p className="text-xs font-semibold text-[#999999] mb-1 uppercase tracking-wider">Tokens</p>
            <p className="text-sm text-[#e0e0e0]">
              <span className="font-bold">{data.tokens_total || 0}</span>
              <span className="text-[#666666] text-xs"> ({data.tokens_in || 0}↑ {data.tokens_out || 0}↓)</span>
            </p>
          </div>
        </div>

        {/* Sources */}
        {data.sources && data.sources.length > 0 && (
          <div className="mt-4 pt-4 border-t border-[#2a2a2a]">
            <p className="text-xs font-semibold text-[#999999] mb-2 uppercase tracking-wider">Sources</p>
            <div className="flex flex-wrap gap-2">
              {data.sources.slice(0, 3).map((source, idx) => (
                <span key={idx} className="px-2 py-1 text-xs bg-[#4a7c59]/10 text-[#5a9c6f] rounded border border-[#4a7c59]/20">
                  {source.substring(0, 15)}...
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PipelineCard;