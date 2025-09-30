# Portfolio Automation Features Guide

Complete guide to portfolio automation features in the CRS Cryptocurrency Marketplace.

**Version**: 3.0.0  
**Phase**: 3 Complete ✅

---

## Table of Contents

- [Overview](#overview)
- [Portfolio Rebalancing](#portfolio-rebalancing)
- [Risk Management](#risk-management)
- [Dollar-Cost Averaging (DCA)](#dollar-cost-averaging-dca)
- [Stop-Loss Automation](#stop-loss-automation)
- [Best Practices](#best-practices)
- [Use Cases](#use-cases)

---

## Overview

Phase 3 portfolio automation provides hands-free portfolio management:

- **Rebalancing** - Automatic portfolio rebalancing to target allocation
- **Risk Management** - Portfolio risk assessment and position sizing
- **Dollar-Cost Averaging** - Automated recurring purchases
- **Stop-Loss/Take-Profit** - Automated exit strategies

All features work 24/7 to optimize your portfolio while you sleep.

---

## Portfolio Rebalancing

### Overview

Automatically rebalance your portfolio when allocations drift from targets.

### Analyze Rebalancing Needs

**Endpoint**: `POST /api/phase3/portfolio/rebalance/analyze`

**Example**:
```bash
curl -X POST http://localhost:5006/api/phase3/portfolio/rebalance/analyze \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

**Response**:
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
  "estimatedCost": 30.0
}
```

### Generate Rebalancing Orders

**Endpoint**: `POST /api/phase3/portfolio/rebalance/orders`

**Example**:
```bash
curl -X POST http://localhost:5006/api/phase3/portfolio/rebalance/orders \
  -H "Content-Type: application/json" \
  -d '{
    "currentAllocation": {"BTC": 0.45, "ETH": 0.35, "USDT": 0.20},
    "targetAllocation": {"BTC": 0.40, "ETH": 0.30, "USDT": 0.30},
    "totalValue": 100000.0
  }'
```

**Response**:
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
  "estimatedCost": 30.0
}
```

### Automated Rebalancing

```python
class AutoRebalancer:
    def __init__(self, target_allocation, threshold=0.05, frequency='weekly'):
        self.target_allocation = target_allocation
        self.threshold = threshold
        self.frequency = frequency
        
    def check_and_rebalance(self, portfolio):
        """Check if rebalancing is needed and execute."""
        # Calculate current allocation
        total_value = sum(p['value'] for p in portfolio)
        current_allocation = {
            p['asset']: p['value'] / total_value
            for p in portfolio
        }
        
        # Analyze rebalancing needs
        response = requests.post(
            'http://localhost:5006/api/phase3/portfolio/rebalance/analyze',
            json={
                'currentAllocation': current_allocation,
                'targetAllocation': self.target_allocation,
                'totalValue': total_value,
                'threshold': self.threshold
            }
        )
        
        result = response.json()
        
        if not result['needsRebalancing']:
            print("✅ Portfolio is balanced")
            return None
        
        print(f"⚠️  Rebalancing needed")
        for asset, drift in result['drifts'].items():
            print(f"  {asset}: {drift:+.2%} drift")
        
        # Generate orders
        orders_response = requests.post(
            'http://localhost:5006/api/phase3/portfolio/rebalance/orders',
            json={
                'currentAllocation': current_allocation,
                'targetAllocation': self.target_allocation,
                'totalValue': total_value
            }
        )
        
        orders = orders_response.json()['orders']
        
        # Execute orders
        for order in orders:
            print(f"\n{order['type']} {order['amount']:.4f} {order['asset']}")
            # self.execute_order(order)
        
        return orders

# Usage
rebalancer = AutoRebalancer(
    target_allocation={
        'BTC': 0.40,
        'ETH': 0.30,
        'USDT': 0.30
    },
    threshold=0.05,
    frequency='weekly'
)

# Check daily
portfolio = get_current_portfolio()
rebalancer.check_and_rebalance(portfolio)
```

### Rebalancing Strategies

**1. Threshold Rebalancing**
```python
# Rebalance when any asset drifts > 5%
threshold = 0.05
```

**2. Calendar Rebalancing**
```python
# Rebalance on first day of month
import datetime

def should_rebalance_calendar():
    return datetime.date.today().day == 1
```

**3. Hybrid Approach**
```python
def should_rebalance_hybrid(last_rebalance, max_drift):
    # Rebalance if:
    # 1. More than 30 days since last rebalance, OR
    # 2. Drift exceeds 7.5%
    days_since = (datetime.date.today() - last_rebalance).days
    return days_since > 30 or max_drift > 0.075
```

---

## Risk Management

### Overview

Assess and manage portfolio risk with advanced metrics.

### Assess Portfolio Risk

**Endpoint**: `POST /api/phase3/portfolio/risk/assess`

**Example**:
```bash
curl -X POST http://localhost:5006/api/phase3/portfolio/risk/assess \
  -H "Content-Type: application/json" \
  -d '{
    "positions": [
      {"asset": "BTC", "value": 50000.0, "volatility": 0.65},
      {"asset": "ETH", "value": 30000.0, "volatility": 0.72},
      {"asset": "USDT", "value": 20000.0, "volatility": 0.01}
    ]
  }'
```

**Response**:
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
  ]
}
```

### Calculate Position Size

**Endpoint**: `POST /api/phase3/portfolio/position-size`

**Example**:
```bash
curl -X POST http://localhost:5006/api/phase3/portfolio/position-size \
  -H "Content-Type: application/json" \
  -d '{
    "portfolioValue": 100000.0,
    "riskPerTrade": 0.02,
    "entryPrice": 52000.0,
    "stopLoss": 50000.0
  }'
```

**Response**:
```json
{
  "recommendedSize": 0.385,
  "recommendedValue": 20000.0,
  "maxLoss": 2000.0,
  "riskRewardRatio": 2.5,
  "leverageRequired": 0.2,
  "recommendations": "Position sized for 2% portfolio risk"
}
```

### Risk Management System

```python
class RiskManager:
    def __init__(self, max_portfolio_risk=0.20, max_position_risk=0.05):
        self.max_portfolio_risk = max_portfolio_risk
        self.max_position_risk = max_position_risk
        
    def assess_trade(self, portfolio_value, trade):
        """Assess if trade meets risk criteria."""
        # Calculate position size
        response = requests.post(
            'http://localhost:5006/api/phase3/portfolio/position-size',
            json={
                'portfolioValue': portfolio_value,
                'riskPerTrade': self.max_position_risk,
                'entryPrice': trade['entry_price'],
                'stopLoss': trade['stop_loss']
            }
        )
        
        sizing = response.json()
        
        # Check if position fits risk parameters
        if sizing['maxLoss'] / portfolio_value > self.max_position_risk:
            print("❌ Trade exceeds position risk limit")
            return False
        
        if sizing['riskRewardRatio'] < 2.0:
            print("❌ Risk/reward ratio too low")
            return False
        
        print("✅ Trade meets risk criteria")
        print(f"  Position size: ${sizing['recommendedValue']:,.2f}")
        print(f"  Max loss: ${sizing['maxLoss']:,.2f}")
        print(f"  R:R ratio: {sizing['riskRewardRatio']:.2f}x")
        
        return True
    
    def assess_portfolio(self, positions):
        """Assess overall portfolio risk."""
        response = requests.post(
            'http://localhost:5006/api/phase3/portfolio/risk/assess',
            json={'positions': positions}
        )
        
        risk = response.json()
        
        print(f"\nPortfolio Risk Assessment:")
        print(f"Risk Score: {risk['riskScore']:.1f}/10 ({risk['riskLevel']})")
        print(f"Volatility: {risk['volatility']:.2%}")
        print(f"Sharpe Ratio: {risk['sharpeRatio']:.2f}")
        print(f"Max Drawdown: {risk['maxDrawdown']:.2%}")
        print(f"Value at Risk: ${risk['valueAtRisk']:,.2f}")
        
        # Check if portfolio risk is acceptable
        if risk['riskScore'] > 7.0:
            print("\n⚠️  WARNING: High portfolio risk!")
            print("Recommendations:")
            for rec in risk['recommendations']:
                print(f"  • {rec}")
            return False
        
        return True
```

### Kelly Criterion Position Sizing

```python
def kelly_position_size(win_rate, avg_win, avg_loss, portfolio_value):
    """Calculate optimal position size using Kelly Criterion."""
    # Kelly % = W - [(1 - W) / R]
    # Where W = win rate, R = win/loss ratio
    
    win_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0
    kelly_pct = win_rate - ((1 - win_rate) / win_loss_ratio)
    
    # Use fractional Kelly (typically 0.25 to 0.5 of full Kelly)
    fractional_kelly = kelly_pct * 0.25
    
    # Ensure position size is reasonable (max 10% of portfolio)
    position_size = min(fractional_kelly, 0.10) * portfolio_value
    
    return {
        'full_kelly': kelly_pct,
        'fractional_kelly': fractional_kelly,
        'position_size': position_size,
        'position_pct': position_size / portfolio_value
    }

# Example: 65% win rate, $1000 avg win, $500 avg loss
result = kelly_position_size(0.65, 1000, 500, 100000)
print(f"Recommended position: ${result['position_size']:,.2f} ({result['position_pct']:.1%})")
```

---

## Dollar-Cost Averaging (DCA)

### Overview

Automate recurring cryptocurrency purchases to average entry prices.

### Create DCA Schedule

**Endpoint**: `POST /api/phase3/portfolio/dca/create`

**Example**:
```bash
curl -X POST http://localhost:5006/api/phase3/portfolio/dca/create \
  -H "Content-Type: application/json" \
  -d '{
    "asset": "BTC",
    "amount": 100.0,
    "frequency": "weekly",
    "durationMonths": 12,
    "startDate": "2024-10-01"
  }'
```

**Response**:
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

### View DCA Schedules

**Endpoint**: `GET /api/phase3/portfolio/dca/schedules`

**Response**:
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
      "currentValue": 1250.0,
      "profitLoss": 50.0,
      "returnPercent": 4.17
    }
  ]
}
```

### DCA Strategies

**1. Fixed Amount DCA**
```python
def fixed_amount_dca(asset, weekly_amount, duration_months):
    """Invest fixed amount at regular intervals."""
    response = requests.post(
        'http://localhost:5006/api/phase3/portfolio/dca/create',
        json={
            'asset': asset,
            'amount': weekly_amount,
            'frequency': 'weekly',
            'durationMonths': duration_months
        }
    )
    return response.json()

# Example: $100/week BTC for 1 year
schedule = fixed_amount_dca('BTC', 100, 12)
print(f"Total investment: ${schedule['totalInvestment']:,.2f}")
```

**2. Value-Based DCA**
```python
def value_based_dca(asset, target_value, duration_months, frequency='weekly'):
    """Adjust purchase amount based on price."""
    # Calculate base amount
    periods_per_month = {'daily': 30, 'weekly': 4, 'biweekly': 2, 'monthly': 1}
    total_periods = duration_months * periods_per_month[frequency]
    base_amount = target_value / total_periods
    
    # Create schedule
    response = requests.post(
        'http://localhost:5006/api/phase3/portfolio/dca/create',
        json={
            'asset': asset,
            'amount': base_amount,
            'frequency': frequency,
            'durationMonths': duration_months
        }
    )
    
    return response.json()

# Example: Accumulate $10,000 worth of ETH over 6 months
schedule = value_based_dca('ETH', 10000, 6, 'weekly')
```

**3. Market-Responsive DCA**
```python
def market_responsive_dca(asset, base_amount, market_conditions):
    """Adjust DCA amount based on market conditions."""
    # Increase purchases during dips
    if market_conditions['price_change_7d'] < -10:
        amount = base_amount * 1.5  # 50% more during 10%+ dips
    elif market_conditions['price_change_7d'] < -5:
        amount = base_amount * 1.25  # 25% more during 5%+ dips
    else:
        amount = base_amount
    
    print(f"Market adjusted DCA amount: ${amount:.2f}")
    return amount
```

### DCA Performance Tracking

```python
def track_dca_performance():
    """Track all DCA schedules performance."""
    response = requests.get('http://localhost:5006/api/phase3/portfolio/dca/schedules')
    schedules = response.json()['schedules']
    
    print("\nDCA Performance Report")
    print("=" * 80)
    
    for schedule in schedules:
        print(f"\n{schedule['asset']} DCA:")
        print(f"  Total Invested: ${schedule['totalInvested']:,.2f}")
        print(f"  Current Value: ${schedule['currentValue']:,.2f}")
        print(f"  P&L: ${schedule['profitLoss']:+,.2f} ({schedule['returnPercent']:+.2f}%)")
        print(f"  Average Price: ${schedule['averagePrice']:,.2f}")
        print(f"  Total Units: {schedule['totalUnits']:.6f}")
        print(f"  Purchases: {schedule['purchasesCompleted']}/{schedule['purchasesCompleted'] + schedule['purchasesRemaining']}")
        
        # Calculate vs lump sum
        first_purchase_price = get_historical_price(schedule['asset'], schedule['startDate'])
        lump_sum_units = schedule['totalInvested'] / first_purchase_price
        lump_sum_value = lump_sum_units * get_current_price(schedule['asset'])
        
        dca_advantage = schedule['currentValue'] - lump_sum_value
        print(f"  DCA vs Lump Sum: ${dca_advantage:+,.2f}")
    
    # Overall statistics
    total_invested = sum(s['totalInvested'] for s in schedules)
    total_value = sum(s['currentValue'] for s in schedules)
    overall_return = ((total_value - total_invested) / total_invested) * 100
    
    print(f"\n{'='*80}")
    print(f"Overall DCA Performance:")
    print(f"  Total Invested: ${total_invested:,.2f}")
    print(f"  Total Value: ${total_value:,.2f}")
    print(f"  Overall Return: {overall_return:+.2f}%")
```

---

## Stop-Loss Automation

### Overview

Automate exit strategies with stop-loss and take-profit orders.

### Create Stop-Loss Order

**Endpoint**: `POST /api/phase3/portfolio/stop-loss/create`

**Example**:
```bash
curl -X POST http://localhost:5006/api/phase3/portfolio/stop-loss/create \
  -H "Content-Type: application/json" \
  -d '{
    "asset": "BTC",
    "amount": 1.0,
    "stopLossPrice": 50000.0,
    "takeProfitPrice": 60000.0,
    "trailingStop": true,
    "trailingPercent": 5.0
  }'
```

**Response**:
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
  "status": "active"
}
```

### View Active Orders

**Endpoint**: `GET /api/phase3/portfolio/stop-loss/active`

**Response**:
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
      "trailingStopPrice": 49875.0,
      "distanceToStop": -4.76,
      "distanceToTarget": 14.29,
      "status": "active"
    }
  ]
}
```

### Stop-Loss Strategies

**1. Fixed Stop-Loss**
```python
def set_fixed_stop_loss(asset, amount, entry_price, stop_loss_pct=0.05):
    """Set fixed percentage stop-loss."""
    stop_loss_price = entry_price * (1 - stop_loss_pct)
    
    response = requests.post(
        'http://localhost:5006/api/phase3/portfolio/stop-loss/create',
        json={
            'asset': asset,
            'amount': amount,
            'stopLossPrice': stop_loss_price,
            'trailingStop': False
        }
    )
    
    return response.json()

