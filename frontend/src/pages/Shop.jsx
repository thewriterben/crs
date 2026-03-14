import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  ShoppingCart, CreditCard, Coins, TrendingUp, TrendingDown,
  Minus, RefreshCw, Loader2, AlertCircle, Tag, CheckCircle2
} from 'lucide-react';
import { api } from '@/lib/api';
import ProductCatalog from '@/components/shop/ProductCatalog';

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

// CFV Valuation indicator
function ValuationBadge({ status }) {
  const styles = {
    undervalued: 'bg-green-500/20 text-green-400 border-green-500/30',
    fair: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    overvalued: 'bg-red-500/20 text-red-400 border-red-500/30',
  };
  const icons = {
    undervalued: <TrendingUp className="w-3 h-3" />,
    fair: <Minus className="w-3 h-3" />,
    overvalued: <TrendingDown className="w-3 h-3" />,
  };
  return (
    <span className={`inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full border ${styles[status] || styles.fair}`}>
      {icons[status]}
      {status}
    </span>
  );
}

// Mock CFV currency data (replaces API when unavailable)
const MOCK_CFV_CURRENCIES = [
  { symbol: 'BTC', name: 'Bitcoin', discount: 0, marketPrice: 45000, fairValue: 48000, valuation: 'undervalued' },
  { symbol: 'ETH', name: 'Ethereum', discount: 5, marketPrice: 3200, fairValue: 3000, valuation: 'overvalued' },
  { symbol: 'SOL', name: 'Solana', discount: 10, marketPrice: 150, fairValue: 155, valuation: 'fair' },
  { symbol: 'BNB', name: 'BNB', discount: 3, marketPrice: 420, fairValue: 450, valuation: 'undervalued' },
  { symbol: 'ADA', name: 'Cardano', discount: 7, marketPrice: 0.45, fairValue: 0.38, valuation: 'overvalued' },
  { symbol: 'USDT', name: 'Tether', discount: 0, marketPrice: 1.0, fairValue: 1.0, valuation: 'fair' },
];

