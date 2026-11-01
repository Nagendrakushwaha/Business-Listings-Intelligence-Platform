import React from 'react';
import { Layers, ShieldCheck, Database, Globe, CheckCircle2, FileText } from 'lucide-react';
import SourceChart from '../charts/SourceChart';

export default function SourceAnalytics({ sourceData = [] }) {
  return (
    <div className="space-y-6">
      {/* Overview Banner */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-9 h-9 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900 dark:text-white">
              Data Lineage & Provenance Governance
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Traceable, legally compliant data ingestion from OpenStreetMap under Open Database License (ODbL)
            </p>
          </div>
        </div>
      </div>

      {/* Main Breakdown & Legal Policy */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-6 bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm">
          <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-1">
            Data Source Distribution
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mb-4">
            Ingestion breakdown by origin engine
          </p>
          <SourceChart data={sourceData} />
        </div>

        <div className="lg:col-span-6 bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm space-y-4">
          <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-2">
            Compliance & Attribution Framework
          </h2>

          <div className="space-y-3 text-xs">
            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-800">
              <span className="font-semibold text-slate-800 dark:text-slate-200 block mb-1">
                1. Open Database License (ODbL)
              </span>
              <p className="text-slate-500 dark:text-slate-400 text-[11px] leading-relaxed">
                OpenStreetMap data is made available under the Open Database License. Any published work or aggregated database acknowledges credit to <code className="text-indigo-600 font-mono">© OpenStreetMap contributors</code>.
              </p>
            </div>

            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-800">
              <span className="font-semibold text-slate-800 dark:text-slate-200 block mb-1">
                2. Rate Limiting & Responsible Scraping
              </span>
              <p className="text-slate-500 dark:text-slate-400 text-[11px] leading-relaxed">
                Collection pipelines respect upstream limits with 1-second pacing delays, descriptive User-Agent headers, automated retry backoffs, and local data caching.
              </p>
            </div>

            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-800">
              <span className="font-semibold text-slate-800 dark:text-slate-200 block mb-1">
                3. Unique Identifier Persistence
              </span>
              <p className="text-slate-500 dark:text-slate-400 text-[11px] leading-relaxed">
                Every record in MySQL maintains its original <code className="text-indigo-600 font-mono">source_id</code> (e.g. <code className="font-mono">OSM:N7518423169</code>) allowing direct cross-referencing on OpenStreetMap.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

