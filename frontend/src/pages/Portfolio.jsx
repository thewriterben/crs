import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Briefcase, TrendingUp, BarChart2, RefreshCw } from 'lucide-react';

export default function Portfolio() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Portfolio Management</h1>
        <p className="text-gray-400 mt-1">Track, analyze, and automate your crypto portfolio</p>
      </div>

      <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-4">
        {[
          { title: 'Total Value', value: '$0.00', icon: Briefcase, color: 'text-blue-400' },
          { title: '24h Change', value: '+0.00%', icon: TrendingUp, color: 'text-green-400' },
          { title: 'Assets', value: '0', icon: BarChart2, color: 'text-purple-400' },
          { title: 'Auto-Rebalance', value: 'Off', icon: RefreshCw, color: 'text-orange-400' },
        ].map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.title} className="bg-gray-800 border-gray-700">
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-400">{stat.title}</p>
                    <p className={`text-2xl font-bold mt-1 ${stat.color}`}>{stat.value}</p>
                  </div>
                  <Icon className={`w-8 h-8 ${stat.color} opacity-80`} />
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle className="text-white">Portfolio Overview</CardTitle>
          <CardDescription className="text-gray-400">
            Connect your exchange accounts to see live portfolio data
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <Briefcase className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400 mb-2">No portfolio data yet</p>
            <p className="text-sm text-gray-500">
              Portfolio automation, risk management, DCA, and stop-loss features are available once
              you connect an exchange.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
