'use client'

import { useState } from 'react'
import Sidebar from '@/components/sidebar'
import Header from '@/components/header'
import { Bell, Lock, Users, Key } from 'lucide-react'

export default function Settings() {
  const [workspace, setWorkspace] = useState('My Research Pod')
  const [notice, setNotice] = useState<string | null>(null)
  const [apiKey, setApiKey] = useState('sk-oracle-xxxxxxxxxxxxxxxx')
  const [members, setMembers] = useState([
    { name: 'You', email: 'emeka@example.com', role: 'Owner' },
    { name: 'Zainab', email: 'zainab@example.com', role: 'Editor' },
    { name: 'Tunde', email: 'tunde@example.com', role: 'Viewer' },
  ])
  const [notifications, setNotifications] = useState([
    { label: 'Simulation Completed', desc: 'Notify when simulations finish running', enabled: true },
    { label: 'Weekly Digest', desc: 'Summary of experiments and insights', enabled: true },
    { label: 'Error Alerts', desc: 'Get notified of API or system issues', enabled: true },
  ])
  const [deleteArmed, setDeleteArmed] = useState(false)

  const showNotice = (message: string) => {
    setNotice(message)
    window.setTimeout(() => setNotice(null), 2400)
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-60 flex-1 flex flex-col">
        <Header />

        <div className="flex-1 overflow-auto bg-oracle-void p-8">
          <div className="max-w-3xl mx-auto">
            <div className="mb-12">
              <h1 className="text-3xl font-bold mb-2">Settings</h1>
              <p className="text-text-secondary">Manage your Oracle workspace and preferences</p>
            </div>
            {notice && <p className="mb-6 rounded border border-oracle-green-500/40 px-4 py-2 text-sm text-oracle-green-500">{notice}</p>}

            <div className="space-y-8">
              {/* Account Section */}
              <div className="card-accent p-8">
                <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <Lock className="w-5 h-5 text-oracle-amber-500" />
                  Account
                </h2>
                <div className="space-y-6">
                  <div>
                    <label className="block text-text-secondary text-sm mb-2">Email</label>
                    <input
                      type="email"
                      value="emeka@example.com"
                      disabled
                      className="w-full bg-oracle-void border border-oracle-ash text-text-primary px-4 py-2 rounded-lg disabled:opacity-50"
                    />
                  </div>
                  <div>
                    <label className="block text-text-secondary text-sm mb-2">Workspace Name</label>
                    <input
                      type="text"
                      value={workspace}
                      onChange={(event) => setWorkspace(event.target.value)}
                      className="w-full bg-oracle-void border border-oracle-ash text-text-primary px-4 py-2 rounded-lg focus:border-oracle-amber-500 focus:outline-none"
                    />
                  </div>
                  <button onClick={() => showNotice(`Workspace saved as ${workspace}`)} className="btn-primary" type="button">Save Changes</button>
                </div>
              </div>

              {/* Notifications */}
              <div className="card-accent p-8">
                <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <Bell className="w-5 h-5 text-oracle-amber-500" />
                  Notifications
                </h2>
                <div className="space-y-4">
                  {notifications.map((notif, i) => (
                    <div key={i} className="flex items-center justify-between p-4 border border-oracle-ash rounded-lg">
                      <div>
                        <p className="font-medium text-text-primary">{notif.label}</p>
                        <p className="text-text-secondary text-sm">{notif.desc}</p>
                      </div>
                      <input
                        type="checkbox"
                        checked={notif.enabled}
                        onChange={() => setNotifications((current) => current.map((item, index) => index === i ? { ...item, enabled: !item.enabled } : item))}
                        className="w-5 h-5 cursor-pointer"
                      />
                    </div>
                  ))}
                </div>
              </div>

              {/* API Keys */}
              <div id="api-keys" className="card-accent p-8">
                <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <Key className="w-5 h-5 text-oracle-amber-500" />
                  API Keys
                </h2>
                <div className="space-y-4">
                  <div className="p-4 bg-oracle-void border border-oracle-ash rounded-lg">
                    <p className="text-text-secondary text-xs uppercase mb-2">Production Key</p>
                    <div className="flex gap-2">
                      <input
                        type="password"
                        value={apiKey}
                        readOnly
                        className="flex-1 bg-oracle-charcoal border border-oracle-ash text-text-primary px-3 py-2 rounded text-sm font-mono"
                      />
                      <button
                        onClick={async () => {
                          await navigator.clipboard.writeText(apiKey)
                          showNotice('API key copied')
                        }}
                        className="btn-ghost text-sm px-4"
                        type="button"
                      >
                        Copy
                      </button>
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      setApiKey(`sk-oracle-${crypto.randomUUID().replaceAll('-', '').slice(0, 20)}`)
                      showNotice('New API key generated')
                    }}
                    className="btn-primary"
                    type="button"
                  >
                    Generate New Key
                  </button>
                </div>
              </div>

              {/* Team */}
              <div className="card-accent p-8">
                <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <Users className="w-5 h-5 text-oracle-amber-500" />
                  Team Members
                </h2>
                <div className="space-y-4 mb-6">
                  {members.map((member, i) => (
                    <div key={i} className="flex items-center justify-between p-4 border border-oracle-ash rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-oracle-amber-500/20 flex items-center justify-center text-oracle-amber-500 font-bold">
                          {member.name.charAt(0)}
                        </div>
                        <div>
                          <p className="font-medium text-text-primary">{member.name}</p>
                          <p className="text-text-secondary text-sm">{member.email}</p>
                        </div>
                      </div>
                      <select
                        defaultValue={member.role}
                        onChange={(event) => setMembers((current) => current.map((item, index) => index === i ? { ...item, role: event.target.value } : item))}
                        className="bg-oracle-void border border-oracle-ash text-text-primary px-3 py-1.5 rounded text-sm"
                      >
                        <option>Owner</option>
                        <option>Editor</option>
                        <option>Viewer</option>
                      </select>
                    </div>
                  ))}
                </div>
                <button
                  onClick={() => {
                    setMembers((current) => [...current, { name: `Guest ${current.length}`, email: `guest${current.length}@example.com`, role: 'Viewer' }])
                    showNotice('Demo team member invited')
                  }}
                  className="btn-ghost"
                  type="button"
                >
                  Invite Team Member
                </button>
              </div>

              {/* Danger Zone */}
              <div className="card-accent border-l-4 border-l-oracle-terra-500 p-8">
                <h2 className="text-xl font-bold mb-6 text-oracle-terra-500">Danger Zone</h2>
                <button
                  onClick={() => {
                    if (!deleteArmed) {
                      setDeleteArmed(true)
                      showNotice('Click again to confirm delete')
                      return
                    }
                    setDeleteArmed(false)
                    showNotice('Demo workspace delete cancelled')
                  }}
                  className="px-6 py-3 border border-oracle-terra-500 text-oracle-terra-500 rounded-lg hover:bg-oracle-terra-500/10 transition-colors"
                  type="button"
                >
                  {deleteArmed ? 'Confirm Delete' : 'Delete Workspace'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
