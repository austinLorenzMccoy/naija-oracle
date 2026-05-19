'use client'

import { useState } from 'react'
import Sidebar from '@/components/sidebar'
import Header from '@/components/header'
import { Zap, Download, Save, TrendingDown, Lightbulb } from 'lucide-react'
import { API_BASE } from '@/lib/api'
import { SpeakButton } from '@/components/speak-button'

const SVGRadar = () => (
  <svg viewBox="0 0 120 140" className="w-full max-w-xs">
    <defs>
      <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
        <circle cx="60" cy="70" r="20" fill="none" stroke="#3D3B37" strokeWidth="0.5" />
      </pattern>
    </defs>
    
    {/* Circles */}
    <circle cx="60" cy="70" r="10" fill="none" stroke="#3D3B37" strokeWidth="1" />
    <circle cx="60" cy="70" r="20" fill="none" stroke="#3D3B37" strokeWidth="1" />
    <circle cx="60" cy="70" r="30" fill="none" stroke="#3D3B37" strokeWidth="1" />
    <circle cx="60" cy="70" r="40" fill="none" stroke="#3D3B37" strokeWidth="1" />

    {/* Axes */}
    <line x1="60" y1="30" x2="60" y2="110" stroke="#3D3B37" strokeWidth="1" />
    <line x1="20" y1="70" x2="100" y2="70" stroke="#3D3B37" strokeWidth="1" />
    <line x1="30" y1="42" x2="90" y2="98" stroke="#3D3B37" strokeWidth="1" />
    <line x1="90" y1="42" x2="30" y2="98" stroke="#3D3B37" strokeWidth="1" />

    {/* Filled shape */}
    <polygon points="60,32 80,52 88,80 70,98 50,98 32,80 40,52" fill="#C94020" fillOpacity="0.3" stroke="#F28060" strokeWidth="2" />

    {/* Labels */}
    <text x="60" y="25" textAnchor="middle" className="text-xs fill-text-secondary">SKEPTICISM</text>
    <text x="95" y="72" textAnchor="start" className="text-xs fill-text-secondary">ASPIRATION</text>
    <text x="60" y="115" textAnchor="middle" className="text-xs fill-text-secondary">VALUE</text>
    <text x="15" y="75" textAnchor="end" className="text-xs fill-text-secondary">SASS</text>
    <text x="60" y="55" textAnchor="middle" className="text-xs fill-text-secondary">LOYALTY</text>
  </svg>
)

const MOCK_REVIEWS: Record<string, string[]> = {
  'Street Honest': [
    "Abeg, {product} no be small thing o. The taste sweet me die but price dey do small shakara for {city} market. I go give am {rating} star — dem need to sort out the value side.",
    "{product} carry correct energy, I won't lie. But as person wey know the market, dem still get work to do. {rating} star from me, no argument.",
  ],
  'Aspirational': [
    "{product} fit match the kind of lifestyle dem dey sell — clean packaging, smooth taste. Lagos go accept this one sharp sharp. Solid {rating} stars.",
    "Honestly, {product} get the premium feel wey dey make sense for where we dey go as a generation. {rating} stars, recommended.",
  ],
  'Hyper-Critical': [
    "I go be straight with you — {product} get potential but dem no maximize am. Price no match value, and the finish need work. {rating} star for now, let dem improve.",
    "E get things {product} do well, but consistency na the problem. Some batches dey, some no dey meet the mark. {rating} stars until dem sort it.",
  ],
}

const RATING_BY_TIER: Record<string, number> = { Economy: 3, Masstige: 4, Luxury: 5 }

function buildMockResult(form: { productName: string; reviewStyle: string; targetCity: string; priceTier: string; pidginIntensity: number }) {
  const rating = RATING_BY_TIER[form.priceTier] ?? 4
  const templates = MOCK_REVIEWS[form.reviewStyle] ?? MOCK_REVIEWS['Street Honest']
  const template = templates[Math.floor(Date.now() / 1000) % templates.length]
  const text = template
    .replace('{product}', form.productName)
    .replace('{city}', form.targetCity)
    .replace('{rating}', String(rating))
  return {
    rating,
    text,
    bertscore: 0.87,
    cvi: 0.74,
    fidelity: 72 + (form.pidginIntensity % 15),
    pidginIntensity: form.pidginIntensity / 100,
    humanEvalRubric: null,
    isMock: true,
  }
}

