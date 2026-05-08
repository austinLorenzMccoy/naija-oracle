import React, { useState } from 'react';
import { 
  Zap, 
  ChevronRight, 
  Star, 
  ArrowDownCircle, 
  Sparkles,
  RefreshCw,
  Download,
  CheckCircle2
} from 'lucide-react';
import { cn } from '@/src/lib/utils';

export default function ReviewSimulator() {
  const [pidgin, setPidgin] = useState(75);
  const [isSimulating, setIsSimulating] = useState(false);

  const runSimulation = () => {
    setIsSimulating(true);
    setTimeout(() => setIsSimulating(false), 1500);
  };

  return (
    <div className="flex flex-1 overflow-hidden h-[calc(100vh-64px)]">
      {/* Left Panel: Controls */}
      <section className="w-[420px] bg-oracle-charcoal border-r border-oracle-ash p-8 overflow-y-auto custom-scrollbar">
        <div className="mb-8">
          <h2 className="font-display text-2xl text-text-primary font-bold">Simulator Config</h2>
          <p className="font-sans text-sm text-text-secondary mt-1">Define your target persona and product parameters.</p>
        </div>

        <div className="space-y-6">
          <div className="p-5 border-l-4 border-terra-500 bg-oracle-void/50 rounded-r-lg space-y-4 shadow-inner">
            <p className="text-[10px] text-terra-300 font-bold uppercase tracking-[.25em]">Product Details</p>
            <div>
              <label className="block text-[10px] text-text-secondary font-bold uppercase mb-1">Product Name</label>
              <input 
                className="w-full bg-oracle-void border border-oracle-ash text-text-primary text-sm px-4 py-2.5 focus:border-amber-500 focus:ring-0 outline-none transition-all" 
                defaultValue="Zobo Premium Sparkle"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-[10px] text-text-secondary font-bold uppercase mb-1">Category</label>
                <select className="w-full bg-oracle-void border border-oracle-ash text-text-primary text-sm px-4 py-2 focus:border-amber-500 outline-none">
                  <option>Beverage</option>
                  <option>Tech Gadget</option>
                  <option>Fashion</option>
                </select>
              </div>
              <div>
                <label className="block text-[10px] text-text-secondary font-bold uppercase mb-1">Price Tier</label>
                <select className="w-full bg-oracle-void border border-oracle-ash text-text-primary text-sm px-4 py-2 focus:border-amber-500 outline-none">
                  <option>Masstige</option>
                  <option>Luxury</option>
                  <option>Economy</option>
                </select>
              </div>
            </div>
          </div>

          <div className="space-y-6 pt-4">
            <div>
              <label className="block text-[10px] text-text-secondary font-bold uppercase mb-3">Target Cities</label>
              <div className="flex gap-2 flex-wrap">
                {['Lagos', 'Abuja', 'Port Harcourt', 'Kano'].map((city, i) => (
                  <button 
                    key={city}
                    className={cn(
                      "px-4 py-2 border text-[11px] font-bold transition-all",
                      i === 0 ? "border-amber-500 bg-amber-500/10 text-amber-500" : "border-oracle-ash text-text-tertiary hover:border-text-secondary"
                    )}
                  >
                    {city}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-[10px] text-text-secondary font-bold uppercase mb-1">Primary Language</label>
              <select className="w-full bg-oracle-void border border-oracle-ash text-text-primary text-sm px-4 py-2 focus:border-amber-500 outline-none">
                <option>Nigerian English</option>
                <option>Yoruba-Infused</option>
                <option>Igbo-Infused</option>
                <option>Hausa-Infused</option>
              </select>
            </div>

            <div className="pt-2">
              <label className="block text-[10px] text-text-secondary font-bold uppercase mb-4">Pidgin Intensity</label>
              <input 
                type="range" 
                min="0" 
                max="100" 
                value={pidgin} 
                onChange={(e) => setPidgin(Number(e.target.value))} 
                className="w-full"
              />
              <div className="flex justify-between mt-2 text-[10px] text-text-tertiary font-bold">
                <span>SUNDAY CHURCH</span>
                <span>OWAMBE DJ</span>
              </div>
            </div>

            <div>
              <label className="block text-[10px] text-text-secondary font-bold uppercase mb-1">Review Narrative Style</label>
              <select className="w-full bg-oracle-void border border-oracle-ash text-text-primary text-sm px-4 py-2 focus:border-amber-500 outline-none">
                <option>Street Honest</option>
                <option>Aspirational</option>
                <option>Hyper-Critical</option>
              </select>
            </div>
          </div>

          <button 
            onClick={runSimulation}
            disabled={isSimulating}
            className="w-full bg-amber-500 text-oracle-void py-4 rounded-md font-bold hover:bg-amber-300 transition-all flex items-center justify-center gap-2 group active:scale-[0.98] disabled:opacity-50"
          >
            {isSimulating ? (
              <RefreshCw className="animate-spin" size={18} />
            ) : (
              <>
                RUN SIMULATION
                <Zap className="fill-oracle-void group-hover:translate-x-1 transition-transform" size={18} />
              </>
            )}
          </button>
        </div>
      </section>

      {/* Right Panel: Output */}
      <section className="flex-1 bg-oracle-void p-12 overflow-y-auto relative adire-pattern">
        <div className="relative z-10 max-w-3xl mx-auto space-y-8">
          {/* Main Results Card */}
          <div className="bg-oracle-charcoal border-t-4 border-amber-500 border-x border-b border-oracle-ash p-8 rounded-b-lg shadow-2xl">
            <div className="flex justify-between items-start mb-10">
              <div>
                <h3 className="font-display text-2xl text-text-primary font-bold">Predicted Reception</h3>
                <p className="text-text-secondary text-sm mt-1">Generated for Mainland Persona #420</p>
              </div>
              <div className="flex gap-2">
                <MetricPill label="BERTScore" value="0.92" color="amber" />
                <MetricPill label="CVI Rating" value="0.88" color="terra" />
              </div>
            </div>

            <div className="space-y-8">
              <div className="flex gap-2 items-center">
                {[1,2,3,4].map(s => <Star key={s} className="fill-amber-500 text-amber-500" size={24} />)}
                <Star className="text-oracle-ash" size={24} />
                <span className="ml-4 font-mono text-2xl text-text-primary">4.0 / 5.0</span>
              </div>

              <div className="p-8 bg-oracle-void border border-oracle-ash rounded-lg relative overflow-hidden group">
                <div className="absolute top-0 right-0 w-12 h-12 bg-amber-500/5 rotate-45 translate-x-6 -translate-y-6 border border-amber-500/10"></div>
                <p className="font-display text-xl leading-relaxed text-text-primary italic relative">
                  "Omo, the packaging reach to show off for public, but the sugar for inside na different matter. 
                  <span className="bg-amber-500/20 text-amber-500 px-1 mx-1 rounded not-italic font-bold">No be small tin</span> 
                  I see when I open am. The taste get 
                  <span className="bg-amber-500/20 text-amber-500 px-1 mx-1 rounded not-italic font-bold">shakara</span> 
                  too much for the price. If you want make your guest 
                  <span className="bg-amber-500/20 text-amber-500 px-1 mx-1 rounded not-italic font-bold">feel among</span>, 
                  you fit buy am, but if na enjoyment you dey find, look another side."
                </p>
              </div>
            </div>

            <div className="mt-12 pt-8 border-t border-oracle-ash flex items-center justify-between">
              <div className="flex items-center gap-6">
                <div className="relative w-16 h-16 flex items-center justify-center">
                   <svg className="w-full h-full -rotate-90">
                     <circle cx="32" cy="32" r="28" fill="none" stroke="#2A2825" strokeWidth="4" />
                     <circle 
                      cx="32" cy="32" r="28" fill="none" stroke="#2DB37A" strokeWidth="4" 
                      strokeDasharray="176" strokeDashoffset={176 - (176 * 0.82)} 
                     />
                   </svg>
                   <span className="absolute font-mono text-[10px] text-green-500">82%</span>
                </div>
                <div>
                  <p className="font-display font-bold text-text-primary">Behavioral Fidelity</p>
                  <p className="text-[10px] text-text-secondary uppercase tracking-widest mt-1">High probability of authentic engagement</p>
                </div>
              </div>
              <div className="flex gap-3">
                <button className="flex items-center gap-2 px-5 py-2.5 border border-oracle-ash text-text-secondary text-xs hover:bg-oracle-smoke transition-all">
                  <Download size={14} /> EXPORT JSON
                </button>
                <button className="flex items-center gap-2 px-5 py-2.5 bg-oracle-smoke text-text-primary text-xs border border-oracle-ash hover:border-amber-500 transition-all">
                  SAVE TO LIBRARY
                </button>
              </div>
            </div>
          </div>

          {/* Bento Insights */}
          <div className="grid grid-cols-2 gap-6">
            <BentoItem 
              title="Pain Points" 
              color="terra" 
              icon={<ArrowDownCircle size={18} />}
              items={[
                'Sugar content perceived as "excessive" for luxury tier.',
                'Price-to-value friction in Pidgin context.'
              ]}
            />
            <BentoItem 
              title="Growth Levers" 
              color="green" 
              icon={<Sparkles size={18} />}
              items={[
                'Visual aesthetic (shakara) is a high-performing asset.',
                'Strong gifting potential for festive seasons.'
              ]}
            />
          </div>
        </div>
      </section>
    </div>
  );
}

function MetricPill({ label, value, color }: any) {
  const isAmber = color === 'amber';
  return (
    <div className={cn(
      "px-3 py-1 bg-opacity-10 border rounded-full font-mono text-[9px] font-bold uppercase",
      isAmber ? "bg-amber-500 border-amber-500/40 text-amber-500" : "bg-terra-500 border-terra-500/40 text-terra-500"
    )}>
      {label}: {value}
    </div>
  );
}

function BentoItem({ title, items, color, icon }: any) {
  const isTerra = color === 'terra';
  return (
    <div className="bg-oracle-charcoal border border-oracle-ash p-6 rounded-lg group hover:border-text-secondary transition-all">
      <div className={cn("flex items-center gap-2 mb-4", isTerra ? "text-terra-500" : "text-green-500")}>
        {icon}
        <h4 className="text-[10px] font-bold uppercase tracking-[.25em]">{title}</h4>
      </div>
      <ul className="space-y-3">
        {items.map((item: string, i: number) => (
          <li key={i} className="flex gap-3 items-start">
            <span className={cn("mt-1.5 w-1 h-1 rounded-full shrink-0", isTerra ? "bg-terra-500" : "bg-green-500")} />
            <p className="text-sm text-text-secondary leading-relaxed group-hover:text-text-primary transition-colors">{item}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
