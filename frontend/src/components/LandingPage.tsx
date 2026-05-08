import React from 'react';
import { Bolt, ArrowRight, ShieldCheck, Globe, Zap, CheckCircle2 } from 'lucide-react';
import { PERSONAS } from '@/src/types';
import { cn } from '@/src/lib/utils';

export default function LandingPage({ onStart }: { onStart: () => void }) {
  return (
    <div className="bg-oracle-void text-text-primary overflow-x-hidden min-h-screen relative font-sans">
      <div className="fixed inset-0 adire-pattern opacity-10 pointer-events-none z-0"></div>
      
      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex flex-col justify-center items-center text-center px-8 z-10 overflow-hidden">
        {/* Background Image with Overlay */}
        <div className="absolute inset-0 z-0">
          <img 
            src="https://images.unsplash.com/photo-1618828665011-0abb99c4078a?auto=format&fit=crop&q=80&w=2000" 
            alt="Lagos Skyline"
            className="w-full h-full object-cover grayscale opacity-40 mix-blend-luminosity scale-110 animate-pulse-slow"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-oracle-void/40 via-oracle-void/80 to-oracle-void"></div>
          <div className="absolute inset-0 bg-gradient-to-r from-oracle-void/20 via-transparent to-oracle-void/20"></div>
        </div>

        <div className="relative max-w-4xl mx-auto space-y-12 animate-in fade-in slide-in-from-bottom-8 duration-1000 z-10 pt-16">
          <h1 className="flex flex-col">
            <span className="font-display font-light italic text-[clamp(2rem,6vw,4rem)] text-amber-500/80 leading-tight">The oracle that</span>
            <span className="font-display font-bold text-[clamp(3.5rem,10vw,8rem)] text-text-primary -mt-4 leading-none tracking-tighter">speaks Naija.</span>
          </h1>
          <p className="text-xl md:text-2xl text-text-secondary max-w-2xl mx-auto leading-relaxed font-light">
            Advanced consumer intelligence tuned to the cadence of the Nigerian market. From Balogun market dynamics to Ikoyi luxury trends—we decode the nuance.
          </p>
          <div className="flex flex-wrap justify-center gap-6 pt-6">
            <button 
              onClick={onStart}
              className="bg-amber-500 text-oracle-void font-bold text-lg h-16 px-10 rounded-lg flex items-center gap-3 hover:bg-amber-300 transition-all active:scale-95 shadow-[0_0_40px_rgba(245,131,31,0.2)]"
            >
              Try the Oracle
              <Bolt size={20} className="fill-oracle-void" />
            </button>
            <button className="bg-oracle-charcoal/50 backdrop-blur-md border border-amber-700/50 text-amber-500 font-bold text-lg h-16 px-10 rounded-lg flex items-center gap-3 hover:bg-oracle-smoke transition-all">
              View API Docs
              <ArrowRight size={20} />
            </button>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-oracle-charcoal border-y border-oracle-ash px-8 py-20 z-10 relative">
        <div className="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-12">
          <StatItem label="Active Models" value="2 Agents Built" />
          <StatItem label="Training Data" value="3 Datasets" />
          <StatItem label="Market Reach" value="500+ Personas" />
          <StatItem label="Response Time" value="<200ms Latency" />
        </div>
      </section>

      {/* How it Works */}
      <section className="px-8 py-32 max-w-7xl mx-auto z-10 relative">
        <div className="grid md:grid-cols-2 gap-24 items-center">
          <div className="space-y-12">
            <div className="space-y-4">
              <span className="font-mono text-[10px] text-terra-500 uppercase font-bold tracking-[0.3em]">The Pipeline</span>
              <h2 className="font-display text-5xl text-text-primary font-bold">How It Works</h2>
            </div>
            
            <div className="space-y-10">
              <ProcessStep 
                num="01" 
                title="Cultural Context Injection" 
                desc="We ingest live conversational data from across the 36 states, ensuring regional slang and sentiment are captured in real-time." 
              />
              <ProcessStep 
                num="02" 
                title="Persona Synthesis" 
                desc="Our engine creates hyper-realistic simulated personas that range from 'The Gen-Z Techie' to 'The Market Woman'." 
              />
            </div>
          </div>

          <div className="relative group">
            <div className="absolute -inset-10 bg-gradient-to-tr from-amber-500/10 to-terra-500/5 rounded-full blur-3xl group-hover:blur-[100px] transition-all duration-1000 opacity-50"></div>
            <div className="relative bg-oracle-charcoal border border-oracle-ash p-10 rounded-2xl shadow-2xl overflow-hidden backdrop-blur-sm">
               <div className="flex justify-between items-center mb-10">
                 <div className="flex gap-2">
                   <div className="w-3 h-3 rounded-full bg-terra-500"></div>
                   <div className="w-3 h-3 rounded-full bg-amber-500"></div>
                   <div className="w-3 h-3 rounded-full bg-oracle-smoke"></div>
                 </div>
                 <span className="font-mono text-[10px] text-text-tertiary">simulator_v2.log</span>
               </div>
               <div className="space-y-6 font-mono text-sm leading-relaxed">
                 <div className="text-green-500 flex items-center gap-3">
                   <CheckCircle2 size={16} /> <span>Loading Pidgin Weights...</span>
                 </div>
                 <p className="text-text-secondary">&gt;&gt;&gt; Query: "How dem view dis new data plan?"</p>
                 <p className="text-amber-500">&gt;&gt;&gt; Generating response based on Lagos Mainland persona...</p>
                 <div className="pl-5 border-l-2 border-oracle-ash py-3 ml-2">
                   <p className="text-text-primary italic">"Omo, d price don high small, but d network dey gbege once once."</p>
                 </div>
                 <div className="pt-6 flex gap-3">
                    <span className="bg-amber-500/10 text-amber-500 px-3 py-1 text-[10px] font-bold rounded">BERTSCORE: 0.94</span>
                    <span className="bg-terra-500/10 text-terra-500 px-3 py-1 text-[10px] font-bold rounded">NDCG: 0.88</span>
                 </div>
               </div>
            </div>
          </div>
        </div>
      </section>

      {/* Voice Section */}
      <section className="bg-oracle-charcoal/30 px-8 py-32 z-10 relative">
        <div className="max-w-7xl mx-auto space-y-20">
          <div className="text-center space-y-6">
            <h2 className="font-display text-5xl text-text-primary font-bold">E go sound like them</h2>
            <p className="text-xl text-text-secondary max-w-2xl mx-auto leading-relaxed">
              Different strokes for different folks. Our personas speak with the specific cadence of their tribe and trade.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {PERSONAS.map((p, i) => (
              <div key={p.id} className={cn(
                "bg-oracle-charcoal border-t-4 p-10 space-y-8 hover:-translate-y-2 transition-all duration-500 shadow-xl",
                i % 2 === 0 ? "border-amber-500" : "border-terra-500"
              )}>
                <div className="w-20 h-20 rounded-full overflow-hidden border-2 border-oracle-ash shadow-2xl">
                  <img src={p.avatar} alt={p.name} className="w-full h-full object-cover" />
                </div>
                <div className="space-y-2">
                  <h3 className="font-display text-2xl font-bold">{p.name}</h3>
                  <p className="font-mono text-[10px] text-amber-500 font-bold uppercase tracking-widest">{p.role}</p>
                </div>
                <div className={cn("p-6 rounded-lg italic text-text-secondary text-sm border-l-2", i % 2 === 0 ? "bg-amber-500/5 border-amber-500" : "bg-terra-500/5 border-terra-500")}>
                  "{p.id === 'emeka' ? 'Abeg, if d quality no reach, no bother bring am. Market people no get time for story.' : p.id === 'teniola' ? 'The UI of that app is mid. If the API no fast, we go just port go another one sharp sharp.' : 'The service is okay, but I prefer if I can pay with my local wallet directly. Nagode.'}"
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

function StatItem({ label, value }: any) {
  return (
    <div className="space-y-2">
      <p className="font-mono text-[10px] text-amber-500 uppercase font-bold tracking-[0.25em]">{label}</p>
      <p className="font-display text-3xl text-text-primary font-bold">{value}</p>
    </div>
  );
}

function ProcessStep({ num, title, desc }: any) {
  return (
    <div className="flex gap-8 items-start group">
      <span className="flex-shrink-0 w-14 h-14 rounded-full border border-oracle-ash flex items-center justify-center text-amber-500 font-mono text-lg font-bold group-hover:border-amber-500 group-hover:bg-amber-500/10 transition-all">{num}</span>
      <div className="space-y-3">
        <h3 className="font-display text-2xl text-text-primary font-bold">{title}</h3>
        <p className="text-text-secondary leading-relaxed">{desc}</p>
      </div>
    </div>
  );
}