// CFV Payment Method Selector
function CFVPaymentSelector({ onSelect, selected }) {
  const [currencies, setCurrencies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchCurrencies = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.cfv.getSupportedCurrencies();
      setCurrencies(result.currencies || MOCK_CFV_CURRENCIES);
    } catch {
      setCurrencies(MOCK_CFV_CURRENCIES);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchCurrencies(); }, [fetchCurrencies]);

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-white flex items-center gap-2">
            <Coins className="w-5 h-5 text-yellow-400" />
            CFV Payment Method
          </CardTitle>
          <Button variant="ghost" size="icon" onClick={fetchCurrencies} disabled={loading}>
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription className="text-gray-400">Pay with crypto — undervalued coins earn extra discounts</CardDescription>
      </CardHeader>
      <CardContent>
        {loading && <LoadingSkeleton />}
        {error && <ErrorMessage message={error} />}
        <div className="grid sm:grid-cols-2 gap-2 mt-2">
          {currencies.map((currency) => (
            <button
              key={currency.symbol}
              onClick={() => onSelect?.(currency)}
              className={`flex items-center gap-3 p-3 rounded-lg border text-left transition-all ${
                selected?.symbol === currency.symbol
                  ? 'border-orange-500 bg-orange-500/10'
                  : 'border-gray-700 bg-gray-700/30 hover:border-gray-500'
              }`}
            >
              <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center text-xs font-bold text-white flex-shrink-0">
                {currency.symbol.slice(0, 2)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-white text-sm font-medium">{currency.symbol}</span>
                  {currency.discount > 0 && (
                    <Badge className="bg-green-500/20 text-green-400 text-xs px-1.5">
                      -{currency.discount}%
                    </Badge>
                  )}
                </div>
                <div className="flex items-center gap-1 mt-0.5">
                  <ValuationBadge status={currency.valuation} />
                </div>
              </div>
              {selected?.symbol === currency.symbol && (
                <CheckCircle2 className="w-4 h-4 text-orange-400 flex-shrink-0" />
              )}
            </button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

// CFV Coin Analytics
function CFVAnalytics() {
  const currencies = MOCK_CFV_CURRENCIES;

  const undervalued = currencies.filter((c) => c.valuation === 'undervalued');
  const overvalued = currencies.filter((c) => c.valuation === 'overvalued');
  const fair = currencies.filter((c) => c.valuation === 'fair');

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          <Tag className="w-5 h-5 text-purple-400" />
          CFV Coin Valuation Analytics
        </CardTitle>
        <CardDescription className="text-gray-400">Market price vs. fair value for payment coins</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-3 gap-3 text-center">
          <div className="p-3 bg-green-500/10 border border-green-500/20 rounded-lg">
            <div className="text-2xl font-bold text-green-400">{undervalued.length}</div>
            <div className="text-xs text-gray-400 mt-1">Undervalued</div>
            <div className="text-xs text-green-400">Best to pay with</div>
          </div>
          <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
            <div className="text-2xl font-bold text-blue-400">{fair.length}</div>
            <div className="text-xs text-gray-400 mt-1">Fair Value</div>
            <div className="text-xs text-blue-400">Neutral</div>
          </div>
          <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
            <div className="text-2xl font-bold text-red-400">{overvalued.length}</div>
            <div className="text-xs text-gray-400 mt-1">Overvalued</div>
            <div className="text-xs text-red-400">Consider holding</div>
          </div>
        </div>

        <div className="space-y-2">
          <div className="text-xs text-gray-400 uppercase tracking-wide">Price vs Fair Value</div>
          {currencies.map((currency) => {
            const diff = ((currency.marketPrice - currency.fairValue) / currency.fairValue) * 100;
            const isUnder = diff < 0;
            return (
              <div key={currency.symbol} className="flex items-center gap-3 p-2.5 bg-gray-700/30 rounded-lg">
                <div className="w-16 text-white text-sm font-medium">{currency.symbol}</div>
                <div className="flex-1">
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-gray-400">${currency.marketPrice < 1 ? currency.marketPrice.toFixed(4) : currency.marketPrice.toLocaleString()}</span>
                    <span className={isUnder ? 'text-green-400' : diff > 0 ? 'text-red-400' : 'text-blue-400'}>
                      {isUnder ? '' : '+'}{diff.toFixed(1)}% vs fair
                    </span>
                  </div>
                  <div className="h-1.5 bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${isUnder ? 'bg-green-500' : diff > 0 ? 'bg-red-500' : 'bg-blue-500'}`}
                      style={{ width: `${Math.min(Math.abs(diff) * 3 + 20, 100)}%` }}
                    />
                  </div>
                </div>
                <ValuationBadge status={currency.valuation} />
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

// Checkout with selected payment
function CheckoutPanel({ selected }) {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const handleCheckout = async () => {
    if (!selected) return;
    setLoading(true);
    setError(null);
    try {
      await api.cfv.createPayment({ currency: selected.symbol, amount: 100 });
      setSuccess(true);
    } catch (err) {
      setError(err.message || 'Payment failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          <CreditCard className="w-5 h-5 text-orange-400" />
          Checkout
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {selected ? (
          <>
            <div className="p-3 bg-gray-700/50 rounded-lg space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Payment Method</span>
                <span className="text-white">{selected.name} ({selected.symbol})</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Valuation</span>
                <ValuationBadge status={selected.valuation} />
              </div>
              {selected.discount > 0 && (
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">CFV Discount</span>
                  <span className="text-green-400">-{selected.discount}%</span>
                </div>
              )}
            </div>
            {error && <ErrorMessage message={error} />}
            {success ? (
              <div className="flex items-center gap-2 text-green-400 p-3 bg-green-500/10 rounded-lg">
                <CheckCircle2 className="w-4 h-4" />
                Payment initiated successfully
              </div>
            ) : (
              <Button onClick={handleCheckout} disabled={loading} className="w-full bg-orange-500 hover:bg-orange-600">
                {loading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <CreditCard className="w-4 h-4 mr-2" />}
                Pay with {selected.symbol}
              </Button>
            )}
          </>
        ) : (
          <p className="text-gray-400 text-sm text-center py-4">Select a payment method above</p>
        )}
      </CardContent>
    </Card>
  );
}

// Main Shop page
export default function Shop() {
  const [selectedPayment, setSelectedPayment] = useState(null);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Crypto Shop</h1>
        <p className="text-gray-400 mt-1">Buy AI tools, trading bots &amp; analytics — pay with crypto for CFV discounts</p>
      </div>

      <Tabs defaultValue="catalog">
        <TabsList className="bg-gray-800 border border-gray-700">
          <TabsTrigger value="catalog" className="data-[state=active]:bg-gray-700">
            <ShoppingCart className="w-4 h-4 mr-1" /> Catalog
          </TabsTrigger>
          <TabsTrigger value="payment" className="data-[state=active]:bg-gray-700">
            <Coins className="w-4 h-4 mr-1" /> CFV Payment
          </TabsTrigger>
          <TabsTrigger value="analytics" className="data-[state=active]:bg-gray-700">
            <TrendingUp className="w-4 h-4 mr-1" /> Analytics
          </TabsTrigger>
        </TabsList>

        <TabsContent value="catalog" className="mt-4">
          <ProductCatalog />
        </TabsContent>

        <TabsContent value="payment" className="mt-4">
          <div className="grid md:grid-cols-2 gap-4">
            <CFVPaymentSelector selected={selectedPayment} onSelect={setSelectedPayment} />
            <CheckoutPanel selected={selectedPayment} />
          </div>
        </TabsContent>

        <TabsContent value="analytics" className="mt-4">
          <CFVAnalytics />
        </TabsContent>
      </Tabs>
    </div>
  );
}
