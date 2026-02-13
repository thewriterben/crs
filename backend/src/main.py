#!/usr/bin/env python3
"""
Main Flask app for AI Marketplace Backend
Deployable version of the simple AI API
"""

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
import json
from datetime import datetime, timedelta
import os


def create_app(config=None):
    """
    Application factory for creating Flask app instances
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///marketplace.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
    
    # Apply custom config if provided
    if config:
        app.config.update(config)
    
    # Initialize extensions
    from src.models import db, bcrypt
    from src.auth_routes import auth_bp
    from src.health_routes import health_bp
    
    # Configure security (CORS, rate limiting, security headers, caching, compression)
    try:
        from src.security_config import configure_security
        configure_security(app)
    except ImportError:
        # Fallback to basic CORS if security module not available
        from flask_cors import CORS
        CORS(app, origins="*", supports_credentials=True)
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register routes
    register_routes(app)
    
    return app


def register_routes(app):
    """Register application routes"""
    
    @app.route('/', methods=['GET'])
    def home():
        """Home endpoint"""
        return jsonify({
            'message': 'AI Marketplace Backend API',
            'version': '1.0.0',
            'status': 'operational',
            'endpoints': [
                '/api/ai/dashboard-data',
                '/api/ai/status',
                '/api/auth/register',
                '/api/auth/login',
                '/api/auth/logout',
                '/api/auth/refresh',
                '/api/auth/verify',
                '/api/auth/profile'
            ]
        })

    @app.route('/api/ai/status', methods=['GET'])
    def ai_status():
        """AI system status endpoint"""
        from src.security_config import get_cache
        cache = get_cache()
        
        @cache.cached(timeout=60, key_prefix='ai_status')
        def get_status():
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
        
        return get_status()

    @app.route('/api/ai/dashboard-data', methods=['GET'])
    def dashboard_data():
        """Main dashboard data endpoint"""
        from src.security_config import get_cache
        cache = get_cache()
        
        @cache.cached(timeout=30, key_prefix='dashboard_data')
        def get_dashboard():
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
        
        return get_dashboard()


# Create default app instance
app = create_app()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

