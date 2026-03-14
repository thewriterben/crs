import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from '@/contexts/AuthContext';
import Layout from '@/components/Layout';
import Dashboard from '@/pages/Dashboard';
import Trading from '@/pages/Trading';
import Shop from '@/pages/Shop';
import Portfolio from '@/pages/Portfolio';
import DeFi from '@/pages/DeFi';
import Social from '@/pages/Social';
import Settings from '@/pages/Settings';
import Login from '@/pages/auth/Login';
import Register from '@/pages/auth/Register';

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4" />
          <p className="text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/auth/login" replace />;
}

function AppRoutes() {
  return (
    <Routes>
      {/* Auth routes — no layout */}
      <Route path="/auth/login" element={<Login />} />
      <Route path="/auth/register" element={<Register />} />

      {/* Protected routes — wrapped in Layout */}
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/trading" element={<Trading />} />
                <Route path="/shop" element={<Shop />} />
                <Route path="/portfolio" element={<Portfolio />} />
                <Route path="/defi" element={<DeFi />} />
                <Route path="/social" element={<Social />} />
                <Route path="/settings" element={<Settings />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </Layout>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;