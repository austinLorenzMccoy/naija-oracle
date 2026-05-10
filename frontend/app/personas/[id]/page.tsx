import Link from 'next/link'
import Sidebar from '@/components/sidebar'
import Header from '@/components/header'
import { ArrowLeft, FileText, Lightbulb } from 'lucide-react'

export async function generateStaticParams() {
  // Generate static params for persona IDs
  return [
    { id: '1' },
    { id: '2' },
    { id: '3' },
    { id: '4' },
  ]
}

export default function PersonaDetail({ params }: { params: { id: string } }) {
  const personaId = params.id

  const persona = {
    id: 1,
    name: 'Emeka O.',
    title: 'Premium Tech Enthusiast',
    location: 'Lagos, NG',
    lga: 'Eti-Osa',
    languages: 'English, Igbo, Pidgin',
    status: 'ACTIVE_ORACLE',
    reviews: [
      { product: 'MTN Data Plan 5G', sentiment: 'MIXED', score: 0.72, excerpt: '"The speed dey sharp sharp, but price high like NEPA restoring light"' },
      { product: 'Kuda Bank UI Update', sentiment: 'POSITIVE', score: 0.94, excerpt: '"Everything set finish, clean design"' },
      { product: 'Glo Mega Data 100GB', sentiment: 'NEGATIVE', score: 0.45, excerpt: '"Connection dey fall hand for inside Eti-Osa, this one na fall hand"' },
    ],
    recommendations: [
      { product: 'iPhone 15 Pro Max', fit: '98%', reason: 'Matched for Aspiration & Tech-savviness' },
      { product: 'Terra Kulture Dining', fit: '84%', reason: 'Cultural alignment with Sunday Church lifestyle' },
    ]
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-60 flex-1 flex flex-col">
        <Header />

        <div className="flex-1 overflow-auto bg-oracle-void p-8">
          <Link href="/personas" className="flex items-center gap-2 text-oracle-amber-500 hover:text-oracle-amber-300 mb-8 w-fit">
            <ArrowLeft className="w-4 h-4" />
            Back to Personas
          </Link>

          <div className="max-w-6xl mx-auto grid lg:grid-cols-3 gap-8">
            {/* Left Column: Persona Info */}
            <div className="lg:col-span-1">
              <div className="card-accent-amber p-8 mb-8">
                <div className="w-20 h-20 rounded-full bg-oracle-amber-500/20 flex items-center justify-center text-oracle-amber-500 font-bold text-2xl mx-auto mb-6">
                  {persona.name.charAt(0)}
                </div>
                <h1 className="text-2xl font-bold text-center mb-1">{persona.name}</h1>
                <p className="text-oracle-amber-500 text-center text-sm mb-6">{persona.title}</p>

                <div className="space-y-4 pt-6 border-t border-oracle-ash">
                  <div>
                    <p className="text-text-tertiary text-xs uppercase">Location</p>
                    <p className="text-text-primary font-medium">{persona.location}</p>
                  </div>
                  <div>
                    <p className="text-text-tertiary text-xs uppercase">LGA</p>
                    <p className="text-text-primary font-medium">{persona.lga}</p>
                  </div>
                  <div>
                    <p className="text-text-tertiary text-xs uppercase">Languages</p>
                    <p className="text-text-primary font-medium">{persona.languages}</p>
                  </div>
                  <div>
                    <p className="text-text-tertiary text-xs uppercase">Status</p>
                    <p className="text-oracle-green-500 font-medium text-sm">{persona.status}</p>
                  </div>
                </div>
              </div>

              {/* Voice Fingerprint */}
              <div className="card-accent p-8">
                <h3 className="font-bold mb-6">Voice Fingerprint</h3>
                <svg viewBox="0 0 120 140" className="w-full mb-6">
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
                  <polygon points="60,35 78,55 85,78 68,95 52,95 35,78 42,55" fill="#C94020" fillOpacity="0.3" stroke="#F28060" strokeWidth="2" />

                  {/* Labels */}
                  <text x="60" y="25" textAnchor="middle" className="text-xs fill-text-secondary">SKEPTICISM</text>
                  <text x="95" y="72" textAnchor="start" className="text-xs fill-text-secondary">ASPIRATION</text>
                  <text x="60" y="115" textAnchor="middle" className="text-xs fill-text-secondary">VALUE</text>
                  <text x="15" y="75" textAnchor="end" className="text-xs fill-text-secondary">SASS</text>
                  <text x="60" y="50" textAnchor="middle" className="text-xs fill-text-secondary">LOYALTY</text>
                </svg>

                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-text-secondary">Cultural Density</span>
                    <span className="text-oracle-amber-500 font-mono">88%</span>
                  </div>
                  <div className="w-full h-1 bg-oracle-ash rounded overflow-hidden">
                    <div className="h-full bg-oracle-amber-500" style={{ width: '88%' }} />
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column: History */}
            <div className="lg:col-span-2 space-y-8">
              {/* Review History */}
              <div className="card-accent p-8">
                <div className="flex items-center gap-2 mb-6">
                  <FileText className="w-5 h-5 text-oracle-amber-500" />
                  <h3 className="font-bold text-lg">Review History</h3>
                  <span className="ml-auto text-text-secondary text-sm">{persona.reviews.length} Total Reviews</span>
                </div>

                <div className="space-y-4">
                  {persona.reviews.map((review, i) => (
                    <div key={i} className="border-b border-oracle-ash last:border-0 pb-4 last:pb-0">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <p className="font-medium text-text-primary">{review.product}</p>
                          <p className="text-sm text-text-secondary mt-1">{review.excerpt}</p>
                        </div>
                        <div className="text-right">
                          <p className={`text-xs font-medium uppercase ${
                            review.sentiment === 'POSITIVE' ? 'text-oracle-green-500' :
                            review.sentiment === 'NEGATIVE' ? 'text-oracle-terra-500' :
                            'text-oracle-amber-500'
                          }`}>
                            {review.sentiment}
                          </p>
                          <p className="text-sm font-mono text-oracle-amber-500">{review.score}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendation History */}
              <div className="card-accent p-8">
                <div className="flex items-center gap-2 mb-6">
                  <Lightbulb className="w-5 h-5 text-oracle-green-500" />
                  <h3 className="font-bold text-lg">Recommendation History</h3>
                  <span className="ml-auto text-oracle-green-500 text-sm font-medium">View All</span>
                </div>

                <div className="space-y-4">
                  {persona.recommendations.map((rec, i) => (
                    <div
                      key={i}
                      className="p-4 bg-oracle-charcoal border border-oracle-ash rounded-lg hover:border-oracle-amber-500 transition-colors cursor-pointer"
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="font-medium text-text-primary">{rec.product}</p>
                          <p className="text-sm text-text-secondary mt-1">{rec.reason}</p>
                        </div>
                        <div className="text-right">
                          <div className="relative w-12 h-12 flex items-center justify-center">
                            <svg className="w-full h-full transform -rotate-90">
                              <circle cx="24" cy="24" r="20" fill="none" stroke="#3D3B37" strokeWidth="3" />
                              <circle
                                cx="24"
                                cy="24"
                                r="20"
                                fill="none"
                                stroke="#2DB37A"
                                strokeWidth="3"
                                strokeDasharray={`${2 * Math.PI * 20 * parseInt(rec.fit) / 100} ${2 * Math.PI * 20}`}
                              />
                            </svg>
                            <span className="absolute font-mono text-xs font-bold text-oracle-green-500">{rec.fit}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
