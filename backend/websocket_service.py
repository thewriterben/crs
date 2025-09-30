#!/usr/bin/env python3
"""
WebSocket Service for Real-time Data Streaming
Provides live market data feeds, instant price updates, and event-driven notifications
"""

from flask_socketio import SocketIO, emit
from datetime import datetime
import random
import threading
import time

# Initialize SocketIO with CORS support
socketio = None

def init_socketio(app):
    """Initialize SocketIO with the Flask app"""
    global socketio
    socketio = SocketIO(
        app, 
        cors_allowed_origins="*",
        async_mode='eventlet',
        logger=True,
        engineio_logger=False
    )
    
    # Register event handlers
    register_handlers()
    
    # Start background tasks
    start_background_tasks()
    
    return socketio

def register_handlers():
    """Register WebSocket event handlers"""
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        print(f'Client connected: {datetime.now().isoformat()}')
        emit('connection_status', {
            'status': 'connected',
            'message': 'Connected to real-time data stream',
            'timestamp': datetime.now().isoformat()
        })
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        print(f'Client disconnected: {datetime.now().isoformat()}')
    
    @socketio.on('subscribe')
    def handle_subscribe(data):
        """Handle subscription to specific data streams"""
        symbols = data.get('symbols', ['BTC', 'ETH'])
        print(f'Client subscribed to: {symbols}')
        emit('subscription_confirmed', {
            'symbols': symbols,
            'timestamp': datetime.now().isoformat()
        })

def generate_market_data():
    """Generate simulated real-time market data"""
    symbols = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'SOL', 'MATIC', 'AVAX']
    
    # Base prices for simulation
    base_prices = {
        'BTC': 45000,
        'ETH': 2500,
        'ADA': 0.45,
        'DOT': 6.5,
        'LINK': 14.5,
        'SOL': 100,
        'MATIC': 0.85,
        'AVAX': 35
    }
    
    data = {}
    for symbol in symbols:
        base_price = base_prices.get(symbol, 100)
        # Add random variation (-2% to +2%)
        price_change = random.uniform(-0.02, 0.02)
        current_price = base_price * (1 + price_change)
        
        # Calculate 24h change
        change_24h = random.uniform(-5, 5)
        
        data[symbol] = {
            'symbol': symbol,
            'price': round(current_price, 2 if current_price > 1 else 6),
            'change_24h': round(change_24h, 2),
            'volume_24h': round(random.uniform(1000000, 50000000), 2),
            'timestamp': datetime.now().isoformat()
        }
    
    return data

def generate_sentiment_update():
    """Generate real-time sentiment analysis updates"""
    sentiments = ['POSITIVE', 'NEUTRAL', 'NEGATIVE', 'BULLISH', 'BEARISH']
    
    return {
        'overall_sentiment': random.choice(sentiments),
        'market_fear_greed': random.randint(20, 80),
        'market_mood': random.choice(['BULLISH', 'BEARISH', 'NEUTRAL']),
        'confidence': round(random.uniform(0.6, 0.95), 2),
        'trending_topics': random.sample(['bitcoin', 'ethereum', 'defi', 'nft', 'regulation', 'institutional'], 3),
        'timestamp': datetime.now().isoformat()
    }

def generate_trading_signal():
    """Generate trading signals and alerts"""
    signal_types = ['BUY', 'SELL', 'HOLD', 'STRONG_BUY', 'STRONG_SELL']
    symbols = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK']
    
    return {
        'symbol': random.choice(symbols),
        'signal': random.choice(signal_types),
        'strength': round(random.uniform(0.5, 1.0), 2),
        'reason': random.choice([
            'Strong momentum detected',
            'Volume surge observed',
            'Breakout pattern forming',
            'Support level reached',
            'Resistance level approaching'
        ]),
        'timestamp': datetime.now().isoformat()
    }

def broadcast_market_data():
    """Broadcast market data to all connected clients"""
    while True:
        try:
            if socketio:
                market_data = generate_market_data()
                socketio.emit('market_update', market_data, namespace='/')
        except Exception as e:
            print(f"Error broadcasting market data: {e}")
        time.sleep(2)  # Update every 2 seconds

def broadcast_sentiment_updates():
    """Broadcast sentiment analysis updates"""
    while True:
        try:
            if socketio:
                sentiment_data = generate_sentiment_update()
                socketio.emit('sentiment_update', sentiment_data, namespace='/')
        except Exception as e:
            print(f"Error broadcasting sentiment: {e}")
        time.sleep(10)  # Update every 10 seconds

def broadcast_trading_signals():
    """Broadcast trading signals"""
    while True:
        try:
            if socketio:
                signal = generate_trading_signal()
                socketio.emit('trading_signal', signal, namespace='/')
        except Exception as e:
            print(f"Error broadcasting signal: {e}")
        time.sleep(15)  # Send signal every 15 seconds

def start_background_tasks():
    """Start background tasks for broadcasting data"""
    # Start market data broadcaster
    market_thread = threading.Thread(target=broadcast_market_data, daemon=True)
    market_thread.start()
    
    # Start sentiment updates broadcaster
    sentiment_thread = threading.Thread(target=broadcast_sentiment_updates, daemon=True)
    sentiment_thread.start()
    
    # Start trading signals broadcaster
    signal_thread = threading.Thread(target=broadcast_trading_signals, daemon=True)
    signal_thread.start()
    
    print("Real-time data streaming started")
