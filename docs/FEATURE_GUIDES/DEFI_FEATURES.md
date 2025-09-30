# DeFi Integration Features Guide

Complete guide to using DeFi features in the CRS Cryptocurrency Marketplace.

**Version**: 3.0.0  
**Phase**: 3 Complete ✅

---

## Table of Contents

- [Overview](#overview)
- [DEX Aggregator](#dex-aggregator)
- [Yield Farming](#yield-farming)
- [Staking](#staking)
- [Liquidity Pools](#liquidity-pools)
- [Best Practices](#best-practices)
- [Use Cases](#use-cases)

---

## Overview

Phase 3 DeFi integration provides comprehensive access to decentralized finance protocols:

- **3 DEX Integrations**: Uniswap V3, PancakeSwap V2, SushiSwap
- **5 Yield Farming Pools**: Compound, Aave, Curve, Yearn, Convex (38-68% APY)
- **5 Staking Options**: ETH, BNB, ADA, DOT, SOL
- **3 Liquidity Pools**: ETH-USDT, BTC-ETH, BNB-BUSD

All features are accessible via REST API with full transparency and control.

---

## DEX Aggregator

### Overview

The DEX Aggregator finds the best prices across multiple decentralized exchanges automatically.

### Supported DEXes

1. **Uniswap V3** - Concentrated liquidity, capital efficient
2. **PancakeSwap V2** - Low fees, BSC-based
3. **SushiSwap** - Community-driven, multi-chain

### Get Quote

Find the best price across all DEXes.

**Endpoint**: `GET /api/phase3/defi/dex/quote`

**Example**:
```bash
curl "http://localhost:5006/api/phase3/defi/dex/quote?tokenIn=ETH&tokenOut=USDT&amountIn=1.0"
```

**Response**:
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
      "dex": "PancakeSwap",
      "amountOut": 3022.67,
      "priceImpact": 0.10,
      "fee": 0.25,
      "gasEstimate": 120000
    },
    {
      "dex": "SushiSwap",
      "amountOut": 3018.23,
      "priceImpact": 0.15,
      "fee": 0.3,
      "gasEstimate": 145000
    }
  ],
  "bestQuote": {
    "dex": "PancakeSwap",
    "amountOut": 3022.67,
    "savings": 2.22
  }
}
```

### Execute Swap

Execute a token swap on the selected DEX.

**Endpoint**: `POST /api/phase3/defi/dex/swap`

**Example**:
```bash
curl -X POST http://localhost:5006/api/phase3/defi/dex/swap \
  -H "Content-Type: application/json" \
  -d '{
    "tokenIn": "ETH",
    "tokenOut": "USDT",
    "amountIn": 1.0,
    "dex": "PancakeSwap",
    "slippageTolerance": 0.5
  }'
```

**Response**:
```json
{
  "transactionId": "tx_abc123def456",
  "status": "completed",
  "amountIn": 1.0,
  "amountOut": 3020.45,
  "effectivePrice": 3020.45,
  "fee": 9.06,
  "gasUsed": 145000
}
```

### Best Practices

```python
import requests

def find_best_swap(token_in, token_out, amount):
    """Find and execute best swap across DEXes."""
    # Get quotes from all DEXes
    response = requests.get(
        f'http://localhost:5006/api/phase3/defi/dex/quote',
        params={
            'tokenIn': token_in,
            'tokenOut': token_out,
            'amountIn': amount
        }
    )
    
    if response.status_code != 200:
        print(f"Error getting quotes: {response.json()}")
        return None
    
    data = response.json()
    best = data['bestQuote']
    
    print(f"Best rate: {best['dex']} - {best['amountOut']} {token_out}")
    print(f"Savings vs worst: ${best['savings']:.2f}")
    
    # Calculate total cost (output + gas)
    quotes_with_cost = []
    for quote in data['quotes']:
        # Estimate gas cost in USD (assume $50 per 100k gas)
        gas_cost_usd = (quote['gasEstimate'] / 100000) * 50
        net_output = quote['amountOut'] - gas_cost_usd
        quotes_with_cost.append({
            **quote,
            'gas_cost_usd': gas_cost_usd,
            'net_output': net_output
        })
    
    # Sort by net output
    best_overall = max(quotes_with_cost, key=lambda x: x['net_output'])
    
    print(f"\nBest after gas: {best_overall['dex']}")
    print(f"Net output: ${best_overall['net_output']:.2f}")
    
    # Execute swap
    confirm = input("Execute swap? (y/n): ")
    if confirm.lower() == 'y':
        swap_response = requests.post(
            'http://localhost:5006/api/phase3/defi/dex/swap',
            json={
                'tokenIn': token_in,
                'tokenOut': token_out,
                'amountIn': amount,
                'dex': best_overall['dex'],
                'slippageTolerance': 0.5
            }
        )
        
        return swap_response.json()
    
    return None

# Usage
find_best_swap('ETH', 'USDT', 1.0)
```

### Key Metrics

- **Price Impact**: How much your trade moves the market (lower is better)
- **Fee**: DEX trading fee percentage
- **Gas Estimate**: Estimated gas cost for transaction
- **Slippage**: Maximum acceptable price change (default: 0.5%)

---

## Yield Farming

### Overview

Earn passive income by providing liquidity to DeFi protocols.

### Available Pools

| Pool ID | Protocol | Asset | APY | TVL | Risk |
|---------|----------|-------|-----|-----|------|
| farm_001 | Compound | USDC | 45.2% | $1.25B | Low |
| farm_002 | Curve | 3CRV | 52.8% | $850M | Low |
| farm_003 | Aave | DAI | 38.5% | $2.1B | Low |
| farm_004 | Yearn | WETH | 48.9% | $680M | Medium |
| farm_005 | Convex | CVX | 68.9% | $450M | Medium |

### Browse Opportunities

**Endpoint**: `GET /api/phase3/defi/farming/opportunities`

**Example**:
```bash
# Get all farms with APY > 40%
curl "http://localhost:5006/api/phase3/defi/farming/opportunities?minApy=40"
```

**Response**:
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
    }
  ]
}
```

### Deposit to Farm

**Endpoint**: `POST /api/phase3/defi/farming/deposit`

**Example**:
```bash
curl -X POST http://localhost:5006/api/phase3/defi/farming/deposit \
  -H "Content-Type: application/json" \
  -d '{
    "poolId": "farm_001",
    "amount": 10000.0
  }'
```

**Response**:
```json
{
  "positionId": "pos_xyz789",
  "poolId": "farm_001",
  "protocol": "Compound",
  "asset": "USDC",
  "depositAmount": 10000.0,
  "startTime": "2024-09-30T12:00:00Z",
  "currentApy": 45.2,
  "estimatedDailyYield": 12.38
}
```

### View Positions

**Endpoint**: `GET /api/phase3/defi/farming/positions`

**Response**:
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
      "daysActive": 28
    }
  ],
  "totalDeposited": 10000.0,
  "totalValue": 10350.25,
  "totalEarned": 350.25
}
```

### Yield Farming Calculator

```python
def calculate_farming_returns(principal, apy, days):
    """Calculate expected returns from yield farming."""
    # Daily compound rate
    daily_rate = (1 + apy / 100) ** (1/365) - 1
    
    # Compound for specified days
    final_value = principal * ((1 + daily_rate) ** days)
    
    profit = final_value - principal
    roi = (profit / principal) * 100
    
    return {
        'initial': principal,
        'final': final_value,
        'profit': profit,
        'roi': roi,
        'daily_avg': profit / days
    }

