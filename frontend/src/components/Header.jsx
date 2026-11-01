import React from 'react';
import { Search, RefreshCw, Sun, Moon, Sparkles } from 'lucide-react';

const TAB_TITLES = {
  overview: {
    title: 'Platform Overview',
    subtitle: 'High-level business intelligence, data source metrics, and real-time coverage',
  },
  listings: {
    title: 'Business Directory',
    subtitle: 'Search, filter, paginate, and export validated Indian commercial establishments',
  },
  city: {
    title: 'City Analytics',
    subtitle: 'Cross-city distribution, establishment concentration, and regional rankings',
  },
  category: {
    title: 'Category Analytics',
    subtitle: 'Commercial sector distribution across Restaurants, Hospitals, Hotels, Schools, & Tech',
  },
  source: {
    title: 'Data Provenance',
    subtitle: 'Origin distribution, OSM node attribution, and compliance traceability',
  },
  quality: {
    title: 'Data Quality & Audit',
    subtitle: 'Integrity scorecard, deduplication metrics, and zero-fabrication verification',
  },
  settings: {
    title: 'Platform Configuration',
    subtitle: 'API endpoints, database credentials, environment status, and pipelines',
  },
};

export default function Header({
  activeTab,
  onRefresh,
  isRefreshing,
  lastUpdated,
  darkMode,
  setDarkMode,
  globalSearch,
  setGlobalSearch,
  onSearchSubmit,
}) {
  const currentTab = TAB_TITLES[activeTab] || TAB_TITLES.overview;

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && onSearchSubmit) {
      onSearchSubmit();
    }
  };

  return (
    <header className="h-16 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-6 flex items-center justify-between shrink-0 transition-colors duration-200">
      {/* Title & Subtitle */}
      <div>
        <h1 className="text-base font-bold text-slate-900 dark:text-white leading-tight">
          {currentTab.title}
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 hidden sm:block">
          {currentTab.subtitle}
        </p>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-3">
        {/* Global Search */}
        <div className="relative w-48 md:w-64">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Quick search name or city..."
            value={globalSearch}
            onChange={(e) => setGlobalSearch(e.target.value)}
            onKeyDown={handleKeyDown}
            className="w-full bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
          />
        </div>

        {/* Refresh Button */}
        <button
          onClick={onRefresh}
          disabled={isRefreshing}
          title="Refresh platform data"
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700/80 text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all active:scale-95 disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin text-indigo-600' : ''}`} />
          <span className="hidden md:inline">Refresh</span>
        </button>

        {/* Last Updated Timestamp */}
        {lastUpdated && (
          <span className="hidden lg:inline text-[11px] text-slate-500 dark:text-slate-400">
            Updated {lastUpdated}
          </span>
        )}

        {/* Theme Toggle */}
        <button
          onClick={() => setDarkMode(!darkMode)}
          title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          className="w-8 h-8 rounded-lg flex items-center justify-center border border-slate-200 dark:border-slate-700/80 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all"
        >
          {darkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
        </button>
      </div>
    </header>
  );
}

