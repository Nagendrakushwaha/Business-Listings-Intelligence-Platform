import React from 'react';

export default function KPICard({
  title,
  value,
  subtitle,
  icon: Icon,
  badgeText,
  badgeType = 'neutral', // 'positive', 'warning', 'info', 'neutral'
  color = 'indigo',
}) {
  const colorMap = {
    indigo: {
      bg: 'bg-indigo-50 dark:bg-indigo-950/40',
      text: 'text-indigo-600 dark:text-indigo-400',
      border: 'hover:border-indigo-300 dark:hover:border-indigo-800',
    },
    emerald: {
      bg: 'bg-emerald-50 dark:bg-emerald-950/40',
      text: 'text-emerald-600 dark:text-emerald-400',
      border: 'hover:border-emerald-300 dark:hover:border-emerald-800',
    },
    amber: {
      bg: 'bg-amber-50 dark:bg-amber-950/40',
      text: 'text-amber-600 dark:text-amber-400',
      border: 'hover:border-amber-300 dark:hover:border-amber-800',
    },
    blue: {
      bg: 'bg-blue-50 dark:bg-blue-950/40',
      text: 'text-blue-600 dark:text-blue-400',
      border: 'hover:border-blue-300 dark:hover:border-blue-800',
    },
    purple: {
      bg: 'bg-purple-50 dark:bg-purple-950/40',
      text: 'text-purple-600 dark:text-purple-400',
      border: 'hover:border-purple-300 dark:hover:border-purple-800',
    },
    rose: {
      bg: 'bg-rose-50 dark:bg-rose-950/40',
      text: 'text-rose-600 dark:text-rose-400',
      border: 'hover:border-rose-300 dark:hover:border-rose-800',
    },
  };

  const badgeStyles = {
    positive: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800/40',
    warning: 'bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400 border-amber-200 dark:border-amber-800/40',
    info: 'bg-indigo-50 text-indigo-700 dark:bg-indigo-500/10 dark:text-indigo-400 border-indigo-200 dark:border-indigo-800/40',
    neutral: 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border-slate-200 dark:border-slate-700',
  };

  const c = colorMap[color] || colorMap.indigo;

  return (
    <div className={`bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-5 shadow-sm transition-all duration-200 ${c.border}`}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
          {title}
        </span>
        {Icon && (
          <div className={`w-9 h-9 rounded-lg ${c.bg} flex items-center justify-center ${c.text}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>

      <div className="flex items-baseline justify-between gap-2">
        <span className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          {typeof value === 'number' ? value.toLocaleString() : value ?? '—'}
        </span>
        {badgeText && (
          <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold border ${badgeStyles[badgeType]}`}>
            {badgeText}
          </span>
        )}
      </div>

      {subtitle && (
        <p className="mt-2 text-xs text-slate-500 dark:text-slate-400 leading-normal">
          {subtitle}
        </p>
      )}
    </div>
  );
}

