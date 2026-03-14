import React from 'react';
import { useNavigate } from 'react-router-dom';
import LoginForm from '@/components/auth/Login';

export default function Login() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
      <LoginForm
        onSwitchToRegister={() => navigate('/auth/register')}
        onLoginSuccess={() => navigate('/')}
      />
    </div>
  );
}
