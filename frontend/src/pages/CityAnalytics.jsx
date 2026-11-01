import React from 'react';
import { MapPin, Trophy, Building2, CheckCircle2, ArrowRight } from 'lucide-react';
import CityBarChart from '../charts/CityBarChart';

export default function CityAnalytics({ cityData = [], onSelectCity }) {
  const sortedCities = [...cityData].sort((a, b) => b.count - a.count);
  const totalVolume = sortedCities.reduce((acc, curr) => acc + curr.count, 0);

  return (
    <div className="space-y-6">
      {/* Top City Overview Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {sortedCities.map((c, idx) => (
          <div
            key={c.city}
            onClick={() => onSelectCity(c.city)}
            className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-4 shadow-sm hover:border-indigo-400 dark:hover:border-indigo-600 transition-all cursor-pointer group"
          >
            <div className="flex items-center justify-between text-xs mb-2">
              <span className="font-bold text-slate-500 dark:text-slate-400 flex items-center gap-1">
                {idx === 0 && <Trophy className="w-3.5 h-3.5 text-amber-500" />}
                Rank #{idx + 1}
              </span>
              <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10 px-1.5 py-0.5 rounded">
                <CheckCircle2 className="w-3 h-3" /> Met
              </span>
            </div>

            <h3 className="text-base font-bold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
              {c.city}
            </h3>

            <div className="mt-2 flex items-baseline justify-between">
              <span className="text-xl font-extrabold text-slate-900 dark:text-white">
                {c.count}
              </span>
              <span className="text-xs font-semibold text-indigo-600 dark:text-indigo-400">
                {c.percentage}%
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-1">Verified businesses</p>
          </div>
        ))}
      </div>

      {/* Main City Chart */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-sm font-bold text-slate-900 dark:text-white">
              Comparative City Distribution
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Volume distribution across all {cityData.length} target metropolitan regions (Total: {totalVolume} records)
            </p>
          </div>
        </div>
        <CityBarChart data={sortedCities} height={320} />
      </div>

      {/* City Rankings Table */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm">
        <div className="p-4 border-b border-slate-200 dark:border-slate-800">
          <h2 className="text-sm font-bold text-slate-900 dark:text-white">
            City Performance Breakdown
          </h2>
        </div>
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-50/80 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800 text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              <th className="py-3 px-4">Rank</th>
              <th className="py-3 px-4">City</th>
              <th className="py-3 px-4 text-right">Listing Count</th>
              <th className="py-3 px-4 text-right">Share of Directory</th>
              <th className="py-3 px-4 text-center">Internship Target (&gt;=100)</th>
              <th className="py-3 px-4 text-center">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
            {sortedCities.map((item, idx) => (
              <tr key={item.city} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40">
                <td className="py-3 px-4 font-mono font-bold text-slate-400">#{idx + 1}</td>
                <td className="py-3 px-4 font-semibold text-slate-900 dark:text-white flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-indigo-500" />
                  {item.city}
                </td>
                <td className="py-3 px-4 text-right font-bold text-slate-900 dark:text-white">
                  {item.count}
                </td>
                <td className="py-3 px-4 text-right font-medium text-indigo-600 dark:text-indigo-400">
                  {item.percentage}%
                </td>
                <td className="py-3 px-4 text-center">
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/40">
                    <CheckCircle2 className="w-3 h-3" /> Exceeded Target ({item.count}/100)
                  </span>
                </td>
                <td className="py-3 px-4 text-center">
                  <button
                    onClick={() => onSelectCity(item.city)}
                    className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1 mx-auto"
                  >
                    View Directory <ArrowRight className="w-3 h-3" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

