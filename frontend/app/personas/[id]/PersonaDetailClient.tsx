'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Sidebar from '@/components/sidebar'
import Header from '@/components/header'
import { ArrowLeft, FileText, Lightbulb, Loader2, RefreshCw } from 'lucide-react'
import { API_BASE } from '@/lib/api'
import { MOCK_PERSONA_BY_ID } from '@/lib/mock-data'
import { SpeakButton } from '@/components/speak-button'

interface VoiceRadar {
  skepticism: number
  aspiration: number
  value: number
  sass: number
  loyalty: number
}

interface Persona {
  id: string
  name: string
  city: string
  lga: string
  primary_language: string
  review_style: string
  avg_rating: number
  pidgin_intensity: number
  cultural_density: number
  status: string
  age_range?: string
  voice_radar?: VoiceRadar
  cultural_markers?: string[]
  sample_reviews?: string[]
  categories_reviewed?: string[]
}

interface HistoryItem {
  id?: string
  product_name?: string
  product?: string
  sentiment?: string
  score?: number
  bertscore?: number
  review_text?: string
  review_excerpt?: string
  type?: 'review' | 'recommendation'
  fit_score?: number
  reasoning?: string
  created_at?: string
}

// Radar chart: 5-axis polygon mapped from VoiceRadar values
function RadarChart({ data }: { data: VoiceRadar }) {
  const cx = 60
  const cy = 70
  const maxR = 40

  const axes = [
    { key: 'skepticism' as const, angle: -90, label: 'SKEPTICISM', lx: 60, ly: 22 },
    { key: 'aspiration' as const, angle: -18, label: 'ASPIRATION', lx: 100, ly: 58 },
    { key: 'value' as const, angle: 54, label: 'VALUE', lx: 80, ly: 115 },
    { key: 'sass' as const, angle: 126, label: 'SASS', lx: 14, ly: 115 },
    { key: 'loyalty' as const, angle: 198, label: 'LOYALTY', lx: 4, ly: 58 },
  ]

  const toXY = (angle: number, r: number) => ({
    x: cx + r * Math.cos((angle * Math.PI) / 180),
    y: cy + r * Math.sin((angle * Math.PI) / 180),
  })

  const points = axes
    .map(({ key, angle }) => {
      const r = (data[key] ?? 0.5) * maxR
      const { x, y } = toXY(angle, r)
      return `${x},${y}`
    })
    .join(' ')

  return (
    <svg viewBox="0 0 120 140" className="w-full mb-6">
      {[10, 20, 30, 40].map((r) => (
        <polygon
          key={r}
          points={axes.map(({ angle }) => {
            const { x, y } = toXY(angle, r)
            return `${x},${y}`
          }).join(' ')}
          fill="none"
          stroke="#3D3B37"
          strokeWidth="1"
        />
      ))}
      {axes.map(({ angle, key }) => {
        const outer = toXY(angle, maxR)
        return <line key={key} x1={cx} y1={cy} x2={outer.x} y2={outer.y} stroke="#3D3B37" strokeWidth="1" />
      })}
      <polygon points={points} fill="#C94020" fillOpacity="0.3" stroke="#F28060" strokeWidth="2" />
      {axes.map(({ label, lx, ly }) => (
        <text key={label} x={lx} y={ly} textAnchor="middle" style={{ fontSize: '6px', fill: '#9A9590' }}>
          {label}
        </text>
      ))}
    </svg>
  )
}

function statusColor(status: string) {
  if (status.includes('active')) return 'text-oracle-green-500'
  if (status.includes('inactive')) return 'text-oracle-terra-500'
  return 'text-oracle-amber-500'
}

