import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, Copy, Bell, Share2 } from 'lucide-react';

export default function Social() {
  const features = [
    {
      icon: Copy,
      title: 'Copy Trading',
      description: 'Automatically copy the trades of top-performing traders.',
      color: 'text-blue-400',
    },
    {
      icon: Bell,
      title: 'Trading Signals',
      description: 'Receive real-time buy/sell signals from expert traders.',
      color: 'text-yellow-400',
    },
    {
      icon: Share2,
      title: 'Portfolio Sharing',
      description: 'Share your portfolio performance and strategies with the community.',
      color: 'text-green-400',
    },
    {
      icon: Users,
      title: 'Trader Leaderboard',
      description: 'Discover and follow the highest-performing traders on the platform.',
      color: 'text-purple-400',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Social Trading</h1>
        <p className="text-gray-400 mt-1">Community-driven trading features — coming in Phase 3</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {features.map((feature) => {
          const Icon = feature.icon;
          return (
            <Card key={feature.title} className="bg-gray-800 border-gray-700">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <Icon className={`w-6 h-6 ${feature.color}`} />
                  <CardTitle className="text-white">{feature.title}</CardTitle>
                </div>
                <CardDescription className="text-gray-400">{feature.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-sm text-gray-500 bg-gray-900/50 rounded-md px-3 py-2">
                  Phase 3 feature — available soon
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
