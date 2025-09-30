import React, { useState, lazy, Suspense } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { 
  Search, 
  ShoppingCart as ShoppingCartIcon, 
  User, 
  Brain, 
  Coins, 
  TrendingUp,
  Menu,
  X,
  Store,
  CreditCard,
  LogOut
} from 'lucide-react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

// App Content Component
function AppContent() {
  const { user, loading, isAuthenticated, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [currentView, setCurrentView] = useState('dashboard');
  const [showAuth, setShowAuth] = useState(false);
  const [authMode, setAuthMode] = useState('login'); // 'login' or 'register'

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  // Show auth screen if not authenticated
  if (!isAuthenticated && !showAuth) {
    return (
      <div className="min-h-screen bg-gray-900 text-white">
        <header className="bg-gray-800 border-b border-gray-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <h1 className="text-xl font-bold text-white">CRS Marketplace</h1>
              <div className="flex gap-2">
                <Button 
                  onClick={() => { setAuthMode('login'); setShowAuth(true); }}
                  variant="outline"
                  className="border-gray-600 text-white hover:bg-gray-700"
                >
                  Login
                </Button>
                <Button 
                  onClick={() => { setAuthMode('register'); setShowAuth(true); }}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  Register
                </Button>
              </div>
            </div>
          </div>
        </header>
        <main className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Welcome to CRS Marketplace</h2>
            <p className="text-xl text-gray-400 mb-8">
              AI-powered cryptocurrency trading platform with advanced portfolio optimization
            </p>
            <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="pt-6">
                  <Brain className="w-12 h-12 text-blue-500 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-white mb-2">AI Trading</h3>
                  <p className="text-gray-400">Advanced AI-powered trading bots and portfolio optimization</p>
                </CardContent>
              </Card>
              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="pt-6">
                  <TrendingUp className="w-12 h-12 text-green-500 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-white mb-2">Real-time Analytics</h3>
                  <p className="text-gray-400">Market sentiment analysis and predictive insights</p>
                </CardContent>
              </Card>
              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="pt-6">
                  <Store className="w-12 h-12 text-purple-500 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-white mb-2">Marketplace</h3>
                  <p className="text-gray-400">Buy and sell AI trading tools and crypto products</p>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    );
  }

  // Show auth form
  if (!isAuthenticated && showAuth) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center p-4">
        {authMode === 'login' ? (
          <Login
            onSwitchToRegister={() => setAuthMode('register')}
            onLoginSuccess={() => setShowAuth(false)}
          />
        ) : (
          <Register
            onSwitchToLogin={() => setAuthMode('login')}
            onRegisterSuccess={() => setShowAuth(false)}
          />
        )}
      </div>
    );
  }

  const navigation = [
    { id: 'dashboard', name: 'AI Dashboard', icon: Brain },
    { id: 'capabilities', name: 'Advanced Features', icon: TrendingUp },
    { id: 'marketplace', name: 'Marketplace', icon: Store },
    { id: 'cart', name: 'Cart', icon: ShoppingCartIcon },
    { id: 'portfolio', name: 'Portfolio', icon: Coins },
    { id: 'profile', name: 'Profile', icon: User },
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
            
            <div className="hidden md:flex items-center space-x-4">
              <div className="flex items-baseline space-x-4">
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
              
              <div className="flex items-center gap-2 ml-4 pl-4 border-l border-gray-700">
                <span className="text-sm text-gray-400">Hi, {user?.username}</span>
                <Button
                  onClick={logout}
                  variant="outline"
                  size="sm"
                  className="border-gray-600 text-white hover:bg-gray-700"
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  Logout
                </Button>
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
            <div className="border-t border-gray-700 pt-2 mt-2">
              <div className="px-3 py-2 text-sm text-gray-400">
                Logged in as {user?.username}
              </div>
              <button
                onClick={logout}
                className="block px-3 py-2 rounded-md text-base font-medium w-full text-left text-gray-300 hover:bg-gray-700 hover:text-white flex items-center gap-2"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      </main>
    </div>
  );
}

// Placeholder components for future development
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