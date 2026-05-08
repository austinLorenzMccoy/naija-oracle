/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import TopNav from './components/TopNav';
import Dashboard from './components/Dashboard';
import ReviewSimulator from './components/ReviewSimulator';
import Recommendations from './components/Recommendations';
import PersonaProfiles from './components/PersonaProfiles';
import LandingPage from './components/LandingPage';
import { View } from './types';
import { motion, AnimatePresence } from 'motion/react';

export default function App() {
  const [currentView, setCurrentView] = useState<View>('landing');
  const [activeTab, setActiveTab] = useState('overview');

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard activeTab={activeTab} />;
      case 'simulator':
        return <ReviewSimulator />;
      case 'recommendations':
        return <Recommendations />;
      case 'personas':
        return <PersonaProfiles />;
      default:
        return <Dashboard />;
    }
  };

  const dashboardTabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'analytics', label: 'Analytics' },
    { id: 'reports', label: 'Reports' },
  ];

  if (currentView === 'landing') {
    return <LandingPage onStart={() => setCurrentView('dashboard')} />;
  }

  return (
    <div className="flex min-h-screen bg-oracle-void overflow-hidden">
      <Sidebar currentView={currentView} onViewChange={(view) => {
        setCurrentView(view);
        setActiveTab('overview');
      }} />
      
      <main className="flex-1 ml-60 flex flex-col h-screen overflow-hidden">
        <TopNav 
          title={
            currentView === 'dashboard' ? 'Dashboard' :
            currentView === 'simulator' ? 'Review Simulator' :
            currentView === 'recommendations' ? 'Recommendations' : 'Persona Profiles'
          }
          tabs={currentView === 'dashboard' ? dashboardTabs : undefined}
          activeTab={activeTab}
          onTabChange={setActiveTab}
        />
        
        <div className="flex-1 overflow-y-auto custom-scrollbar">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentView}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3 }}
              className="h-full"
            >
              {renderView()}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Global Footer */}
        <footer className="px-8 py-4 bg-oracle-void border-t border-oracle-ash flex justify-between items-center text-[10px] text-text-tertiary">
          <div className="flex items-center gap-3 italic">
            <span className="text-amber-500 font-display">Oracle</span>
            <span>© 2024 Naija Oracle. Built for Balogun, Optimized for Global.</span>
          </div>
          <div className="flex gap-6 uppercase tracking-widest font-bold">
            <a href="#" className="hover:text-amber-500 transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-amber-500 transition-colors">Terms of Service</a>
            <a href="#" className="hover:text-amber-500 transition-colors">API Docs</a>
          </div>
        </footer>
      </main>
    </div>
  );
}
