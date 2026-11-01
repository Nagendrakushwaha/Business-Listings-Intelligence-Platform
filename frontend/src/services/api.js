import axios from 'axios';

// Base API configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

export const api = {
  // System Health
  getHealth: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  // Dashboard Aggregations & KPIs
  getSummary: async () => {
    const response = await apiClient.get('/dashboard/summary');
    return response.data;
  },

  getCityWise: async () => {
    const response = await apiClient.get('/dashboard/city-wise');
    return response.data;
  },

  getCategoryWise: async () => {
    const response = await apiClient.get('/dashboard/category-wise');
    return response.data;
  },

  getSourceWise: async () => {
    const response = await apiClient.get('/dashboard/source-wise');
    return response.data;
  },

  getDataQuality: async () => {
    const response = await apiClient.get('/dashboard/data-quality');
    return response.data;
  },

  // Business Listings
  getListings: async (params = {}) => {
    const response = await apiClient.get('/listings', { params });
    return response.data;
  },

  // Bulk Insert Listings
  bulkInsertListings: async (listings) => {
    const response = await apiClient.post('/listings/bulk', { listings });
    return response.data;
  },

  // CSV Export URL builder
  getExportUrl: (filters = {}) => {
    const query = new URLSearchParams();
    if (filters.search) query.append('search', filters.search);
    if (filters.city) query.append('city', filters.city);
    if (filters.category) query.append('category', filters.category);
    if (filters.source) query.append('source', filters.source);
    const qs = query.toString();
    return `${API_BASE_URL}/listings/export${qs ? `?${qs}` : ''}`;
  }
};

export default api;

