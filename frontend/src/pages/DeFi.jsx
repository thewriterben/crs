import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Layers, Droplets, Percent, Lock, ArrowRightLeft, RefreshCw, Loader2, AlertCircle, Plus, Minus } from 'lucide-react';
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

// DEX Aggregator Quote Widget
function DexAggregator() {
  const [tokenIn, setTokenIn] = useState('ETH');
  const [tokenOut, setTokenOut] = useState('USDT');
  const [amount, setAmount] = useState('1.0');
  const [quotes, setQuotes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [swapping, setSwapping] = useState(false);

  const fetchQuote = async () => {
    if (!amount || isNaN(amount)) return;
    setLoading(true);
    setError(null);
    try {
      const result = await api.phase3.defi.getDexQuote(tokenIn, tokenOut, parseFloat(amount));
      setQuotes(result);
    } catch (err) {
      setError(err.message || 'Failed to fetch quotes');
    } finally {
      setLoading(false);
    }
  };

  const handleSwap = async () => {
    if (!quotes?.bestQuote) return;
    setSwapping(true);
    try {
      await api.phase3.defi.executeSwap(tokenIn, tokenOut, parseFloat(amount));
      setQuotes(null);
    } catch {
      // handled silently
    } finally {
      setSwapping(false);
    }
  };

  const tokens = ['ETH', 'BTC', 'USDT', 'USDC', 'BNB', 'SOL'];

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          <ArrowRightLeft className="w-5 h-5 text-orange-400" />
          DEX Aggregator
        </CardTitle>
        <CardDescription className="text-gray-400">Best rates across Uniswap, PancakeSwap, SushiSwap</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-1">
            <label className="text-xs text-gray-400">From</label>
            <Select value={tokenIn} onValueChange={setTokenIn}>
              <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-gray-800 border-gray-700">
                {tokens.map((t) => <SelectItem key={t} value={t} className="text-white">{t}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-1">
            <label className="text-xs text-gray-400">To</label>
            <Select value={tokenOut} onValueChange={setTokenOut}>
              <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-gray-800 border-gray-700">
                {tokens.map((t) => <SelectItem key={t} value={t} className="text-white">{t}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="space-y-1">
          <label className="text-xs text-gray-400">Amount</label>
          <Input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="bg-gray-700 border-gray-600 text-white"
            placeholder="Enter amount"
          />
        </div>

        <Button onClick={fetchQuote} disabled={loading} className="w-full bg-orange-500 hover:bg-orange-600">
          {loading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <RefreshCw className="w-4 h-4 mr-2" />}
          Get Best Quote
        </Button>

        {error && <ErrorMessage message={error} />}

        {quotes && (
          <div className="space-y-2">
            <div className="text-xs text-gray-400 font-medium uppercase tracking-wide">Available Quotes</div>
            {(quotes.quotes || []).map((q, i) => (
              <div key={i} className={`flex items-center justify-between p-2.5 rounded-lg border ${i === 0 ? 'border-orange-500/50 bg-orange-500/5' : 'border-gray-700 bg-gray-700/30'}`}>
                <div>
                  <span className="text-white text-sm font-medium">{q.exchange}</span>
                  {i === 0 && <Badge className="ml-2 bg-orange-500/20 text-orange-400 text-xs">Best</Badge>}
                </div>
                <div className="text-right">
                  <div className="text-white text-sm font-mono">{q.amountOut?.toLocaleString()} {tokenOut}</div>
                  <div className="text-gray-400 text-xs">Fee: {(q.fee * 100).toFixed(2)}%</div>
                </div>
              </div>
            ))}
            <Button
              onClick={handleSwap}
              disabled={swapping}
              variant="outline"
              className="w-full border-orange-500 text-orange-400 hover:bg-orange-500/20"
            >
              {swapping ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
              Execute Swap via {quotes.bestQuote?.exchange}
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// Yield Farming Manager
function YieldFarming() {
  const [pools, setPools] = useState([]);
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [depositing, setDepositing] = useState(null);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [opps, pos] = await Promise.all([
        api.phase3.defi.getFarmingOpportunities(),
        api.phase3.defi.getFarmingPositions(),
      ]);
      setPools(opps.pools || []);
      setPositions(pos.positions || []);
    } catch (err) {
      setError(err.message || 'Failed to load farming data');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleDeposit = async (poolId) => {
    setDepositing(poolId);
    try {
      await api.phase3.defi.depositToFarm(poolId, 100);
      await fetchData();
    } catch {
      // handled silently
    } finally {
      setDepositing(null);
    }
  };

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-white flex items-center gap-2">
            <Percent className="w-5 h-5 text-green-400" />
            Yield Farming
          </CardTitle>
          <Button variant="ghost" size="icon" onClick={fetchData} disabled={loading}>
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription className="text-gray-400">Maximize returns across DeFi protocols</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {loading && <LoadingSkeleton />}
        {error && <ErrorMessage message={error} />}

        {positions.length > 0 && (
          <div className="mb-4">
            <div className="text-xs text-gray-400 uppercase tracking-wide mb-2">Your Positions</div>
            {positions.map((pos, i) => (
              <div key={i} className="p-2.5 bg-green-500/10 border border-green-500/20 rounded-lg text-sm mb-2">
                <div className="flex justify-between">
                  <span className="text-white">{pos.pair}</span>
                  <span className="text-green-400">{pos.apy}% APY</span>
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="text-xs text-gray-400 uppercase tracking-wide mb-2">Available Pools</div>
        {pools.map((pool) => (
          <div key={pool.id} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
            <div>
              <div className="text-white text-sm font-medium">{pool.pair}</div>
              <div className="text-gray-400 text-xs">{pool.protocol} • TVL: ${(pool.tvl / 1e6).toFixed(1)}M</div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-green-400 font-bold text-sm">{pool.apy}% APY</span>
              <Button
                size="sm"
                className="bg-green-600 hover:bg-green-700 text-xs"
                onClick={() => handleDeposit(pool.id)}
                disabled={depositing === pool.id}
              >
                {depositing === pool.id ? <Loader2 className="w-3 h-3 animate-spin" /> : <Plus className="w-3 h-3 mr-1" />}
                Deposit
              </Button>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

// Staking Dashboard
function StakingDashboard() {
  const [options, setOptions] = useState([]);
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [staking, setStaking] = useState(null);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [opts, pos] = await Promise.all([
        api.phase3.defi.getStakingOptions(),
        api.phase3.defi.getStakingPositions(),
      ]);
      setOptions(opts.options || []);
      setPositions(pos.positions || []);
    } catch (err) {
      setError(err.message || 'Failed to load staking data');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleStake = async (token) => {
    setStaking(token);
    try {
      await api.phase3.defi.stakeTokens(token, 1);
      await fetchData();
    } catch {
      // handled silently
    } finally {
      setStaking(null);
    }
  };

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-white flex items-center gap-2">
            <Lock className="w-5 h-5 text-purple-400" />
            Staking
          </CardTitle>
          <Button variant="ghost" size="icon" onClick={fetchData} disabled={loading}>
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription className="text-gray-400">Stake tokens to earn rewards</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {loading && <LoadingSkeleton />}
        {error && <ErrorMessage message={error} />}

        {positions.length > 0 && (
          <div className="mb-4">
            <div className="text-xs text-gray-400 uppercase tracking-wide mb-2">Your Stakes</div>
            {positions.map((pos, i) => (
              <div key={i} className="p-2.5 bg-purple-500/10 border border-purple-500/20 rounded-lg text-sm mb-2">
                <div className="flex justify-between">
                  <span className="text-white">{pos.token}: {pos.amount}</span>
                  <span className="text-purple-400">{pos.apy}% APY</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {options.map((opt) => (
          <div key={opt.token} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
            <div>
              <div className="text-white text-sm font-medium">{opt.token}</div>
              <div className="text-gray-400 text-xs">
                Min: {opt.minAmount} {opt.token} •{' '}
                {opt.lockPeriod > 0 ? `${opt.lockPeriod}d lock` : 'Flexible'}
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-purple-400 font-bold text-sm">{opt.apy}% APY</span>
              <Button
                size="sm"
                className="bg-purple-600 hover:bg-purple-700 text-xs"
                onClick={() => handleStake(opt.token)}
                disabled={staking === opt.token}
              >
                {staking === opt.token ? <Loader2 className="w-3 h-3 animate-spin" /> : null}
                Stake
              </Button>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

// Liquidity Pool Manager
function LiquidityPools() {
  const [pools, setPools] = useState([]);
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [adding, setAdding] = useState(null);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [poolData, posData] = await Promise.all([
        api.phase3.defi.getLiquidityPools(),
        api.phase3.defi.getLiquidityPositions(),
      ]);
      setPools(poolData.pools || []);
      setPositions(posData.positions || []);
    } catch (err) {
      setError(err.message || 'Failed to load liquidity pools');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleAddLiquidity = async (poolId) => {
    setAdding(poolId);
    try {
      await api.phase3.defi.addLiquidity(poolId, { token0: 1, token1: 1 });
      await fetchData();
    } catch {
      // handled silently
    } finally {
      setAdding(null);
    }
  };

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-white flex items-center gap-2">
            <Droplets className="w-5 h-5 text-blue-400" />
            Liquidity Pools
          </CardTitle>
          <Button variant="ghost" size="icon" onClick={fetchData} disabled={loading}>
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription className="text-gray-400">Provide liquidity and earn trading fees</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {loading && <LoadingSkeleton />}
        {error && <ErrorMessage message={error} />}

        {positions.length > 0 && (
          <div className="mb-4">
            <div className="text-xs text-gray-400 uppercase tracking-wide mb-2">Your Positions</div>
            {positions.map((pos, i) => (
              <div key={i} className="flex items-center justify-between p-2.5 bg-blue-500/10 border border-blue-500/20 rounded-lg text-sm mb-2">
                <span className="text-white">{pos.name}</span>
                <Button size="sm" variant="outline" className="border-red-500 text-red-400 hover:bg-red-500/20 text-xs">
                  <Minus className="w-3 h-3 mr-1" /> Remove
                </Button>
              </div>
            ))}
          </div>
        )}

        {pools.map((pool) => (
          <div key={pool.id} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
            <div>
              <div className="text-white text-sm font-medium">{pool.name}</div>
              <div className="text-gray-400 text-xs">{pool.protocol} • TVL: ${(pool.tvl / 1e6).toFixed(0)}M • Fee: {(pool.fee * 100).toFixed(1)}%</div>
            </div>
            <Button
              size="sm"
              className="bg-blue-600 hover:bg-blue-700 text-xs"
              onClick={() => handleAddLiquidity(pool.id)}
              disabled={adding === pool.id}
            >
              {adding === pool.id ? <Loader2 className="w-3 h-3 animate-spin" /> : <Plus className="w-3 h-3 mr-1" />}
              Add
            </Button>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

// Main DeFi page
export default function DeFi() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">DeFi Features</h1>
        <p className="text-gray-400 mt-1">Decentralized finance integrations — DEX, Farming, Staking &amp; Liquidity</p>
      </div>

      <Tabs defaultValue="dex">
        <TabsList className="bg-gray-800 border border-gray-700">
          <TabsTrigger value="dex" className="data-[state=active]:bg-gray-700">
            <ArrowRightLeft className="w-4 h-4 mr-1" /> DEX Swap
          </TabsTrigger>
          <TabsTrigger value="farming" className="data-[state=active]:bg-gray-700">
            <Percent className="w-4 h-4 mr-1" /> Farming
          </TabsTrigger>
          <TabsTrigger value="staking" className="data-[state=active]:bg-gray-700">
            <Lock className="w-4 h-4 mr-1" /> Staking
          </TabsTrigger>
          <TabsTrigger value="liquidity" className="data-[state=active]:bg-gray-700">
            <Droplets className="w-4 h-4 mr-1" /> Liquidity
          </TabsTrigger>
        </TabsList>

        <TabsContent value="dex" className="mt-4">
          <div className="max-w-md">
            <DexAggregator />
          </div>
        </TabsContent>

        <TabsContent value="farming" className="mt-4">
          <YieldFarming />
        </TabsContent>

        <TabsContent value="staking" className="mt-4">
          <StakingDashboard />
        </TabsContent>

        <TabsContent value="liquidity" className="mt-4">
          <LiquidityPools />
        </TabsContent>
      </Tabs>
    </div>
  );
}
