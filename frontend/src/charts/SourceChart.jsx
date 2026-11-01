import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell
} from 'recharts';
import { Layers, ShieldCheck } from 'lucide-react';

export default function SourceChart({ data = [] }) {
  if (!data || data.length === 0) {
    return (
      <div className="h-48 flex items-center justify-center text-xs text-slate-400">
        No source distribution data available.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="h-44 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <XAxis type="number" hide />
            <YAxis
              dataKey="source"
              type="category"
              tick={{ fontSize: 12, fill: '#64748b' }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              formatter={(value) => [`${value} listings`, 'Volume']}
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                borderRadius: '8px',
                border: '1px solid #e2e8f0',
                fontSize: '12px'
              }}
            />
            <Bar dataKey="count" fill="#4f46e5" radius={[0, 6, 6, 0]}>
              {data.map((_, index) => (
                <Cell key={index} fill="#4f46e5" />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-slate-50 dark:bg-slate-800/40 rounded-lg p-3 border border-slate-200/80 dark:border-slate-800 text-xs">
        <div className="flex items-center gap-2 font-semibold text-slate-800 dark:text-slate-200 mb-1">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>Open Database License (ODbL) Compliant</span>
        </div>
        <p className="text-[11px] text-slate-500 dark:text-slate-400">
          All records collected comply with OpenStreetMap terms. Attributions and canonical node/way identifiers are preserved for full lineage traceability.
        </p>
      </div>
    </div>
  );
}
