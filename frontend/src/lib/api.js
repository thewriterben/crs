// API utility functions for backend integration
const API_BASE_URL = import.meta.env.PROD
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

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
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
      ...getAuthHeaders(),
    },
  };

  try {
    const response = await fetch(url, { ...defaultOptions, ...options, headers: { ...defaultOptions.headers, ...options.headers } });
    
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
    },
    '/phase3/ai/lstm/predict': {
      symbol: 'BTC',
      predictions: [{ timestamp: Date.now(), price: 45000, confidence: 0.82 }],
      confidence: 0.82,
      trend: 'bullish',
      model: 'LSTM'
    },
    '/phase3/ai/transformer/predict': {
      symbol: 'BTC',
      predictions: [{ timestamp: Date.now(), price: 45200, confidence: 0.79 }],
      confidence: 0.79,
      trend: 'bullish',
      model: 'Transformer'
    },
    '/phase3/ai/ensemble/predict': {
      symbol: 'BTC',
      predictions: [{ timestamp: Date.now(), price: 45100, confidence: 0.85 }],
      confidence: 0.85,
      trend: 'bullish',
      model: 'Ensemble'
    },
    '/phase3/ai/sentiment/analyze': {
      symbol: 'BTC',
      sentiment_score: 0.68,
      sentiment_label: 'BULLISH',
      confidence: 0.76,
      sources: { news: 0.72, social: 0.64, reddit: 0.68 }
    },
    '/phase3/defi/dex/quote': {
      tokenIn: 'ETH',
      tokenOut: 'USDT',
      amountIn: 1.0,
      quotes: [
        { exchange: 'Uniswap', amountOut: 2796.25, priceImpact: 0.001, fee: 0.003 },
        { exchange: 'SushiSwap', amountOut: 2793.10, priceImpact: 0.002, fee: 0.003 },
        { exchange: 'PancakeSwap', amountOut: 2790.50, priceImpact: 0.0015, fee: 0.0025 }
      ],
      bestQuote: { exchange: 'Uniswap', amountOut: 2796.25 }
    },
    '/phase3/defi/farming/opportunities': {
      pools: [
        { id: 'pool_1', protocol: 'Raydium', pair: 'SOL-USDC', apy: 68.5, tvl: 12500000 },
        { id: 'pool_2', protocol: 'Curve', pair: 'ETH-USDT', apy: 45.2, tvl: 45000000 },
        { id: 'pool_3', protocol: 'Yearn', pair: 'BTC-ETH', apy: 38.1, tvl: 28000000 }
      ]
    },
    '/phase3/defi/farming/positions': { positions: [] },
    '/phase3/defi/staking/options': {
      options: [
        { token: 'ETH', minAmount: 0.1, apy: 5.5, lockPeriod: 0, protocol: 'Ethereum' },
        { token: 'BNB', minAmount: 1, apy: 8.2, lockPeriod: 30, protocol: 'BNB Chain' },
        { token: 'SOL', minAmount: 1, apy: 12.0, lockPeriod: 0, protocol: 'Solana' }
      ]
    },
    '/phase3/defi/staking/positions': { positions: [] },
    '/phase3/defi/liquidity/pools': {
      pools: [
        { id: 'lp_1', name: 'ETH/USDT', protocol: 'Uniswap V3', fee: 0.003, tvl: 125000000 },
        { id: 'lp_2', name: 'BTC/ETH', protocol: 'SushiSwap', fee: 0.003, tvl: 87000000 }
      ]
    },
    '/phase3/defi/liquidity/positions': { positions: [] },
    '/phase3/social/traders/top': {
      traders: [
        { id: 'trader_001', username: 'CryptoMaster', winRate: 0.72, avgReturn: 0.18, followers: 2547, verified: true },
        { id: 'trader_002', username: 'BullRunner', winRate: 0.68, avgReturn: 0.14, followers: 1832, verified: true },
        { id: 'trader_003', username: 'AlphaTrader', winRate: 0.65, avgReturn: 0.11, followers: 1205, verified: false }
      ]
    },
    '/phase3/social/signals': {
      signals: [
        { id: 'sig_1', symbol: 'BTC', action: 'BUY', strength: 0.74, confidence: 0.72, timestamp: Date.now() },
        { id: 'sig_2', symbol: 'ETH', action: 'HOLD', strength: 0.55, confidence: 0.65, timestamp: Date.now() },
        { id: 'sig_3', symbol: 'SOL', action: 'BUY', strength: 0.82, confidence: 0.78, timestamp: Date.now() }
      ]
    },
    '/phase3/social/portfolios/featured': {
      portfolios: [
        { id: 'pf_1', name: 'DeFi Focus', owner: 'CryptoMaster', yearlyReturn: 0.452, riskLevel: 'high' },
        { id: 'pf_2', name: 'Blue Chip Crypto', owner: 'BullRunner', yearlyReturn: 0.287, riskLevel: 'medium' }
      ]
    },
    '/phase3/portfolio/stop-loss/active': { stops: [] },
    '/phase3/portfolio/dca/schedules': { schedules: [] },
  };

  return mockData[endpoint] || { error: 'No mock data available', endpoint };
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

  // AI endpoints (legacy)
  ai: {
    getDashboardData: () => apiRequest('/ai/dashboard-data'),
    getStatus: () => apiRequest('/ai/status'),
    getPredictions: (symbol) => apiRequest(`/ai/predictions/${symbol}`),
    getSentiment: (symbol) => apiRequest(`/ai/sentiment/${symbol}`),
    getTradingSignals: () => apiRequest('/ai/trading-signals'),
  },

  // Phase 3 AI/ML endpoints
  phase3: {
    ai: {
      lstmPredict: (symbol, periods = 7) =>
        apiRequest('/phase3/ai/lstm/predict', {
          method: 'POST',
          body: JSON.stringify({ symbol, periods })
        }),
      transformerPredict: (symbol, periods = 7) =>
        apiRequest('/phase3/ai/transformer/predict', {
          method: 'POST',
          body: JSON.stringify({ symbol, periods })
        }),
      ensemblePredict: (symbol, periods = 7) =>
        apiRequest('/phase3/ai/ensemble/predict', {
          method: 'POST',
          body: JSON.stringify({ symbol, periods })
        }),
      analyzeSentiment: (symbol, sources = ['news', 'social']) =>
        apiRequest('/phase3/ai/sentiment/analyze', {
          method: 'POST',
          body: JSON.stringify({ symbol, sources })
        }),
    },

    // Phase 3 DeFi endpoints
    defi: {
      getDexQuote: (tokenIn, tokenOut, amountIn) =>
        apiRequest(`/phase3/defi/dex/quote?tokenIn=${tokenIn}&tokenOut=${tokenOut}&amountIn=${amountIn}`),
      executeSwap: (tokenIn, tokenOut, amountIn, slippage = 0.005) =>
        apiRequest('/phase3/defi/dex/swap', {
          method: 'POST',
          body: JSON.stringify({ tokenIn, tokenOut, amountIn, slippage })
        }),
      getFarmingOpportunities: () => apiRequest('/phase3/defi/farming/opportunities'),
      depositToFarm: (poolId, amount) =>
        apiRequest('/phase3/defi/farming/deposit', {
          method: 'POST',
          body: JSON.stringify({ poolId, amount })
        }),
      getFarmingPositions: () => apiRequest('/phase3/defi/farming/positions'),
      getStakingOptions: () => apiRequest('/phase3/defi/staking/options'),
      stakeTokens: (token, amount, lockPeriod = 0) =>
        apiRequest('/phase3/defi/staking/stake', {
          method: 'POST',
          body: JSON.stringify({ token, amount, lockPeriod })
        }),
      getStakingPositions: () => apiRequest('/phase3/defi/staking/positions'),
      getLiquidityPools: () => apiRequest('/phase3/defi/liquidity/pools'),
      addLiquidity: (poolId, amounts) =>
        apiRequest('/phase3/defi/liquidity/add', {
          method: 'POST',
          body: JSON.stringify({ poolId, amounts })
        }),
      getLiquidityPositions: () => apiRequest('/phase3/defi/liquidity/positions'),
    },

    // Phase 3 Social Trading endpoints
    social: {
      getTopTraders: (limit = 10) => apiRequest(`/phase3/social/traders/top?limit=${limit}`),
      followTrader: (traderId, copyAmount) =>
        apiRequest('/phase3/social/traders/follow', {
          method: 'POST',
          body: JSON.stringify({ traderId, copyAmount })
        }),
      getSignals: () => apiRequest('/phase3/social/signals'),
      getFeaturedPortfolios: () => apiRequest('/phase3/social/portfolios/featured'),
    },

    // Phase 3 Portfolio Automation endpoints
    portfolio: {
      analyzeRebalance: (currentAllocation, targetAllocation) =>
        apiRequest('/phase3/portfolio/rebalance/analyze', {
          method: 'POST',
          body: JSON.stringify({ currentAllocation, targetAllocation })
        }),
      generateRebalanceOrders: (currentAllocation, targetAllocation, totalValue) =>
        apiRequest('/phase3/portfolio/rebalance/orders', {
          method: 'POST',
          body: JSON.stringify({ currentAllocation, targetAllocation, totalValue })
        }),
      assessRisk: (portfolio) =>
        apiRequest('/phase3/portfolio/risk/assess', {
          method: 'POST',
          body: JSON.stringify({ portfolio })
        }),
      calculatePositionSize: (capital, riskPercent, entryPrice, stopLoss) =>
        apiRequest('/phase3/portfolio/position-size', {
          method: 'POST',
          body: JSON.stringify({ capital, riskPercent, entryPrice, stopLoss })
        }),
      createDCA: (asset, amount, frequency, periods) =>
        apiRequest('/phase3/portfolio/dca/create', {
          method: 'POST',
          body: JSON.stringify({ asset, amount, frequency, periods })
        }),
      getDCASchedules: () => apiRequest('/phase3/portfolio/dca/schedules'),
      createStopLoss: (asset, entryPrice, stopPrice, trailingPercent) =>
        apiRequest('/phase3/portfolio/stop-loss/create', {
          method: 'POST',
          body: JSON.stringify({ asset, entryPrice, stopPrice, trailingPercent })
        }),
      getActiveStopLosses: () => apiRequest('/phase3/portfolio/stop-loss/active'),
    },
  },

  // DeFi endpoints (legacy)
  defi: {
    getLiquidityPools: () => apiRequest('/defi/liquidity-pools'),
    getYieldFarming: () => apiRequest('/defi/yield-farming'),
    getStakingOptions: () => apiRequest('/defi/staking'),
    getDexRates: (fromToken, toToken, amount) =>
      apiRequest(`/defi/dex/rates?from=${fromToken}&to=${toToken}&amount=${amount}`),
    executeSwap: (swapData) =>
      apiRequest('/defi/dex/swap', { method: 'POST', body: JSON.stringify(swapData) }),
  },

  // Social trading endpoints (legacy)
  social: {
    getLeaderboard: () => apiRequest('/social/leaderboard'),
    getSignals: () => apiRequest('/social/signals'),
    getTraderProfile: (traderId) => apiRequest(`/social/traders/${traderId}`),
    copyTrade: (traderId) =>
      apiRequest('/social/copy-trade', { method: 'POST', body: JSON.stringify({ traderId }) }),
    sharePortfolio: (portfolioData) =>
      apiRequest('/social/share', { method: 'POST', body: JSON.stringify(portfolioData) }),
  },

  // Portfolio endpoints (legacy)
  portfolio: {
    getSummary: (token) => apiRequest('/portfolio/summary', { headers: { Authorization: `Bearer ${token}` } }),
    getHoldings: (token) => apiRequest('/portfolio/holdings', { headers: { Authorization: `Bearer ${token}` } }),
    rebalance: (token, strategy) =>
      apiRequest('/portfolio/rebalance', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: JSON.stringify({ strategy }),
      }),
    setStopLoss: (token, params) =>
      apiRequest('/portfolio/stop-loss', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: JSON.stringify(params),
      }),
    setupDCA: (token, params) =>
      apiRequest('/portfolio/dca', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: JSON.stringify(params),
      }),
  },

  // CFV payment endpoints
  cfv: {
    getSupportedCurrencies: () => apiRequest('/cfv/currencies'),
    createPayment: (paymentData) =>
      apiRequest('/cfv/payments', { method: 'POST', body: JSON.stringify(paymentData) }),
    getPaymentStatus: (paymentId) => apiRequest(`/cfv/payments/${paymentId}`),
    getDiscounts: () => apiRequest('/cfv/discounts'),
  },
};