# Example: $10,000 at 45% APY for 30 days
result = calculate_farming_returns(10000, 45.0, 30)
print(f"Initial: ${result['initial']:,.2f}")
print(f"After 30 days: ${result['final']:,.2f}")
print(f"Profit: ${result['profit']:,.2f} ({result['roi']:.2f}% ROI)")
print(f"Daily avg: ${result['daily_avg']:.2f}")
```

### Risk Management

**Low Risk Pools**:
- Established protocols (Compound, Aave, Curve)
- Stablecoins or major assets
- No lock periods
- Insurance available

**Medium Risk Pools**:
- Newer protocols (Yearn, Convex)
- Higher APY (50%+)
- Possible lock periods
- Higher volatility

**Best Practices**:
1. Start with low-risk pools
2. Diversify across multiple protocols
3. Monitor APY changes daily
4. Set up auto-compound when available
5. Have exit strategy ready

---

## Staking

### Overview

Stake cryptocurrencies to earn rewards while supporting network security.

### Supported Tokens

| Token | Min Amount | Flexible APY | Locked 90d APY | Features |
|-------|------------|--------------|----------------|----------|
| ETH | 0.1 | 4.2% | 6.8% | Auto-compound |
| BNB | 0.1 | 6.5% | 8.9% | Instant unstake |
| ADA | 10 | 5.1% | 8.0% | No minimum lock |
| DOT | 1 | 12.3% | 15.8% | Governance rights |
| SOL | 0.1 | 6.8% | 9.2% | Fast rewards |

### Get Staking Options

**Endpoint**: `GET /api/phase3/defi/staking/options`

**Response**:
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
    }
  ]
}
```

