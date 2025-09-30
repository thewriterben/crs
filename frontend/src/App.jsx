import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { 
  Search, 
  ShoppingCart, 
  User, 
  Brain, 
  Coins, 
  TrendingUp,
  Menu,
  X
} from 'lucide-react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import AIDashboard from './components/ai/AIDashboard.jsx';
import NewCapabilitiesDashboard from './components/ai/NewCapabilitiesDashboard.jsx';
import './App.css';

// Main App Component
function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

// App Content Component
function AppContent() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [currentView, setCurrentView] = useState('dashboard');

  const navigation = [
    { id: 'dashboard', name: 'AI Dashboard', icon: Brain },
    { id: 'capabilities', name: 'Advanced Features', icon: TrendingUp },
    { id: 'marketplace', name: 'Marketplace', icon: ShoppingCart },
    { id: 'portfolio', name: 'Portfolio', icon: Coins },
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-xl font-bold text-white">CRS Marketplace</h1>
              </div>
            </div>
            
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                {navigation.map((item) => {
                  const Icon = item.icon;
                  return (
                    <button
                      key={item.id}
                      onClick={() => setCurrentView(item.id)}
                      className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2 ${
                        currentView === item.id
                          ? 'bg-gray-700 text-white'
                          : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                      {item.name}
                    </button>
                  );
                })}
              </div>
            </div>
            
            <div className="md:hidden">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700"
              >
                {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile menu */}
      {isMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-gray-800">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setCurrentView(item.id);
                    setIsMenuOpen(false);
                  }}
                  className={`block px-3 py-2 rounded-md text-base font-medium w-full text-left flex items-center gap-2 ${
                    currentView === item.id
                      ? 'bg-gray-700 text-white'
                      : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {item.name}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {currentView === 'dashboard' && <AIDashboard />}
        {currentView === 'capabilities' && <NewCapabilitiesDashboard />}
        {currentView === 'marketplace' && <MarketplacePlaceholder />}
        {currentView === 'portfolio' && <PortfolioPlaceholder />}
      </main>
    </div>
  );
}

// Placeholder components for future development
function MarketplacePlaceholder() {
  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <CardTitle className="text-white">Cryptocurrency Marketplace</CardTitle>
        <CardDescription className="text-gray-400">
          E-commerce functionality coming soon
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="text-center py-12">
          <ShoppingCart className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400 mb-4">
            The cryptocurrency marketplace is under development. It will feature:
          </p>
          <ul className="text-left text-gray-400 space-y-2 max-w-md mx-auto">
            <li>• Cryptocurrency products and services</li>
            <li>• Secure payment processing</li>
            <li>• User account management</li>
            <li>• Order tracking and history</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}

function PortfolioPlaceholder() {
  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <CardTitle className="text-white">Portfolio Management</CardTitle>
        <CardDescription className="text-gray-400">
          Advanced portfolio features coming soon
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="text-center py-12">
          <Coins className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400 mb-4">
            Portfolio management features are being integrated. They will include:
          </p>
          <ul className="text-left text-gray-400 space-y-2 max-w-md mx-auto">
            <li>• Real-time portfolio tracking</li>
            <li>• Performance analytics</li>
            <li>• Risk assessment tools</li>
            <li>• Automated rebalancing</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}

export default App;