# Example: 5% stop-loss on BTC
order = set_fixed_stop_loss('BTC', 1.0, 52000.0, 0.05)
print(f"Stop-loss set at: ${order['stopLossPrice']:,.2f}")
```

**2. Trailing Stop-Loss**
```python
def set_trailing_stop_loss(asset, amount, trailing_pct=0.05):
    """Set trailing stop-loss that follows price up."""
    current_price = get_current_price(asset)
    
    response = requests.post(
        'http://localhost:5006/api/phase3/portfolio/stop-loss/create',
        json={
            'asset': asset,
            'amount': amount,
            'trailingStop': True,
            'trailingPercent': trailing_pct * 100  # Convert to percentage
        }
    )
    
    order = response.json()
    print(f"Trailing stop set at {trailing_pct:.0%} below price")
    print(f"Current: ${current_price:,.2f}")
    print(f"Stop: ${order['trailingStopPrice']:,.2f}")
    
    return order

# Example: 5% trailing stop on ETH
order = set_trailing_stop_loss('ETH', 10.0, 0.05)
```

**3. Take-Profit with Stop-Loss**
```python
def set_bracket_order(asset, amount, entry_price, stop_pct=0.05, profit_pct=0.15):
    """Set both stop-loss and take-profit."""
    stop_loss_price = entry_price * (1 - stop_pct)
    take_profit_price = entry_price * (1 + profit_pct)
    
    response = requests.post(
        'http://localhost:5006/api/phase3/portfolio/stop-loss/create',
        json={
            'asset': asset,
            'amount': amount,
            'stopLossPrice': stop_loss_price,
            'takeProfitPrice': take_profit_price,
            'trailingStop': False
        }
    )
    
    order = response.json()
    
    print(f"Bracket order created:")
    print(f"  Entry: ${entry_price:,.2f}")
    print(f"  Stop-Loss: ${stop_loss_price:,.2f} (-{stop_pct:.0%})")
    print(f"  Take-Profit: ${take_profit_price:,.2f} (+{profit_pct:.0%})")
    print(f"  Risk/Reward: {profit_pct/stop_pct:.1f}x")
    
    return order

