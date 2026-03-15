import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Users, Copy, Bell, Share2, TrendingUp, TrendingDown,
  RefreshCw, Loader2, AlertCircle, Star, Award
} from 'lucide-react';
import { api } from '@/lib/api';

function LoadingSkeleton() {
  return (
    <div className="animate-pulse space-y-3">
      <div className="h-4 bg-gray-700 rounded w-3/4" />
      <div className="h-4 bg-gray-700 rounded w-1/2" />
      <div className="h-8 bg-gray-700 rounded" />
    </div>
  );
}

function ErrorMessage({ message }) {
  return (
    <div className="flex items-center gap-2 text-red-400 text-sm p-3 bg-red-500/10 rounded-lg">
      <AlertCircle className="w-4 h-4 flex-shrink-0" />
      <span>{message}</span>
    </div>
  );
}

// Top Traders Leaderboard
function TradersLeaderboard() {
  const [traders, setTraders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [copying, setCopying] = useState(null);
  const [error, setError] = useState(null);

  const fetchTraders = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.phase3.social.getTopTraders(10);
      setTraders(result.traders || []);
    } catch (err) {
      setError(err.message || 'Failed to load traders');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchTraders(); }, [fetchTraders]);

  const handleCopyTrade = async (traderId) => {
    setCopying(traderId);
    try {
      await api.phase3.social.followTrader(traderId, 1000);
    } catch {
      // handled silently
    } finally {
      setCopying(null);
    }
  };

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-yellow-400" />
            Top Traders Leaderboard
          </CardTitle>
          <Button variant="ghost" size="icon" onClick={fetchTraders} disabled={loading}>
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription className="text-gray-400">Community rankings — top performers this month</CardDescription>
      </CardHeader>
      <CardContent>
        {loading && <LoadingSkeleton />}
        {error && <ErrorMessage message={error} />}
        <div className="space-y-3">
          {traders.map((trader, index) => (
            <div key={trader.id} className="flex items-center gap-3 p-3 bg-gray-700/50 rounded-lg">
              <div className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-600 text-sm font-bold text-white flex-shrink-0">
                {index + 1}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-white font-medium text-sm truncate">{trader.username}</span>
                  {trader.verified && (
                    <Badge className="bg-blue-500/20 text-blue-400 text-xs px-1.5 flex-shrink-0">✓</Badge>
                  )}
                  {index < 3 && (
                    <Star className="w-3 h-3 text-yellow-400 flex-shrink-0" />
                  )}
                </div>
                <div className="flex flex-wrap gap-2 text-xs text-gray-400 mt-0.5">
                  <span className="text-green-400">
                    Win: {Math.round((trader.winRate || 0) * 100)}%
                  </span>
                  <span>Avg: +{Math.round((trader.avgReturn || 0) * 100)}%</span>
                  <span>{trader.followers?.toLocaleString()} followers</span>
                </div>
              </div>
              <Button
                size="sm"
                variant="outline"
                className="border-blue-500 text-blue-400 hover:bg-blue-500/20 text-xs flex-shrink-0"
                onClick={() => handleCopyTrade(trader.id)}
                disabled={copying === trader.id}
              >
                {copying === trader.id
                  ? <Loader2 className="w-3 h-3 animate-spin" />
                  : <Copy className="w-3 h-3 mr-1" />
                }
                Copy
              </Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

// Trading Signals Panel
function TradingSignals() {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSignals = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.phase3.social.getSignals();
      setSignals(result.signals || []);
    } catch (err) {
      setError(err.message || 'Failed to load signals');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchSignals(); }, [fetchSignals]);

  const getActionStyle = (action) => {
    if (action === 'BUY') return 'bg-green-500/20 text-green-400 border-green-500/30';
    if (action === 'SELL') return 'bg-red-500/20 text-red-400 border-red-500/30';
    return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
  };

  const ActionIcon = ({ action }) => {
    if (action === 'BUY') return <TrendingUp className="w-4 h-4" />;
    if (action === 'SELL') return <TrendingDown className="w-4 h-4" />;
    return <Bell className="w-4 h-4" />;
  };

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-white flex items-center gap-2">
            <Bell className="w-5 h-5 text-yellow-400" />
            Live Trading Signals
          </CardTitle>
          <Button variant="ghost" size="icon" onClick={fetchSignals} disabled={loading}>
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription className="text-gray-400">AI-generated buy/sell/hold recommendations</CardDescription>
      </CardHeader>
      <CardContent>
        {loading && <LoadingSkeleton />}
        {error && <ErrorMessage message={error} />}
        <div className="space-y-3">
          {signals.map((signal) => (
            <div key={signal.id} className={`flex items-center gap-3 p-3 rounded-lg border ${getActionStyle(signal.action)}`}>
              <div className="flex items-center gap-2 flex-shrink-0">
                <ActionIcon action={signal.action} />
                <span className="font-bold text-sm">{signal.action}</span>
              </div>
              <div className="flex-1">
                <div className="text-white font-medium text-sm">{signal.symbol}</div>
                <div className="text-xs opacity-70 mt-0.5">
                  Strength: {Math.round((signal.strength || 0) * 100)}% •
                  Confidence: {Math.round((signal.confidence || 0) * 100)}%
                </div>
              </div>
              <div className="flex-shrink-0">
                <div className="h-1.5 w-16 bg-gray-700 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full bg-current opacity-70"
                    style={{ width: `${(signal.strength || 0) * 100}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
          {signals.length === 0 && !loading && (
            <p className="text-gray-400 text-sm text-center py-4">No signals available right now</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

// Featured Portfolios
function FeaturedPortfolios() {
  const [portfolios, setPortfolios] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPortfolios = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.phase3.social.getFeaturedPortfolios();
      setPortfolios(result.portfolios || []);
    } catch (err) {
      setError(err.message || 'Failed to load portfolios');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchPortfolios(); }, [fetchPortfolios]);

  const getRiskBadge = (level) => {
    const styles = {
      low: 'bg-green-500/20 text-green-400',
      medium: 'bg-yellow-500/20 text-yellow-400',
      high: 'bg-red-500/20 text-red-400',
    };
    return styles[level] || styles.medium;
  };

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-white flex items-center gap-2">
            <Share2 className="w-5 h-5 text-green-400" />
            Featured Portfolios
          </CardTitle>
          <Button variant="ghost" size="icon" onClick={fetchPortfolios} disabled={loading}>
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription className="text-gray-400">Top community portfolios with verified performance</CardDescription>
      </CardHeader>
      <CardContent>
        {loading && <LoadingSkeleton />}
        {error && <ErrorMessage message={error} />}
        <div className="grid sm:grid-cols-2 gap-3">
          {portfolios.map((portfolio) => (
            <div key={portfolio.id} className="p-4 bg-gray-700/50 rounded-lg space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-white font-medium text-sm">{portfolio.name}</span>
                <Badge className={`text-xs ${getRiskBadge(portfolio.riskLevel)}`}>
                  {portfolio.riskLevel}
                </Badge>
              </div>
              <div className="text-gray-400 text-xs">by {portfolio.owner}</div>
              <div className="flex items-center gap-1 text-green-400 font-bold">
                <TrendingUp className="w-4 h-4" />
                +{Math.round((portfolio.yearlyReturn || 0) * 100)}% this year
              </div>
              <Button
                size="sm"
                variant="outline"
                className="w-full border-gray-600 text-gray-300 hover:bg-gray-600 text-xs mt-1"
              >
                View Portfolio
              </Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

// Copy Trading Widget
function CopyTradingWidget() {
  const [traderId, setTraderId] = useState('');
  const [copyAmount, setCopyAmount] = useState('1000');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const handleCopy = async () => {
    if (!traderId.trim()) return;
    setLoading(true);
    setError(null);
    setSuccess(false);
    try {
      await api.phase3.social.followTrader(traderId.trim(), parseFloat(copyAmount));
      setSuccess(true);
      setTraderId('');
    } catch (err) {
      setError(err.message || 'Failed to set up copy trading');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          <Copy className="w-5 h-5 text-blue-400" />
          Copy Trading Setup
        </CardTitle>
        <CardDescription className="text-gray-400">Automatically mirror a trader's positions</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-1">
          <label className="text-xs text-gray-400">Trader ID or Username</label>
          <input
            type="text"
            value={traderId}
            onChange={(e) => setTraderId(e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white text-sm focus:outline-none focus:border-blue-500"
            placeholder="e.g. trader_001 or CryptoMaster"
          />
        </div>
        <div className="space-y-1">
          <label className="text-xs text-gray-400">Copy Amount (USD)</label>
          <input
            type="number"
            value={copyAmount}
            onChange={(e) => setCopyAmount(e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white text-sm focus:outline-none focus:border-blue-500"
            placeholder="1000"
          />
        </div>
        {error && <ErrorMessage message={error} />}
        {success && (
          <div className="flex items-center gap-2 text-green-400 text-sm p-3 bg-green-500/10 rounded-lg">
            ✓ Copy trading activated successfully
          </div>
        )}
        <Button
          onClick={handleCopy}
          disabled={loading || !traderId.trim()}
          className="w-full bg-blue-600 hover:bg-blue-700"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Copy className="w-4 h-4 mr-2" />}
          Start Copy Trading
        </Button>
      </CardContent>
    </Card>
  );
}

// Main Social page
export default function Social() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Social Trading</h1>
        <p className="text-gray-400 mt-1">Community-driven trading — copy top traders &amp; follow live signals</p>
      </div>

      <Tabs defaultValue="leaderboard">
        <TabsList className="bg-gray-800 border border-gray-700">
          <TabsTrigger value="leaderboard" className="data-[state=active]:bg-gray-700">
            <Award className="w-4 h-4 mr-1" /> Leaderboard
          </TabsTrigger>
          <TabsTrigger value="signals" className="data-[state=active]:bg-gray-700">
            <Bell className="w-4 h-4 mr-1" /> Signals
          </TabsTrigger>
          <TabsTrigger value="portfolios" className="data-[state=active]:bg-gray-700">
            <Share2 className="w-4 h-4 mr-1" /> Portfolios
          </TabsTrigger>
          <TabsTrigger value="copy" className="data-[state=active]:bg-gray-700">
            <Copy className="w-4 h-4 mr-1" /> Copy Trade
          </TabsTrigger>
        </TabsList>

        <TabsContent value="leaderboard" className="mt-4">
          <TradersLeaderboard />
        </TabsContent>

        <TabsContent value="signals" className="mt-4">
          <TradingSignals />
        </TabsContent>

        <TabsContent value="portfolios" className="mt-4">
          <FeaturedPortfolios />
        </TabsContent>

        <TabsContent value="copy" className="mt-4">
          <div className="max-w-md">
            <CopyTradingWidget />
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
