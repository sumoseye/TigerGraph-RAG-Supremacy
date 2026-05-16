// frontend/src/components/LoadingSpinner.jsx
import React from 'react';

const LoadingSpinner = ({ message = "Processing..." }) => {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      {/* Animated spinner */}
      <div className="relative w-20 h-20 mb-8">
        <div className="absolute inset-0 rounded-full border-2 border-[#2a2a2a]"></div>
        <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-[#5a9c6f] animate-spin"></div>
      </div>

      <p className="text-white font-semibold text-lg mb-2">{message}</p>
      <p className="text-[#666666] text-sm">This may take a moment...</p>

      {/* Progress dots */}
      <div className="flex gap-2 mt-6">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="w-2 h-2 rounded-full bg-[#5a9c6f] animate-pulse"
            style={{ animationDelay: `${i * 0.2}s` }}
          ></div>
        ))}
      </div>
    </div>
  );
};

export default LoadingSpinner;