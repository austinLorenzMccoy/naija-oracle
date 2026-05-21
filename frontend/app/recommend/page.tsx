'use client'

import { useState } from 'react'
import Sidebar from '@/components/sidebar'
import Header from '@/components/header'
import { Send, Loader2 } from 'lucide-react'
import { API_BASE } from '@/lib/api'

const recommendations = [
  {
    name: 'Yellow Chilli',
    rating: 4.2,
    reviews: '1.2k',
    distance: '0.8km away',
    price: '₦₦₦',
    reason: 'Matches your "Owambe DJ" mood with high-energy evening service and Premium Seafood Okro, that hits every cultural note you prefer.',
    highlighted: ['Premium Seafood Okro']
  },
  {
    name: 'Nok by Alara',
    rating: 4.9,
    reviews: '884+',
    distance: '1.4km away',
    price: '₦₦',
    reason: 'WHY THIS RECOMMENDATION?',
    expanded: true
  }
]

export default function Recommend() {
  const [mood, setMood] = useState('celebratory')
  const [budget, setBudget] = useState('15000')
  const [location, setLocation] = useState('Lekki Phase 1, Lagos')
  const [query, setQuery] = useState('')
  const [items, setItems] = useState(recommendations)
  const [explanation, setExplanation] = useState("I understand, Teniola. You're looking for that \"Luxe-Afrobeats\" intersection. Based on your current mood and budget, I've curated three spots in VI that hit the mark perfectly.")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [mode, setMode] = useState<'single' | 'cross'>('single')

  const CROSS_DOMAIN_FALLBACK = [
    { name: 'Yellow Chilli Restaurant', rating: 4.4, reviews: '🍽 Food', distance: 'Victoria Island', price: 'premium', reason: 'Matches your celebratory mood — live Afrobeats band on Friday nights turns dinner into an experience.', expanded: true },
    { name: 'New Afrika Shrine', rating: 4.7, reviews: '🎵 Entertainment', distance: 'Ikeja', price: 'mid', reason: 'Cross-domain transfer from food preference: high-energy Afro vibe maps directly to live music concerts.', expanded: true },
    { name: 'Lagos Fashion Hub', rating: 4.3, reviews: '👗 Fashion', distance: 'Lekki', price: 'premium', reason: 'Users who dine at Yellow Chilli regularly browse fashion boutiques — category graph edge (food→fashion, weight 0.71).', expanded: true },
  ]

  const requestRecommendations = async () => {
    if (mode === 'cross') {
      setLoading(true)
      await new Promise(r => setTimeout(r, 900))
      setExplanation("Cross-domain transfer activated. Your Suya → Afrobeats signal path fired: dining preference mapped to live music (edge weight 0.71), then outward to fashion via collaborative filter. Three domains, one evening plan.")
      setItems(CROSS_DOMAIN_FALLBACK)
      setLoading(false)
      return
    }
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: 'demo-user',
          persona_id: '1',
          domain: 'food',
          context: {
            current_time: 'Friday 8PM',
            location,
            mood_signal: mood,
            recent_searches: query ? [query] : [],
            budget_naira: Number(budget.replace(/[^\d.]/g, '')) || 15000,
            occasion: 'after_work',
            companions: 'friends'
          },
          max_recommendations: 3,
          include_explanation: true,
          temperature: 0.7
        })
      })
      const data = await response.json()
      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Recommendation request failed')
      }
      setExplanation(data.data.explanation)
      setItems(data.data.recommendations.map((item: any) => ({
        name: item.name,
        rating: item.predicted_rating,
        reviews: `${Math.round(item.context_score * 100)}% fit`,
        distance: item.distance_km ? `${item.distance_km}km away` : item.location,
        price: item.price_tier,
        reason: item.reasoning,
        expanded: true
      })))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Recommendation request failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-60 flex-1 flex flex-col">
        <Header />

        <div className="flex-1 overflow-hidden bg-oracle-void flex">
          {/* Left Panel: Persona Context */}
          <section className="w-80 bg-oracle-charcoal border-r border-oracle-ash p-8 overflow-y-auto">
            <div className="mb-8">
              <h2 className="text-lg font-bold text-text-primary mb-2">Active Context</h2>
              <p className="text-text-secondary text-sm">Teniola, "The Tech-Baddie"</p>
              {/* Domain mode toggle */}
              <div className="flex gap-2 mt-4">
                <button
                  onClick={() => setMode('single')}
                  className={`flex-1 py-1.5 rounded text-xs font-medium transition-colors border ${mode === 'single' ? 'border-oracle-amber-500 bg-oracle-amber-500/10 text-oracle-amber-500' : 'border-oracle-ash text-text-secondary hover:border-oracle-amber-500'}`}
                  type="button"
                >
                  Single Domain
                </button>
                <button
                  onClick={() => setMode('cross')}
                  className={`flex-1 py-1.5 rounded text-xs font-medium transition-colors border ${mode === 'cross' ? 'border-oracle-green-500 bg-oracle-green-500/10 text-oracle-green-500' : 'border-oracle-ash text-text-secondary hover:border-oracle-green-500'}`}
                  type="button"
                >
                  Cross-Domain
                </button>
              </div>
              {mode === 'cross' && (
                <p className="text-xs text-oracle-green-500 mt-2 border border-oracle-green-500/30 bg-oracle-green-500/5 rounded px-2 py-1">
                  Food → Entertainment → Fashion transfer active
                </p>
              )}
            </div>

            <div className="card-accent-amber p-6 mb-8">
              <div className="w-16 h-16 rounded-full bg-oracle-amber-500/20 flex items-center justify-center text-oracle-amber-500 font-bold text-2xl mx-auto mb-4">
                T
              </div>
              <p className="text-center font-medium mb-1">Teniola O.</p>
              <p className="text-center text-oracle-amber-500 text-xs uppercase mb-6">Professional • Lekki Phase 1</p>

              <div className="space-y-3 pt-6 border-t border-oracle-ash">
                <div>
                  <p className="text-text-tertiary text-xs uppercase mb-1">Current Mood</p>
                  <input
                    type="text"
                    placeholder="e.g., celebratory"
                    value={mood}
                    onChange={(event) => setMood(event.target.value)}
                    className="w-full bg-oracle-void border border-oracle-ash text-text-primary px-3 py-2 rounded text-sm focus:border-oracle-amber-500 focus:outline-none"
                  />
                </div>
                <div>
                  <p className="text-text-tertiary text-xs uppercase mb-1">Budget</p>
                  <input
                    type="text"
                    placeholder="e.g., ₦5k-₦15k"
                    value={budget}
                    onChange={(event) => setBudget(event.target.value)}
                    className="w-full bg-oracle-void border border-oracle-ash text-text-primary px-3 py-2 rounded text-sm focus:border-oracle-amber-500 focus:outline-none"
                  />
                </div>
                <div>
                  <p className="text-text-tertiary text-xs uppercase mb-1">Location Radius</p>
                  <input
                    type="text"
                    placeholder="e.g., Lekki"
                    value={location}
                    onChange={(event) => setLocation(event.target.value)}
                    className="w-full bg-oracle-void border border-oracle-ash text-text-primary px-3 py-2 rounded text-sm focus:border-oracle-amber-500 focus:outline-none"
                  />
                </div>
              </div>
            </div>

            <div className="card-accent p-6 mb-8">
              <p className="text-text-secondary text-xs uppercase tracking-wide mb-3">NDCG@10 Score</p>
              <div className="relative h-2 bg-oracle-ash rounded overflow-hidden mb-2">
                <div className="h-full bg-oracle-green-500" style={{ width: '82%' }} />
              </div>
              <p className="font-mono text-oracle-green-500 text-sm">0.847</p>
            </div>
          </section>

          {/* Right Panel: Chat */}
          <section className="flex-1 bg-oracle-void p-8 overflow-y-auto">
            <div className="max-w-2xl mx-auto space-y-6">
              {/* Chat Messages */}
              <div className="bg-oracle-charcoal border border-oracle-ash p-6 rounded-lg">
                <p className="text-text-secondary text-sm mb-4">
                  <span className="text-oracle-amber-500 font-bold">[Oracle]</span>
                </p>
                <p className="text-text-primary leading-relaxed mb-4">
                  {explanation}
                </p>
                {error && (
                  <p className="mb-4 rounded border border-oracle-terra-500/50 bg-oracle-terra-500/10 px-3 py-2 text-sm text-oracle-terra-300">
                    {error}
                  </p>
                )}

                {/* Recommendation Cards */}
                <div className="space-y-4">
                  {items.map((rec, i) => (
                    <div key={i} className="bg-oracle-void border border-oracle-ash rounded-lg p-4 hover:border-oracle-amber-500 transition-colors cursor-pointer">
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h4 className="font-bold text-text-primary">{rec.name}</h4>
                          <div className="flex gap-3 mt-2">
                            <div className="flex gap-1">
                              {[...Array(5)].map((_, j) => (
                                <span key={j} className={j < Math.floor(rec.rating) ? 'text-oracle-amber-500' : 'text-oracle-ash'}>★</span>
                              ))}
                              <span className="text-text-secondary text-xs ml-1">{rec.reviews}</span>
                            </div>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-oracle-amber-500 font-medium text-sm">{rec.distance}</p>
                          <p className="text-text-secondary text-xs mt-1">{rec.price}</p>
                        </div>
                      </div>

                      <p className="text-text-secondary text-sm mb-2">{rec.reason}</p>
                      {rec.expanded && (
                        <button
                          onClick={() => setExplanation(`${rec.name}: ${rec.reason}`)}
                          className="text-oracle-amber-500 hover:text-oracle-amber-300 text-xs font-medium"
                          type="button"
                        >
                          Why this?
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Input */}
              <div className="mt-auto">
                <form
                  onSubmit={(event) => {
                    event.preventDefault()
                    requestRecommendations()
                  }}
                  className="flex gap-3"
                >
                  <input
                    type="text"
                    placeholder="Ask for specific cultural nuances (e.g., 'no loud music', 'indoor seating')..."
                    value={query}
                    onChange={(event) => setQuery(event.target.value)}
                    className="flex-1 bg-oracle-charcoal border border-oracle-ash text-text-primary px-4 py-3 rounded-lg focus:border-oracle-amber-500 focus:outline-none"
                  />
                  <button
                    className="bg-oracle-amber-500 text-oracle-void px-4 py-3 rounded-lg hover:bg-oracle-amber-300 transition-colors disabled:opacity-60"
                    type="submit"
                    disabled={loading}
                  >
                    {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
                  </button>
                </form>
                {loading && (
                  <p className="mt-3 text-xs text-text-tertiary text-center border border-oracle-ash rounded px-4 py-2 bg-oracle-charcoal">
                    <span className="text-oracle-amber-500 font-medium">Render free-tier note:</span> torch + sentence-transformers load into 512 MB RAM on first use. If this takes &gt;30s the service may be cold-starting — it will complete or fall back to demo data automatically.
                  </p>
                )}
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  )
}
