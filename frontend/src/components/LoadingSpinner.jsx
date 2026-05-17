// frontend/src/components/LoadingSpinner.jsx
import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="flex flex-col items-center justify-center space-y-16">
      {/* Animated Blocks */}
      <div className="flex gap-4">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="neoborder-thick border-black bg-orange w-16 h-16 spinner-block"
            style={{
              animationDelay: `${i * 0.15}s`
            }}
          ></div>
        ))}
      </div>

      {/* Text - LOWER */}
      <div className="text-center">
        <h2 className="heading-lg text-black mb-2">EXECUTING ALL PIPELINES</h2>
        <p className="font-semibold text-gray-700">Running 3 approaches in parallel...</p>
      </div>

      {/* Progress Dots - LOWER */}
      <div className="flex gap-2">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="w-3 h-3 bg-orange rounded-full pulse-dot"
            style={{
              animationDelay: `${i * 0.2}s`
            }}
          ></div>
        ))}
      </div>
    </div>
  );
};

export default LoadingSpinner;