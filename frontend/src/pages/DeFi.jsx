import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Layers, Droplets, Percent, Lock } from 'lucide-react';

export default function DeFi() {
  const features = [
    {
      icon: Droplets,
      title: 'Liquidity Pools',
      description: 'Provide liquidity to earn trading fees and yield rewards.',
      color: 'text-blue-400',
    },
    {
      icon: Percent,
      title: 'Yield Farming',
      description: 'Maximize returns by allocating assets to high-yield protocols.',
      color: 'text-green-400',
    },
    {
      icon: Lock,
      title: 'Staking',
      description: 'Stake tokens to secure networks and earn staking rewards.',
      color: 'text-purple-400',
    },
    {
      icon: Layers,
      title: 'DEX Aggregator',
      description: 'Swap tokens at the best rates across decentralized exchanges.',
      color: 'text-orange-400',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">DeFi Features</h1>
        <p className="text-gray-400 mt-1">Decentralized finance integrations — coming in Phase 3</p>
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
