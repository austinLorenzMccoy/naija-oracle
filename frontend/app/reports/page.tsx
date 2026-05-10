'use client'

import { useRouter } from 'next/navigation'
import Sidebar from '@/components/sidebar'
import Header from '@/components/header'
import { Download, Calendar, Filter, ArrowLeft, FileText } from 'lucide-react'

const reports = [
  {
    title: 'Monthly Performance Report',
    month: 'April 2026',
    metrics: { reviews: '12,482', sentiment: '84.2%', engagement: '87.5%' },
    generated: '2026-05-01'
  },
  {
    title: 'Cultural Alignment Analysis',
    month: 'Q1 2026',
    metrics: { accuracy: '92.3%', relevance: '89.7%', adoption: '78.2%' },
    generated: '2026-04-30'
  },
  {
    title: 'Regional Performance Breakdown',
    month: 'April 2026',
    metrics: { regions: '5', topRegion: 'Lagos (0.89)', coverage: '94.2%' },
    generated: '2026-04-28'
  },
  {
    title: 'Persona Effectiveness Report',
    month: 'Q1 2026',
    metrics: { personas: '25', activePersonas: '23', avgScore: '0.847' },
    generated: '2026-04-25'
  },
]

export default function Reports() {
  const router = useRouter()

  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-60 flex-1 flex flex-col">
        <Header
          tabs={[
            { label: 'Overview', href: '/dashboard', active: false },
            { label: 'Analytics', href: '/analytics', active: false },
            { label: 'Reports', href: '/reports', active: true },
          ]}
        />

        {/* Back to Dashboard Button */}
        <div className="bg-oracle-void border-b border-oracle-ash px-8 py-3">
          <button
            onClick={() => router.push('/dashboard')}
            className="flex items-center gap-2 text-oracle-amber-500 hover:text-oracle-amber-300 transition-colors text-sm font-medium"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </button>
        </div>

        <div className="flex-1 overflow-auto bg-oracle-void p-8">
          <div className="max-w-7xl mx-auto space-y-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-text-primary mb-2">Reports</h1>
                <p className="text-text-secondary">Generated insights and performance summaries</p>
              </div>
              <button className="btn-primary flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                Generate New Report
              </button>
            </div>

            {/* Filters */}
            <div className="flex gap-4">
              <button className="flex items-center gap-2 px-4 py-2 bg-oracle-charcoal border border-oracle-ash rounded-lg text-text-secondary hover:border-oracle-amber-500 transition-colors text-sm">
                <Filter className="w-4 h-4" />
                Period
              </button>
              <button className="flex items-center gap-2 px-4 py-2 bg-oracle-charcoal border border-oracle-ash rounded-lg text-text-secondary hover:border-oracle-amber-500 transition-colors text-sm">
                <Filter className="w-4 h-4" />
                Type
              </button>
            </div>

            {/* Reports List */}
            <div className="space-y-4">
              {reports.map((report, i) => (
                <div key={i} className="card-accent p-6 hover:border-oracle-ash transition-colors cursor-pointer group">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4 flex-1">
                      <FileText className="w-6 h-6 text-oracle-amber-500 flex-shrink-0 mt-1" />
                      <div className="flex-1">
                        <h3 className="text-lg font-bold text-text-primary group-hover:text-oracle-amber-300 transition-colors">{report.title}</h3>
                        <p className="text-text-secondary text-sm mt-1">{report.month} • Generated {report.generated}</p>
                        <div className="flex gap-6 mt-4">
                          {Object.entries(report.metrics).map(([key, value]) => (
                            <div key={key}>
                              <p className="text-xs text-text-tertiary uppercase tracking-wide">{key}</p>
                              <p className="text-sm font-bold text-oracle-amber-500">{value}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                    <button className="text-oracle-amber-500 hover:text-oracle-amber-300 transition-colors opacity-0 group-hover:opacity-100 transition-opacity">
                      <Download className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Report Scheduling */}
            <div className="card-accent p-8">
              <h3 className="text-lg font-bold mb-4">Scheduled Reports</h3>
              <p className="text-text-secondary text-sm mb-6">Set up automatic report generation and delivery</p>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-4 bg-oracle-void rounded-lg border border-oracle-ash">
                  <div>
                    <p className="text-sm font-medium text-text-primary">Weekly Performance Report</p>
                    <p className="text-xs text-text-secondary mt-1">Every Monday at 9:00 AM</p>
                  </div>
                  <button className="text-oracle-amber-500 hover:text-oracle-amber-300">Edit</button>
                </div>
                <div className="flex items-center justify-between p-4 bg-oracle-void rounded-lg border border-oracle-ash">
                  <div>
                    <p className="text-sm font-medium text-text-primary">Monthly Insights Report</p>
                    <p className="text-xs text-text-secondary mt-1">1st of every month at 8:00 AM</p>
                  </div>
                  <button className="text-oracle-amber-500 hover:text-oracle-amber-300">Edit</button>
                </div>
              </div>
              <button className="w-full mt-4 px-4 py-2 border border-oracle-ash text-text-secondary hover:border-oracle-amber-500 hover:text-oracle-amber-300 rounded-lg transition-colors text-sm">
                + Add Scheduled Report
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
