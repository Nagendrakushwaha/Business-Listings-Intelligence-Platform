import React from 'react';
import {
  LayoutDashboard,
  Building2,
  MapPin,
  PieChart as PieIcon,
  Layers,
  ShieldCheck,
  Settings as SettingsIcon,
  Database,
  ExternalLink
} from 'lucide-react';

export const navItems = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'listings', label: 'Business Listings', icon: Building2 },
  { id: 'city', label: 'City Analytics', icon: MapPin },
  { id: 'category', label: 'Category Analytics', icon: PieIcon },
  { id: 'source', label: 'Source Analytics', icon: Layers },
  { id: 'quality', label: 'Data Quality', icon: ShieldCheck },
  { id: 'settings', label: 'Settings', icon: SettingsIcon },
];

export default function Sidebar({ activeTab, setActiveTab, dbStatus }) {
  return (
    <aside className="w-64 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col shrink-0 select-none transition-colors duration-200">
      {/* Brand Header */}
      <div className="h-16 flex items-center gap-3 px-6 border-b border-slate-200 dark:border-slate-800">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-500 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
          <Building2 className="w-5 h-5" />
        </div>
        <div>
          <span className="font-bold text-base tracking-tight text-slate-900 dark:text-white">
            Listings<span className="text-indigo-600 dark:text-indigo-400">Intel</span>
          </span>
          <span className="block text-[10px] font-semibold tracking-wider text-slate-500 dark:text-slate-400 uppercase">
            Platform 1.0
          </span>
        </div>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
        <div className="px-3 pb-2 text-[11px] font-bold tracking-wider text-slate-500 dark:text-slate-400 uppercase">
          Analytics & Data
        </div>

        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 text-left ${
                isActive
                  ? 'bg-indigo-50 text-indigo-700 dark:bg-indigo-500/10 dark:text-indigo-300 font-semibold shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/60 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-400 dark:text-slate-500'}`} />
              <span>{item.label}</span>
              {isActive && (
                <span className="ml-auto w-1.5 h-1.5 rounded-full bg-indigo-600 dark:bg-indigo-400"></span>
              )}
            </button>
          );
        })}
      </div>

      {/* Database / Status Footer */}
      <div className="p-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50">
        <div className="flex items-center justify-between text-xs mb-2">
          <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
            <Database className="w-3.5 h-3.5 text-slate-400" />
            <span className="font-medium">MySQL Engine</span>
          </div>
          <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-medium ${
            dbStatus?.database_connected
              ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400'
              : 'bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400'
          }`}>
            <span className={`w-1.5 h-1.5 rounded-full ${
              dbStatus?.database_connected ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'
            }`}></span>
            {dbStatus?.database_connected ? 'Live' : 'Standby'}
          </span>
        </div>
        <div className="text-[11px] text-slate-600 dark:text-slate-400 flex items-center justify-between pt-1">
          <span>business_listings_db</span>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-0.5"
          >
            Swagger <ExternalLink className="w-2.5 h-2.5" />
          </a>
        </div>
      </div>
    </aside>
  );
}
