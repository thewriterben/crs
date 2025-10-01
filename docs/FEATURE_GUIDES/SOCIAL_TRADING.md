# Social Trading Features Guide

Complete guide to social trading features in the Cryptons.com Cryptocurrency Marketplace.

**Version**: 3.0.0  
**Phase**: 3 Complete ✅

---

## Table of Contents

- [Overview](#overview)
- [Copy Trading](#copy-trading)
- [Trading Signals](#trading-signals)
- [Portfolio Sharing](#portfolio-sharing)
- [Best Practices](#best-practices)
- [Use Cases](#use-cases)

---

## Overview

Phase 3 social trading features enable community-driven trading strategies:

- **Copy Trading** - Automatically copy trades from top performers
- **Trading Signals** - AI-generated BUY/SELL/HOLD recommendations
- **Portfolio Sharing** - Browse and replicate successful portfolios
- **Trader Leaderboards** - Track top traders by win rate and returns

All features include verification, performance tracking, and risk management.

---

## Copy Trading

### Overview

Copy trading allows you to automatically replicate trades from experienced traders.

### Top Traders

Get a list of the best-performing traders.

**Endpoint**: `GET /api/phase3/social/traders/top`

**Example**:
```bash
# Get top 10 traders sorted by win rate
curl "http://localhost:5006/api/phase3/social/traders/top?limit=10&sortBy=winRate"
```

**Response**:
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
  ]
}
```

### Follow a Trader

Start copying a trader's positions.

**Endpoint**: `POST /api/phase3/social/traders/follow`

**Example**:
```bash
curl -X POST http://localhost:5006/api/phase3/social/traders/follow \
  -H "Content-Type: application/json" \
  -d '{
    "traderId": "trader_001",
    "copyAmount": 5000.0,
    "copyPercentage": 100,
    "stopLoss": -10.0,
    "takeProfit": 25.0
  }'
```

**Parameters**:
- `traderId`: ID of trader to follow
- `copyAmount`: Total capital to allocate
- `copyPercentage`: Percentage of their positions to copy (1-100)
- `stopLoss`: Stop loss percentage (optional)
- `takeProfit`: Take profit percentage (optional)

**Response**:
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

### Selecting Traders

```python
def select_trader(criteria):
    """Select best trader based on criteria."""
    # Get top traders
    response = requests.get(
        'http://localhost:5006/api/phase3/social/traders/top',
        params={'limit': 50, 'sortBy': 'totalReturn'}
    )
    
    traders = response.json()['traders']
    
    # Filter by criteria
    filtered = [
        t for t in traders
        if t['winRate'] >= criteria['min_win_rate']
        and t['verified']
        and t['riskLevel'] == criteria['risk_level']
        and t['totalTrades'] >= criteria['min_trades']
    ]
    
    if not filtered:
        return None
    
    # Sort by risk-adjusted return
    for t in filtered:
        # Sharpe-like ratio: return / (100 - win_rate)
        t['score'] = t['totalReturn'] / (100 - t['winRate'] + 1)
    
    filtered.sort(key=lambda x: x['score'], reverse=True)
    
    best = filtered[0]
    print(f"Selected: {best['username']}")
    print(f"Win Rate: {best['winRate']}%")
    print(f"Total Return: {best['totalReturn']}%")
    print(f"Risk Level: {best['riskLevel']}")
    
    return best

# Example criteria
criteria = {
    'min_win_rate': 65,
    'risk_level': 'medium',
    'min_trades': 100
}

trader = select_trader(criteria)
```

### Position Sizing

```python
def calculate_copy_amount(trader_stats, your_capital, your_risk_tolerance):
    """Calculate how much to allocate to copying a trader."""
    # Base allocation on risk level
    risk_multipliers = {
        'low': 0.30,    # 30% of capital
        'medium': 0.20, # 20% of capital
        'high': 0.10    # 10% of capital
    }
    
    base_allocation = your_capital * risk_multipliers[trader_stats['riskLevel']]
    
    # Adjust based on win rate (higher win rate = more allocation)
    win_rate_factor = trader_stats['winRate'] / 100
    adjusted_allocation = base_allocation * (0.5 + win_rate_factor)
    
    # Adjust based on your risk tolerance (1-10)
    final_allocation = adjusted_allocation * (your_risk_tolerance / 5)
    
    return round(final_allocation, 2)

# Example
trader_stats = {
    'riskLevel': 'medium',
    'winRate': 72.5
}

amount = calculate_copy_amount(trader_stats, 50000, 7)
print(f"Recommended copy amount: ${amount:,.2f}")  # ~$10,150
```

### Managing Copy Positions

```python
def manage_copy_trading():
    """Monitor and manage copy trading positions."""
    # Get current positions
    positions = get_copy_positions()
    
    for pos in positions:
        # Calculate current P&L
        pnl_pct = ((pos['currentValue'] - pos['copyAmount']) / pos['copyAmount']) * 100
        
        print(f"\n{pos['username']}:")
        print(f"  Investment: ${pos['copyAmount']:,.2f}")
        print(f"  Current: ${pos['currentValue']:,.2f}")
        print(f"  P&L: {pnl_pct:+.2f}%")
        
        # Check stop loss
        if pos['stopLoss'] and pnl_pct <= pos['stopLoss']:
            print(f"  🔴 STOP LOSS HIT - Closing position")
            unfollow_trader(pos['followId'])
        
        # Check take profit
        elif pos['takeProfit'] and pnl_pct >= pos['takeProfit']:
            print(f"  🟢 TAKE PROFIT HIT - Closing position")
            unfollow_trader(pos['followId'])
        
        # Check trader performance change
        elif pos['recentWinRate'] < 50:
            print(f"  ⚠️  WARNING - Recent win rate dropped to {pos['recentWinRate']}%")
```

---

## Trading Signals

### Overview

AI-generated trading signals provide actionable BUY/SELL/HOLD recommendations.

### Get Signals

**Endpoint**: `GET /api/phase3/social/signals`

**Example**:
```bash
# Get high-confidence BTC signals
curl "http://localhost:5006/api/phase3/social/signals?asset=BTC&minConfidence=0.7"
```

**Response**:
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
    }
  ]
}
```

### Signal Types

- **BUY**: Strong buy recommendation
- **SELL**: Sell/short recommendation  
- **HOLD**: Hold position or wait for better entry

### Using Signals

```python
def execute_signals(min_confidence=0.80):
    """Execute trades based on trading signals."""
    # Get all signals
    response = requests.get(
        'http://localhost:5006/api/phase3/social/signals',
        params={'minConfidence': min_confidence}
    )
    
    signals = response.json()['signals']
    
    for signal in signals:
        print(f"\n{signal['asset']} - {signal['action']}")
        print(f"Confidence: {signal['confidence']:.0%}")
        print(f"Current: ${signal['currentPrice']:,.2f}")
        print(f"Target: ${signal['targetPrice']:,.2f}")
        print(f"Stop Loss: ${signal['stopLoss']:,.2f}")
        print(f"Reasoning: {signal['reasoning']}")
        
        # Calculate risk/reward
        if signal['action'] == 'BUY':
            potential_gain = signal['targetPrice'] - signal['currentPrice']
            potential_loss = signal['currentPrice'] - signal['stopLoss']
            risk_reward = potential_gain / potential_loss if potential_loss > 0 else 0
            
            print(f"Risk/Reward: {risk_reward:.2f}x")
            
            # Execute if R:R > 2
            if risk_reward > 2 and signal['confidence'] > min_confidence:
                print("✅ EXECUTING TRADE")
                # execute_trade(signal)
            else:
                print("⏸️  SKIPPING - Criteria not met")
```

### Signal Filtering

```python
def filter_signals(signals, filters):
    """Filter signals by multiple criteria."""
    filtered = signals
    
    # Filter by confidence
    if 'min_confidence' in filters:
        filtered = [s for s in filtered if s['confidence'] >= filters['min_confidence']]
    
    # Filter by action
    if 'actions' in filters:
        filtered = [s for s in filtered if s['action'] in filters['actions']]
    
    # Filter by risk/reward
    if 'min_risk_reward' in filters:
        filtered = [
            s for s in filtered
            if calculate_risk_reward(s) >= filters['min_risk_reward']
        ]
    
    # Filter by technical indicators
    if 'require_volume' in filters and filters['require_volume']:
        filtered = [s for s in filtered if s['indicators']['volume'] == 'high']
    
    return filtered

# Example usage
filters = {
    'min_confidence': 0.80,
    'actions': ['BUY'],
    'min_risk_reward': 2.0,
    'require_volume': True
}

good_signals = filter_signals(all_signals, filters)
print(f"Found {len(good_signals)} high-quality signals")
```

### Combining Signals with Analysis

```python
def comprehensive_analysis(asset):
    """Combine signals with AI predictions and sentiment."""
    # Get trading signal
    signal_resp = requests.get(
        f'http://localhost:5006/api/phase3/social/signals?asset={asset}'
    )
    signal = signal_resp.json()['signals'][0] if signal_resp.json()['signals'] else None
    
    # Get AI prediction
    pred_resp = requests.post(
        'http://localhost:5006/api/phase3/ai/ensemble/predict',
        json={'symbol': asset, 'data': get_price_history(asset)}
    )
    prediction = pred_resp.json()
    
    # Get sentiment
    news = get_latest_news(asset)
    sent_resp = requests.post(
        'http://localhost:5006/api/phase3/ai/sentiment/analyze',
        json={'text': news}
    )
    sentiment = sent_resp.json()
    
    # Analyze all signals
    score = 0
    
    if signal and signal['action'] == 'BUY':
        score += signal['confidence'] * 33
    
    if prediction['predictions'][0] > get_current_price(asset):
        score += prediction['confidence'] * 33
    
    if sentiment['sentiment'] == 'positive':
        score += sentiment['confidence'] * 33
    
    decision = 'STRONG BUY' if score > 80 else 'BUY' if score > 60 else 'HOLD'
    
    return {
        'decision': decision,
        'score': score,
        'signal': signal,
        'prediction': prediction,
        'sentiment': sentiment
    }
```

---

## Portfolio Sharing

### Overview

Browse and replicate successful portfolios from the community.

### Featured Portfolios

**Endpoint**: `GET /api/phase3/social/portfolios/featured`

**Example**:
```bash
# Get top-performing portfolios
curl "http://localhost:5006/api/phase3/social/portfolios/featured?sortBy=performance&minReturn=30"
```

**Response**:
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

### Replicating Portfolios

```python
def replicate_portfolio(portfolio_id, your_capital):
    """Replicate a successful portfolio with your capital."""
    # Get portfolio details
    response = requests.get(
        f'http://localhost:5006/api/phase3/social/portfolios/{portfolio_id}'
    )
    portfolio = response.json()
    
    # Calculate amounts for each asset
    your_allocation = {}
    for asset, percent in portfolio['allocation'].items():
        amount = your_capital * (percent / 100)
        your_allocation[asset] = {
            'percent': percent,
            'usd_amount': amount,
            'shares': amount / get_current_price(asset)
        }
    
    print(f"Replicating: {portfolio['name']}")
    print(f"Your capital: ${your_capital:,.2f}\n")
    
    for asset, alloc in your_allocation.items():
        print(f"{asset}:")
        print(f"  Allocation: {alloc['percent']}%")
        print(f"  Amount: ${alloc['usd_amount']:,.2f}")
        print(f"  Shares: {alloc['shares']:.4f}\n")
    
    return your_allocation

# Example: Replicate with $10,000
allocation = replicate_portfolio('port_vwx234', 10000)
```

### Portfolio Comparison

```python
def compare_portfolios(portfolio_ids):
    """Compare multiple portfolios."""
    portfolios = []
    for pid in portfolio_ids:
        resp = requests.get(f'http://localhost:5006/api/phase3/social/portfolios/{pid}')
        portfolios.append(resp.json())
    
    print("\nPortfolio Comparison:")
    print("-" * 80)
    print(f"{'Name':<30} {'Return':<10} {'Risk':<10} {'Followers':<10}")
    print("-" * 80)
    
    for p in portfolios:
        print(f"{p['name']:<30} {p['totalReturn']:>8.1f}% {p['riskLevel']:<10} {p['followers']:<10}")
    
    # Find best by different criteria
    best_return = max(portfolios, key=lambda x: x['totalReturn'])
    most_popular = max(portfolios, key=lambda x: x['followers'])
    
    print("\nBest return:", best_return['name'])
    print("Most popular:", most_popular['name'])
    
    return portfolios
```

### Creating Your Portfolio

```python
def create_shared_portfolio(name, description, allocation, risk_level):
    """Create and share your portfolio."""
    portfolio = {
        'name': name,
        'description': description,
        'allocation': allocation,
        'riskLevel': risk_level,
        'rebalanceFrequency': 'monthly',
        'public': True
    }
    
    response = requests.post(
        'http://localhost:5006/api/phase3/social/portfolios/create',
        json=portfolio
    )
    
    return response.json()

# Example
allocation = {
    'BTC': 40.0,
    'ETH': 30.0,
    'SOL': 15.0,
    'AVAX': 15.0
}

portfolio = create_shared_portfolio(
    name="Aggressive Growth",
    description="High-growth altcoins with BTC/ETH foundation",
    allocation=allocation,
    risk_level="high"
)
```

---

## Best Practices

### 1. Diversify Social Strategies

```python
def diversified_social_strategy(capital):
    """Implement diversified social trading strategy."""
    return {
        'copy_trading': {
            'amount': capital * 0.40,
            'traders': [
                {'id': 'trader_001', 'allocation': 0.60},  # Conservative
                {'id': 'trader_003', 'allocation': 0.40}   # Aggressive
            ]
        },
        'signal_trading': {
            'amount': capital * 0.30,
            'min_confidence': 0.85,
            'max_risk_per_trade': 0.02
        },
        'portfolio_replication': {
            'amount': capital * 0.30,
            'portfolio': 'port_vwx234'
        }
    }
```

### 2. Risk Management

```python
def social_trading_risk_limits():
    """Define risk limits for social trading."""
    return {
        'max_per_trader': 0.20,  # Max 20% with one trader
        'max_total_copy': 0.50,  # Max 50% in copy trading
        'max_position': 0.10,    # Max 10% in one position
        'stop_loss': -0.10,      # Exit at 10% loss
        'take_profit': 0.25,     # Exit at 25% gain
        'max_correlation': 0.70  # Avoid highly correlated traders
    }
```

### 3. Performance Tracking

```python
def track_social_performance():
    """Track performance of social trading strategies."""
    # Get all positions
    copy_positions = get_copy_positions()
    signal_trades = get_signal_trades()
    portfolio_value = get_portfolio_value()
    
    # Calculate metrics
    total_invested = sum(p['copyAmount'] for p in copy_positions)
    total_value = sum(p['currentValue'] for p in copy_positions)
    total_return = ((total_value - total_invested) / total_invested) * 100
    
    # Per-trader performance
    print("\nCopy Trading Performance:")
    for pos in copy_positions:
        pnl = ((pos['currentValue'] - pos['copyAmount']) / pos['copyAmount']) * 100
        print(f"{pos['username']}: {pnl:+.2f}%")
    
    # Signal trading performance
    signal_wins = sum(1 for t in signal_trades if t['pnl'] > 0)
    signal_win_rate = (signal_wins / len(signal_trades)) * 100 if signal_trades else 0
    
    print(f"\nSignal Trading:")
    print(f"Win Rate: {signal_win_rate:.1f}%")
    print(f"Total Trades: {len(signal_trades)}")
    
    print(f"\nOverall Return: {total_return:+.2f}%")
    
    return {
        'total_return': total_return,
        'signal_win_rate': signal_win_rate,
        'total_trades': len(signal_trades)
    }
```

---

## Use Cases

### 1. Beginner Investor

```python
class BeginnerStrategy:
    def __init__(self, capital):
        self.capital = capital
        
    def setup(self):
        # Follow verified low-risk trader with proven track record
        best_safe_trader = self.find_trader({
            'min_win_rate': 70,
            'risk_level': 'low',
            'min_trades': 500,
            'verified': True
        })
        
        # Allocate 80% to copy trading
        self.follow_trader(best_safe_trader['traderId'], self.capital * 0.80)
        
        # Use 20% for high-confidence signals
        self.signal_trading_amount = self.capital * 0.20
        
    def trade_signals(self):
        signals = get_signals(min_confidence=0.90)
        for signal in signals:
            if signal['action'] == 'BUY':
                amount = self.signal_trading_amount * 0.10  # 10% per trade
                self.execute_signal_trade(signal, amount)
```

### 2. Active Trader

```python
class ActiveTraderStrategy:
    def __init__(self, capital):
        self.capital = capital
        
    def setup(self):
        # Follow 3 different traders (diversification)
        traders = self.find_top_traders(3)
        for trader in traders:
            self.follow_trader(trader['traderId'], self.capital * 0.20)
        
        # Use 40% for personal signal trading
        self.signal_amount = self.capital * 0.40
        
    def execute_daily(self):
        # Check signals multiple times per day
        signals = get_signals(min_confidence=0.75)
        
        # Execute high R:R trades
        for signal in signals:
            rr = self.calculate_risk_reward(signal)
            if rr > 2.5:
                self.execute_signal_trade(signal)
```

### 3. Portfolio Replicator

```python
class PortfolioReplicator:
    def __init__(self, capital):
        self.capital = capital
        
    def setup(self):
        # Find top 3 portfolios
        portfolios = get_featured_portfolios(limit=3)
        
        # Replicate with equal weight
        for portfolio in portfolios:
            self.replicate(portfolio, self.capital / 3)
        
    def rebalance_monthly(self):
        # Check if source portfolios rebalanced
        for portfolio in self.portfolios:
            if portfolio.last_rebalance_changed():
                self.replicate(portfolio.get_updated_allocation())
```

---

## Support

For social trading support:

- **Documentation**: [API_REFERENCE.md](../API_REFERENCE.md)
- **GitHub Issues**: [https://github.com/thewriterben/crs/issues](https://github.com/thewriterben/crs/issues)

---

**Version**: 3.0.0  
**Last Updated**: September 30, 2024  
**Phase**: 3 Complete ✅
