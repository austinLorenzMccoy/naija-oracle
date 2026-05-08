import React, { useState } from 'react';
import { 
  Bolt, 
  Download, 
  RefreshCw, 
  Star, 
  ChevronDown, 
  Send, 
  Mic, 
  TrendingUp,
  History,
  Smartphone,
  UtensilsCrossed,
  Layers,
  MapPin,
  PartyPopper,
  DollarSign
} from 'lucide-react';
import { cn } from '@/src/lib/utils';
import { PERSONAS } from '@/src/types';

export default function Recommendations() {
  const teniola = PERSONAS[1];
  
  return (
    <div className="flex h-[calc(100vh-64px)] overflow-hidden adire-pattern">
      {/* Persona Context Panel */}
      <section className="w-[400px] h-full border-r border-oracle-ash bg-oracle-charcoal/40 p-8 flex flex-col gap-8 overflow-y-auto custom-scrollbar">
        <div>
          <h2 className="font-display text-2xl text-amber-500 font-bold mb-2">Active Persona</h2>
          <p className="text-text-secondary text-sm leading-relaxed">Defining the cultural and economic filter for this recommendation loop.</p>
        </div>

        {/* Persona Card */}
        <div className="bg-oracle-charcoal border-l-4 border-amber-500 p-6 rounded-r-lg shadow-xl shadow-black/20">
          <div className="flex items-center gap-4 mb-8">
            <img 
              alt={teniola.name} 
              className="w-16 h-16 rounded-full border-2 border-oracle-ash object-cover shadow-sm" 
              src={teniola.avatar} 
            />
            <div>
              <h3 className="font-display text-lg text-text-primary font-bold">{teniola.name}, "The Tech-Baddie"</h3>
              <p className="text-[10px] text-amber-500 font-bold uppercase tracking-widest">{teniola.role}</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <PersonaMeta icon={<PartyPopper size={14} />} label="Mood" value="Like Owambe DJ" />
            <PersonaMeta icon={<DollarSign size={14} />} label="Budget" value="Premium Shells" />
            <PersonaMeta icon={<MapPin size={14} />} label="Current Location" value={teniola.location} full />
          </div>
        </div>

        {/* Live Metrics Card */}
        <div className="bg-oracle-charcoal border border-oracle-ash p-6 rounded-lg flex flex-col gap-6">
          <div className="flex justify-between items-center">
            <h3 className="font-display font-bold text-text-primary">Performance Metrics</h3>
            <span className="bg-green-500/10 text-green-500 text-[9px] font-mono font-bold px-2 py-1 rounded border border-green-500/20">LIVE</span>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between items-end">
              <span className="text-text-tertiary text-[10px] uppercase font-bold tracking-widest">NDCG@10 Tracking</span>
              <span className="text-amber-500 font-mono text-2xl font-bold">0.892</span>
            </div>
            <div className="w-full bg-oracle-ash h-1.5 rounded-full overflow-hidden shadow-inner">
              <div className="bg-amber-500 h-full w-[89.2%]" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
             <MetricTile label="BERTScore" value="0.941" />
             <MetricTile label="CVI Rating" value="A+" accent />
          </div>
        </div>

        {/* Constraints */}
        <div className="space-y-4">
          <h3 className="font-display text-sm font-bold text-text-primary">Contextual Constraints</h3>
          <div className="space-y-2">
            <div className="flex items-center gap-3 p-3 bg-oracle-smoke/30 rounded border border-oracle-ash">
              <TrendingUp className="text-amber-500" size={16} />
              <span className="text-[11px] text-text-secondary font-medium">Pidgin Density Filter: 15%</span>
            </div>
            <div className="flex items-center gap-3 p-3 bg-oracle-smoke/30 rounded border border-oracle-ash">
              <History className="text-amber-500" size={16} />
              <span className="text-[11px] text-text-secondary font-medium">Cultural Relevance Weights: Active</span>
            </div>
          </div>
        </div>
      </section>

      {/* Main Chat Interface */}
      <section className="flex-1 h-full flex flex-col bg-oracle-void/90">
        <header className="h-16 px-8 border-b border-oracle-ash flex justify-between items-center bg-oracle-void/40 backdrop-blur-md sticky top-0 z-10">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
            <span className="font-display font-medium text-sm">Recommendation Loop: #4092</span>
          </div>
          <div className="flex gap-4">
            <button className="text-text-tertiary hover:text-amber-500 transition-colors"><Download size={18} /></button>
            <button className="text-text-tertiary hover:text-amber-500 transition-colors"><RefreshCw size={18} /></button>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-8 space-y-8 scroll-smooth custom-scrollbar">
          {/* User Message */}
          <div className="flex justify-end">
            <div className="max-w-[70%] bg-oracle-charcoal border border-oracle-ash p-5 rounded-2xl rounded-tr-none shadow-xl">
              <p className="text-sm leading-relaxed">
                Oracle, I need a spot for dinner tonight. Something high-end but with a <span className="italic text-amber-500 font-medium">proper Lagos groove</span>. No boring fine dining.
              </p>
            </div>
          </div>

          {/* AI Response Block */}
          <div className="flex flex-col gap-4">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-8 h-8 rounded-md bg-amber-500 flex items-center justify-center shadow-lg shadow-amber-500/20">
                <Bolt className="text-oracle-void" size={16} />
              </div>
              <span className="text-[10px] uppercase font-bold tracking-[0.3em] text-amber-500">Oracle Intelligence</span>
            </div>

            <div className="bg-oracle-smoke border border-oracle-ash p-6 rounded-2xl rounded-tl-none shadow-2xl space-y-6 max-w-[90%]">
              <p className="text-sm leading-relaxed">
                I understand, Teniola. You're looking for that "Luxe-Afrobeats" intersection. Based on your current mood and budget, I've curated three spots in VI that hit the mark perfectly.
              </p>

              {/* Recommendation Cards */}
              <div className="space-y-4">
                <RecCard 
                  img="https://lh3.googleusercontent.com/aida-public/AB6AXuALs2yxSTpT-x1tP4DwfNehnSrTom3BNw3shiIWFP4nrsEkXA1TYjd2fY44rZVSjI1Xqeoqj99X-olovS8y7bsogLQeX0vky1hIpi0BohFx-W2muFjvNMnIugC7wQvzqcvzU8OSGQvUtn_GmJc6ZlHGWN_3SXsjJpNYUYIhVTeVQtj3tZ4Xlh8BsqPyHA4Yy34eS2ywGM7CSYqbw0fXoqpLGG9nAQeeUtgJPM_6fK1I0TaDKHskOzSW5x2MGl_rxE3TUV92rA6B8ys"
                  title="The Yellow Chilli"
                  dist="0.8km away"
                  rating="4.2 (1.2k)"
                  reason="Matches your 'Owambe DJ' mood with high-energy evening service and Premium Seafood Okro that hits every cultural note you prefer."
                />
                <RecCard 
                  img="https://lh3.googleusercontent.com/aida-public/AB6AXuAxqGzGVaE4HtUAMsQmtDofA9Xi023ed_UPcC_n8amJrCJ55kp0x6qNV1iILeH0veRkVTwE23PHz2bSv39dbHLr2Ecxj2aUrq6wBZoLnpa8arQsCEggZaq3k8NaObD3vtsbQ0dtJhApWYqFfYGGCJ9_tK7OSA2SlQwW9nsYtQ-Cq8hJXQAmzR2kwrthL-HzgOmjbvSQS-iggKbGKUy2NU6VG2jwYYmwzzQAyRYW0YZRicbY8JG12G62EWr_D8ZsSRFmbWedNfRhWts"
                  title="Nok by Alara"
                  dist="1.4km away"
                  rating="4.9 (800+)"
                  reason="Elite minimalist vibes with highly curated fusion dishes. Perfect for quiet confidence."
                  dimmed
                />
              </div>
            </div>

            {/* Response Polling UI */}
            <div className="flex items-center gap-3 text-text-tertiary">
              <span className="w-1 h-4 bg-amber-500 animate-pulse" />
              <span className="text-[10px] uppercase font-bold tracking-widest italic group-hover:text-text-secondary transition-colors">
                Oracle is refining secondary options...
              </span>
            </div>
          </div>
        </div>

        {/* Chat Input Shell */}
        <footer className="p-8 border-t border-oracle-ash bg-oracle-charcoal/20 backdrop-blur-xl">
          <div className="max-w-4xl mx-auto relative group">
            <input 
              className="w-full bg-oracle-void border border-oracle-ash focus:border-amber-500 rounded-xl px-6 py-5 pr-28 text-text-primary text-sm outline-none transition-all focus:ring-1 focus:ring-amber-500/20"
              placeholder="Ask for specific cultural nuances (e.g., 'no loud music', 'indoor seating')"
            />
            <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1">
              <button className="p-3 text-text-tertiary hover:text-amber-500 transition-colors"><Mic size={18} /></button>
              <button className="p-3 bg-amber-500 rounded-lg text-oracle-void hover:bg-amber-300 transition-all shadow-lg active:scale-95"><Send size={18} /></button>
            </div>
          </div>
          <div className="mt-4 flex justify-center gap-8">
            <button className="flex items-center gap-2 group cursor-pointer">
              <Layers className="text-text-tertiary group-hover:text-amber-500 transition-colors" size={14} />
              <span className="text-[9px] font-bold text-text-tertiary uppercase tracking-widest group-hover:text-text-secondary">Persona Filter: ON</span>
            </button>
            <button className="flex items-center gap-2 group cursor-pointer">
              <History className="text-text-tertiary group-hover:text-amber-500 transition-colors" size={14} />
              <span className="text-[9px] font-bold text-text-tertiary uppercase tracking-widest group-hover:text-text-secondary">Cultural Weights: MAX</span>
            </button>
          </div>
        </footer>
      </section>
    </div>
  );
}