### Stake Tokens

**Endpoint**: `POST /api/phase3/defi/staking/stake`

**Example**:
```bash
# Stake 5 ETH for 90 days
curl -X POST http://localhost:5006/api/phase3/defi/staking/stake \
  -H "Content-Type: application/json" \
  -d '{
    "token": "ETH",
    "amount": 5.0,
    "lockPeriod": "90days"
  }'
```

**Response**:
```json
{
  "stakeId": "stake_def456",
  "token": "ETH",
  "amount": 5.0,
  "apy": 6.8,
  "lockPeriod": "90days",
  "startTime": "2024-09-30T12:00:00Z",
  "unlockTime": "2024-12-29T12:00:00Z",
  "estimatedDailyReward": 0.000931
}
```

### View Staking Positions

**Endpoint**: `GET /api/phase3/defi/staking/positions`

**Response**:
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
      "estimatedTotal": 0.084
    }
  ],
  "totalStaked": 5.0,
  "totalEarned": 0.028
}
```

### Staking Calculator

```python
def calculate_staking_rewards(amount, apy, days, compound_frequency='daily'):
    """Calculate staking rewards with compounding."""
    # Annual rate
    r = apy / 100
    
    # Compounding periods per year
    if compound_frequency == 'daily':
        n = 365
    elif compound_frequency == 'weekly':
        n = 52
    elif compound_frequency == 'monthly':
        n = 12
    else:
        n = 1
    
    # Time in years
    t = days / 365
    
    # Compound interest formula
    final = amount * (1 + r/n) ** (n * t)
    earned = final - amount
    
    return {
        'initial': amount,
        'final': final,
        'earned': earned,
        'apy': apy,
        'days': days
    }

# Example: 5 ETH at 6.8% APY for 90 days
result = calculate_staking_rewards(5.0, 6.8, 90)
print(f"Stake: {result['initial']} ETH")
print(f"After 90 days: {result['final']:.4f} ETH")
print(f"Earned: {result['earned']:.4f} ETH")
```

### Flexible vs Locked Staking

**Flexible Staking**:
- ✅ Withdraw anytime
- ✅ No penalties
- ❌ Lower APY
- ✅ Good for testing

**Locked Staking**:
- ✅ Higher APY
- ✅ Predictable returns
- ❌ Locked for period
- ❌ Early withdrawal penalty
- ✅ Best for long-term holders

---

## Liquidity Pools

### Overview

Provide liquidity to AMM pools and earn trading fees.

### Available Pools

| Pool | DEX | Fee Tier | 24h Volume | APY |
|------|-----|----------|------------|-----|
| ETH-USDT | Uniswap | 0.3% | $500M | 12.5% |
| BTC-ETH | Uniswap | 0.3% | $300M | 15.8% |
| BNB-BUSD | PancakeSwap | 0.25% | $200M | 18.3% |

### Add Liquidity

**Endpoint**: `POST /api/phase3/defi/liquidity/add`

**Example**:
```bash
curl -X POST http://localhost:5006/api/phase3/defi/liquidity/add \
  -H "Content-Type: application/json" \
  -d '{
    "pool": "ETH-USDT",
    "token0Amount": 1.0,
    "token1Amount": 3000.0
  }'
```

**Response**:
```json
{
  "positionId": "lp_jkl012",
  "pool": "ETH-USDT",
  "lpTokens": 54.77,
  "share": 0.0012,
  "token0Deposited": 1.0,
  "token1Deposited": 3000.0,
  "currentValue": 6000.0,
  "feeApy": 12.5
}
```

### View LP Positions

**Endpoint**: `GET /api/phase3/defi/liquidity/positions`

**Response**:
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
  ]
}
```

