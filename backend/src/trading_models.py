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


class EcommerceOrder(db.Model):
    """E-commerce order model with CFV discount support"""
    __tablename__ = 'ecommerce_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Order details
    items = db.Column(db.JSON, nullable=False)  # Array of {product_id, name, quantity, price}
    subtotal = db.Column(db.Float, nullable=False)
    original_price_usd = db.Column(db.Float, nullable=False)  # Price before CFV discount
    
    # CFV discount information
    cfv_discount = db.Column(db.Float, default=0.0)  # Discount percentage (0-100)
    cfv_metrics = db.Column(db.JSON)  # {valuationStatus, valuationPercent, calculatedAt}
    
    # Final pricing
    total = db.Column(db.Float, nullable=False)  # After discount
    
    # Status and fulfillment
    status = db.Column(db.String(20), default='pending')  # pending, paid, processing, shipped, completed, cancelled
    
    # Shipping information
    shipping_address = db.Column(db.JSON)
    shipping_method = db.Column(db.String(50))
    shipping_cost = db.Column(db.Float, default=0.0)
    tracking_number = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = db.Column(db.DateTime)
    shipped_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    payments = db.relationship('Payment', backref='ecommerce_order', lazy=True)
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'items': self.items,
            'subtotal': self.subtotal,
            'original_price_usd': self.original_price_usd,
            'cfv_discount': self.cfv_discount,
            'cfv_metrics': self.cfv_metrics,
            'total': self.total,
            'status': self.status,
            'shipping_address': self.shipping_address,
            'shipping_method': self.shipping_method,
            'shipping_cost': self.shipping_cost,
            'tracking_number': self.tracking_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None
        }


class Payment(db.Model):
    """Payment model with CFV metrics support"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(64), unique=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('ecommerce_orders.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Payment details
    cryptocurrency = db.Column(db.String(20), nullable=False)  # XNO, NEAR, ICP, EGLD, DGB, DASH, XCH, XEC, XMR, RVN, DGD, BTC-LN
    amount_crypto = db.Column(db.Float, nullable=False)  # Amount in cryptocurrency
    amount_usd = db.Column(db.Float, nullable=False)  # USD equivalent
    
    # CFV metrics
    fair_value = db.Column(db.Float)  # CFV calculated fair value at transaction time
    cfv_discount = db.Column(db.Float, default=0.0)  # Percentage discount applied
    cfv_metrics = db.Column(db.JSON)  # {valuationStatus, valuationPercent, calculatedAt}
    
    # Payment address and transaction
    payment_address = db.Column(db.String(255), nullable=False)
    transaction_hash = db.Column(db.String(255))
    confirmations = db.Column(db.Integer, default=0)
    
    # Network fees
    network_fee = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False)  # amount_crypto + network_fee
    
    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed, expired
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    confirmed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Metadata
    metadata = db.Column(db.JSON)
    
    def to_dict(self):
        """Convert payment to dictionary"""
        return {
            'payment_id': self.payment_id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'cryptocurrency': self.cryptocurrency,
            'amount_crypto': self.amount_crypto,
            'amount_usd': self.amount_usd,
            'fair_value': self.fair_value,
            'cfv_discount': self.cfv_discount,
            'cfv_metrics': self.cfv_metrics,
            'payment_address': self.payment_address,
            'transaction_hash': self.transaction_hash,
            'confirmations': self.confirmations,
            'network_fee': self.network_fee,
            'total_amount': self.total_amount,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'metadata': self.metadata
        }
