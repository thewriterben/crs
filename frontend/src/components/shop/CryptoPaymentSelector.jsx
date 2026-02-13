/**
 * CryptoPaymentSelector Component
 * 
 * Displays all 12 DGF cryptocurrencies with CFV information,
 * real-time discounts, and valuation status indicators.
 */

import React, { useState, useEffect } from 'react';
import { 
  getSupportedCoins, 
  getPaymentInfo,
  formatCurrency,
  getValuationColor,
  getValuationIcon
} from '../../lib/cfvPaymentApi';

export default function CryptoPaymentSelector({ amount, onSelect, onError }) {
  const [coins, setCoins] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCoin, setSelectedCoin] = useState(null);
  const [paymentInfo, setPaymentInfo] = useState(null);
  const [loadingPaymentInfo, setLoadingPaymentInfo] = useState(false);

  // Fetch supported coins on mount
  useEffect(() => {
    loadSupportedCoins();
  }, []);

  const loadSupportedCoins = async () => {
    try {
      setLoading(true);
      const data = await getSupportedCoins();
      
      // Sort by discount (highest first)
      const sorted = data.sort((a, b) => (b.discount || 0) - (a.discount || 0));
      setCoins(sorted);
    } catch (error) {
      console.error('Error loading coins:', error);
      if (onError) onError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCoinSelect = async (coin) => {
    setSelectedCoin(coin);
    
    if (amount && amount > 0) {
      try {
        setLoadingPaymentInfo(true);
        const info = await getPaymentInfo(coin.symbol, amount);
        setPaymentInfo(info);
      } catch (error) {
        console.error('Error getting payment info:', error);
        if (onError) onError(error.message);
      } finally {
        setLoadingPaymentInfo(false);
      }
    }
  };

  const handleConfirmSelection = () => {
    if (selectedCoin && onSelect) {
      onSelect(selectedCoin, paymentInfo);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-400"></div>
        <span className="ml-3 text-gray-400">Loading cryptocurrencies...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-2xl font-bold text-white mb-2">
          Select Payment Cryptocurrency
        </h2>
        <p className="text-gray-400">
          Save up to 10% by paying with undervalued cryptocurrencies
        </p>
      </div>

      {/* Coin Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {coins.map((coin) => (
          <CoinCard
            key={coin.symbol}
            coin={coin}
            isSelected={selectedCoin?.symbol === coin.symbol}
            onSelect={handleCoinSelect}
          />
        ))}
      </div>

      {/* Payment Info Panel */}
      {selectedCoin && (
        <PaymentInfoPanel
          coin={selectedCoin}
          amount={amount}
          paymentInfo={paymentInfo}
          loading={loadingPaymentInfo}
          onConfirm={handleConfirmSelection}
        />
      )}
    </div>
  );
}

/**
 * Individual Coin Card Component
 */
function CoinCard({ coin, isSelected, onSelect }) {
  const hasDiscount = coin.discount > 0;
  const valuationStatus = coin.cfv?.valuationStatus || 'fair';
  const valuationColor = getValuationColor(valuationStatus);
  const valuationIcon = getValuationIcon(valuationStatus);

  return (
    <button
      onClick={() => onSelect(coin)}
      className={`
        relative p-4 rounded-lg border-2 transition-all
        ${isSelected 
          ? 'border-orange-400 bg-orange-400/10' 
          : 'border-gray-700 bg-gray-800 hover:border-gray-600'
        }
      `}
    >
      {/* Discount Badge */}
      {hasDiscount && (
        <div className="absolute top-2 right-2 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded-full">
          {coin.discount}% OFF
        </div>
      )}

      {/* Coin Header */}
      <div className="text-left mb-3">
        <div className="flex items-center space-x-2">
          <h3 className="text-lg font-bold text-white">{coin.symbol}</h3>
          <span className="text-xl">{valuationIcon}</span>
        </div>
        <p className="text-sm text-gray-400">{coin.name}</p>
        <span className="inline-block mt-1 text-xs bg-gray-700 text-gray-300 px-2 py-0.5 rounded">
          {coin.category}
        </span>
      </div>

      {/* CFV Information */}
      {coin.cfv && (
        <div className="text-left space-y-1 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-400">Current Price:</span>
            <span className="text-white">${coin.cfv.currentPrice.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Fair Value:</span>
            <span className="text-white">${coin.cfv.fairValue.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Valuation:</span>
            <span className={valuationColor}>
              {coin.cfv.valuationPercent > 0 ? '+' : ''}
              {coin.cfv.valuationPercent.toFixed(1)}%
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Status:</span>
            <span className={valuationColor + ' capitalize'}>
              {valuationStatus}
            </span>
          </div>
        </div>
      )}

      {/* Selection Indicator */}
      {isSelected && (
        <div className="mt-3 text-center">
          <span className="inline-block bg-orange-400 text-white text-sm font-bold px-3 py-1 rounded">
            ✓ Selected
          </span>
        </div>
      )}
    </button>
  );
}

/**
 * Payment Info Panel Component
 */
function PaymentInfoPanel({ coin, amount, paymentInfo, loading, onConfirm }) {
  if (loading) {
    return (
      <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-400"></div>
          <span className="ml-3 text-gray-400">Calculating payment details...</span>
        </div>
      </div>
    );
  }

  if (!paymentInfo) {
    return null;
  }

  const hasDiscount = paymentInfo.discountPercent > 0;
  const savings = paymentInfo.discountAmount;

  return (
    <div className="bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-700 rounded-lg p-6 space-y-4">
      <h3 className="text-xl font-bold text-white text-center">
        Payment Summary - {coin.name}
      </h3>

      {/* Price Breakdown */}
      <div className="space-y-2">
        <div className="flex justify-between text-gray-300">
          <span>Original Price:</span>
          <span>{formatCurrency(paymentInfo.originalPriceUSD)}</span>
        </div>

        {hasDiscount && (
          <>
            <div className="flex justify-between text-green-400 font-semibold">
              <span>CFV Discount ({paymentInfo.discountPercent}%):</span>
              <span>-{formatCurrency(savings)}</span>
            </div>
            <div className="border-t border-gray-700 pt-2"></div>
          </>
        )}

        <div className="flex justify-between text-xl font-bold text-white">
          <span>Final Price:</span>
          <span>{formatCurrency(paymentInfo.finalPriceUSD)}</span>
        </div>

        <div className="flex justify-between text-orange-400 font-mono">
          <span>Amount in {coin.symbol}:</span>
          <span>{paymentInfo.amountCrypto.toFixed(8)} {coin.symbol}</span>
        </div>
      </div>

      {/* Savings Highlight */}
      {hasDiscount && (
        <div className="bg-green-500/20 border border-green-500 rounded-lg p-3 text-center">
          <p className="text-green-400 font-bold text-lg">
            🎉 You Save {formatCurrency(savings)}!
          </p>
          <p className="text-green-300 text-sm mt-1">
            {coin.symbol} is {paymentInfo.cfvMetrics.valuationPercent.toFixed(1)}% undervalued
          </p>
        </div>
      )}

      {/* CFV Metrics */}
      {paymentInfo.cfvMetrics && (
        <div className="bg-gray-900/50 rounded-lg p-3 space-y-1 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-400">Current Market Price:</span>
            <span className="text-white">${paymentInfo.cfvMetrics.currentPrice.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Calculated Fair Value:</span>
            <span className="text-white">${paymentInfo.cfvMetrics.fairValue.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Valuation Status:</span>
            <span className={getValuationColor(paymentInfo.cfvMetrics.valuationStatus) + ' capitalize'}>
              {paymentInfo.cfvMetrics.valuationStatus}
            </span>
          </div>
        </div>
      )}

      {/* Confirm Button */}
      <button
        onClick={onConfirm}
        className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 px-6 rounded-lg transition-colors"
      >
        Continue with {coin.symbol}
      </button>

      {/* Info Note */}
      <p className="text-xs text-gray-500 text-center">
        Payment address will be generated after confirmation
      </p>
    </div>
  );
}
