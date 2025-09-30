"""
Enhanced database models for trading data
"""
from datetime import datetime
from src.models import db


class TradingPair(db.Model):
    """Trading pair model"""
    __tablename__ = 'trading_pairs'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), unique=True, nullable=False)  # e.g., BTC/USDT
    base_currency = db.Column(db.String(10), nullable=False)  # e.g., BTC
    quote_currency = db.Column(db.String(10), nullable=False)  # e.g., USDT
    is_active = db.Column(db.Boolean, default=True)
    min_order_size = db.Column(db.Float, default=0.0001)
    max_order_size = db.Column(db.Float, default=1000.0)
    price_precision = db.Column(db.Integer, default=2)
    quantity_precision = db.Column(db.Integer, default=8)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='trading_pair', lazy=True)
    trades = db.relationship('Trade', backref='trading_pair', lazy=True)


class Order(db.Model):
    """Order model for trading"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pair_id = db.Column(db.Integer, db.ForeignKey('trading_pairs.id'), nullable=False)
    
    # Order details
    order_type = db.Column(db.String(20), nullable=False)  # market, limit, stop_loss, etc.
    side = db.Column(db.String(10), nullable=False)  # buy, sell
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float)  # null for market orders
    stop_price = db.Column(db.Float)  # for stop orders
    
    # Status and execution
    status = db.Column(db.String(20), default='pending')  # pending, filled, partially_filled, cancelled
    filled_quantity = db.Column(db.Float, default=0.0)
    average_price = db.Column(db.Float)
    
    # Fees and costs
    fee = db.Column(db.Float, default=0.0)
    fee_currency = db.Column(db.String(10))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    filled_at = db.Column(db.DateTime)
    
    # Relationships
    trades = db.relationship('Trade', backref='order', lazy=True)


class Trade(db.Model):
    """Trade execution model"""
    __tablename__ = 'trades'
    
    id = db.Column(db.Integer, primary_key=True)
    trade_id = db.Column(db.String(64), unique=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    pair_id = db.Column(db.Integer, db.ForeignKey('trading_pairs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Trade details
    side = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, default=0.0)
    fee_currency = db.Column(db.String(10))
    
    # Timestamps
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)


class Portfolio(db.Model):
    """User portfolio holdings"""
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    
    # Balance information
    total_balance = db.Column(db.Float, default=0.0)
    available_balance = db.Column(db.Float, default=0.0)
    locked_balance = db.Column(db.Float, default=0.0)
    
    # Portfolio metrics
    average_buy_price = db.Column(db.Float)
    total_invested = db.Column(db.Float, default=0.0)
    unrealized_pnl = db.Column(db.Float, default=0.0)
    realized_pnl = db.Column(db.Float, default=0.0)
    
    # Timestamps
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'currency', name='unique_user_currency'),)


class Transaction(db.Model):
    """Transaction history model"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Transaction details
    transaction_type = db.Column(db.String(20), nullable=False)  # deposit, withdrawal, trade, fee
    currency = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    balance_after = db.Column(db.Float)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, cancelled
    
    # Reference
    reference_id = db.Column(db.String(64))  # Reference to order_id, trade_id, etc.
    reference_type = db.Column(db.String(20))  # order, trade, deposit, withdrawal
    
    # Additional info
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)


class MarketData(db.Model):
    """Historical market data"""
    __tablename__ = 'market_data'
    
    id = db.Column(db.Integer, primary_key=True)
    pair_id = db.Column(db.Integer, db.ForeignKey('trading_pairs.id'), nullable=False)
    
    # OHLCV data
    timestamp = db.Column(db.DateTime, nullable=False)
    open_price = db.Column(db.Float, nullable=False)
    high_price = db.Column(db.Float, nullable=False)
    low_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, default=0.0)
    
    # Timeframe
    timeframe = db.Column(db.String(10), nullable=False)  # 1m, 5m, 1h, 1d, etc.
    
    # Index for faster queries
    __table_args__ = (
        db.Index('idx_pair_timeframe_timestamp', 'pair_id', 'timeframe', 'timestamp'),
    )


class AuditLog(db.Model):
    """Audit log for security and compliance"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Event details
    event_type = db.Column(db.String(50), nullable=False)  # login, order, trade, withdrawal, etc.
    action = db.Column(db.String(50), nullable=False)
    resource = db.Column(db.String(100))
    
    # Request information
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    
    # Event data
    details = db.Column(db.JSON)
    
    # Status
    status = db.Column(db.String(20))  # success, failure
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Index for faster queries
    __table_args__ = (
        db.Index('idx_user_event_created', 'user_id', 'event_type', 'created_at'),
    )
