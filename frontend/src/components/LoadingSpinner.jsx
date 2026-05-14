// frontend/src/components/LoadingSpinner.jsx
import React from 'react';

const LoadingSpinner = ({ message = "Processing..." }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 min-h-[400px]">
      <div className="relative mb-8">
        <div className="animate-spin rounded-full h-16 w-16 border-4 border-white border-b-transparent"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="animate-pulse text-white text-2xl">⚡</div>
        </div>
      </div>
      
      <p className="text-white text-lg font-semibold animate-pulse text-center max-w-md">
        {message}
      </p>
      
      <div className="mt-6 flex gap-1">
        <div className="h-2 w-2 bg-white rounded-full animate-bounce"></div>
        <div className="h-2 w-2 bg-white rounded-full animate-bounce delay-100"></div>
        <div className="h-2 w-2 bg-white rounded-full animate-bounce delay-200"></div>
      </div>
    </div>
  );
};

export default LoadingSpinner;