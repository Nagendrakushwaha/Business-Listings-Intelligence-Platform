import React, { useState } from 'react';
import {
  Settings as SettingsIcon,
  Database,
  Server,
  Terminal,
  CheckCircle2,
  RefreshCw,
  ExternalLink,
  Code
} from 'lucide-react';
import api from '../services/api';

export default function Settings({ dbStatus, onRefresh }) {
  const [testingConnection, setTestingConnection] = useState(false);
  const [testResult, setTestResult] = useState(null);

  const handleTestHealth = async () => {
    setTestingConnection(true);
    try {
      const data = await api.getHealth();
      setTestResult({ success: true, data });
    } catch (err) {
      setTestResult({ success: false, error: err.message });
    } finally {
      setTestingConnection(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Platform & Architecture Overview */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-9 h-9 rounded-lg bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 flex items-center justify-center">
            <Server className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-900 dark:text-white">
              System Environment & Runtime Architecture
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Multi-tiered decoupled full-stack platform configuration
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-800 space-y-1.5">
            <span className="font-semibold text-slate-800 dark:text-slate-200 block">
              Backend Server
            </span>
            <div className="text-slate-500 flex justify-between">
              <span>Framework:</span> <span className="font-mono text-slate-800 dark:text-slate-200">FastAPI 0.115 + Python 3.13</span>
            </div>
            <div className="text-slate-500 flex justify-between">
              <span>ASGI Server:</span> <span className="font-mono text-slate-800 dark:text-slate-200">Uvicorn on port 8000</span>
            </div>
            <div className="text-slate-500 flex justify-between">
              <span>API Docs:</span> <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="text-indigo-600 hover:underline flex items-center gap-1">Swagger UI <ExternalLink className="w-3 h-3" /></a>
            </div>
          </div>

          <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-800 space-y-1.5">
            <span className="font-semibold text-slate-800 dark:text-slate-200 block">
              Database Storage
            </span>
            <div className="text-slate-500 flex justify-between">
              <span>RDBMS Engine:</span> <span className="font-mono text-slate-800 dark:text-slate-200">MySQL Server 8.0</span>
            </div>
            <div className="text-slate-500 flex justify-between">
              <span>Database Name:</span> <span className="font-mono text-slate-800 dark:text-slate-200">business_listings_db</span>
            </div>
            <div className="text-slate-500 flex justify-between">
              <span>Primary Table:</span> <span className="font-mono text-slate-800 dark:text-slate-200">listing_master</span>
            </div>
          </div>
        </div>
      </div>

      {/* MySQL Connection Status & Health Test */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm">
        <h3 className="text-sm font-bold text-slate-900 dark:text-white mb-2">
          Database Connection Diagnostics
        </h3>
        <p className="text-xs text-slate-500 dark:text-slate-400 mb-4">
          Test real-time connectivity between FastAPI backend and local MySQL instance.
        </p>

        <div className="flex items-center gap-3 mb-4">
          <button
            onClick={handleTestHealth}
            disabled={testingConnection}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${testingConnection ? 'animate-spin' : ''}`} />
            Test API & Database Health
          </button>
        </div>

        {testResult && (
          <div className={`p-3.5 rounded-lg text-xs border ${
            testResult.success
              ? 'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/20 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800/40'
              : 'bg-rose-50 text-rose-800 dark:bg-rose-950/20 dark:text-rose-300 border-rose-200 dark:border-rose-800/40'
          }`}>
            <pre className="font-mono text-[11px] overflow-x-auto">
              {JSON.stringify(testResult, null, 2)}
            </pre>
          </div>
        )}
      </div>

      {/* CLI & Terminal Quick Reference */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-3 text-slate-900 dark:text-white font-bold text-sm">
          <Terminal className="w-4 h-4 text-indigo-600" />
          <span>Operational Commands Reference</span>
        </div>

        <div className="space-y-3 text-xs font-mono">
          <div>
            <span className="text-[11px] text-slate-500 font-sans block mb-1">Execute Data Ingestion:</span>
            <div className="p-2.5 bg-slate-900 text-slate-100 rounded-lg overflow-x-auto">
              python -m scraper.collect_data --cities Bhopal Indore Jaipur Pune Delhi
            </div>
          </div>

          <div>
            <span className="text-[11px] text-slate-500 font-sans block mb-1">Execute Preprocessing & Data Quality:</span>
            <div className="p-2.5 bg-slate-900 text-slate-100 rounded-lg overflow-x-auto">
              python -m scraper.clean_data
            </div>
          </div>

          <div>
            <span className="text-[11px] text-slate-500 font-sans block mb-1">Seed MySQL Database from CSV:</span>
            <div className="p-2.5 bg-slate-900 text-slate-100 rounded-lg overflow-x-auto">
              python database/seed_data.py
            </div>
          </div>

          <div>
            <span className="text-[11px] text-slate-500 font-sans block mb-1">Run Backend Test Suite:</span>
            <div className="p-2.5 bg-slate-900 text-slate-100 rounded-lg overflow-x-auto">
              cd backend && python -m pytest tests/ -v
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

