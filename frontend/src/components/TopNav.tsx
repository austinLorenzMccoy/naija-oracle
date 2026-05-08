import React from 'react';
import { Search, Bell, Settings } from 'lucide-react';
import { cn } from '@/src/lib/utils';

interface TopNavProps {
  title: string;
  tabs?: { id: string; label: string }[];
  activeTab?: string;
  onTabChange?: (id: string) => void;
}

export default function TopNav({ title, tabs, activeTab, onTabChange }: TopNavProps) {
  return (
    <header className="flex justify-between items-center w-full px-8 h-16 z-40 bg-oracle-void border-b border-oracle-ash sticky top-0 backdrop-blur-md bg-opacity-80">
      <div className="flex items-center gap-4">
        <h2 className="font-display text-lg text-text-primary font-bold">{title}</h2>
        {tabs && (
          <nav className="hidden md:flex items-center gap-6 ml-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => onTabChange?.(tab.id)}
                className={cn(
                  "font-sans text-sm pb-1 transition-all",
                  activeTab === tab.id 
                    ? "text-amber-500 font-bold border-b-2 border-amber-500" 
                    : "text-text-secondary hover:text-amber-300"
                )}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        )}
      </div>

      <div className="flex items-center gap-6">
        <div className="relative hidden lg:block">
          <input 
            className="bg-oracle-charcoal border border-oracle-ash text-text-secondary text-xs px-4 py-2 pl-10 rounded-md focus:ring-1 focus:ring-amber-500 outline-none w-64" 
            placeholder="Search insights..." 
            type="text"
          />
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-text-tertiary" />
        </div>
        
        <button 
          onClick={() => alert('Notifications coming soon!')}
          className="text-text-secondary hover:text-amber-500 transition-colors relative active:scale-90"
        >
          <Bell size={20} />
          <span className="absolute -top-1 -right-1 w-2 h-2 bg-terra-500 rounded-full"></span>
        </button>
        
        <button 
          onClick={() => onTabChange?.('settings')}
          className="text-text-secondary hover:text-amber-500 transition-colors active:scale-90"
        >
          <Settings size={20} />
        </button>
        
        <div className="w-8 h-8 rounded-full bg-amber-500/20 border border-amber-500/40 flex items-center justify-center overflow-hidden cursor-pointer hover:border-amber-500 transition-all active:opacity-80">
          <img 
            alt="User" 
            className="w-full h-full object-cover" 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuCp7tltURWeWO46eS0xZk5v4-8O79dmmQNiMLNkj-AaBZdFKGtbScTogXDRtNT3Zq3s7jEUaMv3GdHKzQgKTXXwl2W5FVl92Y2OLnb4iofKI72Af--Fm5xK7SBpNpp8AQZMrakANj6I2MnsF_p5CdRGG5ZGnHAfcY370ZtIhfTJ-RmTlYfLc_VvjRJx8u9LVy_xkMCJBHO-4oB2Q0KS0_kIfcbY2DFPJcb49g1F5SsqLXLpRbudHg_-2Aj3TxBRW0d8kA-sS3X8g5Y" 
          />
        </div>
      </div>
    </header>
  );
}
