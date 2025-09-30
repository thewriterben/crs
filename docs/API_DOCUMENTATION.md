# API Documentation

## Overview

The CRS Cryptocurrency Marketplace API provides endpoints for authentication, AI-powered market analysis, trading bot management, and cryptocurrency operations.

**Base URLs**: 
- **Core API**: `http://localhost:5000` (Development) or `https://api.yourdomain.com` (Production)
- **Phase 3 API**: `http://localhost:5006` (Development) - Advanced AI/ML, DeFi, Social Trading, Portfolio Automation

**API Versions**: 
- Core API: v1.0.0
- Phase 3 API: v3.0.0

> **💡 Note**: For complete Phase 3 API documentation with all 30+ endpoints, see [API_REFERENCE.md](API_REFERENCE.md)

---

## Table of Contents

1. [Authentication](#authentication)
2. [Health & Status](#health--status)
3. [AI & Market Intelligence](#ai--market-intelligence)
4. [Phase 3 Advanced Features](#phase-3-advanced-features)
5. [Rate Limiting](#rate-limiting)
6. [Error Handling](#error-handling)

---

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

### Register User

Create a new user account.

**Endpoint**: `POST /api/auth/register`

**Rate Limit**: 5 requests per minute

**Request Body**:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response** (201 Created):
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00Z",
    "mfa_enabled": false
  }
}
```

**Errors**:
- `400`: Invalid input (missing fields, weak password)
- `409`: Username or email already exists
- `500`: Server error

### Login

Authenticate and receive JWT tokens.

**Endpoint**: `POST /api/auth/login`

**Rate Limit**: 10 requests per minute

**Request Body**:
```json
{
  "username": "johndoe",
  "password": "SecurePass123!",
  "mfa_code": "123456"  // Optional, required if MFA enabled
}
```

**Response** (200 OK):
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

**Errors**:
- `400`: Missing credentials
- `401`: Invalid credentials or MFA code
- `429`: Too many requests (rate limit)
- `500`: Server error

### Refresh Token

Get a new access token using a refresh token.

**Endpoint**: `POST /api/auth/refresh`

**Rate Limit**: 20 requests per minute

**Headers**:
```http
Authorization: Bearer <refresh_token>
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Logout

Invalidate current tokens.

**Endpoint**: `POST /api/auth/logout`

**Headers**:
```http
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "message": "Logged out successfully"
}
```

### Get Profile

Retrieve current user profile.

**Endpoint**: `GET /api/auth/profile`

**Headers**:
```http
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z",
  "mfa_enabled": true,
  "last_login": "2024-01-20T14:25:00Z"
}
```

### Enable MFA

Enable multi-factor authentication.

**Endpoint**: `POST /api/auth/mfa/enable`

**Headers**:
```http
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "message": "MFA enabled successfully",
  "secret": "JBSWY3DPEHPK3PXP",
  "backup_codes": [
    "12345678",
    "87654321",
    "11223344"
  ]
}
```

### Get MFA QR Code

Get QR code for authenticator app setup.

**Endpoint**: `GET /api/auth/mfa/qr-code`

**Headers**:
```http
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANS..."
}
```

---

## Health & Status

### Liveness Probe

Check if the application is running.

**Endpoint**: `GET /api/health/liveness`

**Rate Limit**: None

**Response** (200 OK):
```json
{
  "status": "alive",
  "timestamp": "2024-01-20T14:30:00Z"
}
```

### Readiness Probe

Check if the application is ready to serve traffic.

**Endpoint**: `GET /api/health/readiness`

**Rate Limit**: None

**Response** (200 OK):
```json
{
  "status": "ready",
  "timestamp": "2024-01-20T14:30:00Z",
  "checks": {
    "database": "healthy",
    "redis": "healthy"
  }
}
```

**Error Response** (503 Service Unavailable):
```json
{
  "status": "not_ready",
  "timestamp": "2024-01-20T14:30:00Z",
  "checks": {
    "database": "unhealthy: connection timeout",
    "redis": "healthy"
  }
}
```

### Application Metrics

Get application performance metrics.

**Endpoint**: `GET /api/health/metrics`

**Rate Limit**: None

**Response** (200 OK):
```json
{
  "timestamp": "2024-01-20T14:30:00Z",
  "system": {
    "python_version": "3.11.0",
    "platform": "linux"
  },
  "process": {
    "memory_rss_mb": 128.5,
    "memory_percent": 2.3,
    "cpu_percent": 5.2,
    "num_threads": 4
  },
  "application": {
    "uptime_seconds": 3600
  }
}
```

### Application Info

Get application information and available endpoints.

**Endpoint**: `GET /api/health/info`

**Rate Limit**: None

**Response** (200 OK):
```json
{
  "name": "CRS Cryptocurrency Marketplace API",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": "2024-01-20T14:30:00Z",
  "endpoints": {
    "health": "/api/health/liveness",
    "readiness": "/api/health/readiness",
    "metrics": "/api/health/metrics",
    "api": "/api/ai/dashboard-data"
  }
}
```

---

## AI & Market Intelligence

### Get AI Status

Get status of AI services.

**Endpoint**: `GET /api/ai/status`

**Rate Limit**: 100 requests per minute

**Cache**: 60 seconds

**Response** (200 OK):
```json
{
  "status": "operational",
  "timestamp": "2024-01-20T14:30:00Z",
  "services": {
    "prediction_engine": "active",
    "sentiment_analysis": "active",
    "trading_bots": "active",
    "portfolio_optimization": "active"
  }
}
```

### Get Dashboard Data

Get comprehensive market intelligence and AI analysis.

**Endpoint**: `GET /api/ai/dashboard-data`

**Rate Limit**: 60 requests per minute

**Cache**: 30 seconds

**Response** (200 OK):
```json
{
  "timestamp": "2024-01-20T14:30:00Z",
  "ai_status": {
    "prediction_engine": "active",
    "sentiment_analysis": "active",
    "trading_bots": "active"
  },
  "market_intelligence": {
    "market_fear_greed": 72,
    "market_mood": "BULLISH",
    "market_sentiment": 0.58,
    "total_news_volume": 125,
    "total_social_mentions": 850
  },
  "predictions": {
    "BTC": {
      "symbol": "BTC",
      "current_price": 45000,
      "predicted_price": 47000,
      "price_change": 2000,
      "price_change_percent": 4.44,
      "confidence": 0.85,
      "recommendation": "BUY",
      "model_consensus": {
        "random_forest": 46500,
        "gradient_boost": 47200,
        "linear_regression": 47300
      }
    },
    "ETH": {
      "symbol": "ETH",
      "current_price": 2800,
      "predicted_price": 2950,
      "price_change": 150,
      "price_change_percent": 5.36,
      "confidence": 0.78,
      "recommendation": "BUY",
      "model_consensus": {
        "random_forest": 2920,
        "gradient_boost": 2960,
        "linear_regression": 2970
      }
    }
  },
  "sentiment_summary": {
    "BTC": {
      "overall_sentiment": 0.65,
      "sentiment_label": "POSITIVE",
      "sentiment_trend": "IMPROVING",
      "confidence": 0.82,
      "news_volume": 25,
      "social_mentions": 150
    },
    "ETH": {
      "overall_sentiment": 0.58,
      "sentiment_label": "POSITIVE",
      "sentiment_trend": "STABLE",
      "confidence": 0.75,
      "news_volume": 18,
      "social_mentions": 120
    }
  },
  "trading_bots": {
    "total_bots": 3,
    "active_bots": 2,
    "bots": [
      {
        "name": "BTC Momentum Bot",
        "status": "active",
        "strategy": "Momentum Strategy",
        "current_balance": 12500,
        "total_pnl": 2500,
        "total_trades": 45,
        "active_positions": 2
      },
      {
        "name": "ETH Mean Reversion Bot",
        "status": "active",
        "strategy": "Mean Reversion Strategy",
        "current_balance": 8750,
        "total_pnl": 1250,
        "total_trades": 32,
        "active_positions": 1
      }
    ]
  },
  "market_signals": [
    {
      "signal_type": "MOMENTUM_UP",
      "description": "BTC showing strong upward momentum",
      "strength": 0.85
    },
    {
      "signal_type": "HIGH_VOLUME",
      "description": "ETH experiencing increased trading volume",
      "strength": 0.72
    }
  ],
  "trending_topics": [
    {
      "topic": "AI Trading Revolution",
      "mentions": 2500,
      "sentiment": 0.75,
      "sentiment_label": "POSITIVE"
    },
    {
      "topic": "DeFi Integration",
      "mentions": 1800,
      "sentiment": 0.68,
      "sentiment_label": "POSITIVE"
    },
    {
      "topic": "Regulatory Clarity",
      "mentions": 1200,
      "sentiment": 0.45,
      "sentiment_label": "NEUTRAL"
    }
  ]
}
```

---

## Rate Limiting

The API implements rate limiting to ensure fair usage and prevent abuse.

### Default Limits

- **Global**: 200 requests per minute, 2000 requests per hour
- **Authentication**: 
  - Register: 5 per minute
  - Login: 10 per minute
  - Refresh: 20 per minute
- **AI Endpoints**: 60-100 per minute
- **Health Checks**: No limit

### Rate Limit Headers

All responses include rate limit information:

```http
X-RateLimit-Limit: 200
X-RateLimit-Remaining: 195
X-RateLimit-Reset: 1705758000
```

### Rate Limit Exceeded

When rate limit is exceeded, the API returns:

**Response** (429 Too Many Requests):
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later.",
  "retry_after": 60
}
```

---

## Error Handling

### Standard Error Response

All errors follow this format:

```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "details": {}  // Optional additional details
}
```

### HTTP Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily unavailable

### Common Errors

**Invalid JSON**:
```json
{
  "error": "Invalid JSON",
  "message": "Request body must be valid JSON"
}
```

**Missing Required Field**:
```json
{
  "error": "Missing required fields",
  "message": "Required fields: username, email, password"
}
```

**Invalid Token**:
```json
{
  "error": "Invalid token",
  "message": "Token is invalid or expired"
}
```

---

## Best Practices

### Authentication

1. **Store tokens securely**: Use httpOnly cookies or secure storage
2. **Refresh tokens proactively**: Refresh before expiration
3. **Handle token expiration**: Implement automatic retry with refresh
4. **Logout on sensitive actions**: Force re-authentication for critical operations

### API Requests

1. **Use HTTPS**: Always use HTTPS in production
2. **Handle rate limits**: Implement exponential backoff
3. **Cache responses**: Respect cache headers
4. **Validate input**: Validate data on client-side before sending
5. **Handle errors gracefully**: Display user-friendly error messages

### Example: API Request with Error Handling

```javascript
async function fetchDashboardData() {
  try {
    const response = await fetch('https://api.yourdomain.com/api/ai/dashboard-data', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.status === 401) {
      // Token expired, refresh
      await refreshToken();
      return fetchDashboardData(); // Retry
    }

    if (response.status === 429) {
      // Rate limited, wait and retry
      const retryAfter = response.headers.get('Retry-After') || 60;
      await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
      return fetchDashboardData();
    }

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data;

  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}
```

---

## Changelog

### Version 1.0.0 (2025-01-15)
- Initial API release
- Authentication endpoints
- Health check endpoints
- AI dashboard data
- Rate limiting implementation
- Comprehensive error handling

---

## Phase 3 Advanced Features

Phase 3 introduces 30+ new API endpoints for advanced cryptocurrency features. For complete documentation, see [API_REFERENCE.md](API_REFERENCE.md).

### Quick Overview

**Advanced AI/ML (4 endpoints)**
- LSTM predictions - Time series forecasting
- Transformer predictions - Pattern analysis with attention
- Ensemble predictions - Combined model predictions (94% confidence)
- BERT sentiment - NLP-based sentiment analysis

**DeFi Integration (11 endpoints)**
- DEX Aggregator - Best prices across Uniswap, PancakeSwap, SushiSwap
- Yield Farming - 5 pools with 38-68% APY
- Staking - ETH, BNB, ADA, DOT, SOL
- Liquidity Pools - AMM pool management

**Social Trading (4 endpoints)**
- Copy Trading - Follow top traders
- Trading Signals - AI-generated BUY/SELL/HOLD
- Portfolio Sharing - Browse successful portfolios
- Leaderboards - Community rankings

**Portfolio Automation (8 endpoints)**
- Auto-Rebalancing - Drift detection and orders
- Risk Management - Portfolio risk assessment
- DCA - Automated dollar-cost averaging
- Stop-Loss - Trailing stops and take-profit

### Example Usage

**Get AI Prediction**
```bash
curl -X POST http://localhost:5006/api/phase3/ai/ensemble/predict \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC", "data": [50000, 51000, 50500, 52000, 51500]}'
```

**Get DEX Quote**
```bash
curl "http://localhost:5006/api/phase3/defi/dex/quote?tokenIn=ETH&tokenOut=USDT&amountIn=1.0"
```

**Follow Top Trader**
```bash
curl -X POST http://localhost:5006/api/phase3/social/traders/follow \
  -H "Content-Type: application/json" \
  -d '{"traderId": "trader_001", "copyAmount": 5000}'
```

**Create DCA Schedule**
```bash
curl -X POST http://localhost:5006/api/phase3/portfolio/dca/create \
  -H "Content-Type: application/json" \
  -d '{"asset": "BTC", "amount": 100, "frequency": "weekly", "durationMonths": 12}'
```

### Phase 3 Resources

- **[Complete API Reference](API_REFERENCE.md)** - All 30+ endpoints with detailed examples
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Contributing to Phase 3 features
- **[Feature Guides](FEATURE_GUIDES/)** - Detailed guides for each feature category
  - [AI/ML Models](FEATURE_GUIDES/AI_ML_MODELS.md)
  - [DeFi Features](FEATURE_GUIDES/DEFI_FEATURES.md)
  - [Social Trading](FEATURE_GUIDES/SOCIAL_TRADING.md)
  - [Portfolio Automation](FEATURE_GUIDES/PORTFOLIO_AUTOMATION.md)

---

## Support

For API support or questions:
- **Documentation**: [docs.yourdomain.com](https://docs.yourdomain.com)
- **Phase 3 API Reference**: [API_REFERENCE.md](API_REFERENCE.md)
- **Email**: api-support@yourdomain.com
- **GitHub Issues**: [github.com/thewriterben/crs/issues](https://github.com/thewriterben/crs/issues)

---

**Last Updated**: September 2024  
**Core API Version**: 1.0.0  
**Phase 3 API Version**: 3.0.0 ✅
