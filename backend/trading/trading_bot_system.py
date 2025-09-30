#!/usr/bin/env python3
"""
Automated Trading Bot System for AI-Driven Marketplace
Advanced trading strategies with risk management and performance tracking
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import random
import time
import threading
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from ai_prediction_engine import PredictionAPI

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"

class OrderStatus(Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    PARTIAL = "partial"

class BotStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"

@dataclass
class TradingOrder:
    """Structure for trading orders"""
    order_id: str
    bot_id: str
    symbol: str
    side: str  # 'buy' or 'sell'
    order_type: OrderType
    quantity: float
    price: Optional[float]
    stop_price: Optional[float]
    status: OrderStatus
    created_at: datetime
    filled_at: Optional[datetime] = None
    filled_price: Optional[float] = None
    filled_quantity: float = 0.0

@dataclass
class Position:
    """Structure for trading positions"""
    symbol: str
    quantity: float
    average_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float
    entry_time: datetime

@dataclass
class BotPerformance:
    """Structure for bot performance metrics"""
    total_trades: int
    winning_trades: int
    losing_trades: int
    total_pnl: float
    win_rate: float
    average_win: float
    average_loss: float
    max_drawdown: float
    sharpe_ratio: float
    start_balance: float
    current_balance: float

class TradingStrategy:
    """Base class for trading strategies"""
    
    def __init__(self, name: str, parameters: Dict):
        self.name = name
        self.parameters = parameters
        self.prediction_api = PredictionAPI()
    
    def should_buy(self, symbol: str, market_data: Dict, position: Optional[Position]) -> Tuple[bool, float]:
        """Determine if should buy and quantity"""
        raise NotImplementedError
    
    def should_sell(self, symbol: str, market_data: Dict, position: Position) -> Tuple[bool, float]:
        """Determine if should sell and quantity"""
        raise NotImplementedError
    
    def calculate_position_size(self, symbol: str, price: float, balance: float) -> float:
        """Calculate position size based on risk management"""
        risk_per_trade = self.parameters.get('risk_per_trade', 0.02)  # 2% risk
        max_position_size = balance * risk_per_trade / price
        return max_position_size

class MomentumStrategy(TradingStrategy):
    """Momentum-based trading strategy"""
    
    def __init__(self, parameters: Dict = None):
        default_params = {
            'momentum_threshold': 0.03,  # 3% price movement
            'prediction_confidence_min': 0.7,
            'risk_per_trade': 0.02,
            'stop_loss_pct': 0.05,  # 5% stop loss
            'take_profit_pct': 0.10  # 10% take profit
        }
        if parameters:
            default_params.update(parameters)
        super().__init__("Momentum Strategy", default_params)
    
    def should_buy(self, symbol: str, market_data: Dict, position: Optional[Position]) -> Tuple[bool, float]:
        """Buy on strong upward momentum with AI confirmation"""
        if position is not None:  # Already have position
            return False, 0.0
        
        # Get AI prediction
        prediction = self.prediction_api.get_prediction(symbol, '1h')
        if 'error' in prediction:
            return False, 0.0
        
        # Check momentum and AI confidence
        price_change_pct = prediction.get('price_change_percent', 0)
        confidence = prediction.get('confidence', 0)
        recommendation = prediction.get('recommendation', 'HOLD')
        
        momentum_signal = price_change_pct > self.parameters['momentum_threshold'] * 100
        ai_signal = (confidence > self.parameters['prediction_confidence_min'] and 
                    recommendation in ['BUY', 'STRONG_BUY'])
        
        if momentum_signal and ai_signal:
            current_price = prediction['current_price']
            balance = market_data.get('balance', 10000)  # Default balance
            quantity = self.calculate_position_size(symbol, current_price, balance)
            return True, quantity
        
        return False, 0.0
    
    def should_sell(self, symbol: str, market_data: Dict, position: Position) -> Tuple[bool, float]:
        """Sell on momentum reversal or stop loss/take profit"""
        # Get AI prediction
        prediction = self.prediction_api.get_prediction(symbol, '1h')
        if 'error' in prediction:
            return False, 0.0
        
        current_price = prediction['current_price']
        entry_price = position.average_price
        
        # Calculate P&L percentage
        pnl_pct = (current_price - entry_price) / entry_price
        
        # Stop loss
        if pnl_pct <= -self.parameters['stop_loss_pct']:
            return True, position.quantity
        
        # Take profit
        if pnl_pct >= self.parameters['take_profit_pct']:
            return True, position.quantity
        
        # Momentum reversal
        price_change_pct = prediction.get('price_change_percent', 0)
        confidence = prediction.get('confidence', 0)
        recommendation = prediction.get('recommendation', 'HOLD')
        
        reversal_signal = (price_change_pct < -self.parameters['momentum_threshold'] * 100 and
                          confidence > self.parameters['prediction_confidence_min'] and
                          recommendation in ['SELL', 'STRONG_SELL'])
        
        if reversal_signal:
            return True, position.quantity
        
        return False, 0.0

class MeanReversionStrategy(TradingStrategy):
    """Mean reversion trading strategy"""
    
    def __init__(self, parameters: Dict = None):
        default_params = {
            'oversold_threshold': 30,  # RSI threshold
            'overbought_threshold': 70,
            'prediction_confidence_min': 0.6,
            'risk_per_trade': 0.015,
            'stop_loss_pct': 0.04,
            'take_profit_pct': 0.08
        }
        if parameters:
            default_params.update(parameters)
        super().__init__("Mean Reversion Strategy", default_params)
    
    def should_buy(self, symbol: str, market_data: Dict, position: Optional[Position]) -> Tuple[bool, float]:
        """Buy when oversold with AI confirmation"""
        if position is not None:
            return False, 0.0
        
        # Get AI prediction
        prediction = self.prediction_api.get_prediction(symbol, '1h')
        if 'error' in prediction:
            return False, 0.0
        
        # Simulate RSI calculation (would use real technical indicators in production)
        rsi = random.uniform(20, 80)  # Simulated RSI
        confidence = prediction.get('confidence', 0)
        recommendation = prediction.get('recommendation', 'HOLD')
        
        oversold_signal = rsi < self.parameters['oversold_threshold']
        ai_signal = (confidence > self.parameters['prediction_confidence_min'] and
                    recommendation in ['BUY', 'STRONG_BUY'])
        
        if oversold_signal and ai_signal:
            current_price = prediction['current_price']
            balance = market_data.get('balance', 10000)
            quantity = self.calculate_position_size(symbol, current_price, balance)
            return True, quantity
        
        return False, 0.0
    
    def should_sell(self, symbol: str, market_data: Dict, position: Position) -> Tuple[bool, float]:
        """Sell when overbought or stop loss/take profit"""
        prediction = self.prediction_api.get_prediction(symbol, '1h')
        if 'error' in prediction:
            return False, 0.0
        
        current_price = prediction['current_price']
        entry_price = position.average_price
        pnl_pct = (current_price - entry_price) / entry_price
        
        # Stop loss / Take profit
        if pnl_pct <= -self.parameters['stop_loss_pct']:
            return True, position.quantity
        if pnl_pct >= self.parameters['take_profit_pct']:
            return True, position.quantity
        
        # Overbought signal
        rsi = random.uniform(20, 80)  # Simulated RSI
        confidence = prediction.get('confidence', 0)
        
        overbought_signal = (rsi > self.parameters['overbought_threshold'] and
                           confidence > self.parameters['prediction_confidence_min'])
        
        if overbought_signal:
            return True, position.quantity
        
        return False, 0.0

class TradingBot:
    """Automated trading bot with strategy execution"""
    
    def __init__(self, bot_id: str, name: str, strategy: TradingStrategy, 
                 symbols: List[str], initial_balance: float = 10000):
        self.bot_id = bot_id
        self.name = name
        self.strategy = strategy
        self.symbols = symbols
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.status = BotStatus.STOPPED
        self.positions: Dict[str, Position] = {}
        self.orders: List[TradingOrder] = []
        self.trade_history: List[Dict] = []
        self.performance_history: List[BotPerformance] = []
        self.created_at = datetime.now()
        self.last_update = datetime.now()
        self.is_running = False
        self.thread = None
    
    def start(self):
        """Start the trading bot"""
        if self.status == BotStatus.ACTIVE:
            return
        
        self.status = BotStatus.ACTIVE
        self.is_running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"Trading bot {self.name} started")
    
    def stop(self):
        """Stop the trading bot"""
        self.status = BotStatus.STOPPED
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
        print(f"Trading bot {self.name} stopped")
    
    def pause(self):
        """Pause the trading bot"""
        self.status = BotStatus.PAUSED
        print(f"Trading bot {self.name} paused")
    
    def resume(self):
        """Resume the trading bot"""
        if self.status == BotStatus.PAUSED:
            self.status = BotStatus.ACTIVE
            print(f"Trading bot {self.name} resumed")
    
    def _run_loop(self):
        """Main trading loop"""
        while self.is_running:
            try:
                if self.status == BotStatus.ACTIVE:
                    self._execute_strategy()
                    self._update_positions()
                    self._calculate_performance()
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Error in bot {self.name}: {e}")
                self.status = BotStatus.ERROR
                time.sleep(60)  # Wait before retrying
    
    def _execute_strategy(self):
        """Execute trading strategy for all symbols"""
        for symbol in self.symbols:
            try:
                market_data = {'balance': self.current_balance}
                position = self.positions.get(symbol)
                
                # Check for buy signals
                should_buy, buy_quantity = self.strategy.should_buy(symbol, market_data, position)
                if should_buy and buy_quantity > 0:
                    self._place_order(symbol, 'buy', buy_quantity, OrderType.MARKET)
                
                # Check for sell signals
                if position:
                    should_sell, sell_quantity = self.strategy.should_sell(symbol, market_data, position)
                    if should_sell and sell_quantity > 0:
                        self._place_order(symbol, 'sell', sell_quantity, OrderType.MARKET)
                
            except Exception as e:
                print(f"Error executing strategy for {symbol}: {e}")
    
    def _place_order(self, symbol: str, side: str, quantity: float, order_type: OrderType, 
                    price: Optional[float] = None):
        """Place a trading order"""
        order_id = str(uuid.uuid4())
        
        order = TradingOrder(
            order_id=order_id,
            bot_id=self.bot_id,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=None,
            status=OrderStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.orders.append(order)
        
        # Simulate order execution (in production, this would interact with exchange API)
        self._simulate_order_execution(order)
    
    def _simulate_order_execution(self, order: TradingOrder):
        """Simulate order execution for demo purposes"""
        # Get current market price
        prediction_api = PredictionAPI()
        prediction = prediction_api.get_prediction(order.symbol, '1h')
        
        if 'error' in prediction:
            order.status = OrderStatus.CANCELLED
            return
        
        current_price = prediction['current_price']
        
        # Simulate market order execution
        if order.order_type == OrderType.MARKET:
            order.status = OrderStatus.FILLED
            order.filled_at = datetime.now()
            order.filled_price = current_price
            order.filled_quantity = order.quantity
            
            # Update position
            self._update_position_from_order(order)
            
            # Record trade
            self._record_trade(order)
    
    def _update_position_from_order(self, order: TradingOrder):
        """Update position based on filled order"""
        symbol = order.symbol
        
        if order.side == 'buy':
            if symbol in self.positions:
                # Add to existing position
                pos = self.positions[symbol]
                total_cost = (pos.quantity * pos.average_price) + (order.filled_quantity * order.filled_price)
                total_quantity = pos.quantity + order.filled_quantity
                pos.average_price = total_cost / total_quantity
                pos.quantity = total_quantity
            else:
                # Create new position
                self.positions[symbol] = Position(
                    symbol=symbol,
                    quantity=order.filled_quantity,
                    average_price=order.filled_price,
                    current_price=order.filled_price,
                    unrealized_pnl=0.0,
                    realized_pnl=0.0,
                    entry_time=order.filled_at
                )
            
            # Update balance
            self.current_balance -= order.filled_quantity * order.filled_price
            
        elif order.side == 'sell':
            if symbol in self.positions:
                pos = self.positions[symbol]
                
                # Calculate realized P&L
                realized_pnl = (order.filled_price - pos.average_price) * order.filled_quantity
                pos.realized_pnl += realized_pnl
                
                # Update position
                pos.quantity -= order.filled_quantity
                
                # Update balance
                self.current_balance += order.filled_quantity * order.filled_price
                
                # Remove position if fully closed
                if pos.quantity <= 0:
                    del self.positions[symbol]
    
    def _update_positions(self):
        """Update current prices and unrealized P&L for all positions"""
        prediction_api = PredictionAPI()
        
        for symbol, position in self.positions.items():
            prediction = prediction_api.get_prediction(symbol, '1h')
            if 'error' not in prediction:
                position.current_price = prediction['current_price']
                position.unrealized_pnl = (position.current_price - position.average_price) * position.quantity
    
    def _record_trade(self, order: TradingOrder):
        """Record completed trade"""
        trade = {
            'trade_id': str(uuid.uuid4()),
            'bot_id': self.bot_id,
            'symbol': order.symbol,
            'side': order.side,
            'quantity': order.filled_quantity,
            'price': order.filled_price,
            'timestamp': order.filled_at.isoformat(),
            'strategy': self.strategy.name
        }
        
        self.trade_history.append(trade)
    
    def _calculate_performance(self):
        """Calculate bot performance metrics"""
        if not self.trade_history:
            return
        
        # Calculate basic metrics
        total_trades = len(self.trade_history)
        total_pnl = sum(pos.realized_pnl + pos.unrealized_pnl for pos in self.positions.values())
        total_pnl += self.current_balance - self.initial_balance
        
        # Calculate win/loss metrics (simplified)
        winning_trades = sum(1 for pos in self.positions.values() if pos.unrealized_pnl > 0)
        losing_trades = sum(1 for pos in self.positions.values() if pos.unrealized_pnl < 0)
        
        win_rate = winning_trades / max(1, winning_trades + losing_trades)
        
        performance = BotPerformance(
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            total_pnl=total_pnl,
            win_rate=win_rate,
            average_win=total_pnl / max(1, winning_trades) if winning_trades > 0 else 0,
            average_loss=total_pnl / max(1, losing_trades) if losing_trades > 0 else 0,
            max_drawdown=0.0,  # Simplified
            sharpe_ratio=random.uniform(0.5, 2.0),  # Simulated
            start_balance=self.initial_balance,
            current_balance=self.current_balance
        )
        
        self.performance_history.append(performance)
        self.last_update = datetime.now()
    
    def get_status(self) -> Dict:
        """Get bot status and performance"""
        return {
            'bot_id': self.bot_id,
            'name': self.name,
            'status': self.status.value,
            'strategy': self.strategy.name,
            'symbols': self.symbols,
            'current_balance': self.current_balance,
            'initial_balance': self.initial_balance,
            'total_pnl': self.current_balance - self.initial_balance,
            'total_trades': len(self.trade_history),
            'active_positions': len(self.positions),
            'last_update': self.last_update.isoformat(),
            'created_at': self.created_at.isoformat()
        }
    
    def get_positions(self) -> List[Dict]:
        """Get current positions"""
        return [
            {
                'symbol': pos.symbol,
                'quantity': pos.quantity,
                'average_price': pos.average_price,
                'current_price': pos.current_price,
                'unrealized_pnl': pos.unrealized_pnl,
                'realized_pnl': pos.realized_pnl,
                'entry_time': pos.entry_time.isoformat()
            }
            for pos in self.positions.values()
        ]
    
    def get_trade_history(self, limit: int = 50) -> List[Dict]:
        """Get recent trade history"""
        return self.trade_history[-limit:]

class TradingBotManager:
    """Manager for multiple trading bots"""
    
    def __init__(self):
        self.bots: Dict[str, TradingBot] = {}
        self.strategies = {
            'momentum': MomentumStrategy,
            'mean_reversion': MeanReversionStrategy
        }
    
    def create_bot(self, name: str, strategy_name: str, symbols: List[str], 
                  initial_balance: float = 10000, strategy_params: Dict = None) -> str:
        """Create a new trading bot"""
        bot_id = str(uuid.uuid4())
        
        if strategy_name not in self.strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        strategy_class = self.strategies[strategy_name]
        strategy = strategy_class(strategy_params)
        
        bot = TradingBot(bot_id, name, strategy, symbols, initial_balance)
        self.bots[bot_id] = bot
        
        return bot_id
    
    def start_bot(self, bot_id: str):
        """Start a trading bot"""
        if bot_id in self.bots:
            self.bots[bot_id].start()
    
    def stop_bot(self, bot_id: str):
        """Stop a trading bot"""
        if bot_id in self.bots:
            self.bots[bot_id].stop()
    
    def pause_bot(self, bot_id: str):
        """Pause a trading bot"""
        if bot_id in self.bots:
            self.bots[bot_id].pause()
    
    def resume_bot(self, bot_id: str):
        """Resume a trading bot"""
        if bot_id in self.bots:
            self.bots[bot_id].resume()
    
    def delete_bot(self, bot_id: str):
        """Delete a trading bot"""
        if bot_id in self.bots:
            self.bots[bot_id].stop()
            del self.bots[bot_id]
    
    def get_all_bots(self) -> List[Dict]:
        """Get status of all bots"""
        return [bot.get_status() for bot in self.bots.values()]
    
    def get_bot_details(self, bot_id: str) -> Optional[Dict]:
        """Get detailed information about a specific bot"""
        if bot_id not in self.bots:
            return None
        
        bot = self.bots[bot_id]
        return {
            'status': bot.get_status(),
            'positions': bot.get_positions(),
            'trade_history': bot.get_trade_history(),
            'performance': bot.performance_history[-1].__dict__ if bot.performance_history else None
        }
    
    def get_available_strategies(self) -> List[Dict]:
        """Get list of available trading strategies"""
        return [
            {
                'name': 'momentum',
                'display_name': 'Momentum Strategy',
                'description': 'Trades based on price momentum and AI predictions',
                'parameters': {
                    'momentum_threshold': 0.03,
                    'prediction_confidence_min': 0.7,
                    'risk_per_trade': 0.02,
                    'stop_loss_pct': 0.05,
                    'take_profit_pct': 0.10
                }
            },
            {
                'name': 'mean_reversion',
                'display_name': 'Mean Reversion Strategy',
                'description': 'Trades based on overbought/oversold conditions',
                'parameters': {
                    'oversold_threshold': 30,
                    'overbought_threshold': 70,
                    'prediction_confidence_min': 0.6,
                    'risk_per_trade': 0.015,
                    'stop_loss_pct': 0.04,
                    'take_profit_pct': 0.08
                }
            }
        ]

if __name__ == "__main__":
    # Test the trading bot system
    print("Testing Trading Bot System...")
    
    manager = TradingBotManager()
    
    # Create test bots
    momentum_bot_id = manager.create_bot(
        name="BTC Momentum Bot",
        strategy_name="momentum",
        symbols=["BTC"],
        initial_balance=10000
    )
    
    mean_reversion_bot_id = manager.create_bot(
        name="ETH Mean Reversion Bot",
        strategy_name="mean_reversion",
        symbols=["ETH"],
        initial_balance=5000
    )
    
    print(f"Created momentum bot: {momentum_bot_id}")
    print(f"Created mean reversion bot: {mean_reversion_bot_id}")
    
    # Start bots
    manager.start_bot(momentum_bot_id)
    manager.start_bot(mean_reversion_bot_id)
    
    # Wait a bit for bots to run
    time.sleep(5)
    
    # Get bot status
    all_bots = manager.get_all_bots()
    print(f"Active bots: {len(all_bots)}")
    for bot in all_bots:
        print(f"Bot {bot['name']}: {bot['status']} - Balance: ${bot['current_balance']:.2f}")
    
    # Stop bots
    manager.stop_bot(momentum_bot_id)
    manager.stop_bot(mean_reversion_bot_id)
    
    print("Trading Bot System test completed successfully!")