# Example: 5% stop, 15% profit (3:1 R:R)
order = set_bracket_order('BTC', 0.5, 52000.0, 0.05, 0.15)
```

### Stop-Loss Management

```python
class StopLossManager:
    def __init__(self):
        self.orders = []
        
    def create_position_with_stops(self, asset, amount, entry_price, strategy='trailing'):
        """Create position with appropriate stop-loss strategy."""
        if strategy == 'trailing':
            # 5% trailing stop
            order = set_trailing_stop_loss(asset, amount, 0.05)
        elif strategy == 'bracket':
            # 5% stop, 15% profit
            order = set_bracket_order(asset, amount, entry_price, 0.05, 0.15)
        else:
            # Fixed 5% stop
            order = set_fixed_stop_loss(asset, amount, entry_price, 0.05)
        
        self.orders.append(order)
        return order
    
    def monitor_stops(self):
        """Monitor all active stop-loss orders."""
        response = requests.get('http://localhost:5006/api/phase3/portfolio/stop-loss/active')
        active_orders = response.json()['orders']
        
        print("\nActive Stop-Loss Orders:")
        print("=" * 80)
        
        for order in active_orders:
            print(f"\n{order['asset']}:")
            print(f"  Current: ${order['currentPrice']:,.2f}")
            print(f"  Stop: ${order['stopLossPrice']:,.2f} ({order['distanceToStop']:+.2f}%)")
            
            if 'takeProfitPrice' in order:
                print(f"  Target: ${order['takeProfitPrice']:,.2f} ({order['distanceToTarget']:+.2f}%)")
            
            if order.get('trailingStop'):
                print(f"  Trailing: ${order['trailingStopPrice']:,.2f}")
            
            # Alert if close to stop
            if abs(order['distanceToStop']) < 2:
                print(f"  ⚠️  WARNING: Close to stop-loss!")