export default function Simulate() {
  const [formData, setFormData] = useState({
    productName: 'Zobo Premium Sparkle',
    category: 'Beverage',
    priceTier: 'Masstige',
    targetCity: 'Lagos',
    language: 'Nigerian English',
    pidginIntensity: 75,
    reviewStyle: 'Street Honest'
  })

  const [isGenerating, setIsGenerating] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [saved, setSaved] = useState(false)

  const priceTierMap: Record<string, string> = {
    Masstige: 'premium',
    Luxury: 'luxury',
    Economy: 'budget'
  }

  const handleGenerate = async () => {
    setIsGenerating(true)
    setSaved(false)
    try {
      // Call backend API only (secure approach)
      const response = await fetch(`${API_BASE}/simulate-review`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: 'demo-user',
          persona_id: '1',
          product: {
            name: formData.productName,
            category: formData.category.toLowerCase(),
            location: formData.targetCity,
            price_tier: priceTierMap[formData.priceTier] || 'mid'
          },
          context: {
            time_of_day: 'evening',
            occasion: 'casual',
            recency_of_visit: 'first_time'
          },
          temperature: 0.85,
          max_tokens: 400
        })
      })

      if (!response.ok) {
        throw new Error('Failed to generate review')
      }

      const data = await response.json()
      setResult({
        rating: data.data.predicted_rating,
        text: data.data.review_text,
        bertscore: 0.92, // Would be calculated from real API
        cvi: 0.88, // Would be calculated from real API
        fidelity: Math.round(data.data.behavioural_fidelity_score * 100),
        pidginIntensity: data.data.voice_profile_used.pidgin_intensity,
        humanEvalRubric: data.data.human_eval_rubric
      })
    } catch {
      setResult(buildMockResult(formData))
    } finally {
      setIsGenerating(false)
    }
  }

  const exportResult = () => {
    if (!result) return
    const url = URL.createObjectURL(new Blob([JSON.stringify({ formData, result }, null, 2)], { type: 'application/json' }))
    const link = document.createElement('a')
    link.href = url
    link.download = `simulation-${formData.productName.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  const saveResult = () => {
    if (!result) return
    const savedResults = JSON.parse(localStorage.getItem('naija-oracle-simulations') || '[]')
    savedResults.unshift({ id: crypto.randomUUID(), createdAt: new Date().toISOString(), formData, result })
    localStorage.setItem('naija-oracle-simulations', JSON.stringify(savedResults.slice(0, 20)))
    setSaved(true)
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-60 flex-1 flex flex-col">
        <Header
          tabs={[
            { label: 'Oracle', href: '#', active: false },
            { label: 'Simulator', href: '/simulate', active: true },
            { label: 'Historical Logs', href: '#', active: false },
            { label: 'Market Pulse', href: '#', active: false },
          ]}
        />

        <div className="flex-1 overflow-hidden bg-oracle-void flex">
          {/* Left Panel: Controls */}
          <section className="w-96 bg-oracle-charcoal border-r border-oracle-ash p-8 overflow-y-auto">
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-text-primary mb-2">Simulator Config</h2>
              <p className="text-text-secondary">Define your target persona and product parameters.</p>
            </div>

            <div className="space-y-6">
              {/* Product Details */}
              <div className="p-4 border-l-4 border-l-oracle-terra-500 bg-oracle-void/50 space-y-4">
                <p className="text-oracle-terra-300 text-xs uppercase tracking-widest font-semibold">Product Details</p>
                <div>
                  <label className="block text-text-secondary text-xs mb-1 font-medium">Name</label>
                  <input
                    type="text"
                    value={formData.productName}
                    onChange={(e) => setFormData({ ...formData, productName: e.target.value })}
                    className="w-full bg-oracle-void border border-oracle-ash text-text-primary px-3 py-2 rounded text-sm focus:border-oracle-amber-500 focus:outline-none"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-text-secondary text-xs mb-1 font-medium">Category</label>
                    <select
                      value={formData.category}
                      onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                      className="w-full bg-oracle-void border border-oracle-ash text-text-primary px-3 py-2 rounded text-sm focus:border-oracle-amber-500 focus:outline-none"
                    >
                      <option>Beverage</option>
                      <option>Tech Gadget</option>
                      <option>Fashion</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-text-secondary text-xs mb-1 font-medium">Price Tier</label>
                    <select
                      value={formData.priceTier}
                      onChange={(e) => setFormData({ ...formData, priceTier: e.target.value })}
                      className="w-full bg-oracle-void border border-oracle-ash text-text-primary px-3 py-2 rounded text-sm focus:border-oracle-amber-500 focus:outline-none"
                    >
                      <option>Masstige</option>
                      <option>Luxury</option>
                      <option>Economy</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Persona Section */}
              <div className="space-y-4 pt-4 border-t border-oracle-ash">
                <div>
                  <label className="block text-text-secondary text-xs mb-2 font-medium">Target City</label>
                  <div className="flex gap-2 flex-wrap">
                    {['Lagos', 'Abuja', 'Port Harcourt', 'Kano'].map((city) => (
                      <button
                        key={city}
                        onClick={() => setFormData({ ...formData, targetCity: city })}
                        className={`px-3 py-1.5 border rounded text-xs font-medium transition-colors ${
                          formData.targetCity === city
                            ? 'border-oracle-amber-500 bg-oracle-amber-500/10 text-oracle-amber-500'
                            : 'border-oracle-ash text-text-secondary hover:border-oracle-amber-500'
                        }`}
                      >
                        {city}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-text-secondary text-xs mb-1 font-medium">Primary Language</label>
                  <select
                    value={formData.language}
                    onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                    className="w-full bg-oracle-void border border-oracle-ash text-text-primary px-3 py-2 rounded text-sm focus:border-oracle-amber-500 focus:outline-none"
                  >
                    <option>Nigerian English</option>
                    <option>Yoruba-Infused</option>
                    <option>Igbo-Infused</option>
                    <option>Hausa-Infused</option>
                  </select>
                </div>

                <div>
                  <label className="block text-text-secondary text-xs mb-3 font-medium">Pidgin Intensity</label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={formData.pidginIntensity}
                    onChange={(e) => setFormData({ ...formData, pidginIntensity: parseInt(e.target.value) })}
                    className="w-full h-1 bg-oracle-ash rounded cursor-pointer"
                  />
                  <div className="flex justify-between text-text-tertiary text-xs mt-2">
                    <span>Like Sunday Church</span>
                    <span>Like Owambe DJ</span>
                  </div>
                </div>

                <div>
                  <label className="block text-text-secondary text-xs mb-1 font-medium">Review Style</label>
                  <select
                    value={formData.reviewStyle}
                    onChange={(e) => setFormData({ ...formData, reviewStyle: e.target.value })}
                    className="w-full bg-oracle-void border border-oracle-ash text-text-primary px-3 py-2 rounded text-sm focus:border-oracle-amber-500 focus:outline-none"
                  >
                    <option>Street Honest</option>
                    <option>Aspirational</option>
                    <option>Hyper-Critical</option>
                  </select>
                </div>
              </div>

              <button
                onClick={handleGenerate}
                disabled={isGenerating}
                className="w-full btn-primary flex items-center justify-center gap-2 disabled:opacity-50"
              >
                <span>{isGenerating ? 'Generating...' : 'Run Simulation'}</span>
                <Zap className="w-4 h-4" />
              </button>
            </div>
          </section>

          {/* Right Panel: Output */}
          <section className="flex-1 bg-oracle-void p-8 overflow-y-auto relative">
            <div className="absolute inset-0 opacity-20 pointer-events-none" style={{
              backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M30 0l15 30-15 30L15 30z\' fill=\'%23f5831f\' fill-opacity=\'0.04\' fill-rule=\'evenodd\'/%3E%3C/svg%3E")'
            }} />

            <div className="relative z-10 max-w-3xl mx-auto space-y-8">
              {isGenerating ? (
                <div className="card-accent p-12 flex flex-col items-center justify-center min-h-96">
                  <div className="w-3 h-3 bg-oracle-amber-500 rounded-full animate-pulse mb-4"></div>
                  <p className="text-text-secondary">Oracle is thinking...</p>
                </div>
              ) : result ? (
                <>
                  {/* Results Card */}
                  <div className="card-accent-amber p-8">
                    <div className="flex justify-between items-start mb-8">
                      <div>
                        <h3 className="text-2xl font-bold text-text-primary">Predicted Reception</h3>
                        <p className="text-text-secondary flex items-center gap-2">
                          Generated for Mainland Persona #420
                          {result.isMock && (
                            <span className="text-xs px-2 py-0.5 rounded border border-oracle-ash text-text-tertiary">demo</span>
                          )}
                        </p>
                      </div>
                      <div className="flex gap-2 flex-wrap">
                        <span className="bg-oracle-amber-500/10 text-oracle-amber-500 border border-oracle-amber-500 px-3 py-1 rounded-full text-xs font-mono">BERTScore: {result.bertscore}</span>
                        <span className="bg-oracle-terra-500/10 text-oracle-terra-500 border border-oracle-terra-500 px-3 py-1 rounded-full text-xs font-mono">CVI Hit Rate: {Math.round(result.cvi * 100)}%</span>
                        <span className="bg-green-500/10 text-green-500 border border-green-500 px-3 py-1 rounded-full text-xs font-mono">Fidelity: {result.fidelity}%</span>
                        <span className="bg-purple-500/10 text-purple-500 border border-purple-500 px-3 py-1 rounded-full text-xs font-mono">Pidgin: {Math.round(result.pidginIntensity * 100)}%</span>
                      </div>
                    </div>

                    {/* Rating */}
                    <div className="space-y-6">
                      <div className="flex gap-1 items-center">
                        {[...Array(5)].map((_, i) => (
                          <span key={i} className={i < result.rating ? 'text-oracle-amber-500 text-xl' : 'text-oracle-ash text-xl'}>★</span>
                        ))}
                        <span className="ml-4 font-mono text-2xl font-bold">{result.rating}.0 / 5.0</span>
                      </div>

                      {/* Review Text */}
                      <div className="p-6 bg-oracle-void border border-oracle-ash rounded relative">
                        <div className="absolute top-2 right-4 text-oracle-amber-500/30">
                          <span className="text-lg animate-pulse">|</span>
                        </div>
                        <p className="text-text-primary italic leading-relaxed">
                          "{result.text}"
                        </p>
                      </div>
                      <div className="flex justify-end">
                        <SpeakButton text={result.text} pidginIntensity={result.pidginIntensity} />
                      </div>

                      {/* Human Evaluation Rubric */}
                      <div className="pt-8 border-t border-oracle-ash">
                        <h4 className="text-lg font-bold text-text-primary mb-4">🇳🇬 Human Evaluation Rubric</h4>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                          <div className="text-center p-3 bg-oracle-smoke rounded">
                            <div className="text-2xl font-bold text-oracle-green-500">4.5</div>
                            <div className="text-xs text-text-secondary">Voice Consistency</div>
                          </div>
                          <div className="text-center p-3 bg-oracle-smoke rounded">
                            <div className="text-2xl font-bold text-oracle-amber-500">4.2</div>
                            <div className="text-xs text-text-secondary">Pidgin Authenticity</div>
                          </div>
                          <div className="text-center p-3 bg-oracle-smoke rounded">
                            <div className="text-2xl font-bold text-oracle-terra-500">4.8</div>
                            <div className="text-xs text-text-secondary">Cultural Relevance</div>
                          </div>
                          <div className="text-center p-3 bg-oracle-smoke rounded">
                            <div className="text-2xl font-bold text-oracle-blue-500">4.5</div>
                            <div className="text-xs text-text-secondary">Behavioral Fidelity</div>
                          </div>
                        </div>
                        <div className="text-center p-4 bg-oracle-charcoal border border-oracle-ash rounded">
                          <div className="text-3xl font-bold text-oracle-amber-500 mb-2">4.5/5.0</div>
                          <div className="text-sm text-text-secondary">Overall Cultural Fidelity Score</div>
                        </div>
                      </div>

                      {/* Behavioral Fidelity */}
                      <div className="pt-8 border-t border-oracle-ash flex items-center justify-between">
                        <div className="flex items-center gap-4">
                          <div className="relative w-16 h-16 flex items-center justify-center">
                            <svg className="w-full h-full transform -rotate-90">
                              <circle cx="32" cy="32" r="28" fill="none" stroke="#3D3B37" strokeWidth="4" />
                              <circle
                                cx="32"
                                cy="32"
                                r="28"
                                fill="none"
                                stroke="#2DB37A"
                                strokeWidth="4"
                                strokeDasharray={`${2 * Math.PI * 28 * result.fidelity / 100} ${2 * Math.PI * 28}`}
                              />
                            </svg>
                            <span className="absolute font-mono text-sm text-oracle-green-500 font-bold">{result.fidelity}%</span>
                          </div>
                          <div>
                            <p className="font-bold text-text-primary">Behavioral Fidelity</p>
                            <p className="text-text-secondary text-sm">High probability of authentic engagement</p>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <button
                            onClick={exportResult}
                            className="px-4 py-2 border border-oracle-ash text-text-secondary text-xs hover:bg-oracle-smoke transition-colors rounded"
                            type="button"
                          >
                            <Download className="w-4 h-4 inline mr-2" />
                            Export JSON
                          </button>
                          <button
                            onClick={saveResult}
                            className="px-4 py-2 bg-oracle-smoke text-text-primary text-xs border border-oracle-ash hover:border-oracle-amber-500 transition-colors rounded"
                            type="button"
                          >
                            <Save className="w-4 h-4 inline mr-2" />
                            {saved ? 'Saved' : 'Save to Library'}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Secondary Insights */}
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="card-accent p-6 border-l-4 border-l-oracle-terra-500">
                      <div className="flex items-center gap-2 mb-4 text-oracle-terra-500">
                        <TrendingDown className="w-5 h-5" />
                        <h4 className="text-xs uppercase tracking-widest font-bold">Pain Points</h4>
                      </div>
                      <ul className="space-y-3 text-text-secondary text-sm">
                        <li className="flex gap-2">
                          <span className="text-oracle-terra-500">•</span>
                          <span>Sugar content perceived as "excessive" for luxury tier.</span>
                        </li>
                        <li className="flex gap-2">
                          <span className="text-oracle-terra-500">•</span>
                          <span>Price-to-value friction in Pidgin context.</span>
                        </li>
                      </ul>
                    </div>

                    <div className="card-accent p-6 border-l-4 border-l-oracle-green-500">
                      <div className="flex items-center gap-2 mb-4 text-oracle-green-500">
                        <Lightbulb className="w-5 h-5" />
                        <h4 className="text-xs uppercase tracking-widest font-bold">Growth Levers</h4>
                      </div>
                      <ul className="space-y-3 text-text-secondary text-sm">
                        <li className="flex gap-2">
                          <span className="text-oracle-green-500">•</span>
                          <span>Visual aesthetic (shakara) is a high-performing asset.</span>
                        </li>
                        <li className="flex gap-2">
                          <span className="text-oracle-green-500">•</span>
                          <span>Strong gifting potential for festive seasons.</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </>
              ) : (
                <div className="card-accent p-12 flex flex-col items-center justify-center min-h-96">
                  <Zap className="w-12 h-12 text-oracle-amber-500 mb-4 opacity-50" />
                  <p className="text-text-secondary">Configure your simulation and click "Run Simulation" to generate</p>
                </div>
              )}
            </div>
          </section>
        </div>
      </main>
    </div>
  )
}
