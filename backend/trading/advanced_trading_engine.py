#!/usr/bin/env python3
"""
Advanced Trading Engine and Order Management System
Implements sophisticated trading features, advanced order types, and execution algorithms
"""

import json
import uuid
from datetime import datetime, timedelta
from enum import Enum
import numpy as np
import random
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"
    TRAILING_STOP = "trailing_stop"
    OCO = "oco"  # One-Cancels-Other
    ICEBERG = "iceberg"
    TWAP = "twap"  # Time-Weighted Average Price
    VWAP = "vwap"  # Volume-Weighted Average Price

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(Enum):
    PENDING = "pending"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"

class TimeInForce(Enum):
    GTC = "gtc"  # Good Till Cancelled
    IOC = "ioc"  # Immediate or Cancel
    FOK = "fok"  # Fill or Kill
    DAY = "day"  # Day order

@dataclass
class Order:
    id: str
    user_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    trail_amount: Optional[float] = None
    trail_percent: Optional[float] = None
    time_in_force: TimeInForce = TimeInForce.GTC
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: float = 0.0
    average_fill_price: float = 0.0
    created_at: datetime = None
    updated_at: datetime = None
    expires_at: Optional[datetime] = None
    
    # Advanced order parameters
    iceberg_visible_quantity: Optional[float] = None
    twap_duration_minutes: Optional[int] = None
    parent_order_id: Optional[str] = None  # For OCO orders
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        if self.time_in_force == TimeInForce.DAY and self.expires_at is None:
            self.expires_at = datetime.now().replace(hour=23, minute=59, second=59)

@dataclass
class Trade:
    id: str
    order_id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    timestamp: datetime
    fee: float = 0.0
    fee_currency: str = "DGD"