manager = StopLossManager()
manager.monitor_stops()
```

---

## Best Practices

### 1. Complete Automation Strategy

```python
class PortfolioAutomationSystem:
    def __init__(self, portfolio_value, risk_tolerance='medium'):
        self.portfolio_value = portfolio_value
        self.risk_tolerance = risk_tolerance
        
        # Initialize sub-systems
        self.rebalancer = AutoRebalancer(
            target_allocation={'BTC': 0.40, 'ETH': 0.30, 'USDT': 0.30},
            threshold=0.05,
            frequency='weekly'
        )
        
        self.risk_manager = RiskManager(
            max_portfolio_risk=0.20,
            max_position_risk=0.05
        )
        
        self.stop_manager = StopLossManager()
        
    def setup_dca(self):
        """Setup DCA for major holdings."""
        # BTC DCA
        create_dca('BTC', amount=100, frequency='weekly', duration=12)
        
        # ETH DCA
        create_dca('ETH', amount=75, frequency='weekly', duration=12)
        
    def daily_routine(self):
        """Run daily automation tasks."""
        print("\n📊 Running Daily Automation...")
        
        # 1. Check rebalancing
        portfolio = get_current_portfolio()
        self.rebalancer.check_and_rebalance(portfolio)
        
        # 2. Assess risk
        positions = get_positions()
        self.risk_manager.assess_portfolio(positions)
        
        # 3. Monitor stops
        self.stop_manager.monitor_stops()
        
        # 4. DCA purchases (if scheduled)
        execute_scheduled_dca()
        
        print("✅ Automation complete\n")

