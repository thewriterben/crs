import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import {
  Brain,
  TrendingUp,
  Store,
  Briefcase,
  Layers,
  Users,
  Settings,
  LogOut,
  Menu,
  X,
  Coins,
  ChevronRight,
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', path: '/', icon: Brain },
  { name: 'Trading', path: '/trading', icon: TrendingUp },
  { name: 'Shop', path: '/shop', icon: Store },
  { name: 'Portfolio', path: '/portfolio', icon: Briefcase },
  { name: 'DeFi', path: '/defi', icon: Layers },
  { name: 'Social', path: '/social', icon: Users },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/auth/login');
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/50 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-30 w-64 bg-gray-800 border-r border-gray-700 transform transition-transform duration-200 md:relative md:translate-x-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Logo */}
        <div className="flex items-center justify-between h-16 px-6 border-b border-gray-700">
          <div className="flex items-center gap-2">
            <Coins className="w-6 h-6 text-orange-500" />
            <span className="text-lg font-bold text-white">Cryptons.com</span>
          </div>
          <button
            className="md:hidden text-gray-400 hover:text-white"
            onClick={() => setSidebarOpen(false)}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-4 space-y-1 overflow-y-auto">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === '/'}
                onClick={() => setSidebarOpen(false)}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-orange-600 text-white'
                      : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }`
                }
              >
                <Icon className="w-4 h-4 flex-shrink-0" />
                {item.name}
                <ChevronRight className="w-3 h-3 ml-auto opacity-50" />
              </NavLink>
            );
          })}
        </nav>

        {/* User section */}
        <div className="px-4 py-4 border-t border-gray-700">
          <div className="flex items-center gap-3 px-3 py-2 mb-2">
            <div className="w-8 h-8 rounded-full bg-orange-600 flex items-center justify-center text-sm font-bold">
              {user?.username?.[0]?.toUpperCase() ?? 'U'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-white truncate">{user?.username}</p>
              <p className="text-xs text-gray-400 truncate">{user?.email}</p>
            </div>
          </div>
          <Button
            variant="outline"
            size="sm"
            className="w-full border-gray-600 text-gray-300 hover:bg-gray-700 hover:text-white"
            onClick={handleLogout}
          >
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </Button>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <header className="h-16 bg-gray-800 border-b border-gray-700 flex items-center px-6 gap-4">
          <button
            className="md:hidden text-gray-400 hover:text-white"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="w-5 h-5" />
          </button>
          <div className="flex-1" />
          <span className="text-sm text-gray-400 hidden sm:block">
            Welcome, <span className="text-white font-medium">{user?.username}</span>
          </span>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-auto p-6">{children}</main>
      </div>
    </div>
  );
}
