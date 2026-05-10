'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { LayoutDashboard, Zap, MessageCircle, Users, Settings, Plus, HelpCircle, UserPlus } from 'lucide-react'

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/cold-start', label: 'Cold Start Demo', icon: UserPlus },
  { href: '/simulate', label: 'Review Simulator', icon: Zap },
  { href: '/recommend', label: 'Get Recommendations', icon: MessageCircle },
  { href: '/personas', label: 'Personas', icon: Users },
  { href: '/settings', label: 'Settings', icon: Settings },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="fixed left-0 top-0 h-full w-60 bg-oracle-charcoal border-r border-oracle-ash flex flex-col py-6 z-40">
      {/* Logo */}
      <div className="px-6 mb-10">
        <h1 className="font-serif italic text-oracle-amber-500 text-xl">Naija Oracle</h1>
        <p className="text-text-secondary text-xs mt-1">Consumer Insights</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3">
        {navItems.map(({ href, label, icon: Icon }) => {
          const isActive = pathname === href
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                isActive
                  ? 'bg-oracle-smoke text-oracle-amber-500 border-l-3 border-oracle-amber-500'
                  : 'text-text-secondary hover:bg-oracle-smoke hover:text-text-primary'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="text-sm font-medium">{label}</span>
            </Link>
          )
        })}
      </nav>

      {/* Bottom Actions */}
      <div className="px-3 mt-auto">
        <button className="w-full btn-primary flex items-center justify-center gap-2 mb-6">
          <Plus className="w-4 h-4" />
          New Simulation
        </button>
        <div className="border-t border-oracle-ash pt-4">
          <button className="flex items-center gap-3 text-text-tertiary hover:text-oracle-amber-300 transition-colors px-2 py-2 w-full">
            <HelpCircle className="w-5 h-5" />
            <span className="text-xs font-medium">Help Center</span>
          </button>
        </div>
      </div>
    </aside>
  )
}