function PersonaMeta({ icon, label, value, full }: any) {
  return (
    <div className={cn("space-y-1", full ? "col-span-2" : "")}>
      <span className="text-[9px] text-text-tertiary uppercase font-bold tracking-widest block">{label}</span>
      <div className="flex items-center gap-2">
         <span className="text-amber-500">{icon}</span>
         <span className="text-text-secondary text-sm font-medium">{value}</span>
      </div>
    </div>
  );
}

function MetricTile({ label, value, accent }: any) {
  return (
    <div className="bg-oracle-smoke/50 p-4 rounded border border-oracle-ash hover:border-amber-500/30 transition-all">
      <span className="text-[9px] text-text-tertiary font-bold uppercase tracking-widest block mb-1">{label}</span>
      <span className={cn("text-lg font-mono font-bold", accent ? "text-terra-500" : "text-amber-500")}>{value}</span>
    </div>
  );
}

function RecCard({ img, title, dist, rating, reason, dimmed }: any) {
  return (
    <div className={cn(
      "bg-oracle-charcoal border border-oracle-ash rounded-xl overflow-hidden group transition-all duration-300 hover:border-amber-500/50",
      dimmed && "opacity-70 grayscale-[0.5]"
    )}>
      <div className="p-4 flex gap-5">
        <div className="w-24 h-24 bg-oracle-ash rounded-lg overflow-hidden flex-shrink-0 border border-oracle-ash shadow-inner">
          <img src={img} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" alt={title} />
        </div>
        <div className="flex-1">
          <div className="flex justify-between items-start">
            <div>
              <h4 className="font-display font-bold text-text-primary group-hover:text-amber-300 transition-colors">{title}</h4>
              <div className="flex items-center gap-1 mt-1 text-amber-500">
                {[1,2,3,4].map(s => <Star key={s} size={10} fill="currentColor" />)}
                <Star size={10} />
                <span className="text-text-tertiary font-mono text-[9px] ml-2 font-bold">{rating}</span>
              </div>
            </div>
            <div className="bg-terra-500/10 text-terra-500 text-[9px] font-bold px-2 py-1 border border-terra-500/20 rounded uppercase">
              {dist}
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-oracle-ash">
             <button className="flex items-center gap-1.5 text-amber-500 text-[10px] font-bold uppercase tracking-tighter hover:text-amber-300 transition-colors">
               WHY THIS RECOMMENDATION? <ChevronDown size={12} />
             </button>
             <p className="mt-2 text-[11px] leading-relaxed text-text-secondary italic">
               {reason}
             </p>
          </div>
        </div>
      </div>
    </div>
  );
}
