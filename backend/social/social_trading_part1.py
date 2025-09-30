#!/usr/bin/env python3
"""
Social Trading Features for Phase 3 - Part 1
Core classes and data structures
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import random


@dataclass
class TraderProfile:
    """Profile of a trader"""
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
    """Trading signal"""
    signal_id: str
    symbol: str
    signal_type: str
    strength: float
    confidence: float
    price_target: float
    stop_loss: float
    take_profit: float
    timeframe: str
    reasoning: str
    created_at: datetime
    expires_at: datetime


@dataclass  
class CopyTradePosition:
    """Copy trading position"""
    position_id: str
    follower_id: str
    trader_id: str
    symbol: str
    entry_price: float
    current_price: float
    quantity: float
    pnl: float
    pnl_percent: float
    opened_at: datetime


@dataclass
class SharedPortfolio:
    """Shared portfolio"""
    portfolio_id: str
    owner_id: str
    owner_username: str
    total_value: float
    daily_return: float
    monthly_return: float
    yearly_return: float
    risk_score: float
    assets: List[Dict]
    followers: int
    likes: int
    is_public: bool