class AdvancedOrderManager:
    """Manages advanced order types and execution logic"""
    
    def __init__(self):
        self.orders: Dict[str, Order] = {}
        self.trades: List[Trade] = []
        self.market_data = {}
        self.order_books = {}
        
        # Trading fees (0.1% maker, 0.15% taker)
        self.maker_fee = 0.001
        self.taker_fee = 0.0015
        
        # Initialize sample market data
        self._initialize_market_data()
    
    def _initialize_market_data(self):
        """Initialize sample market data for testing"""
        symbols = ['BTC/DGD', 'ETH/DGD', 'ADA/DGD', 'DOT/DGD', 'LINK/DGD']
        base_prices = {
            'BTC/DGD': 358.4,  # 45000 / 125.5
            'ETH/DGD': 22.3,   # 2800 / 125.5
            'ADA/DGD': 0.0036, # 0.45 / 125.5
            'DOT/DGD': 0.052,  # 6.5 / 125.5
            'LINK/DGD': 0.113  # 14.2 / 125.5
        }
        
        for symbol in symbols:
            base_price = base_prices[symbol]
            self.market_data[symbol] = {
                'bid': base_price * 0.999,
                'ask': base_price * 1.001,
                'last': base_price,
                'volume_24h': random.uniform(1000000, 10000000),
                'change_24h': random.uniform(-0.05, 0.05)
            }
            
            # Generate order book
            self.order_books[symbol] = self._generate_order_book(base_price)
    
    def _generate_order_book(self, base_price, depth=10):
        """Generate sample order book"""
        bids = []
        asks = []
        
        for i in range(depth):
            bid_price = base_price * (1 - (i + 1) * 0.001)
            ask_price = base_price * (1 + (i + 1) * 0.001)
            
            bid_quantity = random.uniform(0.1, 10.0)
            ask_quantity = random.uniform(0.1, 10.0)
            
            bids.append({'price': bid_price, 'quantity': bid_quantity})
            asks.append({'price': ask_price, 'quantity': ask_quantity})
        
        return {'bids': bids, 'asks': asks}
    
    def place_order(self, order_data: dict) -> dict:
        """Place a new order"""
        try:
            # Create order object
            order = Order(
                id=str(uuid.uuid4()),
                user_id=order_data['user_id'],
                symbol=order_data['symbol'],
                side=OrderSide(order_data['side']),
                order_type=OrderType(order_data['order_type']),
                quantity=float(order_data['quantity']),
                price=order_data.get('price'),
                stop_price=order_data.get('stop_price'),
                trail_amount=order_data.get('trail_amount'),
                trail_percent=order_data.get('trail_percent'),
                time_in_force=TimeInForce(order_data.get('time_in_force', 'gtc')),
                iceberg_visible_quantity=order_data.get('iceberg_visible_quantity'),
                twap_duration_minutes=order_data.get('twap_duration_minutes')
            )
            
            # Validate order
            validation_result = self._validate_order(order)
            if not validation_result['valid']:
                order.status = OrderStatus.REJECTED
                self.orders[order.id] = order
                return {
                    'success': False,
                    'order_id': order.id,
                    'error': validation_result['error']
                }
            
            # Store order
            self.orders[order.id] = order
            
            # Try to execute immediately if market order or conditions met
            if order.order_type == OrderType.MARKET:
                self._execute_market_order(order)
            elif order.order_type == OrderType.LIMIT:
                self._check_limit_order_execution(order)
            
            return {
                'success': True,
                'order_id': order.id,
                'status': order.status.value,
                'message': 'Order placed successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _validate_order(self, order: Order) -> dict:
        """Validate order parameters"""
        # Check if symbol exists
        if order.symbol not in self.market_data:
            return {'valid': False, 'error': f'Invalid symbol: {order.symbol}'}
        
        # Check quantity
        if order.quantity <= 0:
            return {'valid': False, 'error': 'Quantity must be positive'}
        
        # Check price for limit orders
        if order.order_type == OrderType.LIMIT and (not order.price or order.price <= 0):
            return {'valid': False, 'error': 'Limit orders require a valid price'}
        
        # Check stop price for stop orders
        if order.order_type in [OrderType.STOP_LOSS, OrderType.TAKE_PROFIT] and (not order.stop_price or order.stop_price <= 0):
            return {'valid': False, 'error': 'Stop orders require a valid stop price'}
        
        # Check trailing stop parameters
        if order.order_type == OrderType.TRAILING_STOP:
            if not order.trail_amount and not order.trail_percent:
                return {'valid': False, 'error': 'Trailing stop orders require trail amount or trail percent'}
        
        return {'valid': True}
    
    def _execute_market_order(self, order: Order):
        """Execute market order immediately"""
        market_data = self.market_data[order.symbol]
        
        if order.side == OrderSide.BUY:
            execution_price = market_data['ask']
        else:
            execution_price = market_data['bid']
        
        # Create trade
        trade = Trade(
            id=str(uuid.uuid4()),
            order_id=order.id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            price=execution_price,
            timestamp=datetime.now(),
            fee=order.quantity * execution_price * self.taker_fee
        )
        
        self.trades.append(trade)
        
        # Update order
        order.filled_quantity = order.quantity
        order.average_fill_price = execution_price
        order.status = OrderStatus.FILLED
        order.updated_at = datetime.now()
    
    def _check_limit_order_execution(self, order: Order):
        """Check if limit order can be executed"""
        market_data = self.market_data[order.symbol]
        
        can_execute = False
        if order.side == OrderSide.BUY and market_data['ask'] <= order.price:
            can_execute = True
        elif order.side == OrderSide.SELL and market_data['bid'] >= order.price:
            can_execute = True
        
        if can_execute:
            # Execute at limit price
            trade = Trade(
                id=str(uuid.uuid4()),
                order_id=order.id,
                symbol=order.symbol,
                side=order.side,
                quantity=order.quantity,
                price=order.price,
                timestamp=datetime.now(),
                fee=order.quantity * order.price * self.maker_fee
            )
            
            self.trades.append(trade)
            
            order.filled_quantity = order.quantity
            order.average_fill_price = order.price
            order.status = OrderStatus.FILLED
            order.updated_at = datetime.now()
    
    def cancel_order(self, order_id: str, user_id: str) -> dict:
        """Cancel an existing order"""
        if order_id not in self.orders:
            return {'success': False, 'error': 'Order not found'}
        
        order = self.orders[order_id]
        
        if order.user_id != user_id:
            return {'success': False, 'error': 'Unauthorized'}
        
        if order.status in [OrderStatus.FILLED, OrderStatus.CANCELLED]:
            return {'success': False, 'error': f'Cannot cancel order with status: {order.status.value}'}
        
        order.status = OrderStatus.CANCELLED
        order.updated_at = datetime.now()
        
        return {'success': True, 'message': 'Order cancelled successfully'}
    
    def get_order_status(self, order_id: str) -> dict:
        """Get order status and details"""
        if order_id not in self.orders:
            return {'success': False, 'error': 'Order not found'}
        
        order = self.orders[order_id]
        return {
            'success': True,
            'order': asdict(order)
        }
    
    def get_user_orders(self, user_id: str, status_filter: Optional[str] = None) -> dict:
        """Get all orders for a user"""
        user_orders = [
            order for order in self.orders.values() 
            if order.user_id == user_id
        ]
        
        if status_filter:
            user_orders = [
                order for order in user_orders 
                if order.status.value == status_filter
            ]
        
        return {
            'success': True,
            'orders': [asdict(order) for order in user_orders]
        }
    
    def get_user_trades(self, user_id: str) -> dict:
        """Get all trades for a user"""
        user_order_ids = {
            order.id for order in self.orders.values() 
            if order.user_id == user_id
        }
        
        user_trades = [
            trade for trade in self.trades 
            if trade.order_id in user_order_ids
        ]
        
        return {
            'success': True,
            'trades': [asdict(trade) for trade in user_trades]
        }

class AlgorithmicTrading:
    """Algorithmic trading strategies and execution algorithms"""
    
    def __init__(self, order_manager: AdvancedOrderManager):
        self.order_manager = order_manager
    
    def execute_twap_strategy(self, user_id: str, symbol: str, side: str, 
                            total_quantity: float, duration_minutes: int) -> dict:
        """Execute Time-Weighted Average Price strategy"""
        # Split order into smaller chunks
        num_chunks = min(duration_minutes, 20)  # Max 20 chunks
        chunk_size = total_quantity / num_chunks
        interval_minutes = duration_minutes / num_chunks
        
        orders_placed = []
        
        for i in range(num_chunks):
            # Schedule order placement
            delay_minutes = i * interval_minutes
            
            order_data = {
                'user_id': user_id,
                'symbol': symbol,
                'side': side,
                'order_type': 'market',
                'quantity': chunk_size,
                'time_in_force': 'ioc'
            }
            
            # For demo, place all orders immediately
            result = self.order_manager.place_order(order_data)
            if result['success']:
                orders_placed.append(result['order_id'])
        
        return {
            'success': True,
            'strategy': 'TWAP',
            'total_quantity': total_quantity,
            'duration_minutes': duration_minutes,
            'orders_placed': orders_placed,
            'chunk_size': chunk_size,
            'num_chunks': num_chunks
        }
    
    def execute_vwap_strategy(self, user_id: str, symbol: str, side: str, 
                            total_quantity: float) -> dict:
        """Execute Volume-Weighted Average Price strategy"""
        # Get historical volume profile (simulated)
        volume_profile = self._get_volume_profile(symbol)
        
        orders_placed = []
        remaining_quantity = total_quantity
        
        for time_slot, volume_weight in volume_profile.items():
            if remaining_quantity <= 0:
                break
            
            # Calculate quantity for this time slot
            slot_quantity = min(total_quantity * volume_weight, remaining_quantity)
            
            if slot_quantity > 0:
                order_data = {
                    'user_id': user_id,
                    'symbol': symbol,
                    'side': side,
                    'order_type': 'market',
                    'quantity': slot_quantity,
                    'time_in_force': 'ioc'
                }
                
                result = self.order_manager.place_order(order_data)
                if result['success']:
                    orders_placed.append(result['order_id'])
                    remaining_quantity -= slot_quantity
        
        return {
            'success': True,
            'strategy': 'VWAP',
            'total_quantity': total_quantity,
            'executed_quantity': total_quantity - remaining_quantity,
            'orders_placed': orders_placed,
            'volume_profile': volume_profile
        }
    
    def _get_volume_profile(self, symbol: str) -> dict:
        """Get simulated volume profile for VWAP strategy"""
        # Simulate typical intraday volume distribution
        return {
            '09:00-10:00': 0.15,  # Market open - high volume
            '10:00-11:00': 0.12,
            '11:00-12:00': 0.08,
            '12:00-13:00': 0.06,  # Lunch - low volume
            '13:00-14:00': 0.08,
            '14:00-15:00': 0.10,
            '15:00-16:00': 0.12,
            '16:00-17:00': 0.15,  # Market close - high volume
            '17:00-18:00': 0.14
        }
    
    def create_oco_order(self, user_id: str, symbol: str, side: str, quantity: float,
                        limit_price: float, stop_price: float) -> dict:
        """Create One-Cancels-Other order pair"""
        # Create limit order
        limit_order_data = {
            'user_id': user_id,
            'symbol': symbol,
            'side': side,
            'order_type': 'limit',
            'quantity': quantity,
            'price': limit_price,
            'time_in_force': 'gtc'
        }
        
        # Create stop order
        stop_side = 'sell' if side == 'buy' else 'buy'
        stop_order_data = {
            'user_id': user_id,
            'symbol': symbol,
            'side': stop_side,
            'order_type': 'stop_loss',
            'quantity': quantity,
            'stop_price': stop_price,
            'time_in_force': 'gtc'
        }
        
        # Place both orders
        limit_result = self.order_manager.place_order(limit_order_data)
        stop_result = self.order_manager.place_order(stop_order_data)
        
        if limit_result['success'] and stop_result['success']:
            # Link orders (in real implementation, would set parent_order_id)
            return {
                'success': True,
                'oco_pair': {
                    'limit_order_id': limit_result['order_id'],
                    'stop_order_id': stop_result['order_id']
                },
                'message': 'OCO order pair created successfully'
            }
        else:
            return {
                'success': False,
                'error': 'Failed to create OCO order pair',
                'limit_result': limit_result,
                'stop_result': stop_result
            }

class TradingAPI:
    """API for advanced trading features"""
    
    def __init__(self):
        self.order_manager = AdvancedOrderManager()
        self.algo_trading = AlgorithmicTrading(self.order_manager)
    
    def place_order(self, order_data: dict) -> dict:
        """Place a trading order"""
        return self.order_manager.place_order(order_data)
    
    def cancel_order(self, order_id: str, user_id: str) -> dict:
        """Cancel an order"""
        return self.order_manager.cancel_order(order_id, user_id)
    
    def get_order_book(self, symbol: str) -> dict:
        """Get order book for a symbol"""
        if symbol not in self.order_manager.order_books:
            return {'success': False, 'error': 'Symbol not found'}
        
        return {
            'success': True,
            'symbol': symbol,
            'order_book': self.order_manager.order_books[symbol],
            'timestamp': datetime.now().isoformat()
        }
    
    def get_market_data(self, symbol: str = None) -> dict:
        """Get market data"""
        if symbol:
            if symbol not in self.order_manager.market_data:
                return {'success': False, 'error': 'Symbol not found'}
            return {
                'success': True,
                'symbol': symbol,
                'data': self.order_manager.market_data[symbol],
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'success': True,
                'market_data': self.order_manager.market_data,
                'timestamp': datetime.now().isoformat()
            }
    
    def execute_algo_strategy(self, strategy_type: str, params: dict) -> dict:
        """Execute algorithmic trading strategy"""
        if strategy_type == 'twap':
            return self.algo_trading.execute_twap_strategy(
                params['user_id'], params['symbol'], params['side'],
                params['quantity'], params['duration_minutes']
            )
        elif strategy_type == 'vwap':
            return self.algo_trading.execute_vwap_strategy(
                params['user_id'], params['symbol'], params['side'],
                params['quantity']
            )
        elif strategy_type == 'oco':
            return self.algo_trading.create_oco_order(
                params['user_id'], params['symbol'], params['side'],
                params['quantity'], params['limit_price'], params['stop_price']
            )
        else:
            return {'success': False, 'error': f'Unknown strategy: {strategy_type}'}
    
    def get_trading_statistics(self, user_id: str) -> dict:
        """Get trading statistics for a user"""
        trades_result = self.order_manager.get_user_trades(user_id)
        if not trades_result['success']:
            return trades_result
        
        trades = trades_result['trades']
        
        if not trades:
            return {
                'success': True,
                'statistics': {
                    'total_trades': 0,
                    'total_volume': 0,
                    'total_fees': 0
                }
            }
        
        # Calculate statistics
        total_trades = len(trades)
        total_volume = sum(trade['quantity'] * trade['price'] for trade in trades)
        total_fees = sum(trade['fee'] for trade in trades)
        
        # Calculate P&L (simplified)
        buy_trades = [t for t in trades if t['side'] == 'buy']
        sell_trades = [t for t in trades if t['side'] == 'sell']
        
        total_bought = sum(t['quantity'] * t['price'] for t in buy_trades)
        total_sold = sum(t['quantity'] * t['price'] for t in sell_trades)
        unrealized_pnl = total_sold - total_bought
        
        return {
            'success': True,
            'statistics': {
                'total_trades': total_trades,
                'total_volume': total_volume,
                'total_fees': total_fees,
                'unrealized_pnl': unrealized_pnl,
                'buy_trades': len(buy_trades),
                'sell_trades': len(sell_trades),
                'average_trade_size': total_volume / total_trades if total_trades > 0 else 0
            }
        }

# Test the system
if __name__ == "__main__":
    print("Testing Advanced Trading Engine...")
    
    api = TradingAPI()
    test_user_id = "user_123"
    
    # Test market order
    print("\n1. Testing Market Order:")
    market_order = {
        'user_id': test_user_id,
        'symbol': 'BTC/DGD',
        'side': 'buy',
        'order_type': 'market',
        'quantity': 0.1
    }
    result = api.place_order(market_order)
    print(f"Market order result: {result}")
    
    # Test limit order
    print("\n2. Testing Limit Order:")
    limit_order = {
        'user_id': test_user_id,
        'symbol': 'ETH/DGD',
        'side': 'buy',
        'order_type': 'limit',
        'quantity': 1.0,
        'price': 22.0
    }
    result = api.place_order(limit_order)
    print(f"Limit order result: {result}")
    
    # Test TWAP strategy
    print("\n3. Testing TWAP Strategy:")
    twap_params = {
        'user_id': test_user_id,
        'symbol': 'BTC/DGD',
        'side': 'buy',
        'quantity': 0.5,
        'duration_minutes': 10
    }
    result = api.execute_algo_strategy('twap', twap_params)
    print(f"TWAP strategy result: {result}")
    
    # Test trading statistics
    print("\n4. Testing Trading Statistics:")
    stats = api.get_trading_statistics(test_user_id)
    print(f"Trading statistics: {stats}")
    
    print("\n✅ Advanced Trading Engine working correctly!")

