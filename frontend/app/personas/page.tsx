'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import Sidebar from '@/components/sidebar'
import Header from '@/components/header'
import { MapPin, ChevronRight, Loader2, Search, RefreshCw } from 'lucide-react'
import { API_BASE } from '@/lib/api'
import { MOCK_PERSONAS } from '@/lib/mock-data'

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
  categories_reviewed?: string[]
}

function languageLabel(lang: string): string {
  const map: Record<string, string> = {
    igbo: 'English, Igbo, Pidgin',
    yoruba: 'English, Yoruba, Pidgin',
    hausa: 'English, Hausa, Pidgin',
    pidgin: 'Pidgin, English',
    english: 'English',
  }
  return map[lang?.toLowerCase()] ?? lang
}

export default function Personas() {
  const [personas, setPersonas] = useState<Persona[]>(MOCK_PERSONAS as Persona[])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [query, setQuery] = useState('')

  const fetchPersonas = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/personas?user_id=demo-user`)
      if (!res.ok) throw new Error('Failed to load personas')
      const data: Persona[] = await res.json()
      setPersonas(data)
    } catch {
      // Keep showing mock data — no error banner needed
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const urlQuery = new URLSearchParams(window.location.search).get('search')?.toLowerCase() || ''
    setQuery(urlQuery)
    fetchPersonas()
  }, [])

  const filtered = personas.filter((p) => {
    if (!query) return true
    const haystack = `${p.name} ${p.city} ${p.primary_language} ${p.review_style}`.toLowerCase()
    return haystack.includes(query)
  })

  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-60 flex-1 flex flex-col">
        <Header />

        <div className="flex-1 overflow-auto bg-oracle-void p-8">
          <div className="max-w-6xl mx-auto">
            <div className="flex items-start justify-between mb-8">
              <div>
                <h1 className="text-3xl font-bold mb-2">Persona Profiles</h1>
                <p className="text-text-secondary">
                  {loading
                    ? 'Loading personas...'
                    : query
                    ? `Showing matches for "${query}"`
                    : `${personas.length} simulated personas in your research pool`}
                </p>
              </div>
              <div className="flex items-center gap-3">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary pointer-events-none" />
                  <input
                    type="text"
                    placeholder="Search personas..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value.toLowerCase())}
                    className="pl-9 pr-4 py-2 bg-oracle-charcoal border border-oracle-ash text-text-primary rounded-lg text-sm focus:border-oracle-amber-500 focus:outline-none w-52"
                  />
                </div>
                <button
                  onClick={fetchPersonas}
                  title="Refresh"
                  className="p-2 border border-oracle-ash text-text-secondary hover:border-oracle-amber-500 hover:text-oracle-amber-500 rounded-lg transition-colors"
                  type="button"
                >
                  <RefreshCw className="w-4 h-4" />
                </button>
              </div>
            </div>

            {loading ? (
              <div className="flex items-center justify-center py-24">
                <Loader2 className="w-8 h-8 animate-spin text-oracle-amber-500 mr-3" />
                <span className="text-text-secondary">Loading personas...</span>
              </div>
            ) : error ? (
              <div className="card-accent p-8 text-center">
                <p className="text-oracle-terra-300 mb-4">{error}</p>
                <button onClick={fetchPersonas} className="btn-primary text-sm px-5 py-2" type="button">
                  Retry
                </button>
              </div>
            ) : filtered.length === 0 ? (
              <div className="card-accent p-12 text-center">
                <p className="text-text-secondary">No personas match "{query}"</p>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filtered.map((persona) => (
                  <Link
                    key={persona.id}
                    href={`/personas/${persona.id}`}
                    className="card-accent p-6 hover:border-oracle-amber-500 transition-colors group"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-4">
                        <div className="w-12 h-12 rounded-full bg-oracle-amber-500/20 flex items-center justify-center text-oracle-amber-500 font-bold text-lg">
                          {persona.name.charAt(0)}
                        </div>
                        <div>
                          <h3 className="font-bold text-text-primary group-hover:text-oracle-amber-500 transition-colors">
                            {persona.name}
                          </h3>
                          <p className="text-text-secondary text-xs capitalize">
                            {persona.review_style} · {persona.age_range || '25-34'}
                          </p>
                        </div>
                      </div>
                      <ChevronRight className="w-5 h-5 text-text-tertiary group-hover:text-oracle-amber-500 transition-colors" />
                    </div>

                    <div className="space-y-3 pt-4 border-t border-oracle-ash">
                      <div className="flex items-center gap-2 text-sm">
                        <MapPin className="w-4 h-4 text-oracle-amber-500" />
                        <span className="text-text-secondary">{persona.city}, NG</span>
                        {persona.lga && <span className="text-text-tertiary text-xs">· {persona.lga}</span>}
                      </div>
                      <p className="text-xs text-text-primary font-medium">{languageLabel(persona.primary_language)}</p>

                      <div className="flex justify-between pt-3 border-t border-oracle-ash">
                        <div>
                          <p className="text-xs text-text-tertiary">Avg Rating</p>
                          <p className="text-sm font-mono text-oracle-amber-500">{persona.avg_rating?.toFixed(1)}</p>
                        </div>
                        <div>
                          <p className="text-xs text-text-tertiary">Pidgin</p>
                          <p className="text-sm font-mono text-oracle-amber-500">
                            {Math.round((persona.pidgin_intensity ?? 0) * 100)}%
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-text-tertiary">Cultural</p>
                          <p className="text-sm font-mono text-oracle-green-500">{persona.cultural_density ?? 0}%</p>
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
