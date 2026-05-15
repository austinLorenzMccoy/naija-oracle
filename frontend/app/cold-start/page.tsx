'use client'

import { useState } from 'react'
import Link from 'next/link'
import Sidebar from '@/components/sidebar'
import { Loader2, ArrowLeft } from 'lucide-react'
import { API_BASE } from '@/lib/api'

interface ColdStartAnswer {
  food: string
  entertainment: string
  bank: string
  transport: string
  social: string
}

interface Recommendation {
  id: string
  name: string
  category: string
  rating: number
  description: string
  distance?: string
  price?: string
  confidence: number
}

const questions = [
  { id: 'food', q: "What's your go-to street food?", opts: ['Suya', 'Shawarma', 'Boli', 'Moi Moi'], icon: '🍢' },
  { id: 'entertainment', q: 'Weekend vibes: what\'s your move?', opts: ['AMVCA Movies', 'BBNaija Drama', 'Live Concert', 'Gaming'], icon: '🎬' },
  { id: 'bank', q: 'Your trusted banking app?', opts: ['GTB', 'Kuda', 'Opay', 'PalmPay'], icon: '🏦' },
  { id: 'transport', q: 'How do you move around Lagos?', opts: ['Uber/Bolt', 'Danfo Bus', 'Keke Napep', 'Bike'], icon: '🚗' },
  { id: 'social', q: 'Your social media poison?', opts: ['Twitter/X', 'Instagram', 'TikTok', 'WhatsApp'], icon: '📱' },
]

