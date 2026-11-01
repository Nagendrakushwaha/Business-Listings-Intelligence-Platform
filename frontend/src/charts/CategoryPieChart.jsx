import React from 'react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
} from 'recharts';

const CATEGORY_COLORS = {
  Restaurant: '#f59e0b',  // Amber
  Hospital: '#f43f5e',    // Rose
  Hotel: '#3b82f6',       // Blue
  School: '#10b981',      // Emerald
  'IT Company': '#6366f1', // Indigo
};

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-3 shadow-lg text-xs">
        <div className="font-bold text-slate-900 dark:text-white mb-1">
          {data.category}
        </div>
        <div className="text-slate-600 dark:text-slate-400 flex items-center justify-between gap-4">
          <span>Listings:</span>
          <span className="font-semibold text-slate-900 dark:text-white">{data.count}</span>
        </div>
        <div className="text-slate-600 dark:text-slate-400 flex items-center justify-between gap-4">
          <span>Share:</span>
          <span className="font-semibold text-indigo-600 dark:text-indigo-400">{data.percentage}%</span>
        </div>
      </div>
    );
  }
  return null;
};

export default function CategoryPieChart({ data = [], height = 280 }) {
  if (!data || data.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-xs text-slate-400">
        No category distribution data available.
      </div>
    );
  }

  return (
    <div className="w-full flex flex-col md:flex-row items-center justify-between" style={{ height }}>
      {/* Donut Chart */}
      <div className="w-full md:w-3/5 h-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Tooltip content={<CustomTooltip />} />
            <Pie
              data={data}
              dataKey="count"
              nameKey="category"
              cx="50%"
              cy="50%"
              innerRadius={55}
              outerRadius={85}
              paddingAngle={3}
            >
              {data.map((entry) => (
                <Cell
                  key={entry.category}
                  fill={CATEGORY_COLORS[entry.category] || '#94a3b8'}
                  stroke="transparent"
                />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Legend & Breakdown Badges */}
      <div className="w-full md:w-2/5 space-y-2 pr-2">
        {data.map((item) => (
          <div key={item.category} className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <span
                className="w-2.5 h-2.5 rounded-full shrink-0"
                style={{ backgroundColor: CATEGORY_COLORS[item.category] || '#94a3b8' }}
              ></span>
              <span className="text-slate-700 dark:text-slate-300 font-medium truncate max-w-[100px]">
                {item.category}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-slate-900 dark:text-white">
                {item.count}
              </span>
              <span className="text-[11px] text-slate-400 dark:text-slate-500 w-11 text-right">
                {item.percentage}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
