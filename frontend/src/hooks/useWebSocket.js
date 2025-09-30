/**
 * Custom React hook for WebSocket real-time data streaming
 */

import { useEffect, useState, useCallback, useRef } from 'react';
import websocketService from '@/lib/websocket.js';

/**
 * Hook for managing WebSocket connection and receiving real-time updates
 * @param {Object} options - Configuration options
 * @param {boolean} options.autoConnect - Auto connect on mount (default: true)
 * @param {string[]} options.symbols - Symbols to subscribe to
 * @returns {Object} WebSocket state and methods
 */
export const useWebSocket = (options = {}) => {
  const { autoConnect = true, symbols = ['BTC', 'ETH'] } = options;
  
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [marketData, setMarketData] = useState({});
  const [sentimentData, setSentimentData] = useState(null);
  const [tradingSignals, setTradingSignals] = useState([]);
  const [lastUpdate, setLastUpdate] = useState(null);
  
  const signalsRef = useRef([]);

  // Handle connection status updates
  const handleConnectionStatus = useCallback((data) => {
    setConnectionStatus(data.status);
    setLastUpdate(data.timestamp);
  }, []);

  // Handle market data updates
  const handleMarketUpdate = useCallback((data) => {
    setMarketData(prev => ({
      ...prev,
      ...data
    }));
    setLastUpdate(new Date().toISOString());
  }, []);

  // Handle sentiment updates
  const handleSentimentUpdate = useCallback((data) => {
    setSentimentData(data);
    setLastUpdate(new Date().toISOString());
  }, []);

  // Handle trading signals
  const handleTradingSignal = useCallback((signal) => {
    // Keep only last 10 signals
    signalsRef.current = [signal, ...signalsRef.current].slice(0, 10);
    setTradingSignals([...signalsRef.current]);
    setLastUpdate(new Date().toISOString());
  }, []);

  // Connect to WebSocket
  const connect = useCallback(() => {
    websocketService.connect();
    if (symbols && symbols.length > 0) {
      // Subscribe after a short delay to ensure connection is established
      setTimeout(() => {
        websocketService.subscribe(symbols);
      }, 500);
    }
  }, [symbols]);

  // Disconnect from WebSocket
  const disconnect = useCallback(() => {
    websocketService.disconnect();
    setConnectionStatus('disconnected');
  }, []);

  // Subscribe to additional symbols
  const subscribe = useCallback((newSymbols) => {
    websocketService.subscribe(newSymbols);
  }, []);

  // Setup event listeners
  useEffect(() => {
    const unsubscribers = [
      websocketService.on('connection_status', handleConnectionStatus),
      websocketService.on('market_update', handleMarketUpdate),
      websocketService.on('sentiment_update', handleSentimentUpdate),
      websocketService.on('trading_signal', handleTradingSignal)
    ];

    // Auto connect if enabled
    if (autoConnect) {
      connect();
    }

    // Cleanup
    return () => {
      unsubscribers.forEach(unsubscribe => unsubscribe());
      if (autoConnect) {
        disconnect();
      }
    };
  }, [autoConnect, connect, disconnect, handleConnectionStatus, handleMarketUpdate, handleSentimentUpdate, handleTradingSignal]);

  return {
    // State
    isConnected: connectionStatus === 'connected',
    connectionStatus,
    marketData,
    sentimentData,
    tradingSignals,
    lastUpdate,
    
    // Methods
    connect,
    disconnect,
    subscribe
  };
};

export default useWebSocket;