export default function ColdStartDemo() {
  const [step, setStep] = useState(0)
  const [answers, setAnswers] = useState<Partial<ColdStartAnswer>>({})
  const [recommendations, setRecommendations] = useState<Recommendation[]>([])
  const [selected, setSelected] = useState<Recommendation | null>(null)
  const [loading, setLoading] = useState(false)

  const fetchRecommendations = async (ans: ColdStartAnswer) => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: 'demo-user',
          persona_id: '1',
          domain: ans.food === 'Suya' ? 'food' : 'entertainment',
          context: {
            current_time: 'Saturday 7PM',
            location: 'Lekki Phase 1, Lagos',
            mood_signal: ans.entertainment === 'Live Concert' ? 'celebratory' : 'casual',
            recent_searches: Object.values(ans),
            budget_naira: 15000,
            occasion: 'casual',
            companions: 'friends',
          },
          cold_start: true,
          max_recommendations: 3,
          include_explanation: true,
        }),
      })

      const data = await res.json()
      if (res.ok && data.success) {
        setRecommendations(
          (data.data.recommendations || []).map((item: any) => ({
            id: item.item_id,
            name: item.name,
            category: item.category,
            rating: item.predicted_rating,
            description: item.reasoning,
            distance: item.location,
            price: item.price_tier,
            confidence: item.context_score,
          }))
        )
      } else {
        throw new Error('API failed')
      }
    } catch {
      setRecommendations([
        {
          id: 'fallback-1',
          name: ans.food === 'Suya' ? "Mama T's Suya Spot" : 'New Afrika Shrine',
          category: ans.entertainment,
          rating: 4.6,
          description: `Matched your ${ans.food}, ${ans.entertainment}, and ${ans.social} signals.`,
          distance: 'Lagos',
          price: 'mid',
          confidence: 0.86,
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleAnswer = (qid: string, ans: string) => {
    const newAnswers = { ...answers, [qid]: ans }
    setAnswers(newAnswers)
    if (step < questions.length - 1) {
      setStep(step + 1)
    } else {
      fetchRecommendations(newAnswers as ColdStartAnswer)
    }
  }

  const reset = () => {
    setStep(0)
    setAnswers({})
    setRecommendations([])
    setSelected(null)
  }

  const progress = Math.round(((step + 1) / questions.length) * 100)

  // Loading state
  if (loading) {
    return (
      <div className="flex">
        <Sidebar />
        <main className="ml-60 flex-1 flex flex-col bg-oracle-void">
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <div className="w-16 h-16 bg-oracle-amber-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <Loader2 className="w-8 h-8 text-oracle-amber-500 animate-spin" />
              </div>
              <h2 className="text-2xl font-serif font-bold text-text-primary mb-2">Finding Your Vibe...</h2>
              <p className="text-text-secondary">Analysing your Nigerian preferences</p>
            </div>
          </div>
        </main>
      </div>
    )
  }

  // Results state
  if (recommendations.length > 0) {
    return (
      <div className="flex">
        <Sidebar />
        <main className="ml-60 flex-1 flex flex-col bg-oracle-void">
          <div className="flex-1 overflow-auto p-8">
            <div className="max-w-4xl mx-auto">
              <div className="mb-10 text-center">
                <p className="text-oracle-amber-500 font-serif italic text-lg mb-2">Based on your vibes</p>
                <h1 className="text-4xl font-serif font-bold text-text-primary mb-3">Your Personalised Picks</h1>
                <p className="text-text-secondary">Curated from your Nigerian lifestyle signals</p>
              </div>

              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-10">
                {recommendations.map((rec) => (
                  <div
                    key={rec.id}
                    onClick={() => setSelected(rec)}
                    className={`card-accent p-6 cursor-pointer transition-all hover:border-oracle-amber-500 ${selected?.id === rec.id ? 'border-oracle-amber-500 bg-oracle-smoke' : ''}`}
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="font-bold text-text-primary text-lg">{rec.name}</h3>
                        <p className="text-text-secondary text-xs capitalize mt-1">{rec.category}</p>
                      </div>
                      <span className="bg-oracle-amber-500/10 text-oracle-amber-500 border border-oracle-amber-500/30 px-2 py-0.5 rounded-full text-xs font-mono">
                        {Math.round(rec.confidence * 100)}% match
                      </span>
                    </div>

                    <div className="flex items-center gap-1 mb-3">
                      {[...Array(5)].map((_, j) => (
                        <span key={j} className={j < Math.floor(rec.rating) ? 'text-oracle-amber-500' : 'text-oracle-ash'}>★</span>
                      ))}
                      <span className="ml-2 font-mono text-oracle-amber-500 text-sm">{rec.rating}</span>
                    </div>

                    <p className="text-text-secondary text-sm leading-relaxed">{rec.description}</p>

                    {rec.distance && (
                      <p className="text-text-tertiary text-xs mt-3">{rec.distance}</p>
                    )}
                    {rec.price && (
                      <span className="inline-block mt-2 px-2 py-0.5 border border-oracle-ash rounded text-xs text-text-secondary capitalize">
                        {rec.price}
                      </span>
                    )}
                  </div>
                ))}
              </div>

              {selected && (
                <div className="card-accent-amber p-6 mb-8">
                  <h3 className="font-bold text-text-primary mb-2">{selected.name}</h3>
                  <p className="text-text-secondary text-sm">{selected.description}</p>
                  <p className="text-text-tertiary text-xs mt-3">
                    This recommendation was generated because it matches your cold-start onboarding answers and your Lagos context profile.
                  </p>
                </div>
              )}

              <div className="flex gap-4 justify-center">
                <button onClick={reset} className="btn-ghost px-6 py-3" type="button">
                  Try Again
                </button>
                <Link href="/dashboard" className="btn-primary px-6 py-3">
                  Go to Dashboard
                </Link>
              </div>
            </div>
          </div>
        </main>
      </div>
    )
  }

  // Quiz state
  const currentQ = questions[step]

  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-60 flex-1 flex flex-col bg-oracle-void">
        <div className="flex-1 overflow-auto p-8">
          <div className="max-w-xl mx-auto">
            <Link href="/dashboard" className="inline-flex items-center gap-2 text-oracle-amber-500 hover:text-oracle-amber-300 mb-10 text-sm">
              <ArrowLeft className="w-4 h-4" />
              Back to Dashboard
            </Link>

            <div className="mb-10 text-center">
              <p className="text-oracle-amber-500 font-serif italic text-lg mb-2">Cold-Start Onboarding</p>
              <h1 className="text-3xl font-serif font-bold text-text-primary mb-3">Tell us your Nigerian vibe</h1>
              <p className="text-text-secondary text-sm">
                Question {step + 1} of {questions.length}
              </p>
            </div>

            {/* Progress bar */}
            <div className="w-full h-1 bg-oracle-ash rounded overflow-hidden mb-8">
              <div
                className="h-full bg-oracle-amber-500 transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>

            <div className="card-accent p-8">
              <div className="flex items-center gap-3 mb-6">
                <span className="text-3xl">{currentQ.icon}</span>
                <div>
                  <h2 className="text-xl font-bold text-text-primary">{currentQ.q}</h2>
                  <p className="text-text-secondary text-sm">Choose the option that best represents you</p>
                </div>
              </div>

              <div className="space-y-3">
                {currentQ.opts.map((opt) => (
                  <button
                    key={opt}
                    onClick={() => handleAnswer(currentQ.id, opt)}
                    className="w-full text-left px-5 py-4 border border-oracle-ash rounded-lg text-text-primary hover:border-oracle-amber-500 hover:bg-oracle-amber-500/5 transition-all font-medium"
                    type="button"
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>

            <p className="text-center text-text-tertiary text-xs mt-6">
              Your answers help us create recommendations that match your Nigerian lifestyle
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}
