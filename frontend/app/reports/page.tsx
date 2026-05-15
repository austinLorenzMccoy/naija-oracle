'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'
import Sidebar from '@/components/sidebar'
import Header from '@/components/header'
import { Download, Calendar, Filter, ArrowLeft, FileText } from 'lucide-react'

interface Report {
  title: string
  month: string
  metrics: Record<string, string>
  generated: string
}

const reports: Report[] = [
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
  const [reportList, setReportList] = useState<Report[]>(reports)
  const [period, setPeriod] = useState<'All' | 'April 2026' | 'Q1 2026'>('All')
  const [type, setType] = useState<'All' | 'Performance' | 'Cultural' | 'Regional' | 'Persona'>('All')
  const [schedules, setSchedules] = useState([
    { name: 'Weekly Performance Report', cadence: 'Every Monday at 9:00 AM', editing: false },
    { name: 'Monthly Insights Report', cadence: '1st of every month at 8:00 AM', editing: false },
  ])
  const [notice, setNotice] = useState<string | null>(null)

  const showNotice = (message: string) => {
    setNotice(message)
    window.setTimeout(() => setNotice(null), 2400)
  }

  const cyclePeriod = () => {
    const options = ['All', 'April 2026', 'Q1 2026'] as const
    setPeriod(options[(options.indexOf(period) + 1) % options.length])
  }

  const cycleType = () => {
    const options = ['All', 'Performance', 'Cultural', 'Regional', 'Persona'] as const
    setType(options[(options.indexOf(type) + 1) % options.length])
  }

  const visibleReports = reportList.filter((report) => {
    const matchesPeriod = period === 'All' || report.month === period
    const matchesType = type === 'All' || report.title.includes(type)
    return matchesPeriod && matchesType
  })

  const downloadReport = (report: Report) => {
    const url = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' }))
    const link = document.createElement('a')
    link.href = url
    link.download = `${report.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.json`
    link.click()
    URL.revokeObjectURL(url)
    showNotice('Report downloaded')
  }

  const generateReport = () => {
    const generated = new Date().toISOString().slice(0, 10)
    setReportList((current) => [
      {
        title: 'On-Demand Workflow Report',
        month: 'May 2026',
        metrics: { workflows: '18/18', pages: '6', status: '100%' },
        generated
      },
      ...current
    ])
    showNotice('New report generated')
  }

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
              <button onClick={generateReport} className="btn-primary flex items-center gap-2" type="button">
                <Calendar className="w-4 h-4" />
                Generate New Report
              </button>
            </div>
            {notice && <p className="rounded border border-oracle-green-500/40 px-4 py-2 text-sm text-oracle-green-500">{notice}</p>}

            {/* Filters */}
            <div className="flex gap-4">
              <button onClick={cyclePeriod} className="flex items-center gap-2 px-4 py-2 bg-oracle-charcoal border border-oracle-ash rounded-lg text-text-secondary hover:border-oracle-amber-500 transition-colors text-sm" type="button">
                <Filter className="w-4 h-4" />
                Period: {period}
              </button>
              <button onClick={cycleType} className="flex items-center gap-2 px-4 py-2 bg-oracle-charcoal border border-oracle-ash rounded-lg text-text-secondary hover:border-oracle-amber-500 transition-colors text-sm" type="button">
                <Filter className="w-4 h-4" />
                Type: {type}
              </button>
            </div>

            {/* Reports List */}
            <div className="space-y-4">
              {visibleReports.map((report, i) => (
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
                    <button
                      onClick={() => downloadReport(report)}
                      className="text-oracle-amber-500 hover:text-oracle-amber-300 transition-colors opacity-0 group-hover:opacity-100 transition-opacity"
                      type="button"
                    >
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
                {schedules.map((schedule, index) => (
                <div key={schedule.name} className="flex items-center justify-between p-4 bg-oracle-void rounded-lg border border-oracle-ash">
                  <div>
                    <p className="text-sm font-medium text-text-primary">{schedule.name}</p>
                    <p className="text-xs text-text-secondary mt-1">{schedule.editing ? 'Paused for editing' : schedule.cadence}</p>
                  </div>
                  <button
                    onClick={() => setSchedules((current) => current.map((item, i) => i === index ? { ...item, editing: !item.editing } : item))}
                    className="text-oracle-amber-500 hover:text-oracle-amber-300"
                    type="button"
                  >
                    {schedule.editing ? 'Save' : 'Edit'}
                  </button>
                </div>
                ))}
              </div>
              <button
                onClick={() => {
                  setSchedules((current) => [...current, { name: 'Custom Workflow Report', cadence: 'Every Friday at 4:00 PM', editing: false }])
                  showNotice('Scheduled report added')
                }}
                className="w-full mt-4 px-4 py-2 border border-oracle-ash text-text-secondary hover:border-oracle-amber-500 hover:text-oracle-amber-300 rounded-lg transition-colors text-sm"
                type="button"
              >
                + Add Scheduled Report
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
