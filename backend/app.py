#!/usr/bin/env python3
"""
Main Flask app for AI Marketplace Backend
Deployable version of the simple AI API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, origins="*")

# Configure caching
cache_config = {
    'CACHE_TYPE': os.environ.get('CACHE_TYPE', 'SimpleCache'),  # Use 'RedisCache' for production
    'CACHE_DEFAULT_TIMEOUT': 60,
    'CACHE_KEY_PREFIX': 'crs_',
}

# Redis configuration (if available)
if os.environ.get('REDIS_URL'):
    cache_config.update({
        'CACHE_TYPE': 'RedisCache',
        'CACHE_REDIS_URL': os.environ.get('REDIS_URL'),
    })

cache = Cache(app, config=cache_config)

# Enable gzip compression for all responses
compress = Compress(app)

# Rate limiting to prevent abuse
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per minute", "2000 per hour"],
    storage_uri=os.environ.get('REDIS_URL', 'memory://'),
)

@app.route('/', methods=['GET'])
@cache.cached(timeout=300)  # Cache for 5 minutes
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'AI Marketplace Backend API',
        'version': '1.0.0',
        'status': 'operational',
        'endpoints': [
            '/api/ai/dashboard-data',
            '/api/ai/status'
        ]
    })

@app.route('/api/ai/status', methods=['GET'])
@cache.cached(timeout=60)  # Cache for 1 minute
@limiter.limit("30 per minute")
def ai_status():
    """AI system status endpoint"""
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'prediction_engine': 'active',
            'sentiment_analysis': 'active', 
            'trading_bots': 'active',
            'portfolio_optimization': 'active'
        }
    })

@app.route('/api/ai/dashboard-data', methods=['GET'])
@cache.cached(timeout=30)  # Cache for 30 seconds - frequently updated data
@limiter.limit("60 per minute")
def dashboard_data():
    """Main dashboard data endpoint"""
    return jsonify({
        "ai_status": {
            "prediction_engine": "active",
            "sentiment_analysis": "active",
            "trading_bots": "active"
        },
        "market_intelligence": {
            "market_fear_greed": 72,
            "market_mood": "BULLISH",
            "market_sentiment": 0.58,
            "total_news_volume": 125,
            "total_social_mentions": 850
        },
        "market_signals": [
            {
                "description": "BTC showing strong upward momentum",
                "signal_type": "MOMENTUM_UP",
                "strength": 0.85
            },
            {
                "description": "ETH experiencing increased trading volume",
                "signal_type": "HIGH_VOLUME",
                "strength": 0.72
            }
        ],
        "predictions": {
            "BTC": {
                "confidence": 0.85,
                "current_price": 45000,
                "model_consensus": {
                    "gradient_boost": 47200,
                    "linear_regression": 47300,
                    "random_forest": 46500
                },
                "predicted_price": 47000,
                "price_change": 2000,
                "price_change_percent": 4.44,
                "recommendation": "BUY",
                "symbol": "BTC"
            },
            "ETH": {
                "confidence": 0.78,
                "current_price": 2800,
                "model_consensus": {
                    "gradient_boost": 2960,
                    "linear_regression": 2970,
                    "random_forest": 2920
                },
                "predicted_price": 2950,
                "price_change": 150,
                "price_change_percent": 5.36,
                "recommendation": "BUY",
                "symbol": "ETH"
            }
        },
        "sentiment_summary": {
            "BTC": {
                "confidence": 0.82,
                "news_volume": 25,
                "overall_sentiment": 0.65,
                "sentiment_label": "POSITIVE",
                "sentiment_trend": "IMPROVING",
                "social_mentions": 150
            },
            "ETH": {
                "confidence": 0.75,
                "news_volume": 18,
                "overall_sentiment": 0.58,
                "sentiment_label": "POSITIVE",
                "sentiment_trend": "STABLE",
                "social_mentions": 120
            }
        },
        "timestamp": datetime.now().isoformat(),
        "trading_bots": {
            "active_bots": 2,
            "bots": [
                {
                    "active_positions": 2,
                    "current_balance": 12500,
                    "name": "BTC Momentum Bot",
                    "status": "active",
                    "strategy": "Momentum Strategy",
                    "total_pnl": 2500,
                    "total_trades": 45
                },
                {
                    "active_positions": 1,
                    "current_balance": 8750,
                    "name": "ETH Mean Reversion Bot",
                    "status": "active",
                    "strategy": "Mean Reversion Strategy",
                    "total_pnl": 1250,
                    "total_trades": 32
                }
            ],
            "total_bots": 3
        },
        "trending_topics": [
            {
                "mentions": 2500,
                "sentiment": 0.75,
                "sentiment_label": "POSITIVE",
                "topic": "AI Trading Revolution"
            },
            {
                "mentions": 1800,
                "sentiment": 0.68,
                "sentiment_label": "POSITIVE",
                "topic": "DeFi Integration"
            },
            {
                "mentions": 1200,
                "sentiment": 0.45,
                "sentiment_label": "NEUTRAL",
                "topic": "Regulatory Clarity"
            }
        ]
    })

@app.after_request
def add_cache_headers(response):
    """Add cache control headers to responses"""
    if request.endpoint and 'api' in request.endpoint:
        # API endpoints - short cache
        response.headers['Cache-Control'] = 'public, max-age=30'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

