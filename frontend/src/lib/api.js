// API utility functions for backend integration
const API_BASE_URL = typeof process !== 'undefined' && process.env?.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://localhost:5000/api';

// Simple in-memory cache
const cache = new Map();
const CACHE_DURATION = 30000; // 30 seconds

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

const getCacheKey = (endpoint, options) => {
  return `${endpoint}-${JSON.stringify(options)}`;
};

const getCachedData = (key) => {
  const cached = cache.get(key);
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  return null;
};

const setCachedData = (key, data) => {
  cache.set(key, {
    data,
    timestamp: Date.now()
  });
  
  // Clean up old cache entries (keep only last 50)
  if (cache.size > 50) {
    const firstKey = cache.keys().next().value;
    cache.delete(firstKey);
  }
};

const apiRequest = async (endpoint, options = {}) => {
  // Check cache first for GET requests
  if (!options.method || options.method === 'GET') {
    const cacheKey = getCacheKey(endpoint, options);
    const cachedData = getCachedData(cacheKey);
    if (cachedData) {
      return cachedData;
    }
  }

  const url = `${API_BASE_URL}${endpoint}`;
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  try {
    const response = await fetch(url, { ...defaultOptions, ...options });
    
    if (!response.ok) {
      throw new ApiError(`HTTP error! status: ${response.status}`, response.status);
    }
    
    const data = await response.json();
    
    // Cache GET requests
    if (!options.method || options.method === 'GET') {
      const cacheKey = getCacheKey(endpoint, options);
      setCachedData(cacheKey, data);
    }
    
    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    // For network errors or other fetch failures, return mock data
    console.warn(`API request failed for ${endpoint}, using mock data:`, error.message);
    return getMockData(endpoint);
  }
};

// Mock data fallback for when backend is not available
const getMockData = (endpoint) => {
  const mockData = {
    '/marketplace/products': {
      products: [
        {
          id: 1,
          name: 'AI Trading Bot Premium',
          price: 0.001,
          currency: 'BTC',
          description: 'Advanced AI-powered trading bot with portfolio optimization',
          category: 'Trading Tools',
          rating: 4.8,
          features: ['24/7 Trading', 'Portfolio Optimization', 'Risk Management', 'Performance Analytics'],
          popular: true
        },
        {
          id: 2,
          name: 'Market Analysis Pro',
          price: 0.0005,
          currency: 'BTC',
          description: 'Real-time market sentiment analysis and predictions',
          category: 'Analytics',
          rating: 4.6,
          features: ['Sentiment Analysis', 'Price Predictions', 'News Integration', 'Social Media Monitoring'],
          popular: false
        }
      ]
    },
    '/marketplace/cart': {
      cart: [],
      total: 0,
      currency: 'BTC'
    },
    '/ai/dashboard-data': {
      ai_status: {
        prediction_engine: 'active',
        sentiment_analysis: 'active',
        trading_bots: 'active'
      },
      market_intelligence: {
        market_fear_greed: 72,
        market_mood: 'BULLISH',
        market_sentiment: 0.58
      }
    }
  };

  return mockData[endpoint] || { error: 'No mock data available' };
};

// API functions
export const api = {
  // Marketplace endpoints
  marketplace: {
    getProducts: () => apiRequest('/marketplace/products'),
    getCart: () => apiRequest('/marketplace/cart'),
    addToCart: (productId, quantity = 1) => 
      apiRequest('/marketplace/cart', {
        method: 'POST',
        body: JSON.stringify({ productId, quantity })
      }),
    removeFromCart: (productId) =>
      apiRequest('/marketplace/cart', {
        method: 'DELETE',
        body: JSON.stringify({ productId })
      }),
    updateCartItem: (productId, quantity) =>
      apiRequest('/marketplace/cart', {
        method: 'PUT',
        body: JSON.stringify({ productId, quantity })
      }),
    checkout: (paymentData) =>
      apiRequest('/marketplace/checkout', {
        method: 'POST',
        body: JSON.stringify(paymentData)
      })
  },

  // AI endpoints
  ai: {
    getDashboardData: () => apiRequest('/ai/dashboard-data'),
    getStatus: () => apiRequest('/ai/status')
  }
};

export default api;