### Understanding Impermanent Loss

Impermanent loss occurs when the price ratio of your deposited tokens changes.

```python
def calculate_impermanent_loss(initial_price, current_price):
    """Calculate impermanent loss percentage."""
    # Price ratio
    ratio = current_price / initial_price
    
    # IL formula for 50/50 pool
    il = 2 * (ratio ** 0.5) / (1 + ratio) - 1
    
    il_percent = il * 100
    
    return il_percent

# Example: ETH went from $3000 to $3500
il = calculate_impermanent_loss(3000, 3500)
print(f"Impermanent Loss: {il:.2f}%")  # ~-0.82%

# Compare with holding
hodl_gain = ((3500 - 3000) / 3000) * 100
print(f"HODL would have gained: {hodl_gain:.2f}%")  # 16.67%

# LP gains (with fees)
fees_earned = 12.5 / 12 * 0.5  # 0.5 months of 12.5% APY
lp_gain = (6180.25 - 6000) / 6000 * 100
print(f"LP gained: {lp_gain:.2f}%")  # ~3%
```

### LP Best Practices

1. **Choose Stable Pairs**: Less impermanent loss
2. **Monitor Prices**: Exit if prices diverge significantly
3. **Factor in Fees**: High-volume pools compensate for IL
4. **Diversify**: Multiple pools reduce risk
5. **Long-term**: IL reduces over time with accumulated fees

---

## Best Practices

### 1. Diversification Strategy

```python
def create_defi_portfolio(total_capital):
    """Create a diversified DeFi portfolio."""
    return {
        'yield_farming': {
            'allocation': 0.40,  # 40%
            'amount': total_capital * 0.40,
            'pools': [
                {'protocol': 'Compound', 'percent': 50},
                {'protocol': 'Curve', 'percent': 50}
            ]
        },
        'staking': {
            'allocation': 0.35,  # 35%
            'amount': total_capital * 0.35,
            'assets': [
                {'token': 'ETH', 'percent': 60},
                {'token': 'DOT', 'percent': 40}
            ]
        },
        'liquidity': {
            'allocation': 0.25,  # 25%
            'amount': total_capital * 0.25,
            'pools': [
                {'pair': 'ETH-USDT', 'percent': 100}
            ]
        }
    }

# Example with $100k
portfolio = create_defi_portfolio(100000)
print("DeFi Portfolio Allocation:")
print(f"Yield Farming: ${portfolio['yield_farming']['amount']:,.2f}")
print(f"Staking: ${portfolio['staking']['amount']:,.2f}")
print(f"Liquidity: ${portfolio['liquidity']['amount']:,.2f}")
```

### 2. Risk Management

```python
def assess_defi_risk(positions):
    """Assess overall DeFi risk."""
    risk_score = 0
    
    for pos in positions:
        # Risk factors
        protocol_risk = {
            'Compound': 1, 'Aave': 1, 'Curve': 1,  # Low risk
            'Yearn': 2, 'Convex': 2  # Medium risk
        }.get(pos['protocol'], 3)
        
        lock_risk = 1 if pos.get('lockPeriod') else 0
        
        # Weight by allocation
        pos_risk = (protocol_risk + lock_risk) * (pos['value'] / total_value)
        risk_score += pos_risk
    
    if risk_score < 1.5:
        return 'LOW'
    elif risk_score < 2.5:
        return 'MEDIUM'
    else:
        return 'HIGH'
```

### 3. Monitoring and Alerts

```python
def monitor_defi_positions():
    """Monitor DeFi positions and alert on changes."""
    # Get all positions
    farming = get_farming_positions()
    staking = get_staking_positions()
    liquidity = get_liquidity_positions()
    
    # Check APY changes
    for pos in farming['positions']:
        if pos['apy'] < 30:  # APY dropped below threshold
            print(f"⚠️  Alert: {pos['protocol']} APY dropped to {pos['apy']}%")
    
    # Check impermanent loss
    for pos in liquidity['positions']:
        if pos['impermanentLoss'] < -5:  # More than 5% IL
            print(f"⚠️  Alert: High IL in {pos['pool']}: {pos['impermanentLoss']:.2f}%")
    
    # Check unlock times
    for pos in staking['positions']:
        if pos['daysRemaining'] <= 7:
            print(f"ℹ️  Info: {pos['token']} stake unlocks in {pos['daysRemaining']} days")
```

