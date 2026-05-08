import React from 'react';
import { cn } from '@/src/lib/utils';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Cell
} from 'recharts';
import { 
  History, 
  TrendingUp, 
  ShieldCheck, 
  Network, 
  Layers, 
  Zap, 
  Lightbulb,
  FileText
} from 'lucide-react';

const data = [
  { name: 'v1.0.2', bert: 0.82 },
  { name: 'v1.0.3', bert: 0.85 },
  { name: 'v1.0.4-beta', bert: 0.91 },
  { name: 'v1.1.0', bert: 0.88 },
  { name: 'v1.1.1-rc', bert: 0.94 },
];

export default function Dashboard({ activeTab = 'overview' }: { activeTab?: string }) {
  if (activeTab === 'analytics') {
    return (
      <div className="p-8 flex flex-col items-center justify-center min-h-[60vh] text-center space-y-4">
        <div className="w-16 h-16 rounded-full bg-amber-500/10 flex items-center justify-center text-amber-500">
          <TrendingUp size={32} />
        </div>
        <h2 className="text-2xl font-display font-bold">In-Depth Analytics</h2>
        <p className="text-text-secondary max-w-md">Detailed sentiment breakdown and demographic penetration metrics are being processed for this period.</p>
      </div>
    );
  }

  if (activeTab === 'reports') {
    return (
      <div className="p-8 flex flex-col items-center justify-center min-h-[60vh] text-center space-y-4">
        <div className="w-16 h-16 rounded-full bg-terra-500/10 flex items-center justify-center text-terra-500">
          <FileText size={32} />
        </div>
        <h2 className="text-2xl font-display font-bold">Monthly Reports</h2>
        <p className="text-text-secondary max-w-md">Your monthly consumer behavior reports will appear here. No reports generated for the current window.</p>
      </div>
    );
  }

  if (activeTab === 'settings') {
    return (
      <div className="p-8 flex flex-col items-center justify-center min-h-[60vh] text-center space-y-4">
        <div className="w-16 h-16 rounded-full bg-oracle-ash flex items-center justify-center text-text-primary">
          <Settings size={32} />
        </div>
        <h2 className="text-2xl font-display font-bold">Account Settings</h2>
        <p className="text-text-secondary max-w-md">Configure your API keys, regional weights, and persona biases here.</p>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8 adire-pattern min-h-screen">
      {/* Metric Grid */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard 
          title="Reviews Generated" 
          value="12,482" 
          change="+14.2% from last week" 
          icon={<History size={18} />} 
          positive 
        />
        <MetricCard 
          title="Avg BERTScore" 
          value="0.892" 
          pill="AMBER PILL" 
          icon={<ShieldCheck size={18} />} 
        />
        <MetricCard 
          title="Avg NDCG@10" 
          value="0.745" 
          pill="GREEN PILL" 
          icon={<Network size={18} />} 
        />
        <MetricCard 
          title="CVI Hit Rate" 
          value="91.4%" 
          pill="TERRACOTTA PILL" 
          icon={<Layers size={18} />} 
        />
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart View */}
        <section className="lg:col-span-2 bg-oracle-charcoal border border-oracle-ash p-6 rounded-lg">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h4 className="font-display text-lg text-text-primary">Experiment Comparison</h4>
              <p className="text-text-tertiary text-xs">BERTScore variance across model iterations</p>
            </div>
            <select className="bg-oracle-void border border-oracle-ash text-text-secondary text-xs rounded px-3 py-1 outline-none">
              <option>Last 5 Versions</option>
              <option>Last 10 Versions</option>
            </select>
          </div>
          
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2A2825" vertical={false} />
                <XAxis 
                  dataKey="name" 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fill: '#5C5955', fontSize: 10 }}
                  dy={10}
                />
                <Tooltip 
                  cursor={{ fill: '#2A2825' }}
                  contentStyle={{ backgroundColor: '#1A1916', border: '1px solid #3D3B37', borderRadius: '4px' }}
                />
                <Bar dataKey="bert" radius={[4, 4, 0, 0]}>
                  {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={index === data.length - 1 ? '#F5831F' : '#3D3B37'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* Live Activity Feed */}
        <section className="bg-oracle-charcoal border border-oracle-ash rounded-lg flex flex-col">
          <div className="p-6 border-b border-oracle-ash flex justify-between items-center">
            <h4 className="font-display text-lg text-text-primary">Live Activity</h4>
            <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
          </div>
          <div className="flex-1 overflow-y-auto max-h-80">
            {[
              { name: 'Ifeanyi from Aba', time: '14:22:05', text: 'The delivery was sharp sharp, no stories at all...' },
              { name: 'Abuja Tech Bro', time: '14:20:12', text: 'Implementation is sleek, but the pricing is bit high o...' },
              { name: 'Mama Nkechi', time: '14:18:45', text: 'God bless you people, my business is moving well...' },
              { name: 'Lagos Island Hustler', time: '14:15:30', text: 'Why is the network behaving like this today?' },
            ].map((item, i) => (
              <div key={i} className="p-4 border-b border-oracle-ash hover:bg-oracle-smoke transition-colors cursor-pointer group">
                <div className="flex justify-between items-start mb-1">
                  <span className="text-xs font-bold text-amber-500">{item.name}</span>
                  <span className="text-[10px] font-mono text-text-tertiary">{item.time}</span>
                </div>
                <p className="text-xs text-text-secondary italic mb-2 line-clamp-1">"{item.text}"</p>
                <div className="flex items-center gap-1">
                   {[1,2,3,4,5].map(s => (
                     <div key={s} className={`w-2 h-2 bg-amber-500 ${s > 4 ? 'opacity-30' : ''}`} />
                   ))}
                </div>
              </div>
            ))}
          </div>
          <button className="p-4 text-xs text-amber-500 font-medium hover:text-amber-300 transition-colors text-center border-t border-oracle-ash uppercase tracking-widest">
            View Full Stream
          </button>
        </section>
      </div>

      {/* Info Tiles */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <InsightCard 
          icon={<Zap className="text-terra-500" size={24} />} 
          title="Optimization Tip" 
          borderClass="border-l-4 border-terra-500"
          description="Your BERTScore has improved by 4% after the latest training set update with more Pidgin dialects." 
        />
        <InsightCard 
          icon={<Lightbulb className="text-amber-500" size={24} />} 
          title="Market Insight" 
          borderClass="border-l-4 border-amber-500"
          description="Sentiment peaks on Friday evenings, matching 'Owambe' patterns across Southwest regions." 
        />
      </section>
    </div>
  );
}

function MetricCard({ title, value, change, pill, icon, positive }: any) {
  return (
    <div className="bg-oracle-charcoal border border-oracle-ash p-6 rounded-lg border-t-4 border-t-amber-500 shadow-sm">
      <div className="flex justify-between items-start mb-4 text-text-tertiary">
        <p className="text-[10px] font-bold uppercase tracking-widest">{title}</p>
        {icon}
      </div>
      <h3 className="font-mono text-3xl text-text-primary tracking-tight">{value}</h3>
      {change && (
        <p className={cn("text-[10px] mt-2 flex items-center gap-1", positive ? "text-green-500" : "text-terra-300")}>
          <TrendingUp size={12} />
          {change}
        </p>
      )}
      {pill && (
        <div className={cn(
          "mt-3 px-2 py-1 inline-block rounded font-mono text-[9px] font-bold tracking-tighter",
          pill.includes('AMBER') ? "bg-amber-500/10 text-amber-500" : 
          pill.includes('GREEN') ? "bg-green-500/10 text-green-500" : "bg-terra-500/10 text-terra-500"
        )}>
          {pill}
        </div>
      )}
    </div>
  );
}

function InsightCard({ icon, title, description, borderClass }: any) {
  return (
    <div className={cn("bg-oracle-charcoal border border-oracle-ash p-6 rounded-lg flex items-center gap-6", borderClass)}>
      <div className="w-16 h-16 shrink-0 bg-oracle-smoke rounded-md flex items-center justify-center border border-oracle-ash shadow-inner">
        {icon}
      </div>
      <div>
        <h5 className="font-display font-bold text-text-primary">{title}</h5>
        <p className="text-xs text-text-secondary leading-relaxed mt-1">{description}</p>
      </div>
    </div>
  );
}
