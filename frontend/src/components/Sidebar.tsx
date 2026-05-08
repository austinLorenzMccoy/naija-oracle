import React from 'react';
import { 
  LayoutDashboard, 
  BrainCircuit, 
  MessageSquare, 
  Users, 
  Settings, 
  Plus, 
  HelpCircle 
} from 'lucide-react';
import { cn } from '@/src/lib/utils';
import { View } from '@/src/types';

interface SidebarProps {
  currentView: View;
  onViewChange: (view: View) => void;
}

export default function Sidebar({ currentView, onViewChange }: SidebarProps) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'simulator', label: 'Review Simulator', icon: BrainCircuit },
    { id: 'recommendations', label: 'Recommendations', icon: MessageSquare },
    { id: 'personas', label: 'Persona Profiles', icon: Users },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="fixed left-0 top-0 h-full w-60 bg-oracle-charcoal border-r border-oracle-ash flex flex-col py-6 z-50">
      <div className="px-6 mb-10 cursor-pointer" onClick={() => onViewChange('landing')}>
        <h1 className="font-display font-light italic text-xl text-amber-500 leading-none">Naija Oracle</h1>
        <p className="font-sans text-[10px] uppercase tracking-widest text-text-tertiary mt-1">Consumer Insights</p>
      </div>

      <nav className="flex-1 space-y-1">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onViewChange(item.id as View)}
            className={cn(
              "w-full flex items-center gap-3 px-4 py-3 transition-all duration-200 group text-left",
              currentView === item.id 
                ? "bg-oracle-smoke text-amber-500 border-l-4 border-amber-500" 
                : "text-text-secondary hover:bg-oracle-smoke hover:text-text-primary"
            )}
          >
            <item.icon size={20} className={cn(currentView === item.id ? "text-amber-500" : "text-text-tertiary group-hover:text-amber-500")} />
            <span className="font-sans text-sm font-medium">{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="px-4 mt-auto">
        <button 
          onClick={() => onViewChange('simulator')}
          className="w-full py-3 bg-amber-500 text-oracle-void font-bold rounded flex items-center justify-center gap-2 hover:bg-amber-300 transition-all shadow-lg shadow-amber-500/10 active:scale-[0.98]"
        >
          <Plus size={18} />
          <span className="text-sm">New Simulation</span>
        </button>
        
        <div className="mt-6 border-t border-oracle-ash pt-4">
          <button className="w-full flex items-center gap-3 text-text-secondary px-4 py-2 hover:text-text-primary transition-all text-left">
            <HelpCircle size={18} />
            <span className="text-xs">Help Center</span>
          </button>
        </div>
      </div>
    </aside>
  );
}