### 4. Gas Optimization

```python
def should_execute_transaction(profit_usd, gas_estimate):
    """Decide if transaction is worth the gas cost."""
    # Estimate gas cost ($50 per 100k gas)
    gas_cost_usd = (gas_estimate / 100000) * 50
    
    # Require at least 2x gas cost in profit
    min_profit = gas_cost_usd * 2
    
    if profit_usd < min_profit:
        print(f"❌ Not worth it: Profit ${profit_usd:.2f} < Min ${min_profit:.2f}")
        return False
    
    print(f"✅ Worth it: Profit ${profit_usd:.2f} > Gas ${gas_cost_usd:.2f}")
    return True
```

---

## Use Cases

### 1. Passive Income Generator

```python
class PassiveIncomeStrategy:
    def __init__(self, capital):
        self.capital = capital
        
    def setup(self):
        # 60% in stable farming (Compound USDC)
        self.farm_usdc(self.capital * 0.6, 'farm_001')
        
        # 30% in ETH staking
        self.stake_eth(self.capital * 0.3, '90days')
        
        # 10% reserve
        self.reserve = self.capital * 0.1
    
    def monthly_returns(self):
        farming_apy = 45.2
        staking_apy = 6.8
        
        monthly_farm = (self.capital * 0.6) * (farming_apy / 100 / 12)
        monthly_stake = (self.capital * 0.3) * (staking_apy / 100 / 12)
        
        return monthly_farm + monthly_stake

# $50k capital example
strategy = PassiveIncomeStrategy(50000)
monthly = strategy.monthly_returns()
print(f"Expected monthly income: ${monthly:,.2f}")  # ~$1,600/month
```

### 2. Yield Optimizer

```python
def optimize_yields():
    """Automatically move funds to highest-yielding opportunities."""
    # Get all opportunities
    farms = get_farming_opportunities()
    stakes = get_staking_options()
    
    # Find best opportunities by risk-adjusted return
    opportunities = []
    
    for farm in farms:
        risk_mult = {'low': 1.0, 'medium': 0.8, 'high': 0.6}[farm['riskLevel']]
        adj_apy = farm['apy'] * risk_mult
        opportunities.append(('farm', farm, adj_apy))
    
    for stake in stakes:
        # Use 90-day locked APY
        adj_apy = stake['locked']['90days']['apy'] * 0.9  # Discount for lock
        opportunities.append(('stake', stake, adj_apy))
    
    # Sort by adjusted APY
    opportunities.sort(key=lambda x: x[2], reverse=True)
    
    # Allocate to top 3
    top_3 = opportunities[:3]
    for i, (typ, opp, apy) in enumerate(top_3):
        print(f"{i+1}. {typ.upper()}: {opp.get('protocol', opp.get('token'))} - {apy:.1f}% APY")
    
    return top_3
```

### 3. LP Position Manager

```python
class LiquidityManager:
    def __init__(self):
        self.il_threshold = -3.0  # Exit if IL > 3%
        self.profit_target = 10.0  # Take profit at 10%
        
    def manage_positions(self):
        positions = get_liquidity_positions()
        
        for pos in positions['positions']:
            # Check impermanent loss
            if pos['impermanentLoss'] < self.il_threshold:
                print(f"🔴 Exit {pos['pool']}: High IL ({pos['impermanentLoss']:.2f}%)")
                self.exit_position(pos['positionId'])
                
            # Check profits
            elif pos['returnPercent'] > self.profit_target:
                print(f"🟢 Take profit {pos['pool']}: {pos['returnPercent']:.2f}% gain")
                self.exit_position(pos['positionId'])
                
            else:
                print(f"⚪ Hold {pos['pool']}: {pos['returnPercent']:.2f}% return")
```

---

## Support

For DeFi feature support:

- **Documentation**: [API_REFERENCE.md](../API_REFERENCE.md)
- **DeFi Strategy**: [DEFI_INTEGRATION.md](../DEFI_INTEGRATION.md)
- **GitHub Issues**: [https://github.com/thewriterben/crs/issues](https://github.com/thewriterben/crs/issues)

---

**Version**: 3.0.0  
**Last Updated**: September 30, 2024  
**Phase**: 3 Complete ✅
