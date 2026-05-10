'use client'

import { useRouter } from 'next/navigation'
import Sidebar from '@/components/sidebar'
import Header from '@/components/header'
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { TrendingUp, ArrowLeft } from 'lucide-react'

const analyticsData = [
  { week: 'Week 1', reviews: 1200, engagement: 65, sentiment: 72 },
  { week: 'Week 2', reviews: 1900, engagement: 72, sentiment: 78 },
  { week: 'Week 3', reviews: 1600, engagement: 68, sentiment: 75 },
  { week: 'Week 4', reviews: 2400, engagement: 85, sentiment: 82 },
  { week: 'Week 5', reviews: 2210, engagement: 88, sentiment: 85 },
]

const regionData = [
  { region: 'Lagos', score: 0.89 },
  { region: 'Abuja', score: 0.85 },
  { region: 'Kano', score: 0.82 },
  { region: 'Port Harcourt', score: 0.88 },
  { region: 'Ibadan', score: 0.84 },
]

export default function Analytics() {
  const router = useRouter()

  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-60 flex-1 flex flex-col">
        <Header
          tabs={[
            { label: 'Overview', href: '/dashboard', active: false },
            { label: 'Analytics', href: '/analytics', active: true },
            { label: 'Reports', href: '/reports', active: false },
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
            <div>
              <h1 className="text-3xl font-bold text-text-primary mb-2">Analytics</h1>
              <p className="text-text-secondary">Detailed performance metrics and insights</p>
            </div>

            {/* Performance Over Time */}
            <div className="card-accent p-8">
              <h3 className="text-lg font-bold mb-6">Performance Over Time</h3>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={analyticsData}>
                  <defs>
                    <linearGradient id="colorReviews" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#F5831F" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#F5831F" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#3D3B37" />
                  <XAxis dataKey="week" stroke="#9A9590" />
                  <YAxis stroke="#9A9590" />
                  <Tooltip contentStyle={{ backgroundColor: '#1A1916', border: '1px solid #3D3B37' }} labelStyle={{ color: '#F0EDE8' }} />
                  <Area type="monotone" dataKey="reviews" stroke="#F5831F" fillOpacity={1} fill="url(#colorReviews)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            <div className="grid lg:grid-cols-2 gap-8">
              {/* Engagement Trend */}
              <div className="card-accent p-8">
                <h3 className="text-lg font-bold mb-6">Engagement Trend</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={analyticsData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#3D3B37" />
                    <XAxis dataKey="week" stroke="#9A9590" />
                    <YAxis stroke="#9A9590" />
                    <Tooltip contentStyle={{ backgroundColor: '#1A1916', border: '1px solid #3D3B37' }} labelStyle={{ color: '#F0EDE8' }} />
                    <Line type="monotone" dataKey="engagement" stroke="#2DB37A" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {/* Regional Performance */}
              <div className="card-accent p-8">
                <h3 className="text-lg font-bold mb-6">Regional Performance</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={regionData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#3D3B37" />
                    <XAxis dataKey="region" stroke="#9A9590" />
                    <YAxis stroke="#9A9590" />
                    <Tooltip contentStyle={{ backgroundColor: '#1A1916', border: '1px solid #3D3B37' }} labelStyle={{ color: '#F0EDE8' }} />
                    <Bar dataKey="score" fill="#C94020" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Key Metrics */}
            <div className="grid md:grid-cols-3 gap-6">
              <div className="card-accent p-6 border-t-2 border-t-oracle-amber-500">
                <p className="text-text-secondary text-sm uppercase tracking-wide mb-2">Avg. Sentiment Score</p>
                <p className="text-3xl font-bold text-oracle-amber-500">82.4%</p>
                <p className="text-oracle-green-500 text-sm mt-2">↑ 3.2% from last period</p>
              </div>
              <div className="card-accent p-6 border-t-2 border-t-oracle-green-500">
                <p className="text-text-secondary text-sm uppercase tracking-wide mb-2">Review Velocity</p>
                <p className="text-3xl font-bold text-oracle-green-500">245/day</p>
                <p className="text-oracle-green-500 text-sm mt-2">↑ 15.8% from last period</p>
              </div>
              <div className="card-accent p-6 border-t-2 border-t-oracle-terra-500">
                <p className="text-text-secondary text-sm uppercase tracking-wide mb-2">Cultural Relevance</p>
                <p className="text-3xl font-bold text-oracle-terra-500">91.7%</p>
                <p className="text-oracle-green-500 text-sm mt-2">↑ 2.1% from last period</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
