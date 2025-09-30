#!/usr/bin/env python3
"""
Portfolio Automation for Phase 3
Rebalancing, risk management, DCA, and stop-loss automation
"""

from datetime import datetime, timedelta
from typing import Dict, List
import random


class PortfolioRebalancer:
    """Automated portfolio rebalancing"""
    
    def __init__(self):
        self.rebalance_threshold = 0.05  # 5% drift triggers rebalance
    
    def analyze_portfolio(self, current_allocation: Dict, target_allocation: Dict) -> Dict:
        """Analyze portfolio drift and recommend rebalancing"""
        drifts = {}
        total_drift = 0
        
        for asset, target_pct in target_allocation.items():
            current_pct = current_allocation.get(asset, 0)
            drift = abs(current_pct - target_pct)
            drifts[asset] = {
                'current': current_pct,
                'target': target_pct,
                'drift': drift,
                'action': 'BUY' if current_pct < target_pct else 'SELL' if current_pct > target_pct else 'HOLD'
            }
            total_drift += drift
        
        needs_rebalance = total_drift > self.rebalance_threshold
        
        return {
            'needs_rebalance': needs_rebalance,
            'total_drift': total_drift,
            'drifts': drifts,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_rebalance_orders(self, portfolio_value: float, drifts: Dict) -> List[Dict]:
        """Generate orders to rebalance portfolio"""
        orders = []
        
        for asset, drift_info in drifts.items():
            if drift_info['action'] == 'HOLD':
                continue
            
            target_value = portfolio_value * drift_info['target']
            current_value = portfolio_value * drift_info['current']
            diff_value = target_value - current_value
            
            orders.append({
                'asset': asset,
                'action': drift_info['action'],
                'amount': abs(diff_value),
                'current_allocation': drift_info['current'],
                'target_allocation': drift_info['target']
            })
        
        return orders


class RiskManagementSystem:
    """Advanced risk assessment and position sizing"""
    
    def __init__(self):
        self.max_position_size = 0.20  # Max 20% in single asset
        self.max_portfolio_risk = 0.30  # Max 30% portfolio risk
    
    def calculate_position_size(self, portfolio_value: float, risk_per_trade: float, 
                                stop_loss_pct: float) -> Dict:
        """Calculate optimal position size based on risk"""
        # Risk per trade as percentage of portfolio
        risk_amount = portfolio_value * risk_per_trade
        
        # Position size based on stop loss
        position_size = risk_amount / stop_loss_pct
        
        # Cap at max position size
        max_size = portfolio_value * self.max_position_size
        final_size = min(position_size, max_size)
        
        return {
            'recommended_position': final_size,
            'risk_amount': risk_amount,
            'stop_loss_pct': stop_loss_pct,
            'max_position_limit': max_size,
            'capped': final_size < position_size
        }
    
    def assess_portfolio_risk(self, positions: List[Dict]) -> Dict:
        """Assess overall portfolio risk"""
        total_value = sum(p['value'] for p in positions)
        total_risk = 0
        high_risk_positions = []
        
        for position in positions:
            risk_score = position.get('risk_score', 0.5)
            position_pct = position['value'] / total_value if total_value > 0 else 0
            position_risk = risk_score * position_pct
            total_risk += position_risk
            
            if position_pct > self.max_position_size:
                high_risk_positions.append({
                    'asset': position['symbol'],
                    'allocation': position_pct,
                    'reason': 'Position too large'
                })
        
        risk_level = 'LOW' if total_risk < 0.3 else 'MEDIUM' if total_risk < 0.6 else 'HIGH'
        
        return {
            'total_risk_score': total_risk,
            'risk_level': risk_level,
            'high_risk_positions': high_risk_positions,
            'within_limits': total_risk <= self.max_portfolio_risk,
            'recommendations': self._generate_risk_recommendations(total_risk, high_risk_positions)
        }
    
    def _generate_risk_recommendations(self, risk_score: float, high_risk: List) -> List[str]:
        """Generate risk management recommendations"""
        recommendations = []
        
        if risk_score > self.max_portfolio_risk:
            recommendations.append("Portfolio risk exceeds limits. Consider reducing position sizes.")
        
        if high_risk:
            recommendations.append(f"Reduce exposure in: {', '.join([p['asset'] for p in high_risk])}")
        
        if risk_score < 0.2:
            recommendations.append("Portfolio is very conservative. Consider increasing diversification.")
        
        return recommendations


class DollarCostAveragingSystem:
    """Automated DCA strategies"""
    
    def __init__(self):
        self.schedules = {}
    
    def create_dca_schedule(self, user_id: str, asset: str, amount_per_period: float,
                           frequency: str, duration_months: int) -> Dict:
        """Create DCA schedule"""
        schedule_id = f"dca_{user_id}_{asset}_{int(datetime.now().timestamp())}"
        
        # Calculate schedule
        periods_per_month = {'daily': 30, 'weekly': 4, 'monthly': 1}
        total_periods = duration_months * periods_per_month.get(frequency, 1)
        total_investment = amount_per_period * total_periods
        
        schedule = {
            'schedule_id': schedule_id,
            'user_id': user_id,
            'asset': asset,
            'amount_per_period': amount_per_period,
            'frequency': frequency,
            'duration_months': duration_months,
            'total_periods': total_periods,
            'total_investment': total_investment,
            'started_at': datetime.now(),
            'next_execution': self._calculate_next_execution(frequency),
            'completed_periods': 0,
            'active': True
        }
        
        self.schedules[schedule_id] = schedule
        return schedule
    
    def _calculate_next_execution(self, frequency: str) -> datetime:
        """Calculate next DCA execution time"""
        now = datetime.now()
        if frequency == 'daily':
            return now + timedelta(days=1)
        elif frequency == 'weekly':
            return now + timedelta(weeks=1)
        elif frequency == 'monthly':
            return now + timedelta(days=30)
        return now
    
    def get_active_schedules(self, user_id: str) -> List[Dict]:
        """Get active DCA schedules for user"""
        return [
            {**schedule, 
             'started_at': schedule['started_at'].isoformat(),
             'next_execution': schedule['next_execution'].isoformat()}
            for schedule in self.schedules.values()
            if schedule['user_id'] == user_id and schedule['active']
        ]


class StopLossAutomation:
    """Smart stop-loss and take-profit mechanisms"""
    
    def __init__(self):
        self.active_orders = {}
    
    def create_trailing_stop(self, position_id: str, symbol: str, entry_price: float,
                            trailing_pct: float, take_profit_pct: float = None) -> Dict:
        """Create trailing stop loss order"""
        order_id = f"stop_{position_id}_{int(datetime.now().timestamp())}"
        
        stop_loss_price = entry_price * (1 - trailing_pct)
        take_profit_price = entry_price * (1 + take_profit_pct) if take_profit_pct else None
        
        order = {
            'order_id': order_id,
            'position_id': position_id,
            'symbol': symbol,
            'entry_price': entry_price,
            'current_stop_loss': stop_loss_price,
            'take_profit': take_profit_price,
            'trailing_pct': trailing_pct,
            'highest_price': entry_price,
            'triggered': False,
            'created_at': datetime.now()
        }
        
        self.active_orders[order_id] = order
        return order
    
    def update_trailing_stops(self, current_prices: Dict) -> List[Dict]:
        """Update trailing stop losses based on current prices"""
        triggered_orders = []
        
        for order_id, order in self.active_orders.items():
            if order['triggered']:
                continue
            
            symbol = order['symbol']
            if symbol not in current_prices:
                continue
            
            current_price = current_prices[symbol]
            
            # Update highest price
            if current_price > order['highest_price']:
                order['highest_price'] = current_price
                # Update trailing stop
                new_stop = current_price * (1 - order['trailing_pct'])
                order['current_stop_loss'] = max(order['current_stop_loss'], new_stop)
            
            # Check if stop loss triggered
            if current_price <= order['current_stop_loss']:
                order['triggered'] = True
                order['trigger_price'] = current_price
                order['trigger_time'] = datetime.now()
                triggered_orders.append(order)
            
            # Check if take profit triggered
            if order['take_profit'] and current_price >= order['take_profit']:
                order['triggered'] = True
                order['trigger_price'] = current_price
                order['trigger_time'] = datetime.now()
                order['trigger_reason'] = 'take_profit'
                triggered_orders.append(order)
        
        return triggered_orders
    
    def get_active_stops(self, position_id: str = None) -> List[Dict]:
        """Get active stop loss orders"""
        orders = [o for o in self.active_orders.values() if not o['triggered']]
        
        if position_id:
            orders = [o for o in orders if o['position_id'] == position_id]
        
        return [{**o, 'created_at': o['created_at'].isoformat()} for o in orders]
