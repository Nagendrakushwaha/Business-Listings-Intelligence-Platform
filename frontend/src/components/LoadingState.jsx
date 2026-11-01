import React from 'react';

export function LoadingCard({ rows = 3 }) {
  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm animate-pulse">
      <div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-1/3 mb-4"></div>
      <div className="h-8 bg-slate-200 dark:bg-slate-800 rounded w-1/2 mb-3"></div>
      <div className="h-3 bg-slate-100 dark:bg-slate-800/60 rounded w-2/3"></div>
    </div>
  );
}

export function LoadingTable({ rows = 6, cols = 5 }) {
  return (
    <div className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm animate-pulse p-4">
      <div className="h-10 bg-slate-100 dark:bg-slate-800/80 rounded-lg mb-4"></div>
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4 py-3 border-b border-slate-100 dark:border-slate-800/50 last:border-0">
          {Array.from({ length: cols }).map((_, j) => (
            <div
              key={j}
              className="h-4 bg-slate-200 dark:bg-slate-800 rounded"
              style={{ width: `${100 / cols}%` }}
            ></div>
          ))}
        </div>
      ))}
    </div>
  );
}

export function LoadingChart() {
  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm animate-pulse h-80 flex flex-col justify-between">
      <div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-1/4"></div>
      <div className="flex items-end gap-3 h-48 justify-around pt-8">
        <div className="w-12 bg-slate-200 dark:bg-slate-800 rounded-t h-32"></div>
        <div className="w-12 bg-slate-200 dark:bg-slate-800 rounded-t h-44"></div>
        <div className="w-12 bg-slate-200 dark:bg-slate-800 rounded-t h-28"></div>
        <div className="w-12 bg-slate-200 dark:bg-slate-800 rounded-t h-40"></div>
        <div className="w-12 bg-slate-200 dark:bg-slate-800 rounded-t h-36"></div>
      </div>
      <div className="h-3 bg-slate-100 dark:bg-slate-800/60 rounded w-full"></div>
    </div>
  );
}

export default function LoadingState({ type = 'card' }) {
  if (type === 'table') return <LoadingTable />;
  if (type === 'chart') return <LoadingChart />;
  return <LoadingCard />;
}

