import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
} from 'recharts';

const CITY_COLORS = {
  Bhopal: '#6366f1',
  Indore: '#3b82f6',
  Jaipur: '#10b981',
  Pune: '#f59e0b',
  Delhi: '#8b5cf6',
};

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-3 shadow-lg text-xs">
        <div className="font-bold text-slate-900 dark:text-white mb-1">
          {data.city}
        </div>
        <div className="text-slate-600 dark:text-slate-400 flex items-center justify-between gap-4">
          <span>Total Listings:</span>
          <span className="font-semibold text-slate-900 dark:text-white">{data.count}</span>
        </div>
        <div className="text-slate-600 dark:text-slate-400 flex items-center justify-between gap-4">
          <span>Distribution:</span>
          <span className="font-semibold text-indigo-600 dark:text-indigo-400">{data.percentage}%</span>
        </div>
      </div>
    );
  }
  return null;
};

export default function CityBarChart({ data = [], height = 280 }) {
  if (!data || data.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-xs text-slate-400">
        No city distribution data available.
      </div>
    );
  }

  return (
    <div className="w-full" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(148, 163, 184, 0.2)" />
          <XAxis
            dataKey="city"
            tick={{ fontSize: 12, fill: '#64748b' }}
            axisLine={{ stroke: '#cbd5e1' }}
            tickLine={false}
          />
          <YAxis
            tick={{ fontSize: 11, fill: '#64748b' }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(99, 102, 241, 0.05)' }} />
          <Bar dataKey="count" radius={[6, 6, 0, 0]}>
            {data.map((entry) => (
              <Cell key={entry.city} fill={CITY_COLORS[entry.city] || '#6366f1'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

