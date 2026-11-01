import React from 'react';
import DataTable from '../components/DataTable';

export default function Listings({
  listingsData,
  isLoading,
  page,
  pageSize,
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
  onPageChange,
  onPageSizeChange,
  onResetFilters
}) {
  return (
    <div className="space-y-4">
      {/* Directory Header Banner */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-slate-900 dark:text-white">
            Commercial Listings Directory
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Querying active MySQL database table <code className="px-1.5 py-0.5 bg-slate-100 dark:bg-slate-800 rounded text-indigo-600 dark:text-indigo-400 font-mono text-[11px]">listing_master</code>. All {listingsData?.total?.toLocaleString() || 0} listings are genuine entities from OpenStreetMap.
          </p>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <div className="text-right">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">Total Directory</span>
            <span className="text-lg font-extrabold text-slate-900 dark:text-white">
              {listingsData?.total?.toLocaleString() || 0} Records
            </span>
          </div>
        </div>
      </div>

      {/* Main Data Table */}
      <DataTable
        listings={listingsData?.items || []}
        total={listingsData?.total || 0}
        page={page}
        pageSize={pageSize}
        totalPages={listingsData?.total_pages || 1}
        onPageChange={onPageChange}
        onPageSizeChange={onPageSizeChange}
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        cityFilter={cityFilter}
        setCityFilter={setCityFilter}
        categoryFilter={categoryFilter}
        setCategoryFilter={setCategoryFilter}
        sourceFilter={sourceFilter}
        setSourceFilter={setSourceFilter}
        sortBy={sortBy}
        sortDesc={sortDesc}
        onSort={onSort}
        isLoading={isLoading}
        onResetFilters={onResetFilters}
      />
    </div>
  );
}

