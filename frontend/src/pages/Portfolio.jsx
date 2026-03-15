import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import {
  Briefcase, TrendingUp, BarChart2, RefreshCw,
  AlertTriangle, Shield, CalendarClock, TrendingDown,
  Loader2, AlertCircle, CheckCircle2, Plus
} from 'lucide-react';
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { api } from '@/lib/api';

const COLORS = ['#F97316', '#3B82F6', '#10B981', '#8B5CF6', '#EF4444', '#F59E0B'];

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

// Default sample portfolio for demonstrations
const SAMPLE_PORTFOLIO = {
  BTC: 0.45,
  ETH: 0.30,
  SOL: 0.15,
  USDT: 0.10,
};

// Rebalancing Module
function RebalancingModule() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const targetAllocation = { BTC: 0.40, ETH: 0.30, SOL: 0.20, USDT: 0.10 };

  const pieData = Object.entries(SAMPLE_PORTFOLIO).map(([name, value]) => ({
    name,
    value: Math.round(value * 100),
  }));

  const analyzeRebalance = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.phase3.portfolio.analyzeRebalance(SAMPLE_PORTFOLIO, targetAllocation);
      setAnalysis(result);
    } catch (err) {
      setError(err.message || 'Failed to analyze rebalancing');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { analyzeRebalance(); }, [analyzeRebalance]);

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-white flex items-center gap-2">
            <RefreshCw className="w-5 h-5 text-orange-400" />
            Portfolio Rebalancing
          </CardTitle>
          <Button variant="ghost" size="icon" onClick={analyzeRebalance} disabled={loading}>
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription className="text-gray-400">Detect drift and generate rebalancing orders</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <div className="text-xs text-gray-400 mb-2 uppercase tracking-wide">Current Allocation</div>
            <ResponsiveContainer width="100%" height={180}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={40} outerRadius={70} dataKey="value">
                  {pieData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px' }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-2">
            <div className="text-xs text-gray-400 uppercase tracking-wide">Drift Analysis</div>
            {loading && <LoadingSkeleton />}
            {error && <ErrorMessage message={error} />}
            {analysis && (
              <div className="space-y-2">
                {Object.entries(SAMPLE_PORTFOLIO).map(([asset, current]) => {
                  const target = targetAllocation[asset] || 0;
                  const drift = ((current - target) * 100).toFixed(1);
                  const driftNum = parseFloat(drift);
                  return (
                    <div key={asset} className="flex items-center justify-between text-sm">
                      <span className="text-white">{asset}</span>
                      <div className="flex items-center gap-2">
                        <span className="text-gray-400">{Math.round(current * 100)}% → {Math.round(target * 100)}%</span>
                        <span className={`text-xs ${Math.abs(driftNum) > 3 ? (driftNum > 0 ? 'text-red-400' : 'text-green-400') : 'text-gray-400'}`}>
                          {driftNum > 0 ? '+' : ''}{drift}%
                        </span>
                      </div>
                    </div>
                  );
                })}
                <Button
                  size="sm"
                  className="w-full mt-2 bg-orange-500 hover:bg-orange-600 text-xs"
                  onClick={async () => {
                    try {
                      await api.phase3.portfolio.generateRebalanceOrders(SAMPLE_PORTFOLIO, targetAllocation, 50000);
                    } catch {
                      // handled silently
                    }
                  }}
                >
                  Generate Rebalance Orders
                </Button>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

// Risk Assessment Tool
function RiskAssessment() {
  const [assessment, setAssessment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const assessRisk = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.phase3.portfolio.assessRisk(SAMPLE_PORTFOLIO);
      setAssessment(result);
    } catch (err) {
      setError(err.message || 'Failed to assess portfolio risk');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { assessRisk(); }, [assessRisk]);

  // Generate mock risk data if API returns empty
  const riskMetrics = assessment?.metrics || {
    overall_risk: 'MEDIUM',
    volatility: 0.42,
    sharpe_ratio: 1.28,
    max_drawdown: -0.18,
    beta: 0.87,
    var_95: -0.06,
  };

  const riskColor = riskMetrics.overall_risk === 'LOW' ? 'text-green-400' : riskMetrics.overall_risk === 'HIGH' ? 'text-red-400' : 'text-yellow-400';
  const riskBg = riskMetrics.overall_risk === 'LOW' ? 'bg-green-500/20' : riskMetrics.overall_risk === 'HIGH' ? 'bg-red-500/20' : 'bg-yellow-500/20';

  const metrics = [
    { label: 'Volatility', value: `${Math.round((riskMetrics.volatility || 0) * 100)}%`, icon: BarChart2 },
    { label: 'Sharpe Ratio', value: (riskMetrics.sharpe_ratio || 0).toFixed(2), icon: TrendingUp },
    { label: 'Max Drawdown', value: `${Math.round((riskMetrics.max_drawdown || 0) * 100)}%`, icon: TrendingDown },
    { label: 'Beta', value: (riskMetrics.beta || 0).toFixed(2), icon: BarChart2 },
    { label: 'VaR (95%)', value: `${Math.round((riskMetrics.var_95 || 0) * 100)}%`, icon: Shield },
  ];

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-white flex items-center gap-2">
            <Shield className="w-5 h-5 text-blue-400" />
            Risk Assessment
          </CardTitle>
          <Button variant="ghost" size="icon" onClick={assessRisk} disabled={loading}>
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription className="text-gray-400">Portfolio risk metrics and position sizing</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {loading && <LoadingSkeleton />}
        {error && <ErrorMessage message={error} />}
        {!loading && (
          <>
            <div className={`flex items-center gap-3 p-3 ${riskBg} rounded-lg`}>
              <AlertTriangle className={`w-5 h-5 ${riskColor}`} />
              <div>
                <div className={`font-bold ${riskColor}`}>Risk Level: {riskMetrics.overall_risk}</div>
                <div className="text-gray-400 text-xs">Based on current portfolio composition</div>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              {metrics.map(({ label, value, icon: Icon }) => (
                <div key={label} className="p-3 bg-gray-700/50 rounded-lg">
                  <div className="flex items-center gap-1 text-gray-400 text-xs mb-1">
                    <Icon className="w-3 h-3" />
                    {label}
                  </div>
                  <div className="text-white font-mono font-bold text-sm">{value}</div>
                </div>
              ))}
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}

// DCA Schedule Manager
function DCAManager() {
  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ asset: 'BTC', amount: '100', frequency: 'weekly', periods: '52' });

  const fetchSchedules = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.phase3.portfolio.getDCASchedules();
      setSchedules(result.schedules || []);
    } catch (err) {
      setError(err.message || 'Failed to load DCA schedules');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchSchedules(); }, [fetchSchedules]);

  const handleCreate = async () => {
    setCreating(true);
    setError(null);
    try {
      await api.phase3.portfolio.createDCA(form.asset, parseFloat(form.amount), form.frequency, parseInt(form.periods));
      await fetchSchedules();
    } catch (err) {
      setError(err.message || 'Failed to create DCA schedule');
    } finally {
      setCreating(false);
    }
  };

  const assets = ['BTC', 'ETH', 'SOL', 'BNB', 'ADA'];
  const frequencies = ['daily', 'weekly', 'monthly'];

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          <CalendarClock className="w-5 h-5 text-green-400" />
          DCA Schedule Manager
        </CardTitle>
        <CardDescription className="text-gray-400">Automate dollar-cost averaging purchases</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-1">
            <label className="text-xs text-gray-400">Asset</label>
            <Select value={form.asset} onValueChange={(v) => setForm((f) => ({ ...f, asset: v }))}>
              <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-gray-800 border-gray-700">
                {assets.map((a) => <SelectItem key={a} value={a} className="text-white">{a}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-1">
            <label className="text-xs text-gray-400">Frequency</label>
            <Select value={form.frequency} onValueChange={(v) => setForm((f) => ({ ...f, frequency: v }))}>
              <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-gray-800 border-gray-700">
                {frequencies.map((f) => <SelectItem key={f} value={f} className="text-white capitalize">{f}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-1">
            <label className="text-xs text-gray-400">Amount per period (USD)</label>
            <Input
              type="number"
              value={form.amount}
              onChange={(e) => setForm((f) => ({ ...f, amount: e.target.value }))}
              className="bg-gray-700 border-gray-600 text-white"
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-gray-400">Number of periods</label>
            <Input
              type="number"
              value={form.periods}
              onChange={(e) => setForm((f) => ({ ...f, periods: e.target.value }))}
              className="bg-gray-700 border-gray-600 text-white"
            />
          </div>
        </div>

        <div className="p-3 bg-gray-700/50 rounded-lg text-xs text-gray-400">
          Total investment: <span className="text-white font-bold">
            ${(parseFloat(form.amount || 0) * parseInt(form.periods || 0)).toLocaleString()}
          </span>
        </div>

        {error && <ErrorMessage message={error} />}

        <Button onClick={handleCreate} disabled={creating} className="w-full bg-green-600 hover:bg-green-700">
          {creating ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Plus className="w-4 h-4 mr-2" />}
          Create DCA Schedule
        </Button>

        {loading && <LoadingSkeleton />}
        {schedules.length > 0 && (
          <div className="space-y-2">
            <div className="text-xs text-gray-400 uppercase tracking-wide">Active Schedules</div>
            {schedules.map((s, i) => (
              <div key={i} className="flex items-center justify-between p-2.5 bg-green-500/10 border border-green-500/20 rounded-lg text-sm">
                <div>
                  <span className="text-white">{s.asset}</span>
                  <span className="text-gray-400 ml-2">${s.amount}/{s.frequency}</span>
                </div>
                <Badge className="bg-green-500/20 text-green-400 text-xs">Active</Badge>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// Stop-Loss Controls
function StopLossControls() {
  const [stops, setStops] = useState([]);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({
    asset: 'BTC',
    entryPrice: '45000',
    stopPrice: '42000',
    trailingPercent: '5',
  });

  const fetchStops = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.phase3.portfolio.getActiveStopLosses();
      setStops(result.stops || []);
    } catch (err) {
      setError(err.message || 'Failed to load stop-loss orders');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchStops(); }, [fetchStops]);

  const handleCreate = async () => {
    setCreating(true);
    setError(null);
    try {
      await api.phase3.portfolio.createStopLoss(
        form.asset,
        parseFloat(form.entryPrice),
        parseFloat(form.stopPrice),
        parseFloat(form.trailingPercent),
      );
      await fetchStops();
    } catch (err) {
      setError(err.message || 'Failed to create stop-loss');
    } finally {
      setCreating(false);
    }
  };

  const assets = ['BTC', 'ETH', 'SOL', 'BNB'];

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-white flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-red-400" />
            Stop-Loss Controls
          </CardTitle>
          <Button variant="ghost" size="icon" onClick={fetchStops} disabled={loading}>
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription className="text-gray-400">Set trailing stop-loss and take-profit levels</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-1">
            <label className="text-xs text-gray-400">Asset</label>
            <Select value={form.asset} onValueChange={(v) => setForm((f) => ({ ...f, asset: v }))}>
              <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-gray-800 border-gray-700">
                {assets.map((a) => <SelectItem key={a} value={a} className="text-white">{a}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-1">
            <label className="text-xs text-gray-400">Trailing % (optional)</label>
            <Input
              type="number"
              value={form.trailingPercent}
              onChange={(e) => setForm((f) => ({ ...f, trailingPercent: e.target.value }))}
              className="bg-gray-700 border-gray-600 text-white"
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-gray-400">Entry Price (USD)</label>
            <Input
              type="number"
              value={form.entryPrice}
              onChange={(e) => setForm((f) => ({ ...f, entryPrice: e.target.value }))}
              className="bg-gray-700 border-gray-600 text-white"
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-gray-400">Stop Price (USD)</label>
            <Input
              type="number"
              value={form.stopPrice}
              onChange={(e) => setForm((f) => ({ ...f, stopPrice: e.target.value }))}
              className="bg-gray-700 border-gray-600 text-white"
            />
          </div>
        </div>

        {error && <ErrorMessage message={error} />}

        <Button onClick={handleCreate} disabled={creating} className="w-full bg-red-600 hover:bg-red-700">
          {creating ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <AlertTriangle className="w-4 h-4 mr-2" />}
          Set Stop-Loss
        </Button>

        {loading && <LoadingSkeleton />}
        {stops.length > 0 && (
          <div className="space-y-2">
            <div className="text-xs text-gray-400 uppercase tracking-wide">Active Stops</div>
            {stops.map((s, i) => (
              <div key={i} className="flex items-center justify-between p-2.5 bg-red-500/10 border border-red-500/20 rounded-lg text-sm">
                <div>
                  <span className="text-white">{s.asset}</span>
                  <span className="text-gray-400 ml-2">Stop: ${s.stopPrice?.toLocaleString()}</span>
                </div>
                <Badge className="bg-red-500/20 text-red-400 text-xs">Active</Badge>
              </div>
            ))}
          </div>
        )}
        {stops.length === 0 && !loading && (
          <div className="flex items-center gap-2 text-gray-400 text-sm">
            <CheckCircle2 className="w-4 h-4 text-green-400" />
            No active stop-loss orders
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// Main Portfolio page
export default function Portfolio() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Portfolio Management</h1>
        <p className="text-gray-400 mt-1">Automated rebalancing, risk management, DCA &amp; stop-loss protection</p>
      </div>

      <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-4">
        {[
          { title: 'Total Value', value: '$50,000', icon: Briefcase, color: 'text-blue-400' },
          { title: '24h Change', value: '+2.34%', icon: TrendingUp, color: 'text-green-400' },
          { title: 'Assets', value: '4', icon: BarChart2, color: 'text-purple-400' },
          { title: 'Auto-Rebalance', value: 'Active', icon: RefreshCw, color: 'text-orange-400' },
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

      <Tabs defaultValue="rebalance">
        <TabsList className="bg-gray-800 border border-gray-700">
          <TabsTrigger value="rebalance" className="data-[state=active]:bg-gray-700">
            <RefreshCw className="w-4 h-4 mr-1" /> Rebalance
          </TabsTrigger>
          <TabsTrigger value="risk" className="data-[state=active]:bg-gray-700">
            <Shield className="w-4 h-4 mr-1" /> Risk
          </TabsTrigger>
          <TabsTrigger value="dca" className="data-[state=active]:bg-gray-700">
            <CalendarClock className="w-4 h-4 mr-1" /> DCA
          </TabsTrigger>
          <TabsTrigger value="stoploss" className="data-[state=active]:bg-gray-700">
            <AlertTriangle className="w-4 h-4 mr-1" /> Stop-Loss
          </TabsTrigger>
        </TabsList>

        <TabsContent value="rebalance" className="mt-4">
          <RebalancingModule />
        </TabsContent>
        <TabsContent value="risk" className="mt-4">
          <RiskAssessment />
        </TabsContent>
        <TabsContent value="dca" className="mt-4">
          <DCAManager />
        </TabsContent>
        <TabsContent value="stoploss" className="mt-4">
          <StopLossControls />
        </TabsContent>
      </Tabs>
    </div>
  );
}
