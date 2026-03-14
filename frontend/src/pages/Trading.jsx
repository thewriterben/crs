import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Brain, TrendingUp, TrendingDown, BarChart2, Activity,
  RefreshCw, Loader2, AlertCircle, Users, Copy, Zap
} from 'lucide-react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, AreaChart, Area
} from 'recharts';
import { api } from '@/lib/api';

// Loading skeleton component
function LoadingSkeleton() {
  return (
    <div className="animate-pulse space-y-3">
      <div className="h-4 bg-gray-700 rounded w-3/4" />
      <div className="h-4 bg-gray-700 rounded w-1/2" />
      <div className="h-8 bg-gray-700 rounded" />
    </div>
  );
}

// Confidence badge
function ConfidenceBadge({ confidence }) {
  const pct = Math.round((confidence || 0) * 100);
  const color = pct >= 75 ? 'bg-green-500/20 text-green-400' : pct >= 55 ? 'bg-yellow-500/20 text-yellow-400' : 'bg-red-500/20 text-red-400';
  return <span className={`text-xs px-2 py-0.5 rounded-full ${color}`}>{pct}% confidence</span>;
}

// AI Prediction Widget
function PredictionWidget({ title, model, symbol, fetcher }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPrediction = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetcher(symbol);
      setData(result);
    } catch (err) {
      setError(err.message || 'Failed to fetch prediction');
    } finally {
      setLoading(false);
    }
  }, [symbol, fetcher]);

  useEffect(() => { fetchPrediction(); }, [fetchPrediction]);

  const trend = data?.trend || 'neutral';
  const TrendIcon = trend === 'bullish' ? TrendingUp : TrendingDown;
  const trendColor = trend === 'bullish' ? 'text-green-400' : 'text-red-400';

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-white text-sm flex items-center gap-2">
            <Brain className="w-4 h-4 text-purple-400" />
            {title}
          </CardTitle>
          <Button variant="ghost" size="icon" className="h-6 w-6" onClick={fetchPrediction} disabled={loading}>
            <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription className="text-gray-400 text-xs">Model: {model}</CardDescription>
      </CardHeader>
      <CardContent>
        {loading && <LoadingSkeleton />}
        {error && (
          <div className="flex items-center gap-2 text-red-400 text-xs">
            <AlertCircle className="w-3 h-3" /> {error}
          </div>
        )}
        {data && !loading && (
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-gray-400 text-xs">Trend</span>
              <div className="flex items-center gap-1">
                <TrendIcon className={`w-4 h-4 ${trendColor}`} />
                <span className={`text-sm font-semibold capitalize ${trendColor}`}>{trend}</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-400 text-xs">Confidence</span>
              <ConfidenceBadge confidence={data.confidence} />
            </div>
            {data.predictions?.[0] && (
              <div className="flex items-center justify-between">
                <span className="text-gray-400 text-xs">Price Forecast</span>
                <span className="text-white text-sm font-mono">
                  ${data.predictions[0].price?.toLocaleString() || 'N/A'}
                </span>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// BERT Sentiment Widget
function SentimentWidget({ symbol }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSentiment = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.phase3.ai.analyzeSentiment(symbol);
      setData(result);
    } catch (err) {
      setError(err.message || 'Failed to fetch sentiment');
    } finally {
      setLoading(false);
    }
  }, [symbol]);

  useEffect(() => { fetchSentiment(); }, [fetchSentiment]);

  const label = data?.sentiment_label || 'NEUTRAL';
  const score = data?.sentiment_score || 0;
  const labelColor = label === 'BULLISH' ? 'text-green-400' : label === 'BEARISH' ? 'text-red-400' : 'text-yellow-400';
  const barColor = label === 'BULLISH' ? 'bg-green-500' : label === 'BEARISH' ? 'bg-red-500' : 'bg-yellow-500';

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-white text-sm flex items-center gap-2">
            <Activity className="w-4 h-4 text-blue-400" />
            BERT Sentiment — {symbol}
          </CardTitle>
          <Button variant="ghost" size="icon" className="h-6 w-6" onClick={fetchSentiment} disabled={loading}>
            <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription className="text-gray-400 text-xs">NLP-based news &amp; social sentiment</CardDescription>
      </CardHeader>
      <CardContent>
        {loading && <LoadingSkeleton />}
        {error && <div className="flex items-center gap-2 text-red-400 text-xs"><AlertCircle className="w-3 h-3" /> {error}</div>}
        {data && !loading && (
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className={`text-lg font-bold ${labelColor}`}>{label}</span>
              <ConfidenceBadge confidence={data.confidence} />
            </div>
            <div className="space-y-1">
              <div className="flex justify-between text-xs text-gray-400">
                <span>Sentiment Score</span>
                <span>{Math.round(score * 100)}%</span>
              </div>
              <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                <div className={`h-full ${barColor} rounded-full transition-all`} style={{ width: `${score * 100}%` }} />
              </div>
            </div>
            {data.sources && (
              <div className="grid grid-cols-3 gap-2 text-xs">
                {Object.entries(data.sources).map(([src, val]) => (
                  <div key={src} className="text-center">
                    <div className="text-gray-400 capitalize">{src}</div>
                    <div className="text-white font-mono">{Math.round(val * 100)}%</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// Copy Trading / Bot Dashboard
function TradingBotDashboard() {
  const [traders, setTraders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [copying, setCopying] = useState(null);
  const [error, setError] = useState(null);

  const fetchTraders = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.phase3.social.getTopTraders(5);
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
        <CardTitle className="text-white flex items-center gap-2">
          <Users className="w-5 h-5 text-blue-400" />
          Copy Trading — Top Bots &amp; Traders
        </CardTitle>
        <CardDescription className="text-gray-400">Follow top-performing traders automatically</CardDescription>
      </CardHeader>
      <CardContent>
        {loading && <LoadingSkeleton />}
        {error && <div className="flex items-center gap-2 text-red-400 text-sm"><AlertCircle className="w-4 h-4" /> {error}</div>}
        <div className="space-y-3">
          {traders.map((trader) => (
            <div key={trader.id} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-white font-medium text-sm">{trader.username}</span>
                  {trader.verified && <Badge className="bg-blue-500/20 text-blue-400 text-xs px-1.5">✓ Verified</Badge>}
                </div>
                <div className="flex gap-3 text-xs text-gray-400 mt-1">
                  <span className="text-green-400">Win: {Math.round((trader.winRate || 0) * 100)}%</span>
                  <span>Avg Return: {Math.round((trader.avgReturn || 0) * 100)}%</span>
                  <span>{trader.followers?.toLocaleString()} followers</span>
                </div>
              </div>
              <Button
                size="sm"
                variant="outline"
                className="border-blue-500 text-blue-400 hover:bg-blue-500/20 text-xs"
                onClick={() => handleCopyTrade(trader.id)}
                disabled={copying === trader.id}
              >
                {copying === trader.id ? <Loader2 className="w-3 h-3 animate-spin" /> : <Copy className="w-3 h-3 mr-1" />}
                Copy
              </Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

// Price forecast chart mock
function PriceForecastChart({ symbol }) {
  const basePrice = symbol === 'BTC' ? 45000 : symbol === 'ETH' ? 3200 : 150;
  const data = Array.from({ length: 14 }, (_, i) => ({
    day: i < 7 ? `T-${6 - i}` : `T+${i - 6}`,
    historical: i < 7 ? basePrice * (1 + (Math.random() - 0.5) * 0.05) : null,
    forecast: i >= 6 ? basePrice * (1 + (i - 6) * 0.008 + (Math.random() - 0.5) * 0.02) : null,
  }));

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          <BarChart2 className="w-5 h-5 text-orange-400" />
          {symbol} Price Forecast
        </CardTitle>
        <CardDescription className="text-gray-400">7-day ensemble prediction</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={200}>
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="day" tick={{ fill: '#9CA3AF', fontSize: 11 }} />
            <YAxis tick={{ fill: '#9CA3AF', fontSize: 11 }} />
            <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px' }} />
            <Area type="monotone" dataKey="historical" stroke="#F97316" fill="#F97316" fillOpacity={0.1} dot={false} name="Historical" />
            <Area type="monotone" dataKey="forecast" stroke="#8B5CF6" fill="#8B5CF6" fillOpacity={0.1} strokeDasharray="5 5" dot={false} name="Forecast" />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

// Main Trading page
export default function Trading() {
  const [selectedSymbol, setSelectedSymbol] = useState('BTC');
  const symbols = ['BTC', 'ETH', 'SOL', 'BNB'];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">AI Trading</h1>
          <p className="text-gray-400 mt-1">Advanced ML predictions, sentiment analysis &amp; copy trading</p>
        </div>
        <div className="flex gap-2">
          {symbols.map((s) => (
            <Button
              key={s}
              size="sm"
              variant={selectedSymbol === s ? 'default' : 'outline'}
              className={selectedSymbol === s ? 'bg-orange-500 hover:bg-orange-600' : 'border-gray-600 text-gray-300'}
              onClick={() => setSelectedSymbol(s)}
            >
              {s}
            </Button>
          ))}
        </div>
      </div>

      <Tabs defaultValue="predictions">
        <TabsList className="bg-gray-800 border border-gray-700">
          <TabsTrigger value="predictions" className="data-[state=active]:bg-gray-700">
            <Brain className="w-4 h-4 mr-1" /> Predictions
          </TabsTrigger>
          <TabsTrigger value="sentiment" className="data-[state=active]:bg-gray-700">
            <Activity className="w-4 h-4 mr-1" /> Sentiment
          </TabsTrigger>
          <TabsTrigger value="copytrade" className="data-[state=active]:bg-gray-700">
            <Copy className="w-4 h-4 mr-1" /> Copy Trade
          </TabsTrigger>
        </TabsList>

        <TabsContent value="predictions" className="mt-4 space-y-4">
          <PriceForecastChart symbol={selectedSymbol} />
          <div className="grid md:grid-cols-3 gap-4">
            <PredictionWidget
              title={`LSTM — ${selectedSymbol}`}
              model="LSTM (60-period lookback)"
              symbol={selectedSymbol}
              fetcher={(sym) => api.phase3.ai.lstmPredict(sym)}
            />
            <PredictionWidget
              title={`Transformer — ${selectedSymbol}`}
              model="Transformer (8-head attention)"
              symbol={selectedSymbol}
              fetcher={(sym) => api.phase3.ai.transformerPredict(sym)}
            />
            <PredictionWidget
              title={`Ensemble — ${selectedSymbol}`}
              model="Ensemble (5 models)"
              symbol={selectedSymbol}
              fetcher={(sym) => api.phase3.ai.ensemblePredict(sym)}
            />
          </div>
        </TabsContent>

        <TabsContent value="sentiment" className="mt-4">
          <div className="grid md:grid-cols-2 gap-4">
            {symbols.map((sym) => (
              <SentimentWidget key={sym} symbol={sym} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="copytrade" className="mt-4">
          <TradingBotDashboard />
        </TabsContent>
      </Tabs>
    </div>
  );
}