// Authentication API
export const authApi = {
  register: async (username, email, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, email, password })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw { response: { data: error } };
    }
    
    return await response.json();
  },

  login: async (username, password, mfaCode = null) => {
    const body = { username, password };
    if (mfaCode) {
      body.mfa_code = mfaCode;
    }

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      if (data.mfa_required) {
        return data;
      }
      throw { response: { data } };
    }
    
    return data;
  },

  logout: async (token) => {
    const response = await fetch(`${API_BASE_URL}/auth/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw { response: { data: error } };
    }
    
    return await response.json();
  },

  verifyToken: async (token) => {
    const response = await fetch(`${API_BASE_URL}/auth/verify`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw { response: { data: error } };
    }
    
    return await response.json();
  },

  refreshToken: async (refreshToken) => {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${refreshToken}`
      }
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw { response: { data: error } };
    }
    
    return await response.json();
  },

  getProfile: async (token) => {
    const response = await fetch(`${API_BASE_URL}/auth/profile`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw { response: { data: error } };
    }
    
    return await response.json();
  },

  updateProfile: async (token, data) => {
    const response = await fetch(`${API_BASE_URL}/auth/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw { response: { data: error } };
    }
    
    return await response.json();
  },

  changePassword: async (token, currentPassword, newPassword) => {
    const response = await fetch(`${API_BASE_URL}/auth/change-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw { response: { data: error } };
    }
    
    return await response.json();
  },

  enableMFA: async (token) => {
    const response = await fetch(`${API_BASE_URL}/auth/mfa/enable`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw { response: { data: error } };
    }
    
    return await response.json();
  },

  disableMFA: async (token, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/mfa/disable`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ password })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw { response: { data: error } };
    }
    
    return await response.json();
  }
};

