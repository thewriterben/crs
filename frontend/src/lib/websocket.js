/**
 * WebSocket Service for Real-time Data Streaming
 * Provides connection management and event handling for live market data
 */

import { io } from 'socket.io-client';

const SOCKET_URL = typeof process !== 'undefined' && process.env?.NODE_ENV === 'production'
  ? window.location.origin
  : 'http://localhost:5000';

class WebSocketService {
  constructor() {
    this.socket = null;
    this.connected = false;
    this.listeners = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }

  /**
   * Connect to WebSocket server
   */
  connect() {
    if (this.socket && this.connected) {
      console.log('WebSocket already connected');
      return;
    }

    console.log(`Connecting to WebSocket server at ${SOCKET_URL}`);

    this.socket = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: this.maxReconnectAttempts
    });

    // Connection event handlers
    this.socket.on('connect', () => {
      console.log('✓ WebSocket connected');
      this.connected = true;
      this.reconnectAttempts = 0;
      this.notifyListeners('connection_status', { 
        status: 'connected', 
        timestamp: new Date().toISOString() 
      });
    });

    this.socket.on('disconnect', (reason) => {
      console.log('WebSocket disconnected:', reason);
      this.connected = false;
      this.notifyListeners('connection_status', { 
        status: 'disconnected', 
        reason,
        timestamp: new Date().toISOString() 
      });
    });

    this.socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
      this.reconnectAttempts++;
      
      if (this.reconnectAttempts >= this.maxReconnectAttempts) {
        console.warn('Max reconnection attempts reached');
        this.notifyListeners('connection_status', { 
          status: 'error', 
          error: 'Connection failed',
          timestamp: new Date().toISOString() 
        });
      }
    });

    // Data event handlers
    this.socket.on('market_update', (data) => {
      this.notifyListeners('market_update', data);
    });

    this.socket.on('sentiment_update', (data) => {
      this.notifyListeners('sentiment_update', data);
    });

    this.socket.on('trading_signal', (data) => {
      this.notifyListeners('trading_signal', data);
    });

    this.socket.on('connection_status', (data) => {
      console.log('Connection status update:', data);
      this.notifyListeners('connection_status', data);
    });

    this.socket.on('subscription_confirmed', (data) => {
      console.log('Subscription confirmed:', data);
      this.notifyListeners('subscription_confirmed', data);
    });
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect() {
    if (this.socket) {
      console.log('Disconnecting WebSocket');
      this.socket.disconnect();
      this.socket = null;
      this.connected = false;
      this.listeners.clear();
    }
  }

  /**
   * Subscribe to specific market symbols
   */
  subscribe(symbols) {
    if (this.socket && this.connected) {
      console.log('Subscribing to symbols:', symbols);
      this.socket.emit('subscribe', { symbols });
    } else {
      console.warn('Cannot subscribe: WebSocket not connected');
    }
  }

  /**
   * Add event listener
   */
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);

    // Return unsubscribe function
    return () => this.off(event, callback);
  }

  /**
   * Remove event listener
   */
  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
      if (callbacks.length === 0) {
        this.listeners.delete(event);
      }
    }
  }

  /**
   * Notify all listeners for an event
   */
  notifyListeners(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in ${event} listener:`, error);
        }
      });
    }
  }

  /**
   * Check if connected
   */
  isConnected() {
    return this.connected;
  }
}

// Create singleton instance
const websocketService = new WebSocketService();

export default websocketService;
