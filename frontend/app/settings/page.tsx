'use client'

import Sidebar from '@/components/sidebar'
import Header from '@/components/header'
import { Bell, Lock, Users, Key } from 'lucide-react'

export default function Settings() {
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
                      defaultValue="My Research Pod"
                      className="w-full bg-oracle-void border border-oracle-ash text-text-primary px-4 py-2 rounded-lg focus:border-oracle-amber-500 focus:outline-none"
                    />
                  </div>
                  <button className="btn-primary">Save Changes</button>
                </div>
              </div>

              {/* Notifications */}
              <div className="card-accent p-8">
                <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <Bell className="w-5 h-5 text-oracle-amber-500" />
                  Notifications
                </h2>
                <div className="space-y-4">
                  {[
                    { label: 'Simulation Completed', desc: 'Notify when simulations finish running' },
                    { label: 'Weekly Digest', desc: 'Summary of experiments and insights' },
                    { label: 'Error Alerts', desc: 'Get notified of API or system issues' },
                  ].map((notif, i) => (
                    <div key={i} className="flex items-center justify-between p-4 border border-oracle-ash rounded-lg">
                      <div>
                        <p className="font-medium text-text-primary">{notif.label}</p>
                        <p className="text-text-secondary text-sm">{notif.desc}</p>
                      </div>
                      <input type="checkbox" defaultChecked className="w-5 h-5 cursor-pointer" />
                    </div>
                  ))}
                </div>
              </div>

              {/* API Keys */}
              <div className="card-accent p-8">
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
                        value="sk-oracle-xxxxxxxxxxxxxxxx"
                        readOnly
                        className="flex-1 bg-oracle-charcoal border border-oracle-ash text-text-primary px-3 py-2 rounded text-sm font-mono"
                      />
                      <button className="btn-ghost text-sm px-4">Copy</button>
                    </div>
                  </div>
                  <button className="btn-primary">Generate New Key</button>
                </div>
              </div>

              {/* Team */}
              <div className="card-accent p-8">
                <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <Users className="w-5 h-5 text-oracle-amber-500" />
                  Team Members
                </h2>
                <div className="space-y-4 mb-6">
                  {[
                    { name: 'You', email: 'emeka@example.com', role: 'Owner' },
                    { name: 'Zainab', email: 'zainab@example.com', role: 'Editor' },
                    { name: 'Tunde', email: 'tunde@example.com', role: 'Viewer' },
                  ].map((member, i) => (
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
                        className="bg-oracle-void border border-oracle-ash text-text-primary px-3 py-1.5 rounded text-sm"
                      >
                        <option>Owner</option>
                        <option>Editor</option>
                        <option>Viewer</option>
                      </select>
                    </div>
                  ))}
                </div>
                <button className="btn-ghost">Invite Team Member</button>
              </div>

              {/* Danger Zone */}
              <div className="card-accent border-l-4 border-l-oracle-terra-500 p-8">
                <h2 className="text-xl font-bold mb-6 text-oracle-terra-500">Danger Zone</h2>
                <button className="px-6 py-3 border border-oracle-terra-500 text-oracle-terra-500 rounded-lg hover:bg-oracle-terra-500/10 transition-colors">
                  Delete Workspace
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
