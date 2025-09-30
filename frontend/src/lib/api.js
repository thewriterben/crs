// API utility functions for backend integration
const API_BASE_URL = typeof process !== 'undefined' && process.env?.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://localhost:5000/api';

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

const apiRequest = async (endpoint, options = {}) => {
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
    
    return await response.json();
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

export default api;