# Usage
system = PortfolioAutomationSystem(portfolio_value=100000, risk_tolerance='medium')
system.setup_dca()
system.daily_routine()
```

### 2. Performance Monitoring

```python
def generate_automation_report():
    """Generate comprehensive automation performance report."""
    # Rebalancing stats
    rebalances = get_rebalancing_history()
    avg_drift_reduction = sum(r['drift_reduced'] for r in rebalances) / len(rebalances)
    
    # DCA performance
    dca_schedules = get_dca_schedules()
    dca_total_return = sum(s['returnPercent'] for s in dca_schedules) / len(dca_schedules)
    
    # Stop-loss effectiveness
    triggered_stops = get_triggered_stops()
    stops_saved = sum(s['amount_saved'] for s in triggered_stops)
    
    print("\nAutomation Performance Report")
    print("=" * 80)
    print(f"\nRebalancing:")
    print(f"  Total rebalances: {len(rebalances)}")
    print(f"  Avg drift reduction: {avg_drift_reduction:.2%}")
    
    print(f"\nDCA Performance:")
    print(f"  Active schedules: {len(dca_schedules)}")
    print(f"  Average return: {dca_total_return:+.2f}%")
    
    print(f"\nStop-Loss Protection:")
    print(f"  Stops triggered: {len(triggered_stops)}")
    print(f"  Total saved: ${stops_saved:,.2f}")
