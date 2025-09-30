#!/usr/bin/env python3
"""
Social Trading Features for Phase 3
Copy trading, signals, portfolio sharing, and community
"""

from datetime import datetime, timedelta
from typing import Dict, List
from dataclasses import dataclass, asdict
import random


@dataclass
class TraderProfile:
    trader_id: str
    username: str
    total_followers: int
    win_rate: float
    total_trades: int
    avg_return: float
    risk_score: str
    specialization: List[str]
    rank: int
    verified: bool


@dataclass
class TradingSignal:
    signal_id: str
    symbol: str
    signal_type: str
    strength: float
    confidence: float
    price_target: float
    stop_loss: float
    reasoning: str
    created_at: datetime


class CopyTradingSystem:
    def __init__(self):
        self.traders = {
            'trader_001': TraderProfile('trader_001', 'CryptoMaster', 2547, 0.72, 1250, 0.18, 'MEDIUM', ['BTC', 'ETH'], 1, True),
            'trader_002': TraderProfile('trader_002', 'DeFiExpert', 1823, 0.68, 980, 0.25, 'HIGH', ['DeFi'], 2, True),
            'trader_003': TraderProfile('trader_003', 'SafeInvestor', 3102, 0.65, 2100, 0.12, 'LOW', ['Stablecoins'], 3, True),
        }
        self.follower_relationships = {}
    
    def get_top_traders(self, limit=10):
        return [asdict(t) for t in sorted(self.traders.values(), key=lambda x: x.rank)][:limit]
    
    def follow_trader(self, follower_id, trader_id, copy_amount):
        if trader_id not in self.traders:
            raise ValueError(f"Trader not found: {trader_id}")
        
        if follower_id not in self.follower_relationships:
            self.follower_relationships[follower_id] = []
        
        self.follower_relationships[follower_id].append({
            'trader_id': trader_id,
            'copy_amount': copy_amount,
            'started_at': datetime.now(),
            'active': True
        })
        
        self.traders[trader_id].total_followers += 1
        return {'success': True, 'trader': asdict(self.traders[trader_id])}


class TradingSignalsGenerator:
    def __init__(self):
        self.active_signals = []
        self._generate_signals()
    
    def _generate_signals(self):
        symbols = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL']
        for symbol in symbols:
            signal_type = random.choice(['BUY', 'SELL', 'HOLD'])
            self.active_signals.append(TradingSignal(
                signal_id=f"sig_{symbol}_{int(datetime.now().timestamp())}",
                symbol=symbol,
                signal_type=signal_type,
                strength=random.uniform(0.6, 0.95),
                confidence=random.uniform(0.65, 0.90),
                price_target=45000 * random.uniform(0.9, 1.1),
                stop_loss=45000 * 0.95,
                reasoning=f"AI analysis shows {signal_type} signal for {symbol}",
                created_at=datetime.now()
            ))
    
    def get_signals(self, symbol=None):
        signals = self.active_signals
        if symbol:
            signals = [s for s in signals if s.symbol == symbol]
        return [asdict(s) for s in signals]


class PortfolioSharingSystem:
    def __init__(self):
        self.portfolios = {
            'p1': {'id': 'p1', 'owner': 'SafeInvestor', 'value': 150000, 'return': 15.8, 'followers': 3102},
            'p2': {'id': 'p2', 'owner': 'DeFiExpert', 'value': 95000, 'return': 45.2, 'followers': 1823},
            'p3': {'id': 'p3', 'owner': 'CryptoMaster', 'value': 220000, 'return': 25.3, 'followers': 2547},
        }
    
    def get_featured_portfolios(self, sort_by='followers'):
        portfolios = list(self.portfolios.values())
        if sort_by == 'return':
            portfolios.sort(key=lambda x: x['return'], reverse=True)
        else:
            portfolios.sort(key=lambda x: x['followers'], reverse=True)
        return portfolios
