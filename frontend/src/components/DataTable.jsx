import React from 'react';
import {
  Search,
  Filter,
  Download,
  Phone,
  PhoneOff,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
  Building2,
  ExternalLink,
  MapPin,
  X
} from 'lucide-react';
import api from '../services/api';

const CATEGORY_STYLES = {
  Restaurant: 'bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400 border-amber-200 dark:border-amber-800/40',
  Hospital: 'bg-rose-50 text-rose-700 dark:bg-rose-500/10 dark:text-rose-400 border-rose-200 dark:border-rose-800/40',
  Hotel: 'bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400 border-blue-200 dark:border-blue-800/40',
  School: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800/40',
  'IT Company': 'bg-indigo-50 text-indigo-700 dark:bg-indigo-500/10 dark:text-indigo-400 border-indigo-200 dark:border-indigo-800/40',
};

export default function DataTable({
  listings = [],
  total = 0,
  page = 1,
  pageSize = 20,
  totalPages = 1,
  onPageChange,
  onPageSizeChange,
  searchTerm,
  setSearchTerm,
  cityFilter,
  setCityFilter,
  categoryFilter,
  setCategoryFilter,
  sourceFilter,
  setSourceFilter,
  sortBy,
  sortDesc,
  onSort,
  isLoading,
  onResetFilters
}) {
  const handleExport = () => {
    const url = api.getExportUrl({
      search: searchTerm,
      city: cityFilter,
      category: categoryFilter,
      source: sourceFilter
    });
    window.open(url, '_blank');
  };

  const hasActiveFilters = Boolean(searchTerm || cityFilter || categoryFilter || sourceFilter);

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl shadow-sm overflow-hidden transition-colors">
      {/* Table Toolbar */}
      <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-3">
        {/* Search & Filters */}
        <div className="flex flex-wrap items-center gap-2.5 flex-1">
          {/* Search Input */}
          <div className="relative min-w-[200px] flex-1 max-w-sm">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search business name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg pl-9 pr-8 py-1.5 text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
            />
            {searchTerm && (
              <button
                onClick={() => setSearchTerm('')}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* City Filter */}
          <select
            value={cityFilter}
            onChange={(e) => setCityFilter(e.target.value)}
            className="bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
          >
            <option value="">All Cities</option>
            <option value="Bhopal">Bhopal</option>
            <option value="Indore">Indore</option>
            <option value="Jaipur">Jaipur</option>
            <option value="Pune">Pune</option>
            <option value="Delhi">Delhi</option>
          </select>

          {/* Category Filter */}
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
          >
            <option value="">All Categories</option>
            <option value="Restaurant">Restaurants</option>
            <option value="Hospital">Hospitals</option>
            <option value="Hotel">Hotels</option>
            <option value="School">Schools</option>
            <option value="IT Company">IT Companies</option>
          </select>

          {/* Reset Filters */}
          {hasActiveFilters && onResetFilters && (
            <button
              onClick={onResetFilters}
              className="text-xs text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 px-2 py-1 flex items-center gap-1"
            >
              <X className="w-3 h-3" /> Reset
            </button>
          )}
        </div>

        {/* Export & Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleExport}
            className="flex items-center gap-1.5 px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold shadow-sm transition-all active:scale-95"
            title="Export filtered records to UTF-8 Excel CSV"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {/* Table Data */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/80 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800 text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 select-none">
              <th className="py-3 px-4 w-12 text-center">#</th>
              <th
                onClick={() => onSort('business_name')}
                className="py-3 px-4 cursor-pointer hover:text-slate-900 dark:hover:text-white"
              >
                <div className="flex items-center gap-1.5">
                  <span>Business Name</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>
              <th
                onClick={() => onSort('category')}
                className="py-3 px-4 cursor-pointer hover:text-slate-900 dark:hover:text-white"
              >
                <div className="flex items-center gap-1.5">
                  <span>Category</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>
              <th
                onClick={() => onSort('city')}
                className="py-3 px-4 cursor-pointer hover:text-slate-900 dark:hover:text-white"
              >
                <div className="flex items-center gap-1.5">
                  <span>City</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>
              <th className="py-3 px-4">Address</th>
              <th className="py-3 px-4">Contact</th>
              <th className="py-3 px-4">Provenance</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60 text-xs">
            {isLoading ? (
              Array.from({ length: 6 }).map((_, idx) => (
                <tr key={idx} className="animate-pulse">
                  <td className="py-4 px-4 text-center"><div className="h-3 bg-slate-200 dark:bg-slate-800 rounded mx-auto w-4"></div></td>
                  <td className="py-4 px-4"><div className="h-3 bg-slate-200 dark:bg-slate-800 rounded w-40"></div></td>
                  <td className="py-4 px-4"><div className="h-5 bg-slate-200 dark:bg-slate-800 rounded-full w-20"></div></td>
                  <td className="py-4 px-4"><div className="h-3 bg-slate-200 dark:bg-slate-800 rounded w-16"></div></td>
                  <td className="py-4 px-4"><div className="h-3 bg-slate-200 dark:bg-slate-800 rounded w-52"></div></td>
                  <td className="py-4 px-4"><div className="h-3 bg-slate-200 dark:bg-slate-800 rounded w-24"></div></td>
                  <td className="py-4 px-4"><div className="h-3 bg-slate-200 dark:bg-slate-800 rounded w-20"></div></td>
                </tr>
              ))
            ) : listings.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-12 text-center text-slate-400">
                  <Building2 className="w-8 h-8 mx-auto mb-2 text-slate-300 dark:text-slate-600" />
                  <p className="font-semibold text-slate-700 dark:text-slate-300">No listings match your search criteria</p>
                  <p className="text-xs text-slate-400 mt-1">Try adjusting the filter options or clearing the search text.</p>
                </td>
              </tr>
            ) : (
              listings.map((item, index) => {
                const catStyle = CATEGORY_STYLES[item.category] || 'bg-slate-100 text-slate-700 border-slate-200';
                const rowNum = (page - 1) * pageSize + index + 1;

                return (
                  <tr
                    key={item.id || item.source_id || index}
                    className="hover:bg-slate-50/70 dark:hover:bg-slate-800/40 transition-colors"
                  >
                    {/* Index */}
                    <td className="py-3 px-4 text-center font-mono text-[11px] text-slate-400">
                      {rowNum}
                    </td>

                    {/* Business Name */}
                    <td className="py-3 px-4">
                      <div className="font-semibold text-slate-900 dark:text-white leading-snug">
                        {item.business_name}
                      </div>
                      {item.latitude && item.longitude && (
                        <div className="text-[10px] text-slate-600 dark:text-slate-400 font-mono mt-0.5 flex items-center gap-1">
                          <MapPin className="w-2.5 h-2.5" />
                          <span>{item.latitude.toFixed(4)}, {item.longitude.toFixed(4)}</span>
                        </div>
                      )}
                    </td>

                    {/* Category */}
                    <td className="py-3 px-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold border ${catStyle}`}>
                        {item.category || 'Uncategorized'}
                      </span>
                    </td>

                    {/* City */}
                    <td className="py-3 px-4 font-medium text-slate-700 dark:text-slate-300 whitespace-nowrap">
                      {item.city}
                    </td>

                    {/* Address */}
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400 max-w-xs truncate" title={item.address}>
                      {item.address || '—'}
                    </td>

                    {/* Phone */}
                    <td className="py-3 px-4 whitespace-nowrap">
                      {item.phone ? (
                        <span className="inline-flex items-center gap-1.5 font-mono text-[11px] font-semibold text-emerald-700 dark:text-emerald-400">
                          <Phone className="w-3 h-3 text-emerald-500" />
                          {item.phone}
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-[11px] text-slate-400 dark:text-slate-500">
                          <PhoneOff className="w-3 h-3 text-slate-300 dark:text-slate-600" />
                          NULL
                        </span>
                      )}
                    </td>

                    {/* Provenance */}
                    <td className="py-3 px-4 whitespace-nowrap">
                      <div className="text-[11px] font-mono text-slate-500 dark:text-slate-400">
                        {item.source_id || item.source}
                      </div>
                      <span className="text-[10px] text-slate-600 dark:text-slate-400">
                        {item.source}
                      </span>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div className="p-4 border-t border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-600 dark:text-slate-400">
        <div className="flex items-center gap-2">
          <span>Rows per page:</span>
          <select
            value={pageSize}
            onChange={(e) => onPageSizeChange(Number(e.target.value))}
            className="bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded px-2 py-1 text-xs text-slate-700 dark:text-slate-300"
          >
            <option value={10}>10</option>
            <option value={20}>20</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </select>
          <span className="text-slate-400 ml-2">
            Showing {total === 0 ? 0 : (page - 1) * pageSize + 1} to {Math.min(page * pageSize, total)} of {total.toLocaleString()} listings
          </span>
        </div>

        <div className="flex items-center gap-1">
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={page <= 1 || isLoading}
            className="p-1.5 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="px-3 py-1 font-semibold text-slate-800 dark:text-slate-200">
            Page {page} of {totalPages || 1}
          </span>
          <button
            onClick={() => onPageChange(page + 1)}
            disabled={page >= totalPages || isLoading}
            className="p-1.5 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

