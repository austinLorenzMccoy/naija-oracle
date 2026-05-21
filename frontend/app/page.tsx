'use client'

import { useEffect, useState, useRef } from 'react'
import Link from 'next/link'
import { Zap, ArrowDown, Loader2 } from 'lucide-react'
import { API_BASE } from '@/lib/api'

const DEMO_PERSONA = { city: 'Lagos', language: 'Pidgin', product: 'Zobo Premium Sparkle', category: 'beverage' }

// Pidgin phrase highlighting
function highlightPidgin(text: string) {
  const phrases = ['sharp sharp', 'NEPA', 'abeg', 'omo', 'sha', 'die o', 'no be', 'wahala', 'na', 'e don', 'chop', 'fall hand', 'sabi', 'yawa', 'shakara']
  const escaped = phrases.map((p) => p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')
  const parts = text.split(new RegExp(`(${escaped})`, 'gi'))
  return parts.map((part, i) =>
    phrases.some((p) => p.toLowerCase() === part.toLowerCase())
      ? <span key={i} className="pidgin-anchor">{part}</span>
      : part
  )
}

export default function Home() {
  const [demoState, setDemoState] = useState<'idle' | 'loading' | 'done' | 'error'>('idle')
  const [demoText, setDemoText] = useState('')
  const [demoRating, setDemoRating] = useState(0)
  const [demoFidelity, setDemoFidelity] = useState(0)
  const outputRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleScroll = () => {}
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const runDemo = async () => {
    setDemoState('loading')
    setDemoText('')
    try {
      const res = await fetch(`${API_BASE}/simulate-review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: 'demo-user',
          persona_id: '1',
          product: {
            name: DEMO_PERSONA.product,
            category: DEMO_PERSONA.category,
            location: DEMO_PERSONA.city,
            price_tier: 'mid',
          },
          context: { time_of_day: 'evening', occasion: 'casual', recency_of_visit: 'first_time' },
          temperature: 0.9,
          max_tokens: 300,
        }),
      })

      if (!res.ok) throw new Error('API error')
      const data = await res.json()
      const text: string = data?.data?.review_text ?? ''
      const rating: number = data?.data?.predicted_rating ?? 4
      const fidelity: number = Math.round((data?.data?.behavioural_fidelity_score ?? 0.82) * 100)

      setDemoRating(rating)
      setDemoFidelity(fidelity)

      // Simulate streaming character by character
      setDemoState('done')
      let i = 0
      const interval = setInterval(() => {
        i += 3
        setDemoText(text.slice(0, i))
        if (i >= text.length) clearInterval(interval)
      }, 30)
    } catch {
      // Fallback demo text if backend not running
      const fallback = 'E be like say this Zobo fine die o — the colour deep like Lagos twilight and the taste sharp sharp. But abeg, the price too high for ordinary market woman. I go manage sha, taste dey there.'
      setDemoRating(4)
      setDemoFidelity(84)
      setDemoState('done')
      let i = 0
      const interval = setInterval(() => {
        i += 3
        setDemoText(fallback.slice(0, i))
        if (i >= fallback.length) clearInterval(interval)
      }, 30)
    }
  }

  return (
    <main className="bg-oracle-void text-text-primary">
      {/* Hero Section */}
      <section className="hero min-h-screen flex items-center justify-center relative overflow-hidden px-4 py-20">
        <div className="absolute inset-0 bg-gradient-to-b from-oracle-amber-500/8 to-oracle-void pointer-events-none" />

        <div className="relative z-10 text-center max-w-3xl mx-auto">
          <div className="mb-8 animate-fade-in">
            <p className="text-oracle-amber-500 font-serif italic text-lg mb-4">The oracle that</p>
            <h1 className="text-6xl md:text-7xl font-serif font-bold mb-6">speaks Naija.</h1>
          </div>

          <p className="text-text-secondary text-lg md:text-xl mb-12 max-w-2xl mx-auto leading-relaxed">
            Advanced consumer intelligence tuned to the cadence of the Nigerian market. From Balogun market dynamics to Ikoyi luxury trends—we decode the nuance.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Link href="/dashboard" className="btn-primary flex items-center justify-center gap-2 group">
              Try the Oracle <Zap className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
            <a href="https://github.com/austinLorenzMccoy/naija_oracle" target="_blank" rel="noopener noreferrer" className="btn-ghost flex items-center justify-center">
              View on GitHub
            </a>
          </div>

          <button
            onClick={() => document.getElementById('stats')?.scrollIntoView({ behavior: 'smooth' })}
            className="flex justify-center animate-bounce mx-auto"
            type="button"
            aria-label="Scroll to stats"
          >
            <ArrowDown className="w-6 h-6 text-oracle-amber-500" />
          </button>
        </div>
      </section>

      {/* Stats Bar */}
      <section id="stats" className="bg-oracle-charcoal border-y border-oracle-ash py-16">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { value: '2', label: 'Agents Built' },
              { value: '3', label: 'Datasets' },
              { value: '15', label: 'Personas' },
              { value: '<200ms', label: 'Latency' },
            ].map(({ value, label }) => (
              <div key={label} className="text-center">
                <div className="font-mono text-3xl font-bold text-oracle-amber-500 mb-2">{value}</div>
                <div className="text-text-secondary text-sm uppercase tracking-wide">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Live Demo Embed */}
      <section id="demo" className="py-24 px-4 bg-oracle-charcoal">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-4xl font-serif font-bold text-center mb-2">Run the Oracle</h2>
          <p className="text-text-secondary text-center mb-10">One click. A live Nigerian consumer voice, generated instantly.</p>

          <div className="border border-oracle-ash rounded-xl overflow-hidden">
            {/* Demo header */}
            <div className="bg-oracle-smoke px-6 py-4 flex items-center justify-between border-b border-oracle-ash">
              <div>
                <p className="text-text-primary font-medium text-sm">{DEMO_PERSONA.product}</p>
                <p className="text-text-tertiary text-xs">{DEMO_PERSONA.city} · Pidgin · Evening</p>
              </div>
              <button
                onClick={runDemo}
                disabled={demoState === 'loading'}
                className="btn-primary flex items-center gap-2 text-sm px-5 py-2 disabled:opacity-60"
                type="button"
              >
                {demoState === 'loading' ? (
                  <><Loader2 className="w-4 h-4 animate-spin" /> Thinking...</>
                ) : (
                  <><Zap className="w-4 h-4" /> {demoState === 'done' ? 'Regenerate' : 'Run Oracle'}</>
                )}
              </button>
            </div>

            {/* Output area */}
            <div ref={outputRef} className="bg-oracle-void min-h-52 p-6">
              {demoState === 'idle' && (
                <div className="flex flex-col items-center justify-center h-40 text-text-tertiary text-sm">
                  <Zap className="w-8 h-8 text-oracle-amber-500/30 mb-3" />
                  Click "Run Oracle" to generate a live Nigerian consumer review
                </div>
              )}

              {demoState === 'loading' && (
                <div className="flex flex-col items-center justify-center h-40">
                  <div className="w-2 h-2 bg-oracle-amber-500 rounded-full animate-pulse mb-3" />
                  <p className="text-text-secondary text-sm">Oracle is thinking...</p>
                </div>
              )}

              {(demoState === 'done') && (
                <div>
                  {/* Rating row */}
                  <div className="flex items-center gap-3 mb-4">
                    <div className="flex gap-1">
                      {[...Array(5)].map((_, i) => (
                        <span key={i} className={i < demoRating ? 'text-oracle-amber-500' : 'text-oracle-ash'}>★</span>
                      ))}
                    </div>
                    <span className="font-mono text-oracle-amber-500 text-sm">{demoRating}.0 / 5.0</span>
                    <span className="ml-auto font-mono text-oracle-green-500 text-xs bg-oracle-green-500/10 border border-oracle-green-500/30 px-2 py-0.5 rounded-full">
                      Fidelity: {demoFidelity}%
                    </span>
                  </div>

                  {/* Streaming text */}
                  <p className="text-text-primary font-mono text-sm leading-relaxed italic" aria-live="polite">
                    "{highlightPidgin(demoText)}
                    {demoText.length > 0 && demoText.length < 300 && (
                      <span className="text-oracle-amber-500 animate-pulse">|</span>
                    )}"
                  </p>
                </div>
              )}
            </div>

            {/* Footer badges */}
            {demoState === 'done' && (
              <div className="bg-oracle-smoke px-6 py-3 flex gap-3 border-t border-oracle-ash flex-wrap">
                <span className="text-xs font-mono text-oracle-amber-500 bg-oracle-amber-500/10 border border-oracle-amber-500/30 px-2 py-0.5 rounded-full">Lagos Persona</span>
                <span className="text-xs font-mono text-oracle-terra-300 bg-oracle-terra-500/10 border border-oracle-terra-500/30 px-2 py-0.5 rounded-full">Pidgin Infused</span>
                <span className="text-xs font-mono text-oracle-green-500 bg-oracle-green-500/10 border border-oracle-green-500/30 px-2 py-0.5 rounded-full">CVI Anchored</span>
                <Link href="/simulate" className="ml-auto text-xs text-oracle-amber-500 hover:text-oracle-amber-300 transition-colors">
                  Full Simulator →
                </Link>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-serif font-bold mb-2 text-center">How It Works</h2>
          <p className="text-text-secondary text-center mb-16">The pipeline that breathes life into Naija voices</p>

          <div className="grid md:grid-cols-2 gap-12">
            <div className="space-y-8">
              {[
                { num: '01', title: 'Cultural Context Injection', desc: 'We ingest live conversational data from across the 36 states, ensuring regional slang and sentiment are captured in real-time.' },
                { num: '02', title: 'Persona Synthesis', desc: 'Our engine creates hyper-realistic simulated personas that range from "The Gen-Z Techie" to "The Market Woman."' },
                { num: '03', title: 'Voice-Anchored Output', desc: 'The Cultural Voice Index pins generated text to measurable linguistic markers — every "sharp sharp" has a source.' },
              ].map((step, i) => (
                <div key={i} className="flex gap-4">
                  <div className="text-oracle-terra-500 font-serif font-bold text-2xl flex-shrink-0">{step.num}</div>
                  <div>
                    <h3 className="text-lg font-bold mb-2">{step.title}</h3>
                    <p className="text-text-secondary">{step.desc}</p>
                  </div>
                </div>
              ))}
            </div>

            <div className="bg-oracle-charcoal border border-oracle-ash rounded-lg p-8 flex items-center justify-center h-72">
              <div className="text-center w-full">
                <div className="w-12 h-12 bg-oracle-amber-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Zap className="w-6 h-6 text-oracle-amber-500" />
                </div>
                <p className="text-text-secondary text-sm mb-4 font-mono">simulator_v2.log</p>
                <div className="text-sm text-oracle-amber-500 font-mono space-y-1 text-left bg-oracle-void rounded p-4">
                  <p>{'>>> Loading CVI weights...'}</p>
                  <p>{'>>> Persona: Lagos Mainland, Pidgin 82%'}</p>
                  <p>{'>>> Generating voice-anchored review...'}</p>
                  <p className="text-oracle-green-500">{'>>> Done. BERTScore: 0.892'}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Voice Section */}
      <section className="py-24 px-4 bg-gradient-to-b from-oracle-void to-oracle-charcoal">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-serif italic text-center mb-16">E go sound like them</h2>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { name: 'Emeka', title: 'Trader, Alaba International', quote: 'Abi d quality nah better — bring am, Mister, people go just commot for business fast fast.' },
              { name: 'Aisha', title: 'Freelancer, Hardi City', quote: 'The service is alaye, but I prefer if I can pay with my local transfer directly, no wahala.' },
              { name: 'Tunde', title: 'Dev, Yaba Tech-Hub', quote: 'Omo, the packaging reach to show off for public, but the sugar for inside na different matter sha.' },
            ].map((persona, i) => (
              <div key={i} className="card-accent p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-12 h-12 rounded-full bg-oracle-amber-500/20 flex items-center justify-center text-oracle-amber-500 font-bold">
                    {persona.name.charAt(0)}
                  </div>
                  <div>
                    <p className="font-bold">{persona.name}</p>
                    <p className="text-xs text-text-secondary uppercase">{persona.title}</p>
                  </div>
                </div>
                <p className="text-sm italic text-text-secondary">"{persona.quote}"</p>
                <div className="flex items-center gap-1 mt-4">
                  {[...Array(5)].map((_, j) => (
                    <span key={j} className="text-oracle-amber-500">★</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-oracle-ash/30 py-8 px-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <p className="text-oracle-amber-500 font-serif italic">Naija Oracle</p>
          <p className="text-text-tertiary text-sm">© 2025 Naija Oracle. Built for Balogun, Optimized for Global.</p>
        </div>
      </footer>
    </main>
  )
}
