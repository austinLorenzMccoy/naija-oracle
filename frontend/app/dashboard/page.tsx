'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import Sidebar from '@/components/sidebar'
import Header from '@/components/header'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts'
import { TrendingUp, Zap, Activity, Award, ArrowLeft, Loader2 } from 'lucide-react'

interface MetricCard {
  label: string
  value: string
  change: string
  trend: string
  icon: any
  color: string
  badge?: string
}

interface ChartData {
  name: string
  score: number
}

interface LiveActivity {
  name: string
  time: string
  review: string
  stars: number
}

export default function Dashboard() {
  const [metricCards, setMetricCards] = useState<MetricCard[]>([])
  const [chartData, setChartData] = useState<ChartData[]>([])
  const [liveActivity, setLiveActivity] = useState<LiveActivity[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Fetch metrics from backend
      const metricsResponse = await fetch('http://localhost:8000/api/v1/eval/metrics')
      if (!metricsResponse.ok) {
        throw new Error('Failed to fetch metrics')
      }
      
      // Mock data for now (would be replaced with real API calls)
      setMetricCards([
        {
          label: 'Reviews Generated',
          value: '12,482',
          change: '+14.2% from last week',
          trend: 'up',
          icon: Award,
          color: 'text-oracle-amber-500'
        },
        {
          label: 'Avg BERTScore',
          value: '0.892',
          change: '',
          icon: Zap,
          color: 'text-oracle-amber-500',
          badge: 'AMBER_PILL'
        },
        {
          label: 'Avg NDCG@10',
          value: '0.745',
          change: '',
          icon: Activity,
          color: 'text-oracle-amber-500'
        },
        {
          label: 'Active Personas',
          value: '3',
          change: '',
          icon: TrendingUp,
          color: 'text-oracle-amber-500'
        }
      ])

      setChartData([
        { name: 'v1.0.2', score: 0.782 },
        { name: 'v1.0.3', score: 0.801 },
        { name: 'v1.0.4-beta', score: 0.845 },
        { name: 'v1.1.0', score: 0.871 },
        { name: 'v1.1.1-rc', score: 0.892 },
      ])

      setLiveActivity([
        { name: 'Ifeanyi from Aba', time: '14:22:55', review: '"The delivery was sharp sharp, no..."', stars: 5 },
        { name: 'Abuja Tech Bro', time: '14:20:32', review: '"Implementation is sleek, but the..."', stars: 4 },
        { name: 'Mama Nkechi', time: '14:18:45', review: '"God bless you people, my busines..."', stars: 5 },
        { name: 'Lagos Island Hustler', time: '14:15:38', review: '"Why is the network behaving like..."', stars: 2 },
      ])
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
      setError('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-60 flex-1 flex flex-col">
        <Header
          tabs={[
            { label: 'Overview', href: '/dashboard', active: true },
            { label: 'Analytics', href: '/analytics', active: false },
            { label: 'Reports', href: '/reports', active: false },
          ]}
        />

        {/* Back to Home Button */}
        <div className="bg-oracle-void border-b border-oracle-ash px-8 py-4">
          <Link
            href="/"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-oracle-amber-500 hover:text-oracle-amber-300 hover:bg-oracle-charcoal active:opacity-70 transition-all text-sm font-medium cursor-pointer border border-transparent hover:border-oracle-ash"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>
        </div>

        <div className="flex-1 overflow-auto bg-oracle-void p-8">
          <div className="max-w-7xl mx-auto space-y-8">
            {loading ? (
              <div className="flex items-center justify-center py-20">
                <Loader2 className="w-8 h-8 animate-spin text-oracle-amber-500" />
                <span className="ml-2 text-text-secondary">Loading dashboard data...</span>
              </div>
            ) : error ? (
              <div className="card-accent p-8 text-center">
                <p className="text-red-500 mb-4">Error: {error}</p>
                <button 
                  onClick={fetchDashboardData}
                  className="px-4 py-2 bg-oracle-amber-500 text-white rounded hover:bg-oracle-amber-600 transition-colors"
                >
                  Retry
                </button>
              </div>
            ) : (
              <>
                {/* Metric Cards Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {metricCards.map((card: MetricCard, i: number) => {
                    const Icon = card.icon
                    return (
                      <div key={i} className="card-accent p-6 border-oracle-amber-500/20">
                        <div className="flex items-start justify-between mb-4">
                          <div>
                            <p className="text-text-secondary text-sm uppercase tracking-wide mb-2">{card.label}</p>
                            <p className="font-mono text-3xl font-bold text-oracle-amber-500">{card.value}</p>
                          </div>
                          <Icon className={`w-6 h-6 ${card.color}`} />
                        </div>
                        {card.change && (
                          <p className="text-oracle-green-500 text-sm">{card.change}</p>
                        )}
                      </div>
                    )
                  })}
                </div>
              </>
            )}

            {/* Charts Row */}
            <div className="grid lg:grid-cols-3 gap-8">
              {/* Experiment Comparison */}
              <div className="lg:col-span-2 card-accent p-8">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-lg font-bold">Experiment Comparison</h3>
                    <p className="text-text-secondary text-sm">BERTScore variance across model iterations</p>
                  </div>
                  <select className="bg-oracle-void border border-oracle-ash text-text-secondary text-sm px-3 py-1.5 rounded">
                    <option>Last 5 Versions</option>
                    <option>Last 10 Versions</option>
                  </select>
                </div>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#3D3B37" />
                    <XAxis dataKey="name" stroke="#9A9590" />
                    <YAxis stroke="#9A9590" />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#1A1916', border: '1px solid #3D3B37' }}
                      labelStyle={{ color: '#F0EDE8' }}
                    />
                    <Bar dataKey="score" fill="#F5831F" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Live Activity */}
              <div className="card-accent p-8">
                <div className="flex items-center gap-2 mb-6">
                  <div className="w-2 h-2 bg-oracle-amber-500 rounded-full animate-pulse"></div>
                  <h3 className="text-lg font-bold">Live Activity</h3>
                </div>
                <div className="space-y-4">
                  {liveActivity.map((item, i) => (
                    <div key={i} className="pb-4 border-b border-oracle-ash last:border-0">
                      <p className="text-oracle-amber-500 text-sm font-medium">{item.name}</p>
                      <p className="text-text-secondary text-xs mt-1">{item.time}</p>
                      <p className="text-text-secondary text-sm mt-2">{item.review}</p>
                      <div className="flex gap-1 mt-2">
                        {[...Array(5)].map((_, j) => (
                          <span key={j} className={j < item.stars ? 'text-oracle-amber-500' : 'text-oracle-ash'}>
                            ★
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
                <button className="w-full mt-6 text-oracle-amber-500 hover:text-oracle-amber-300 text-sm font-medium">
                  View Full Stream
                </button>
              </div>
            </div>

            {/* Insights Row */}
            <div className="grid md:grid-cols-2 gap-8">
              <div className="card-accent p-8 border-l-4 border-l-oracle-terra-500">
                <div className="flex items-start gap-3 mb-4">
                  <Zap className="w-5 h-5 text-oracle-terra-500 flex-shrink-0 mt-1" />
                  <h3 className="text-lg font-bold">Optimization Tip</h3>
                </div>
                <p className="text-text-secondary">
                  Your BERTScore has improved by 4% after the latest training set update with more Pidgin dialects. Consider increasing the cultural density weight.
                </p>
              </div>
              <div className="card-accent p-8 border-l-4 border-l-oracle-green-500">
                <div className="flex items-start gap-3 mb-4">
                  <TrendingUp className="w-5 h-5 text-oracle-green-500 flex-shrink-0 mt-1" />
                  <h3 className="text-lg font-bold">Market Insight</h3>
                </div>
                <p className="text-text-secondary">
                  Sentiment peaks on Friday evenings, matching "Owambe" patterns across Southwest regions. Recommendation timing optimized for this window.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
