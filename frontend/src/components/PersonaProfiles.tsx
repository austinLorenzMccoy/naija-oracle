import React from 'react';
import { PERSONAS } from '@/src/types';
import { MapPin, MessageSquare, ShieldCheck, TrendingUp } from 'lucide-react';
import { cn } from '@/src/lib/utils';

export default function PersonaProfiles() {
  return (
    <div className="p-8 adire-pattern min-h-screen">
      <div className="mb-10">
        <h2 className="font-display text-3xl text-text-primary font-bold">Persona Profiles</h2>
        <p className="text-text-secondary mt-1">Our engine creates hyper-realistic simulated personas that represent Nigerian consumer segments.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {PERSONAS.map((persona) => (
          <div key={persona.id} className="bg-oracle-charcoal border border-oracle-ash rounded-xl overflow-hidden hover:border-amber-500/50 transition-all group flex flex-col">
            <div className="h-24 bg-gradient-to-r from-amber-500/20 to-terra-500/20 group-hover:from-amber-500/30 transition-all"></div>
            <div className="px-6 pb-6 -mt-12 flex-1 flex flex-col">
              <div className="flex flex-col items-center text-center mb-6">
                <div className="w-24 h-24 rounded-full border-4 border-oracle-charcoal p-1 bg-oracle-charcoal">
                  <img 
                    src={persona.avatar} 
                    alt={persona.name} 
                    className="w-full h-full rounded-full object-cover shadow-2xl"
                  />
                </div>
                <h3 className="font-display text-xl text-text-primary mt-4 font-bold">{persona.name}</h3>
                <p className="text-amber-500 font-bold text-[10px] uppercase tracking-widest mt-1">{persona.tagline}</p>
              </div>

              <div className="space-y-4 border-t border-oracle-ash pt-6 flex-1">
                <div className="flex justify-between items-center">
                  <span className="text-[10px] text-text-tertiary uppercase font-bold tracking-widest">Location</span>
                  <span className="text-sm font-medium">{persona.location}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-[10px] text-text-tertiary uppercase font-bold tracking-widest">Role</span>
                  <span className="text-sm font-medium">{persona.role.split(',')[0]}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-[10px] text-text-tertiary uppercase font-bold tracking-widest">Status</span>
                  <span className="px-2 py-0.5 rounded-full bg-green-500/10 text-green-500 font-mono text-[9px] border border-green-500/20">{persona.status}</span>
                </div>
              </div>

              {/* Voice Fingerprint Mini */}
              <div className="mt-8 space-y-3">
                 <div className="flex justify-between text-[10px] font-bold text-text-secondary uppercase">
                    <span>Cultural Density</span>
                    <span className="text-terra-300">{persona.culturalDensity}%</span>
                 </div>
                 <div className="w-full h-1 bg-oracle-ash rounded-full overflow-hidden">
                    <div className="bg-terra-500 h-full" style={{ width: `${persona.culturalDensity}%` }}></div>
                 </div>
              </div>

              <button 
                onClick={() => alert(`Detailed analysis for ${persona.name} coming soon!`)}
                className="w-full mt-8 py-3 border border-oracle-ash text-text-secondary text-xs hover:bg-oracle-smoke hover:text-text-primary transition-all rounded-md font-bold uppercase tracking-widest active:scale-[0.98]"
              >
                View Full Profile
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