```

---

## Use Cases

### 1. Set-and-Forget Portfolio

```python
class SetAndForgetStrategy:
    def __init__(self, initial_capital):
        self.capital = initial_capital
        
    def setup(self):
        # Target allocation
        allocation = {'BTC': 0.40, 'ETH': 0.30, 'SOL': 0.15, 'USDT': 0.15}
        
        # 1. Buy initial positions
        for asset, pct in allocation.items():
            amount = self.capital * pct
            buy_asset(asset, amount)
        
        # 2. Setup monthly rebalancing
        setup_rebalancer(allocation, threshold=0.10, frequency='monthly')
        
        # 3. Setup DCA for additional investment
        setup_dca('BTC', amount=200, frequency='biweekly', duration=12)
        setup_dca('ETH', amount=150, frequency='biweekly', duration=12)
        
        # 4. Set portfolio-wide stop-loss
        for asset in ['BTC', 'ETH', 'SOL']:
            set_trailing_stop_loss(asset, get_holdings(asset), 0.15)  # 15% trailing
        
        print("✅ Set-and-forget portfolio configured")
        print("   Next action required in 1 month")
```

### 2. Active Trader Automation

```python
class ActiveTraderAutomation:
    def __init__(self, trading_capital):
        self.capital = trading_capital
        
    def setup(self):
        # Daily rebalancing for active management
        setup_rebalancer(
            target_allocation={'BTC': 0.50, 'ETH': 0.30, 'USDT': 0.20},
            threshold=0.03,  # Tighter threshold
            frequency='daily'
        )
        
        # Tight stops for active trading
        for position in get_open_positions():
            set_bracket_order(
                asset=position['asset'],
                amount=position['amount'],
                entry_price=position['entry_price'],
                stop_pct=0.03,  # 3% stop
                profit_pct=0.09  # 9% profit (3:1 R:R)
            )
        
        # No DCA (active management instead)
        
    def daily_management(self):
        # Check all automations
        check_rebalancing()
        monitor_stops()
        assess_risk()
        
        # Manual signal trading on top of automation
        signals = get_trading_signals()
        for signal in signals:
            if signal['confidence'] > 0.85:
                execute_signal_with_automation(signal)
```

### 3. Conservative Income Strategy

```python
class ConservativeIncomeStrategy:
    def __init__(self, capital):
        self.capital = capital
        
    def setup(self):
        # Conservative allocation
        allocation = {'USDT': 0.40, 'BTC': 0.30, 'ETH': 0.20, 'BUSD': 0.10}
        
        # Quarterly rebalancing (less frequent)
        setup_rebalancer(allocation, threshold=0.15, frequency='quarterly')
        
        # Consistent DCA into majors
        setup_dca('BTC', amount=500, frequency='monthly', duration=24)
        setup_dca('ETH', amount=300, frequency='monthly', duration=24)
        
        # Wide stops (conservative)
        set_fixed_stop_loss('BTC', get_holdings('BTC'), get_price('BTC'), 0.25)
        set_fixed_stop_loss('ETH', get_holdings('ETH'), get_price('ETH'), 0.25)
        
        # Focus on yield (from DeFi module)
        setup_yield_farming('USDT', amount=self.capital * 0.30)
        
        print("✅ Conservative income strategy configured")
```

---

## Support

For portfolio automation support:

- **Documentation**: [API_REFERENCE.md](../API_REFERENCE.md)
- **GitHub Issues**: [https://github.com/thewriterben/crs/issues](https://github.com/thewriterben/crs/issues)

---

**Version**: 3.0.0  
**Last Updated**: September 30, 2024  
**Phase**: 3 Complete ✅
