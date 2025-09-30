# API Reference Guide

Complete API reference for the CRS Cryptocurrency Marketplace, including all Phase 3 advanced features.

**Base URL**: `http://localhost:5006` (Phase 3 API)  
**API Version**: 3.0.0  
**Last Updated**: September 30, 2024

---

## Table of Contents

- [Authentication](#authentication)
- [Phase 3 Advanced Features](#phase-3-advanced-features)
  - [Advanced AI/ML Models](#advanced-aiml-models)
  - [DeFi Integration](#defi-integration)
  - [Social Trading](#social-trading)
  - [Portfolio Automation](#portfolio-automation)
- [Status & Health](#status--health)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

---

## Authentication

Phase 3 API endpoints follow the same authentication pattern as the main API. Include JWT token in the Authorization header for protected endpoints.

```http
Authorization: Bearer <your_jwt_token>
```

For authentication endpoints, see [authentication-api.md](authentication-api.md).

---

## Phase 3 Advanced Features

### Advanced AI/ML Models

#### 1. LSTM Price Prediction

Generates price predictions using Long Short-Term Memory neural network.

**Endpoint**: `POST /api/phase3/ai/lstm/predict`

**Request Body**:
```json
{
  "symbol": "BTC",
  "data": [50000, 51000, 50500, 52000, 51500]
}
```

**Parameters**:
- `symbol` (string, required): Cryptocurrency symbol (e.g., "BTC", "ETH")
- `data` (array, required): Historical price data (minimum 60 data points for optimal results)

**Response** (200 OK):
```json
{
  "predictions": [52300.45, 52800.23, 53100.67, 53450.89, 53900.12],
  "confidence": 0.87,
  "model": "LSTM",
  "timestamp": "2024-09-30T12:00:00Z"
}
```

**Features**:
- 60-period lookback window
- Captures long-term dependencies
- Suitable for trend analysis

---

#### 2. Transformer Price Prediction

Uses transformer architecture with multi-head attention for market analysis.

**Endpoint**: `POST /api/phase3/ai/transformer/predict`

**Request Body**:
```json
{
  "symbol": "ETH",
  "data": [3000, 3050, 3025, 3100, 3080]
}
```

**Response** (200 OK):
```json
{
  "predictions": [3120.34, 3145.78, 3170.23, 3195.67, 3220.45],
  "confidence": 0.92,
  "model": "Transformer",
  "attention_weights": [0.15, 0.20, 0.25, 0.22, 0.18],
  "timestamp": "2024-09-30T12:00:00Z"
}
```

**Features**:
- 8-head attention mechanism
- Parallel processing of sequences
- Excellent for pattern recognition

---

#### 3. Ensemble Model Prediction

Combines multiple models for robust predictions.

**Endpoint**: `POST /api/phase3/ai/ensemble/predict`

**Request Body**:
```json
{
  "symbol": "BTC",
  "data": [50000, 51000, 50500, 52000, 51500]
}
```

**Response** (200 OK):
```json
{
  "predictions": [52450.67, 52900.34, 53300.89, 53700.12, 54100.56],
  "confidence": 0.94,
  "model": "Ensemble",
  "component_predictions": {
    "random_forest": [52400.0, 52850.0, 53250.0, 53650.0, 54050.0],
    "gradient_boosting": [52500.0, 52950.0, 53350.0, 53750.0, 54150.0],
    "svm": [52450.0, 52900.0, 53300.0, 53700.0, 54100.0],
    "linear_regression": [52430.0, 52880.0, 53280.0, 53680.0, 54080.0],
    "lstm": [52470.0, 52920.0, 53320.0, 53720.0, 54120.0]
  },
  "model_weights": {
    "random_forest": 0.20,
    "gradient_boosting": 0.25,
    "svm": 0.15,
    "linear_regression": 0.15,
    "lstm": 0.25
  },
  "timestamp": "2024-09-30T12:00:00Z"
}
```

**Features**:
- Combines 5 different models
- Weighted ensemble approach
- Highest accuracy and reliability

---

#### 4. BERT Sentiment Analysis

Analyzes sentiment from news articles and social media using BERT.

**Endpoint**: `POST /api/phase3/ai/sentiment/analyze`

**Request Body**:
```json
{
  "text": "Bitcoin surges to new all-time high as institutional adoption grows"
}
```

**Response** (200 OK):
```json
{
  "sentiment": "positive",
  "score": 0.89,
  "confidence": 0.95,
  "model": "BERT",
  "key_phrases": ["surges", "all-time high", "institutional adoption"],
  "entity_sentiment": {
    "Bitcoin": 0.92
  },
  "timestamp": "2024-09-30T12:00:00Z"
}
```

**Sentiment Values**:
- `positive`: Score > 0.3
- `neutral`: Score between -0.3 and 0.3
- `negative`: Score < -0.3

---

### DeFi Integration

#### 1. Get DEX Quote

Get token swap quotes from multiple decentralized exchanges.

**Endpoint**: `GET /api/phase3/defi/dex/quote`

**Query Parameters**:
- `tokenIn` (string, required): Input token symbol (e.g., "ETH")
- `tokenOut` (string, required): Output token symbol (e.g., "USDT")
- `amountIn` (float, required): Input amount

**Example**:
```bash
GET /api/phase3/defi/dex/quote?tokenIn=ETH&tokenOut=USDT&amountIn=1.0
```

**Response** (200 OK):
```json
{
  "quotes": [
    {
      "dex": "Uniswap",
      "amountOut": 3020.45,
      "priceImpact": 0.12,
      "fee": 0.3,
      "gasEstimate": 150000
    },
    {
      "dex": "SushiSwap",
      "amountOut": 3018.23,
      "priceImpact": 0.15,
      "fee": 0.3,
      "gasEstimate": 145000
    },
    {
      "dex": "PancakeSwap",
      "amountOut": 3022.67,
      "priceImpact": 0.10,
      "fee": 0.25,
      "gasEstimate": 120000
    }
  ],
  "bestQuote": {
    "dex": "PancakeSwap",
    "amountOut": 3022.67,
    "savings": 2.22
  },
  "timestamp": "2024-09-30T12:00:00Z"
}
```

---

#### 2. Execute DEX Swap

Execute a token swap on the selected DEX.

**Endpoint**: `POST /api/phase3/defi/dex/swap`

**Request Body**:
```json
{
  "tokenIn": "ETH",
  "tokenOut": "USDT",
  "amountIn": 1.0,
  "dex": "PancakeSwap",
  "slippageTolerance": 0.5
}
```

**Parameters**:
- `tokenIn` (string, required): Input token symbol
- `tokenOut` (string, required): Output token symbol
- `amountIn` (float, required): Input amount
- `dex` (string, required): DEX to use ("Uniswap", "SushiSwap", "PancakeSwap")
- `slippageTolerance` (float, optional): Max slippage tolerance in % (default: 0.5)

**Response** (200 OK):
```json
{
  "transactionId": "tx_abc123def456",
  "status": "completed",
  "amountIn": 1.0,
  "amountOut": 3020.45,
  "effectivePrice": 3020.45,
  "fee": 9.06,
  "gasUsed": 145000,
  "timestamp": "2024-09-30T12:00:00Z"
}
```

---

#### 3. Get Yield Farming Opportunities

Browse available yield farming opportunities across protocols.

**Endpoint**: `GET /api/phase3/defi/farming/opportunities`

**Query Parameters**:
- `minApy` (float, optional): Minimum APY filter (e.g., 40)
- `protocol` (string, optional): Filter by protocol name

**Example**:
```bash
GET /api/phase3/defi/farming/opportunities?minApy=40
```

**Response** (200 OK):
```json
{
  "opportunities": [
    {
      "poolId": "farm_001",
      "protocol": "Compound",
      "asset": "USDC",
      "apy": 45.2,
      "tvl": 1250000000,
      "riskLevel": "low",
      "lockPeriod": null,
      "features": ["auto-compound", "instant-withdraw"]
    },
    {
      "poolId": "farm_002",
      "protocol": "Curve",
      "asset": "3CRV",
      "apy": 52.8,
      "tvl": 850000000,
      "riskLevel": "low",
      "lockPeriod": null,
      "features": ["boosted-rewards", "stable-yield"]
    },
    {
      "poolId": "farm_005",
      "protocol": "Convex",
      "asset": "CVX",
      "apy": 68.9,
      "tvl": 450000000,
      "riskLevel": "medium",
      "lockPeriod": "30 days",
      "features": ["boosted-rewards", "governance-tokens"]
    }
  ],
  "totalOpportunities": 5
}
```

---

#### 4. Deposit to Yield Farm

Deposit funds to a yield farming pool.

**Endpoint**: `POST /api/phase3/defi/farming/deposit`

**Request Body**:
```json
{
  "poolId": "farm_001",
  "amount": 10000.0
}
```

**Response** (200 OK):
```json
{
  "positionId": "pos_xyz789",
  "poolId": "farm_001",
  "protocol": "Compound",
  "asset": "USDC",
  "depositAmount": 10000.0,
  "startTime": "2024-09-30T12:00:00Z",
  "currentApy": 45.2,
  "estimatedDailyYield": 12.38,
  "status": "active"
}
```

---

#### 5. Get Farming Positions

View all active yield farming positions.

**Endpoint**: `GET /api/phase3/defi/farming/positions`

**Response** (200 OK):
```json
{
  "positions": [
    {
      "positionId": "pos_xyz789",
      "poolId": "farm_001",
      "protocol": "Compound",
      "asset": "USDC",
      "depositAmount": 10000.0,
      "currentValue": 10350.25,
      "earned": 350.25,
      "apy": 45.2,
      "daysActive": 28,
      "status": "active"
    },
    {
      "positionId": "pos_abc456",
      "poolId": "farm_002",
      "protocol": "Curve",
      "asset": "3CRV",
      "depositAmount": 5000.0,
      "currentValue": 5180.45,
      "earned": 180.45,
      "apy": 52.8,
      "daysActive": 12,
      "status": "active"
    }
  ],
  "totalDeposited": 15000.0,
  "totalValue": 15530.70,
  "totalEarned": 530.70,
  "averageApy": 47.9
}
```

---

#### 6. Get Staking Options

Get available staking options for various cryptocurrencies.

**Endpoint**: `GET /api/phase3/defi/staking/options`

**Response** (200 OK):
```json
{
  "options": [
    {
      "token": "ETH",
      "minAmount": 0.1,
      "flexible": {
        "apy": 4.2,
        "lockPeriod": null,
        "features": ["instant-unstake", "auto-compound"]
      },
      "locked": {
        "30days": {"apy": 5.5, "penalty": 0.5},
        "90days": {"apy": 6.8, "penalty": 1.0},
        "180days": {"apy": 8.2, "penalty": 2.0}
      }
    },
    {
      "token": "ADA",
      "minAmount": 10,
      "flexible": {
        "apy": 5.1,
        "lockPeriod": null,
        "features": ["instant-unstake"]
      },
      "locked": {
        "30days": {"apy": 6.5, "penalty": 0.3},
        "90days": {"apy": 8.0, "penalty": 0.8}
      }
    }
  ],
  "totalOptions": 5
}
```

---

#### 7. Stake Tokens

Stake tokens to earn rewards.

**Endpoint**: `POST /api/phase3/defi/staking/stake`

**Request Body**:
```json
{
  "token": "ETH",
  "amount": 5.0,
  "lockPeriod": "90days"
}
```

**Parameters**:
- `token` (string, required): Token to stake
- `amount` (float, required): Amount to stake
- `lockPeriod` (string, optional): Lock period ("flexible", "30days", "90days", "180days")

**Response** (200 OK):
```json
{
  "stakeId": "stake_def456",
  "token": "ETH",
  "amount": 5.0,
  "apy": 6.8,
  "lockPeriod": "90days",
  "startTime": "2024-09-30T12:00:00Z",
  "unlockTime": "2024-12-29T12:00:00Z",
  "estimatedDailyReward": 0.000931,
  "status": "active"
}
```

---

#### 8. Unstake Tokens

Unstake tokens (with penalty if unlocking early).

**Endpoint**: `POST /api/phase3/defi/staking/unstake`

**Request Body**:
```json
{
  "stakeId": "stake_def456"
}
```

**Response** (200 OK):
```json
{
  "stakeId": "stake_def456",
  "amountUnstaked": 5.0,
  "rewardsEarned": 0.084,
  "totalReturned": 5.084,
  "penalty": 0.0,
  "status": "completed",
  "timestamp": "2024-12-29T12:00:00Z"
}
```

---

#### 9. Get Staking Positions

View all active staking positions.

**Endpoint**: `GET /api/phase3/defi/staking/positions`

**Response** (200 OK):
```json
{
  "positions": [
    {
      "stakeId": "stake_def456",
      "token": "ETH",
      "amount": 5.0,
      "apy": 6.8,
      "lockPeriod": "90days",
      "daysRemaining": 62,
      "earned": 0.028,
      "estimatedTotal": 0.084,
      "status": "active"
    },
    {
      "stakeId": "stake_ghi789",
      "token": "ADA",
      "amount": 1000.0,
      "apy": 5.1,
      "lockPeriod": "flexible",
      "daysRemaining": 0,
      "earned": 2.3,
      "estimatedTotal": 2.3,
      "status": "active"
    }
  ],
  "totalStaked": 6000.0,
  "totalEarned": 2.328,
  "averageApy": 6.2
}
```

---

#### 10. Add Liquidity to Pool

Add liquidity to an AMM pool.

**Endpoint**: `POST /api/phase3/defi/liquidity/add`

**Request Body**:
```json
{
  "pool": "ETH-USDT",
  "token0Amount": 1.0,
  "token1Amount": 3000.0
}
```

**Response** (200 OK):
```json
{
  "positionId": "lp_jkl012",
  "pool": "ETH-USDT",
  "lpTokens": 54.77,
  "share": 0.0012,
  "token0Deposited": 1.0,
  "token1Deposited": 3000.0,
  "currentValue": 6000.0,
  "feeApy": 12.5,
  "timestamp": "2024-09-30T12:00:00Z"
}
```

---

#### 11. Get Liquidity Positions

View all liquidity pool positions.

**Endpoint**: `GET /api/phase3/defi/liquidity/positions`

**Response** (200 OK):
```json
{
  "positions": [
    {
      "positionId": "lp_jkl012",
      "pool": "ETH-USDT",
      "lpTokens": 54.77,
      "share": 0.0012,
      "initialValue": 6000.0,
      "currentValue": 6180.25,
      "feesEarned": 45.30,
      "totalReturn": 225.55,
      "returnPercent": 3.76,
      "daysActive": 15,
      "impermanentLoss": -0.82
    }
  ],
  "totalValue": 6180.25,
  "totalFeesEarned": 45.30
}
```

---

### Social Trading

#### 1. Get Top Traders

Get list of top-performing traders for copy trading.

**Endpoint**: `GET /api/phase3/social/traders/top`

**Query Parameters**:
- `limit` (int, optional): Number of traders to return (default: 10)
- `sortBy` (string, optional): Sort criteria ("winRate", "totalReturn", "followers")

**Example**:
```bash
GET /api/phase3/social/traders/top?limit=5&sortBy=winRate
```

**Response** (200 OK):
```json
{
  "traders": [
    {
      "traderId": "trader_001",
      "username": "CryptoMaster",
      "winRate": 72.5,
      "totalReturn": 145.3,
      "followers": 1250,
      "totalTrades": 487,
      "avgHoldTime": "3.2 days",
      "specialties": ["BTC", "ETH", "DeFi"],
      "verified": true,
      "riskLevel": "medium",
      "monthlyReturn": 12.4
    },
    {
      "traderId": "trader_002",
      "username": "DeFiWhale",
      "winRate": 68.9,
      "totalReturn": 189.7,
      "followers": 890,
      "totalTrades": 312,
      "avgHoldTime": "7.5 days",
      "specialties": ["DeFi", "Yield"],
      "verified": true,
      "riskLevel": "low",
      "monthlyReturn": 15.8
    }
  ],
  "totalTraders": 5
}
```

---

#### 2. Follow Trader

Follow a trader to automatically copy their trades.

**Endpoint**: `POST /api/phase3/social/traders/follow`

**Request Body**:
```json
{
  "traderId": "trader_001",
  "copyAmount": 5000.0,
  "copyPercentage": 100,
  "stopLoss": -10.0,
  "takeProfit": 25.0
}
```

**Parameters**:
- `traderId` (string, required): ID of trader to follow
- `copyAmount` (float, required): Total amount to allocate for copying
- `copyPercentage` (float, optional): Percentage of trader's positions to copy (1-100, default: 100)
- `stopLoss` (float, optional): Stop loss percentage
- `takeProfit` (float, optional): Take profit percentage

**Response** (200 OK):
```json
{
  "followId": "follow_mno345",
  "traderId": "trader_001",
  "username": "CryptoMaster",
  "status": "active",
  "copyAmount": 5000.0,
  "copyPercentage": 100,
  "stopLoss": -10.0,
  "takeProfit": 25.0,
  "startTime": "2024-09-30T12:00:00Z",
  "openPositions": 3,
  "currentValue": 5000.0
}
```

---

#### 3. Get Trading Signals

Get AI-generated trading signals.

**Endpoint**: `GET /api/phase3/social/signals`

**Query Parameters**:
- `asset` (string, optional): Filter by asset (e.g., "BTC")
- `timeframe` (string, optional): Timeframe ("1h", "4h", "1d")
- `minConfidence` (float, optional): Minimum confidence score (0-1)

**Example**:
```bash
GET /api/phase3/social/signals?asset=BTC&minConfidence=0.7
```

**Response** (200 OK):
```json
{
  "signals": [
    {
      "signalId": "signal_pqr678",
      "asset": "BTC",
      "action": "BUY",
      "confidence": 0.87,
      "currentPrice": 52000.0,
      "targetPrice": 55000.0,
      "stopLoss": 50000.0,
      "timeframe": "4h",
      "reasoning": "Strong bullish momentum with high volume",
      "indicators": {
        "rsi": 45.2,
        "macd": "bullish_cross",
        "volume": "high"
      },
      "timestamp": "2024-09-30T12:00:00Z",
      "expiresAt": "2024-09-30T16:00:00Z"
    },
    {
      "signalId": "signal_stu901",
      "asset": "ETH",
      "action": "HOLD",
      "confidence": 0.75,
      "currentPrice": 3100.0,
      "targetPrice": 3200.0,
      "stopLoss": 2950.0,
      "timeframe": "1d",
      "reasoning": "Consolidation phase, wait for breakout",
      "indicators": {
        "rsi": 52.8,
        "macd": "neutral",
        "volume": "medium"
      },
      "timestamp": "2024-09-30T12:00:00Z",
      "expiresAt": "2024-10-01T12:00:00Z"
    }
  ],
  "totalSignals": 2
}
```

**Action Types**:
- `BUY`: Strong buy signal
- `HOLD`: Hold current position or wait
- `SELL`: Sell signal

---

#### 4. Get Featured Portfolios

Browse public portfolios shared by the community.

**Endpoint**: `GET /api/phase3/social/portfolios/featured`

**Query Parameters**:
- `sortBy` (string, optional): Sort by ("performance", "followers", "recent")
- `minReturn` (float, optional): Minimum return percentage

**Response** (200 OK):
```json
{
  "portfolios": [
    {
      "portfolioId": "port_vwx234",
      "owner": "InvestorPro",
      "name": "Balanced Crypto Portfolio",
      "description": "60% BTC/ETH, 40% DeFi",
      "totalValue": 125000.0,
      "totalReturn": 45.8,
      "allocation": {
        "BTC": 35.0,
        "ETH": 25.0,
        "AAVE": 15.0,
        "UNI": 12.5,
        "LINK": 12.5
      },
      "followers": 450,
      "riskLevel": "medium",
      "rebalanceFrequency": "monthly",
      "lastRebalance": "2024-09-01T00:00:00Z"
    }
  ]
}
```

---

### Portfolio Automation

#### 1. Analyze Portfolio Rebalancing

Analyze portfolio for rebalancing needs.

**Endpoint**: `POST /api/phase3/portfolio/rebalance/analyze`

**Request Body**:
```json
{
  "currentAllocation": {
    "BTC": 0.45,
    "ETH": 0.35,
    "USDT": 0.20
  },
  "targetAllocation": {
    "BTC": 0.40,
    "ETH": 0.30,
    "USDT": 0.30
  },
  "totalValue": 100000.0,
  "threshold": 0.05
}
```

**Parameters**:
- `currentAllocation` (object, required): Current allocation percentages (must sum to 1.0)
- `targetAllocation` (object, required): Target allocation percentages (must sum to 1.0)
- `totalValue` (float, required): Total portfolio value in USD
- `threshold` (float, optional): Drift threshold for rebalancing (default: 0.05 = 5%)

**Response** (200 OK):
```json
{
  "needsRebalancing": true,
  "drifts": {
    "BTC": 0.05,
    "ETH": 0.05,
    "USDT": -0.10
  },
  "recommendations": [
    {
      "asset": "BTC",
      "action": "SELL",
      "currentValue": 45000.0,
      "targetValue": 40000.0,
      "difference": -5000.0,
      "percentChange": -11.1
    },
    {
      "asset": "ETH",
      "action": "SELL",
      "currentValue": 35000.0,
      "targetValue": 30000.0,
      "difference": -5000.0,
      "percentChange": -14.3
    },
    {
      "asset": "USDT",
      "action": "BUY",
      "currentValue": 20000.0,
      "targetValue": 30000.0,
      "difference": 10000.0,
      "percentChange": 50.0
    }
  ],
  "estimatedCost": 30.0,
  "timestamp": "2024-09-30T12:00:00Z"
}
```

---

#### 2. Generate Rebalancing Orders

Generate specific orders to rebalance portfolio.

**Endpoint**: `POST /api/phase3/portfolio/rebalance/orders`

**Request Body**:
```json
{
  "currentAllocation": {
    "BTC": 0.45,
    "ETH": 0.35,
    "USDT": 0.20
  },
  "targetAllocation": {
    "BTC": 0.40,
    "ETH": 0.30,
    "USDT": 0.30
  },
  "totalValue": 100000.0
}
```

**Response** (200 OK):
```json
{
  "orders": [
    {
      "orderId": "order_yz123",
      "type": "SELL",
      "asset": "BTC",
      "amount": 0.096,
      "estimatedValue": 5000.0,
      "priority": 1
    },
    {
      "orderId": "order_yz124",
      "type": "SELL",
      "asset": "ETH",
      "amount": 1.613,
      "estimatedValue": 5000.0,
      "priority": 2
    },
    {
      "orderId": "order_yz125",
      "type": "BUY",
      "asset": "USDT",
      "amount": 10000.0,
      "estimatedValue": 10000.0,
      "priority": 3
    }
  ],
  "totalOrders": 3,
  "estimatedCost": 30.0,
  "timestamp": "2024-09-30T12:00:00Z"
}
```

---

#### 3. Assess Portfolio Risk

Assess overall portfolio risk metrics.

**Endpoint**: `POST /api/phase3/portfolio/risk/assess`

**Request Body**:
```json
{
  "positions": [
    {"asset": "BTC", "value": 50000.0, "volatility": 0.65},
    {"asset": "ETH", "value": 30000.0, "volatility": 0.72},
    {"asset": "USDT", "value": 20000.0, "volatility": 0.01}
  ]
}
```

**Response** (200 OK):
```json
{
  "riskScore": 6.8,
  "riskLevel": "medium",
  "volatility": 0.52,
  "sharpeRatio": 1.85,
  "maxDrawdown": 0.45,
  "valueAtRisk": 15000.0,
  "diversificationScore": 0.72,
  "recommendations": [
    "Consider increasing stablecoin allocation to reduce volatility",
    "Portfolio has moderate concentration risk in BTC",
    "Good Sharpe ratio indicates favorable risk-adjusted returns"
  ],
  "timestamp": "2024-09-30T12:00:00Z"
}
```

**Risk Levels**:
- `low`: Risk score 0-3
- `medium`: Risk score 3-7
- `high`: Risk score 7-10

---

#### 4. Calculate Position Size

Calculate optimal position size based on risk parameters.

**Endpoint**: `POST /api/phase3/portfolio/position-size`

**Request Body**:
```json
{
  "portfolioValue": 100000.0,
  "riskPerTrade": 0.02,
  "entryPrice": 52000.0,
  "stopLoss": 50000.0
}
```

**Parameters**:
- `portfolioValue` (float, required): Total portfolio value
- `riskPerTrade` (float, required): Risk per trade as decimal (e.g., 0.02 = 2%)
- `entryPrice` (float, required): Entry price for position
- `stopLoss` (float, required): Stop loss price

**Response** (200 OK):
```json
{
  "recommendedSize": 0.385,
  "recommendedValue": 20000.0,
  "maxLoss": 2000.0,
  "riskRewardRatio": 2.5,
  "leverageRequired": 0.2,
  "recommendations": "Position sized for 2% portfolio risk",
  "timestamp": "2024-09-30T12:00:00Z"
}
```

---

#### 5. Create DCA Schedule

Create a dollar-cost averaging schedule.

**Endpoint**: `POST /api/phase3/portfolio/dca/create`

**Request Body**:
```json
{
  "asset": "BTC",
  "amount": 100.0,
  "frequency": "weekly",
  "durationMonths": 12,
  "startDate": "2024-10-01"
}
```

**Parameters**:
- `asset` (string, required): Asset to purchase
- `amount` (float, required): Amount to invest per period
- `frequency` (string, required): "daily", "weekly", "biweekly", or "monthly"
- `durationMonths` (int, required): Duration in months
- `startDate` (string, optional): Start date (ISO format, defaults to today)

**Response** (200 OK):
```json
{
  "scheduleId": "dca_abc789",
  "asset": "BTC",
  "amount": 100.0,
  "frequency": "weekly",
  "totalInvestment": 5200.0,
  "startDate": "2024-10-01T00:00:00Z",
  "endDate": "2025-10-01T00:00:00Z",
  "totalPurchases": 52,
  "nextPurchase": "2024-10-01T00:00:00Z",
  "status": "active"
}
```

---

#### 6. Get DCA Schedules

View all active DCA schedules.

**Endpoint**: `GET /api/phase3/portfolio/dca/schedules`

**Response** (200 OK):
```json
{
  "schedules": [
    {
      "scheduleId": "dca_abc789",
      "asset": "BTC",
      "amount": 100.0,
      "frequency": "weekly",
      "totalInvested": 1200.0,
      "averagePrice": 51500.0,
      "totalUnits": 0.0233,
      "nextPurchase": "2024-10-08T00:00:00Z",
      "purchasesCompleted": 12,
      "purchasesRemaining": 40,
      "status": "active"
    },
    {
      "scheduleId": "dca_def456",
      "asset": "ETH",
      "amount": 50.0,
      "frequency": "biweekly",
      "totalInvested": 600.0,
      "averagePrice": 3050.0,
      "totalUnits": 0.197,
      "nextPurchase": "2024-10-15T00:00:00Z",
      "purchasesCompleted": 12,
      "purchasesRemaining": 14,
      "status": "active"
    }
  ],
  "totalSchedules": 2,
  "totalInvested": 1800.0
}
```

---

#### 7. Create Stop-Loss Order

Create an automated stop-loss or take-profit order.

**Endpoint**: `POST /api/phase3/portfolio/stop-loss/create`

**Request Body**:
```json
{
  "asset": "BTC",
  "amount": 1.0,
  "stopLossPrice": 50000.0,
  "takeProfitPrice": 60000.0,
  "trailingStop": true,
  "trailingPercent": 5.0
}
```

**Parameters**:
- `asset` (string, required): Asset symbol
- `amount` (float, required): Amount to protect
- `stopLossPrice` (float, optional): Stop loss price
- `takeProfitPrice` (float, optional): Take profit price
- `trailingStop` (boolean, optional): Enable trailing stop
- `trailingPercent` (float, optional): Trailing stop percentage

**Response** (200 OK):
```json
{
  "orderId": "stop_ghi012",
  "asset": "BTC",
  "amount": 1.0,
  "currentPrice": 52000.0,
  "stopLossPrice": 50000.0,
  "takeProfitPrice": 60000.0,
  "trailingStop": true,
  "trailingPercent": 5.0,
  "trailingStopPrice": 49400.0,
  "status": "active",
  "createdAt": "2024-09-30T12:00:00Z"
}
```

---

#### 8. Get Active Stop-Loss Orders

View all active stop-loss orders.

**Endpoint**: `GET /api/phase3/portfolio/stop-loss/active`

**Response** (200 OK):
```json
{
  "orders": [
    {
      "orderId": "stop_ghi012",
      "asset": "BTC",
      "amount": 1.0,
      "currentPrice": 52500.0,
      "stopLossPrice": 50000.0,
      "takeProfitPrice": 60000.0,
      "trailingStop": true,
      "trailingPercent": 5.0,
      "trailingStopPrice": 49875.0,
      "distanceToStop": -4.76,
      "distanceToTarget": 14.29,
      "status": "active",
      "createdAt": "2024-09-30T12:00:00Z"
    }
  ],
  "totalOrders": 1
}
```

---

## Status & Health

### Get Phase 3 Status

Get overall status of Phase 3 features.

**Endpoint**: `GET /api/phase3/status`

**Response** (200 OK):
```json
{
  "phase": "Phase 3",
  "status": "COMPLETE",
  "features": {
    "aiModels": {
      "status": "operational",
      "models": ["LSTM", "Transformer", "Ensemble", "BERT"]
    },
    "defi": {
      "status": "operational",
      "protocols": ["Uniswap", "PancakeSwap", "SushiSwap", "Compound", "Aave", "Curve", "Yearn", "Convex"]
    },
    "socialTrading": {
      "status": "operational",
      "features": ["copyTrading", "signals", "portfolioSharing"]
    },
    "portfolioAutomation": {
      "status": "operational",
      "features": ["rebalancing", "riskManagement", "dca", "stopLoss"]
    }
  },
  "metrics": {
    "totalEndpoints": 30,
    "totalFeatures": 18,
    "linesOfCode": 2203
  },
  "timestamp": "2024-09-30T12:00:00Z"
}
```

---

### Health Check

Check if the API server is running.

**Endpoint**: `GET /api/phase3/health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2024-09-30T12:00:00Z",
  "uptime": 86400
}
```

---

## Error Handling

All endpoints follow consistent error response format.

### Error Response Format

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": "Additional error details",
  "timestamp": "2024-09-30T12:00:00Z"
}
```

### Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Common Error Codes

- `INVALID_PARAMS`: Invalid request parameters
- `MISSING_PARAMS`: Required parameters missing
- `INSUFFICIENT_BALANCE`: Insufficient balance for operation
- `POSITION_NOT_FOUND`: Position not found
- `INVALID_TOKEN`: Invalid token symbol
- `RATE_LIMIT_EXCEEDED`: API rate limit exceeded
- `SERVICE_UNAVAILABLE`: External service unavailable

---

## Rate Limiting

Phase 3 API implements rate limiting to ensure fair usage:

- **Default Limit**: 100 requests per minute per IP
- **Burst Limit**: 200 requests per minute
- **AI Model Endpoints**: 20 requests per minute (computationally intensive)

Rate limit headers are included in all responses:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1696075200
```

When rate limit is exceeded, API returns `429 Too Many Requests`:

```json
{
  "error": "Rate limit exceeded",
  "code": "RATE_LIMIT_EXCEEDED",
  "retryAfter": 60,
  "timestamp": "2024-09-30T12:00:00Z"
}
```

---

## Best Practices

### 1. Error Handling

Always implement proper error handling:

```javascript
try {
  const response = await fetch('/api/phase3/ai/lstm/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ symbol: 'BTC', data: priceData })
  });
  
  if (!response.ok) {
    const error = await response.json();
    console.error('API Error:', error);
    return;
  }
  
  const result = await response.json();
  console.log('Predictions:', result.predictions);
} catch (error) {
  console.error('Network Error:', error);
}
```

### 2. Rate Limiting

Implement exponential backoff when rate limited:

```javascript
async function apiCallWithRetry(url, options, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    const response = await fetch(url, options);
    
    if (response.status === 429) {
      const retryAfter = parseInt(response.headers.get('X-RateLimit-Reset'));
      await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
      continue;
    }
    
    return response;
  }
  throw new Error('Max retries exceeded');
}
```

### 3. Data Validation

Validate input data before sending requests:

```javascript
function validateAllocation(allocation) {
  const sum = Object.values(allocation).reduce((a, b) => a + b, 0);
  if (Math.abs(sum - 1.0) > 0.001) {
    throw new Error('Allocation must sum to 1.0');
  }
}
```

### 4. Pagination

For endpoints that return large datasets, use pagination:

```javascript
async function getAllPositions() {
  let allPositions = [];
  let page = 1;
  
  while (true) {
    const response = await fetch(`/api/phase3/defi/farming/positions?page=${page}`);
    const data = await response.json();
    
    allPositions = allPositions.concat(data.positions);
    
    if (!data.hasMore) break;
    page++;
  }
  
  return allPositions;
}
```

---

## Support

For issues, questions, or feature requests:

- **Documentation**: [docs/](../docs/)
- **GitHub Issues**: [https://github.com/thewriterben/crs/issues](https://github.com/thewriterben/crs/issues)
- **Email**: support@crs-marketplace.com

---

**Last Updated**: September 30, 2024  
**Version**: 3.0.0  
**Phase**: 3 Complete ✅
