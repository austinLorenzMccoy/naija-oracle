'use client'

import Link from 'next/link'
import Sidebar from '@/components/sidebar'
import Header from '@/components/header'
import { MapPin, ChevronRight } from 'lucide-react'

const personas = [
  {
    id: 1,
    name: 'Emeka O.',
    title: 'Premium Tech Enthusiast',
    location: 'Lagos, NG',
    lga: 'Eti-Osa',
    languages: 'English, Igbo, Pidgin',
    reviews: 14,
    rating: 4.2,
    cvi: 0.82,
  },
  {
    id: 2,
    name: 'Aisha H.',
    title: 'Freelancer, Hardi City',
    location: 'Kano, NG',
    lga: 'Tarauni',
    languages: 'English, Hausa, Pidgin',
    reviews: 8,
    rating: 4.5,
    cvi: 0.88,
  },
  {
    id: 3,
    name: 'Tunde B.',
    title: 'Dev, Yaba Tech-Hub',
    location: 'Lagos, NG',
    lga: 'Yaba',
    languages: 'English, Yoruba, Pidgin',
    reviews: 22,
    rating: 3.9,
    cvi: 0.75,
  },
  {
    id: 4,
    name: 'Chioma E.',
    title: 'Business Owner',
    location: 'Enugu, NG',
    lga: 'Enugu East',
    languages: 'English, Igbo',
    reviews: 11,
    rating: 4.7,
    cvi: 0.91,
  },
  {
    id: 5,
    name: 'Ibrahim M.',
    title: 'Trader',
    location: 'Kano, NG',
    lga: 'Kano Municipal',
    languages: 'Hausa, Arabic, English',
    reviews: 19,
    rating: 4.1,
    cvi: 0.79,
  },
  {
    id: 6,
    name: 'Zainab A.',
    title: 'Student & Content Creator',
    location: 'Lagos, NG',
    lga: 'Ikoyi',
    languages: 'English, Yoruba, Pidgin',
    reviews: 6,
    rating: 4.3,
    cvi: 0.86,
  },
]

export default function Personas() {
  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-60 flex-1 flex flex-col">
        <Header />

        <div className="flex-1 overflow-auto bg-oracle-void p-8">
          <div className="max-w-6xl mx-auto">
            <div className="mb-8">
              <h1 className="text-3xl font-bold mb-2">Persona Profiles</h1>
              <p className="text-text-secondary">Explore the 500+ simulated personas in your research pool</p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {personas.map((persona) => (
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
                        <h3 className="font-bold text-text-primary group-hover:text-oracle-amber-500 transition-colors">{persona.name}</h3>
                        <p className="text-text-secondary text-xs">{persona.title}</p>
                      </div>
                    </div>
                    <ChevronRight className="w-5 h-5 text-text-tertiary group-hover:text-oracle-amber-500 transition-colors" />
                  </div>

                  <div className="space-y-3 pt-4 border-t border-oracle-ash">
                    <div className="flex items-center gap-2 text-sm">
                      <MapPin className="w-4 h-4 text-oracle-amber-500" />
                      <span className="text-text-secondary">{persona.location}</span>
                    </div>
                    <div className="text-xs text-text-secondary">
                      <p><span className="text-text-primary font-medium">{persona.languages}</span></p>
                    </div>

                    <div className="flex justify-between pt-3 border-t border-oracle-ash">
                      <div>
                        <p className="text-xs text-text-tertiary">Reviews</p>
                        <p className="text-sm font-mono text-oracle-amber-500">{persona.reviews}</p>
                      </div>
                      <div>
                        <p className="text-xs text-text-tertiary">Avg Rating</p>
                        <p className="text-sm font-mono text-oracle-amber-500">{persona.rating}</p>
                      </div>
                      <div>
                        <p className="text-xs text-text-tertiary">CVI</p>
                        <p className="text-sm font-mono text-oracle-green-500">{persona.cvi}</p>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
