import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default function ErrorState({
  title = "Failed to load platform data",
  message = "There was an error communicating with the FastAPI backend or MySQL database.",
  onRetry
}) {
  return (
    <div className="bg-rose-50/70 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/50 rounded-xl p-6 text-center max-w-lg mx-auto my-8">
      <div className="w-12 h-12 bg-rose-100 dark:bg-rose-900/50 text-rose-600 dark:text-rose-400 rounded-full flex items-center justify-center mx-auto mb-3">
        <AlertTriangle className="w-6 h-6" />
      </div>
      <h3 className="text-sm font-bold text-rose-900 dark:text-rose-200 mb-1">
        {title}
      </h3>
      <p className="text-xs text-rose-700 dark:text-rose-300/80 mb-4 leading-relaxed">
        {message}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-all active:scale-95"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Retry Connection
        </button>
      )}
    </div>
  );
}

