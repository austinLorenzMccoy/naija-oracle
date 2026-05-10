'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Zap, ArrowDown } from 'lucide-react'

export default function Home() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 100)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <main className="bg-oracle-void text-text-primary">
      {/* Hero Section */}
      <section className="min-h-screen flex items-center justify-center relative overflow-hidden px-4 py-20">
        {/* Subtle gradient glow */}
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
            <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="btn-ghost flex items-center justify-center">
              View on GitHub
            </a>
          </div>

          {/* Scroll indicator */}
          <div className="flex justify-center animate-bounce">
            <ArrowDown className="w-6 h-6 text-oracle-amber-500" />
          </div>
        </div>
      </section>

      {/* Stats Bar */}
      <section className="bg-oracle-charcoal border-y border-oracle-ash py-16">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="font-mono text-3xl font-bold text-oracle-amber-500 mb-2">2</div>
              <div className="text-text-secondary text-sm uppercase tracking-wide">Agents Built</div>
            </div>
            <div className="text-center">
              <div className="font-mono text-3xl font-bold text-oracle-amber-500 mb-2">3</div>
              <div className="text-text-secondary text-sm uppercase tracking-wide">Datasets</div>
            </div>
            <div className="text-center">
              <div className="font-mono text-3xl font-bold text-oracle-amber-500 mb-2">500+</div>
              <div className="text-text-secondary text-sm uppercase tracking-wide">Personas</div>
            </div>
            <div className="text-center">
              <div className="font-mono text-3xl font-bold text-oracle-amber-500 mb-2">&lt;200ms</div>
              <div className="text-text-secondary text-sm uppercase tracking-wide">Latency</div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-serif font-bold mb-2 text-center">How It Works</h2>
          <p className="text-text-secondary text-center mb-16">The pipeline that breathes life into Naija voices</p>
          
          <div className="grid md:grid-cols-2 gap-12">
            {/* Steps */}
            <div className="space-y-8">
              {[
                {
                  num: '01',
                  title: 'Cultural Context Injection',
                  desc: 'We ingest live conversational data from across the 36 states, ensuring regional slang and sentiment are captured in real-time.'
                },
                {
                  num: '02',
                  title: 'Persona Synthesis',
                  desc: 'Our engine creates hyper-realistic simulated personas that range from "The Gen-Z Techie" to "The Market Woman."'
                }
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

            {/* Visualization */}
            <div className="bg-oracle-charcoal border border-oracle-ash rounded-lg p-8 flex items-center justify-center h-80">
              <div className="text-center">
                <div className="w-12 h-12 bg-oracle-amber-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Zap className="w-6 h-6 text-oracle-amber-500" />
                </div>
                <p className="text-text-secondary">simulator_v2.log</p>
                <div className="text-sm text-oracle-amber-500 mt-4">
                  <p>{'>>> Loading Pidgin Weights...'}</p>
                  <p>{'>>> Generating response based on Lagos Mainland persona...'}</p>
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
              {
                name: 'Emeka',
                title: 'Trader, Alaba International',
                quote: 'Abi d quality nah better bring am Mister people go just commot for business'
              },
              {
                name: 'Aisha',
                title: 'Freelancer, Hardi City',
                quote: 'The service is alaye, but I prefer if I can pay with my local wealth directly, Naija'
              },
              {
                name: 'Tunde',
                title: 'Dev, Yaba Tech-Hub',
                quote: 'Omo, the packaging reach to show off for public, but the sugar for inside na different matter'
              }
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
          <p className="text-oracle-amber-500 font-serif italic">Oracle</p>
          <p className="text-text-tertiary text-sm">© 2024 Naija Oracle. Built for Balogun, Optimized for Global.</p>
        </div>
      </footer>
    </main>
  )
}
