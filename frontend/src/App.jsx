import React, { useState, useEffect, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Listings from './pages/Listings';
import CityAnalytics from './pages/CityAnalytics';
import CategoryAnalytics from './pages/CategoryAnalytics';
import SourceAnalytics from './pages/SourceAnalytics';
import DataQuality from './pages/DataQuality';
import Settings from './pages/Settings';
import api from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('theme') === 'dark';
  });

  // Data states
  const [summary, setSummary] = useState(null);
  const [cityData, setCityData] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [sourceData, setSourceData] = useState([]);
  const [qualityData, setQualityData] = useState(null);
  const [listingsData, setListingsData] = useState(null);
  const [dbStatus, setDbStatus] = useState(null);

  // Table & Filter states
  const [searchTerm, setSearchTerm] = useState('');
  const [globalSearch, setGlobalSearch] = useState('');
  const [cityFilter, setCityFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [sourceFilter, setSourceFilter] = useState('');
  const [sortBy, setSortBy] = useState('id');
  const [sortDesc, setSortDesc] = useState(false);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  // UI state
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState('');
  const [error, setError] = useState(null);

  // Dark mode effect
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  // Fetch Dashboard Aggregations
  const fetchDashboardData = useCallback(async () => {
    try {
      setError(null);
      const [sumRes, cityRes, catRes, srcRes, qualRes, healthRes] = await Promise.allSettled([
        api.getSummary(),
        api.getCityWise(),
        api.getCategoryWise(),
        api.getSourceWise(),
        api.getDataQuality(),
        api.getHealth()
      ]);

      if (sumRes.status === 'fulfilled') setSummary(sumRes.value);
      if (cityRes.status === 'fulfilled') setCityData(cityRes.value);
      if (catRes.status === 'fulfilled') setCategoryData(catRes.value);
      if (srcRes.status === 'fulfilled') setSourceData(srcRes.value);
      if (qualRes.status === 'fulfilled') setQualityData(qualRes.value);
      if (healthRes.status === 'fulfilled') setDbStatus(healthRes.value);

      const now = new Date();
      setLastUpdated(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      setError('Failed to connect to the backend server. Make sure FastAPI is running on port 8000.');
    }
  }, []);

  // Fetch Paginated Listings
  const fetchListings = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await api.getListings({
        search: searchTerm || globalSearch,
        city: cityFilter,
        category: categoryFilter,
        source: sourceFilter,
        sort_by: sortBy,
        sort_desc: sortDesc,
        page,
        page_size: pageSize
      });
      setListingsData(data);
    } catch (err) {
      console.error('Failed to fetch listings:', err);
      setError('Unable to load listings. Check database connectivity.');
    } finally {
      setIsLoading(false);
    }
  }, [searchTerm, globalSearch, cityFilter, categoryFilter, sourceFilter, sortBy, sortDesc, page, pageSize]);

  // Initial load
  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  // Listings fetch on dependencies change
  useEffect(() => {
    fetchListings();
  }, [fetchListings]);

  // Refresh handler
  const handleRefresh = async () => {
    setIsRefreshing(true);
    await Promise.all([fetchDashboardData(), fetchListings()]);
    setIsRefreshing(false);
  };

  // Sorting handler
  const handleSort = (column) => {
    if (sortBy === column) {
      setSortDesc(!sortDesc);
    } else {
      setSortBy(column);
      setSortDesc(false);
    }
    setPage(1);
  };

  // Reset filters
  const handleResetFilters = () => {
    setSearchTerm('');
    setGlobalSearch('');
    setCityFilter('');
    setCategoryFilter('');
    setSourceFilter('');
    setPage(1);
  };

  // Global search submit
  const handleGlobalSearchSubmit = () => {
    setSearchTerm(globalSearch);
    setActiveTab('listings');
    setPage(1);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50 dark:bg-slate-950">
      {/* 1. Left Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        dbStatus={dbStatus}
      />

      {/* 2. Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Header */}
        <Header
          activeTab={activeTab}
          onRefresh={handleRefresh}
          isRefreshing={isRefreshing}
          lastUpdated={lastUpdated}
          darkMode={darkMode}
          setDarkMode={setDarkMode}
          globalSearch={globalSearch}
          setGlobalSearch={setGlobalSearch}
          onSearchSubmit={handleGlobalSearchSubmit}
        />

        {/* Dynamic Page Views */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8">
          <div className="max-w-7xl mx-auto">
            {activeTab === 'overview' && (
              <Dashboard
                summary={summary}
                cityData={cityData}
                categoryData={categoryData}
                sourceData={sourceData}
                qualityData={qualityData}
                listingsData={listingsData}
                isLoading={isLoading}
                error={error}
                onRetry={handleRefresh}
                onNavigateTab={(tab) => {
                  setActiveTab(tab);
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
                page={page}
                pageSize={pageSize}
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
                onSort={handleSort}
                onPageChange={setPage}
                onPageSizeChange={(newSize) => {
                  setPageSize(newSize);
                  setPage(1);
                }}
                onResetFilters={handleResetFilters}
              />
            )}

            {activeTab === 'listings' && (
              <Listings
                listingsData={listingsData}
                isLoading={isLoading}
                page={page}
                pageSize={pageSize}
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
                onSort={handleSort}
                onPageChange={setPage}
                onPageSizeChange={(newSize) => {
                  setPageSize(newSize);
                  setPage(1);
                }}
                onResetFilters={handleResetFilters}
              />
            )}

            {activeTab === 'city' && (
              <CityAnalytics
                cityData={cityData}
                onSelectCity={(city) => {
                  setCityFilter(city);
                  setActiveTab('listings');
                  setPage(1);
                }}
              />
            )}

            {activeTab === 'category' && (
              <CategoryAnalytics
                categoryData={categoryData}
                onSelectCategory={(cat) => {
                  setCategoryFilter(cat);
                  setActiveTab('listings');
                  setPage(1);
                }}
              />
            )}

            {activeTab === 'source' && (
              <SourceAnalytics sourceData={sourceData} />
            )}

            {activeTab === 'quality' && (
              <DataQuality qualityData={qualityData} />
            )}

            {activeTab === 'settings' && (
              <Settings
                dbStatus={dbStatus}
                onRefresh={handleRefresh}
              />
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

