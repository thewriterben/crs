import React from 'react';
import { useNavigate } from 'react-router-dom';
import RegisterForm from '@/components/auth/Register';

export default function Register() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
      <RegisterForm
        onSwitchToLogin={() => navigate('/auth/login')}
        onRegisterSuccess={() => navigate('/')}
      />
    </div>
  );
}