export default function PersonaDetailClient({ personaId }: { personaId: string }) {

  const [persona, setPersona] = useState<Persona | null>((MOCK_PERSONA_BY_ID[personaId] as Persona) ?? null)
  const [history, setHistory] = useState<HistoryItem[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    try {
      const [personaRes, historyRes] = await Promise.all([
        fetch(`${API_BASE}/personas/${personaId}`),
        fetch(`${API_BASE}/personas/${personaId}/history?limit=10`),
      ])

      if (!personaRes.ok) throw new Error('Persona not found')
      const personaData: Persona = await personaRes.json()
      setPersona(personaData)

      if (historyRes.ok) {
        const historyData = await historyRes.json()
        setHistory(historyData.history ?? [])
      }
    } catch {
      // Mock persona already shown — silently ignore
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [personaId])

  const reviews = history.filter((h) => h.type === 'review' || h.review_text || h.bertscore)
  const recs = history.filter((h) => h.type === 'recommendation' || h.fit_score !== undefined)

  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-60 flex-1 flex flex-col">
        <Header />

        <div className="flex-1 overflow-auto bg-oracle-void p-8">
          <div className="flex items-center gap-3 mb-8">
            <Link href="/personas" className="flex items-center gap-2 text-oracle-amber-500 hover:text-oracle-amber-300 w-fit">
              <ArrowLeft className="w-4 h-4" />
              Back to Personas
            </Link>
            <button
              onClick={fetchData}
              title="Refresh"
              className="ml-auto p-2 border border-oracle-ash text-text-secondary hover:border-oracle-amber-500 hover:text-oracle-amber-500 rounded-lg transition-colors"
              type="button"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-24">
              <Loader2 className="w-8 h-8 animate-spin text-oracle-amber-500 mr-3" />
              <span className="text-text-secondary">Loading persona...</span>
            </div>
          ) : error || !persona ? (
            <div className="card-accent p-10 text-center max-w-md mx-auto">
              <p className="text-oracle-terra-300 mb-4">{error ?? 'Persona not found'}</p>
              <button onClick={fetchData} className="btn-primary text-sm px-5 py-2" type="button">
                Retry
              </button>
            </div>
          ) : (
            <div className="max-w-6xl mx-auto grid lg:grid-cols-3 gap-8">
              {/* Left: Persona Info */}
              <div className="lg:col-span-1">
                <div className="card-accent-amber p-8 mb-8">
                  <div className="w-20 h-20 rounded-full bg-oracle-amber-500/20 flex items-center justify-center text-oracle-amber-500 font-bold text-2xl mx-auto mb-6">
                    {persona.name.charAt(0)}
                  </div>
                  <h1 className="text-2xl font-bold text-center mb-1">{persona.name}</h1>
                  <p className="text-oracle-amber-500 text-center text-sm mb-6 capitalize">{persona.review_style} · {persona.city}</p>

                  <div className="space-y-4 pt-6 border-t border-oracle-ash">
                    <div>
                      <p className="text-text-tertiary text-xs uppercase">Location</p>
                      <p className="text-text-primary font-medium">{persona.city}, NG</p>
                    </div>
                    {persona.lga && (
                      <div>
                        <p className="text-text-tertiary text-xs uppercase">LGA</p>
                        <p className="text-text-primary font-medium">{persona.lga}</p>
                      </div>
                    )}
                    <div>
                      <p className="text-text-tertiary text-xs uppercase">Primary Language</p>
                      <p className="text-text-primary font-medium capitalize">{persona.primary_language}</p>
                    </div>
                    {persona.age_range && (
                      <div>
                        <p className="text-text-tertiary text-xs uppercase">Age Range</p>
                        <p className="text-text-primary font-medium">{persona.age_range}</p>
                      </div>
                    )}
                    <div>
                      <p className="text-text-tertiary text-xs uppercase">Status</p>
                      <p className={`font-medium text-sm uppercase ${statusColor(persona.status ?? '')}`}>
                        {persona.status}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Voice Fingerprint */}
                <div className="card-accent p-8">
                  <h3 className="font-bold mb-6">Voice Fingerprint</h3>
                  {persona.voice_radar ? (
                    <RadarChart data={persona.voice_radar} />
                  ) : (
                    <div className="h-32 flex items-center justify-center text-text-tertiary text-sm">
                      No radar data
                    </div>
                  )}

                  <div className="space-y-3 text-sm mt-2">
                    <div>
                      <div className="flex justify-between mb-1">
                        <span className="text-text-secondary">Pidgin Intensity</span>
                        <span className="text-oracle-amber-500 font-mono">
                          {Math.round((persona.pidgin_intensity ?? 0) * 100)}%
                        </span>
                      </div>
                      <div className="w-full h-1 bg-oracle-ash rounded overflow-hidden">
                        <div className="h-full bg-oracle-amber-500" style={{ width: `${Math.round((persona.pidgin_intensity ?? 0) * 100)}%` }} />
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between mb-1">
                        <span className="text-text-secondary">Cultural Density</span>
                        <span className="text-oracle-amber-500 font-mono">{persona.cultural_density ?? 0}%</span>
                      </div>
                      <div className="w-full h-1 bg-oracle-ash rounded overflow-hidden">
                        <div className="h-full bg-oracle-amber-500" style={{ width: `${persona.cultural_density ?? 0}%` }} />
                      </div>
                    </div>
                  </div>

                  {persona.cultural_markers && persona.cultural_markers.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-oracle-ash">
                      <p className="text-text-tertiary text-xs uppercase mb-2">Cultural Markers</p>
                      <div className="flex flex-wrap gap-1">
                        {persona.cultural_markers.map((m) => (
                          <span key={m} className="pidgin-anchor text-xs">{m}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Right: History */}
              <div className="lg:col-span-2 space-y-8">
                {/* Sample Reviews */}
                {persona.sample_reviews && persona.sample_reviews.length > 0 && (
                  <div className="card-accent p-8">
                    <div className="flex items-center gap-2 mb-6">
                      <FileText className="w-5 h-5 text-oracle-amber-500" />
                      <h3 className="font-bold text-lg">Sample Reviews</h3>
                    </div>
                    <div className="space-y-3">
                      {persona.sample_reviews.map((r, i) => (
                        <div key={i} className="flex items-start justify-between gap-3">
                          <p className="text-text-secondary text-sm italic border-l-2 border-oracle-amber-500/30 pl-3">
                            "{r}"
                          </p>
                          <SpeakButton text={r} pidginIntensity={persona.pidgin_intensity} />
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Review History from API */}
                <div className="card-accent p-8">
                  <div className="flex items-center gap-2 mb-6">
                    <FileText className="w-5 h-5 text-oracle-amber-500" />
                    <h3 className="font-bold text-lg">Review History</h3>
                    <span className="ml-auto text-text-secondary text-sm">{reviews.length} Records</span>
                  </div>

                  {reviews.length === 0 ? (
                    <p className="text-text-tertiary text-sm text-center py-6">
                      No review history yet — run a simulation with this persona.
                    </p>
                  ) : (
                    <div className="space-y-4">
                      {reviews.map((item, i) => (
                        <div key={i} className="border-b border-oracle-ash last:border-0 pb-4 last:pb-0">
                          <div className="flex justify-between items-start mb-2">
                            <div>
                              <p className="font-medium text-text-primary">
                                {item.product_name ?? item.product ?? 'Product'}
                              </p>
                              {item.review_text && (
                                <p className="text-sm text-text-secondary mt-1 italic">"{item.review_text}"</p>
                              )}
                            </div>
                            <div className="text-right shrink-0 ml-4">
                              {item.sentiment && (
                                <p className={`text-xs font-medium uppercase ${
                                  item.sentiment === 'POSITIVE' ? 'text-oracle-green-500' :
                                  item.sentiment === 'NEGATIVE' ? 'text-oracle-terra-500' :
                                  'text-oracle-amber-500'
                                }`}>{item.sentiment}</p>
                              )}
                              {item.bertscore !== undefined && (
                                <p className="text-sm font-mono text-oracle-amber-500">{item.bertscore.toFixed(2)}</p>
                              )}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Recommendation History */}
                <div className="card-accent p-8">
                  <div className="flex items-center gap-2 mb-6">
                    <Lightbulb className="w-5 h-5 text-oracle-green-500" />
                    <h3 className="font-bold text-lg">Recommendation History</h3>
                  </div>

                  {recs.length === 0 ? (
                    <p className="text-text-tertiary text-sm text-center py-6">
                      No recommendations yet — run the recommendation engine with this persona.
                    </p>
                  ) : (
                    <div className="space-y-4">
                      {recs.map((rec, i) => {
                        const pct = Math.round((rec.fit_score ?? 0) * 100)
                        return (
                          <div key={i} className="p-4 bg-oracle-charcoal border border-oracle-ash rounded-lg hover:border-oracle-amber-500 transition-colors">
                            <div className="flex justify-between items-start">
                              <div>
                                <p className="font-medium text-text-primary">
                                  {rec.product_name ?? rec.product ?? 'Recommendation'}
                                </p>
                                {rec.reasoning && (
                                  <p className="text-sm text-text-secondary mt-1">{rec.reasoning}</p>
                                )}
                              </div>
                              <div className="relative w-12 h-12 flex items-center justify-center shrink-0 ml-4">
                                <svg className="w-full h-full transform -rotate-90">
                                  <circle cx="24" cy="24" r="20" fill="none" stroke="#3D3B37" strokeWidth="3" />
                                  <circle
                                    cx="24" cy="24" r="20" fill="none"
                                    stroke="#2DB37A" strokeWidth="3"
                                    strokeDasharray={`${2 * Math.PI * 20 * pct / 100} ${2 * Math.PI * 20}`}
                                  />
                                </svg>
                                <span className="absolute font-mono text-xs font-bold text-oracle-green-500">{pct}%</span>
                              </div>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  )}
                </div>

                {/* Categories */}
                {persona.categories_reviewed && persona.categories_reviewed.length > 0 && (
                  <div className="card-accent p-8">
                    <h3 className="font-bold text-lg mb-4">Categories Reviewed</h3>
                    <div className="flex flex-wrap gap-2">
                      {persona.categories_reviewed.map((cat) => (
                        <span key={cat} className="px-3 py-1 rounded-full border border-oracle-ash text-text-secondary text-xs capitalize">
                          {cat.replace(/_/g, ' ')}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
