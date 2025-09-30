#!/usr/bin/env python3
"""
Cryptocurrency Marketplace Backend
Main Flask application entry point
"""

import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'CRS Backend API',
        'version': '1.0.0'
    })

# API routes
@app.route('/api/status')
def api_status():
    return jsonify({
        'api_status': 'operational',
        'features': {
            'ai_predictions': True,
            'trading_bots': True,
            'portfolio_optimization': True,
            'sentiment_analysis': True,
            'advanced_charting': True,
            'crypto_payments': True
        }
    })

# Try to import and register AI modules
try:
    from api.unified_api_server import create_app as create_ai_app
    ai_routes = create_ai_app()
    
    # Register AI routes
    @app.route('/api/ai/<path:path>', methods=['GET', 'POST'])
    def ai_proxy(path):
        """Proxy requests to AI service"""
        # This is a simplified proxy - in production, use proper request forwarding
        return jsonify({'message': 'AI service integration in progress'})
        
except ImportError as e:
    print(f"Warning: Could not import AI modules: {e}")
    
    @app.route('/api/ai/<path:path>')
    def ai_fallback(path):
        return jsonify({
            'error': 'AI services not available',
            'message': 'AI modules are being configured'
        }), 503

# Try to import and register payment modules
try:
    from api.payment_api_server import payment_api
    app.register_blueprint(payment_api, url_prefix='/api/payments')
    print("Payment API routes registered successfully")
except ImportError as e:
    print(f"Warning: Could not import payment modules: {e}")
    
    @app.route('/api/payments/<path:path>')
    def payment_fallback(path):
        return jsonify({
            'error': 'Payment services not available',
            'message': 'Payment modules are being configured'
        }), 503

# Marketplace API endpoints
@app.route('/api/marketplace/products')
def get_products():
    """Get cryptocurrency products/services"""
    return jsonify({
        'products': [
            {
                'id': 1,
                'name': 'AI Trading Bot Premium',
                'price': 0.001,
                'currency': 'BTC',
                'description': 'Advanced AI-powered trading bot with portfolio optimization'
            },
            {
                'id': 2,
                'name': 'Market Analysis Pro',
                'price': 0.0005,
                'currency': 'BTC',
                'description': 'Real-time market sentiment analysis and predictions'
            }
        ]
    })

@app.route('/api/marketplace/cart')
def get_cart():
    """Get shopping cart contents"""
    return jsonify({
        'cart': [],
        'total': 0,
        'currency': 'BTC'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting CRS Backend API on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)