import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Settings as SettingsIcon, User, Shield, Bell, Palette } from 'lucide-react';

const sections = [
  {
    icon: User,
    title: 'Account',
    description: 'Manage your profile, username, and email address.',
    color: 'text-blue-400',
  },
  {
    icon: Shield,
    title: 'Security',
    description: 'Password, two-factor authentication, and active sessions.',
    color: 'text-green-400',
  },
  {
    icon: Bell,
    title: 'Notifications',
    description: 'Configure alerts for price movements, trades, and system events.',
    color: 'text-yellow-400',
  },
  {
    icon: Palette,
    title: 'Appearance',
    description: 'Theme, language, and display preferences.',
    color: 'text-purple-400',
  },
];

export default function Settings() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Settings</h1>
        <p className="text-gray-400 mt-1">Manage your account and platform preferences</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {sections.map((section) => {
          const Icon = section.icon;
          return (
            <Card
              key={section.title}
              className="bg-gray-800 border-gray-700 hover:border-gray-600 cursor-pointer transition-colors"
            >
              <CardHeader>
                <div className="flex items-center gap-3">
                  <Icon className={`w-6 h-6 ${section.color}`} />
                  <CardTitle className="text-white">{section.title}</CardTitle>
                </div>
                <CardDescription className="text-gray-400">{section.description}</CardDescription>
              </CardHeader>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
