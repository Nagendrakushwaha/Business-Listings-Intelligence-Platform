import React from 'react';
import { Utensils, Stethoscope, Hotel as HotelIcon, GraduationCap, Cpu, ArrowRight } from 'lucide-react';
import CategoryPieChart from '../charts/CategoryPieChart';

const CATEGORY_META = {
  Restaurant: { icon: Utensils, color: 'text-amber-500', bg: 'bg-amber-50 dark:bg-amber-950/40' },
  Hospital: { icon: Stethoscope, color: 'text-rose-500', bg: 'bg-rose-50 dark:bg-rose-950/40' },
  Hotel: { icon: HotelIcon, color: 'text-blue-500', bg: 'bg-blue-50 dark:bg-blue-950/40' },
  School: { icon: GraduationCap, color: 'text-emerald-500', bg: 'bg-emerald-50 dark:bg-emerald-950/40' },
  'IT Company': { icon: Cpu, color: 'text-indigo-500', bg: 'bg-indigo-50 dark:bg-indigo-950/40' },
};

export default function CategoryAnalytics({ categoryData = [], onSelectCategory }) {
  return (
    <div className="space-y-6">
      {/* Category Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {categoryData.map((cat) => {
          const meta = CATEGORY_META[cat.category] || { icon: Cpu, color: 'text-indigo-500', bg: 'bg-indigo-50' };
          const Icon = meta.icon;
          return (
            <div
              key={cat.category}
              onClick={() => onSelectCategory(cat.category)}
              className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-4 shadow-sm hover:border-indigo-400 dark:hover:border-indigo-600 transition-all cursor-pointer group"
            >
              <div className="flex items-center justify-between mb-3">
                <div className={`w-8 h-8 rounded-lg ${meta.bg} flex items-center justify-center ${meta.color}`}>
                  <Icon className="w-4 h-4" />
                </div>
                <span className="text-xs font-bold text-indigo-600 dark:text-indigo-400">
                  {cat.percentage}%
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                {cat.category}
              </h3>
              <div className="mt-1 flex items-baseline justify-between">
                <span className="text-xl font-extrabold text-slate-900 dark:text-white">
                  {cat.count}
                </span>
                <span className="text-[11px] text-slate-400">listings</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Main Visual Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7 bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm">
          <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-1">
            Category Share Distribution
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mb-6">
            Proportional representation of core commercial sectors in target cities
          </p>
          <CategoryPieChart data={categoryData} height={280} />
        </div>

        <div className="lg:col-span-5 bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-1">
              Sector Normalization Notes
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-4">
              All heterogeneous OpenStreetMap tags are standardized into 5 canonical categories:
            </p>

            <ul className="space-y-2.5 text-xs text-slate-600 dark:text-slate-300">
              <li className="flex items-start gap-2">
                <span className="w-2 h-2 rounded-full bg-amber-500 mt-1.5 shrink-0"></span>
                <div><strong className="text-slate-900 dark:text-white">Restaurants:</strong> cafes, fast food, dhabas, family dining</div>
              </li>
              <li className="flex items-start gap-2">
                <span className="w-2 h-2 rounded-full bg-rose-500 mt-1.5 shrink-0"></span>
                <div><strong className="text-slate-900 dark:text-white">Hospitals:</strong> clinics, multi-specialty, nursing homes</div>
              </li>
              <li className="flex items-start gap-2">
                <span className="w-2 h-2 rounded-full bg-blue-500 mt-1.5 shrink-0"></span>
                <div><strong className="text-slate-900 dark:text-white">Hotels:</strong> guest houses, resorts, business hotels</div>
              </li>
              <li className="flex items-start gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-500 mt-1.5 shrink-0"></span>
                <div><strong className="text-slate-900 dark:text-white">Schools:</strong> public schools, high schools, academies</div>
              </li>
              <li className="flex items-start gap-2">
                <span className="w-2 h-2 rounded-full bg-indigo-500 mt-1.5 shrink-0"></span>
                <div><strong className="text-slate-900 dark:text-white">IT Companies:</strong> software providers, tech consultancies</div>
              </li>
            </ul>
          </div>

          <div className="pt-4 border-t border-slate-100 dark:border-slate-800 text-[11px] text-slate-400">
            Click on any category card to filter the live directory.
          </div>
        </div>
      </div>
    </div>
  );
}
