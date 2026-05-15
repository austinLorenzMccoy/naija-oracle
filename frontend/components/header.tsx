'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Bell, Settings, Search } from 'lucide-react'
import { useState, useRef, useEffect } from 'react'

interface HeaderProps {
  title?: string
  tabs?: Array<{ label: string; href: string; active: boolean }>
}

export default function Header({ title, tabs }: HeaderProps) {
  const router = useRouter()
  const [notificationOpen, setNotificationOpen] = useState(false)
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [profileOpen, setProfileOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [notice, setNotice] = useState<string | null>(null)
  const notificationRef = useRef<HTMLDivElement>(null)
  const settingsRef = useRef<HTMLDivElement>(null)
  const profileRef = useRef<HTMLDivElement>(null)

  const handleNotificationClick = () => {
    setNotificationOpen(!notificationOpen)
    setSettingsOpen(false)
    setProfileOpen(false)
  }

  const handleSettingsClick = () => {
    setSettingsOpen(!settingsOpen)
    setNotificationOpen(false)
    setProfileOpen(false)
  }

  const handleProfileClick = () => {
    setProfileOpen(!profileOpen)
    setNotificationOpen(false)
    setSettingsOpen(false)
  }

  const showNotice = (message: string) => {
    setNotice(message)
    window.setTimeout(() => setNotice(null), 2400)
  }

  const exportWorkspaceData = () => {
    const data = {
      exported_at: new Date().toISOString(),
      workspace: 'Naija Oracle',
      pages: ['dashboard', 'simulate', 'recommend', 'personas', 'reports', 'settings']
    }
    const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }))
    const link = document.createElement('a')
    link.href = url
    link.download = 'naija-oracle-workspace.json'
    link.click()
    URL.revokeObjectURL(url)
    showNotice('Workspace export downloaded')
  }

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (notificationRef.current && !notificationRef.current.contains(event.target as Node)) {
        setNotificationOpen(false)
      }
      if (settingsRef.current && !settingsRef.current.contains(event.target as Node)) {
        setSettingsOpen(false)
      }
      if (profileRef.current && !profileRef.current.contains(event.target as Node)) {
        setProfileOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <header className="sticky top-0 z-50 bg-oracle-void border-b border-oracle-ash">
      <div className="flex justify-between items-center px-8 h-16">
        <div className="flex items-center gap-8">
          <span className="font-serif italic text-oracle-amber-500 text-lg">Oracle</span>
          {tabs && (
            <nav className="hidden md:flex gap-6">
              {tabs.map((tab) => (
                <Link
                  key={tab.label}
                  href={tab.href}
                  className={`text-sm font-medium pb-1 border-b-2 transition-colors ${
                    tab.active
                      ? 'text-oracle-amber-500 border-oracle-amber-500'
                      : 'text-text-secondary border-transparent hover:text-oracle-amber-300'
                  }`}
                >
                  {tab.label}
                </Link>
              ))}
            </nav>
          )}
        </div>

        {/* Right side actions */}
        <div className="flex items-center gap-4">
          {notice && (
            <div className="hidden lg:block text-xs text-oracle-green-500 border border-oracle-green-500/40 rounded px-3 py-1">
              {notice}
            </div>
          )}

          <form
            onSubmit={(event) => {
              event.preventDefault()
              if (!searchQuery.trim()) {
                showNotice('Type something to search')
                return
              }
              router.push(`/personas?search=${encodeURIComponent(searchQuery.trim())}`)
            }}
            className="hidden md:flex items-center bg-oracle-charcoal border border-oracle-ash px-3 py-1.5 rounded-lg"
          >
            <Search className="w-4 h-4 text-text-tertiary" />
            <input
              type="text"
              placeholder="Search insights..."
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
              className="bg-transparent border-none outline-none ml-2 text-text-primary placeholder-text-tertiary text-sm w-48"
            />
          </form>
          
          {/* Notifications Button */}
          <div className="relative" ref={notificationRef}>
            <button 
              onClick={handleNotificationClick}
              className="p-2 text-oracle-amber-500 hover:bg-oracle-charcoal rounded-lg transition-all relative cursor-pointer active:opacity-70"
              title="Notifications"
              type="button"
            >
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-oracle-terra-500 rounded-full"></span>
            </button>
            {notificationOpen && (
              <div className="absolute right-0 mt-2 w-64 bg-oracle-charcoal border border-oracle-ash rounded-lg shadow-2xl p-4 z-[60]">
                <h3 className="text-sm font-bold text-text-primary mb-3">Notifications</h3>
                <div className="space-y-3">
                  <div className="p-2 bg-oracle-smoke rounded border border-oracle-ash">
                    <p className="text-xs font-medium text-oracle-amber-500">Model Training Complete</p>
                    <p className="text-xs text-text-secondary mt-1">v1.2.0 BERTScore improved to 0.915</p>
                  </div>
                  <div className="p-2 bg-oracle-smoke rounded border border-oracle-ash">
                    <p className="text-xs font-medium text-oracle-amber-500">New Review Generated</p>
                    <p className="text-xs text-text-secondary mt-1">Ifeanyi added 5-star review from Lagos</p>
                  </div>
                </div>
                <button
                  onClick={() => {
                    setNotificationOpen(false)
                    router.push('/reports')
                  }}
                  className="w-full mt-3 text-xs text-oracle-amber-500 hover:text-oracle-amber-300"
                  type="button"
                >
                  View all notifications
                </button>
              </div>
            )}
          </div>

          {/* Settings Button */}
          <div className="relative" ref={settingsRef}>
            <button 
              onClick={handleSettingsClick}
              className="p-2 text-oracle-amber-500 hover:bg-oracle-charcoal rounded-lg transition-all cursor-pointer active:opacity-70"
              title="Settings"
              type="button"
            >
              <Settings className="w-5 h-5" />
            </button>
            {settingsOpen && (
              <div className="absolute right-0 mt-2 w-56 bg-oracle-charcoal border border-oracle-ash rounded-lg shadow-2xl p-4 z-[60]">
                <h3 className="text-sm font-bold text-text-primary mb-3">Quick Settings</h3>
                <div className="space-y-2">
                  <Link 
                    href="/settings"
                    className="block w-full text-left px-3 py-2 text-xs text-text-secondary hover:bg-oracle-smoke rounded transition-colors"
                  >
                    Account Settings
                  </Link>
                  <button
                    onClick={() => showNotice('Notification preferences opened in Settings')}
                    className="w-full text-left px-3 py-2 text-xs text-text-secondary hover:bg-oracle-smoke rounded transition-colors"
                    type="button"
                  >
                    Notifications Preferences
                  </button>
                  <button
                    onClick={() => {
                      setSettingsOpen(false)
                      router.push('/settings#api-keys')
                    }}
                    className="w-full text-left px-3 py-2 text-xs text-text-secondary hover:bg-oracle-smoke rounded transition-colors"
                    type="button"
                  >
                    API Keys
                  </button>
                  <button
                    onClick={exportWorkspaceData}
                    className="w-full text-left px-3 py-2 text-xs text-text-secondary hover:bg-oracle-smoke rounded transition-colors"
                    type="button"
                  >
                    Export Data
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Profile Menu */}
          <div className="relative" ref={profileRef}>
            <button
              onClick={handleProfileClick}
              className="w-8 h-8 rounded-full bg-oracle-ash overflow-hidden cursor-pointer hover:ring-2 hover:ring-oracle-amber-500 transition-all active:opacity-70"
              title="Profile menu"
              type="button"
            >
              <img
                src="https://api.dicebear.com/7.x/avataaars/svg?seed=Oracle"
                alt="User profile"
                className="w-full h-full object-cover"
              />
            </button>
            {profileOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-oracle-charcoal border border-oracle-ash rounded-lg shadow-2xl p-4 z-[60]">
                <h3 className="text-sm font-bold text-text-primary mb-3">Oracle Admin</h3>
                <p className="text-xs text-text-secondary mb-4">admin@oracle.naija</p>
                <div className="space-y-2 border-t border-oracle-ash pt-3">
                  <button
                    onClick={() => showNotice('Profile view opened')}
                    className="w-full text-left px-3 py-2 text-xs text-text-secondary hover:bg-oracle-smoke rounded transition-colors"
                    type="button"
                  >
                    My Profile
                  </button>
                  <button
                    onClick={() => router.push('/settings')}
                    className="w-full text-left px-3 py-2 text-xs text-text-secondary hover:bg-oracle-smoke rounded transition-colors"
                    type="button"
                  >
                    Team Settings
                  </button>
                  <button
                    onClick={() => showNotice('Billing is current')}
                    className="w-full text-left px-3 py-2 text-xs text-text-secondary hover:bg-oracle-smoke rounded transition-colors"
                    type="button"
                  >
                    Billing
                  </button>
                  <button
                    onClick={() => showNotice('Signed out of demo session')}
                    className="w-full text-left px-3 py-2 text-xs text-oracle-terra-500 hover:bg-oracle-smoke rounded transition-colors"
                    type="button"
                  >
                    Sign Out
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
