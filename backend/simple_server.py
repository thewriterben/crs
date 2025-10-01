#!/usr/bin/env python3
"""
Simple backend server for Cryptons.com Marketplace
Uses only built-in Python libraries to avoid dependency issues
"""

import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import os

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # API Routes
        if path == '/api/marketplace/products':
            self.handle_get_products()
        elif path == '/api/marketplace/cart':
            self.handle_get_cart()
        elif path == '/api/ai/dashboard-data':
            self.handle_ai_dashboard()
        elif path == '/api/ai/status':
            self.handle_ai_status()
        elif path == '/health':
            self.handle_health()
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        if path == '/api/marketplace/cart':
            self.handle_add_to_cart(post_data)
        elif path == '/api/marketplace/checkout':
            self.handle_checkout(post_data)
        else:
            self.send_error(404, 'Not Found')

    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def handle_health(self):
        data = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'Cryptons.com Marketplace Backend'
        }
        self.send_json_response(data)

    def handle_get_products(self):
        products = [
            {
                'id': 1,
                'name': 'AI Trading Bot Premium',
                'price': 0.001,
                'currency': 'BTC',
                'description': 'Advanced AI-powered trading bot with portfolio optimization and real-time market analysis',
                'category': 'Trading Tools',
                'rating': 4.8,
                'features': ['24/7 Trading', 'Portfolio Optimization', 'Risk Management', 'Performance Analytics'],
                'popular': True
            },
            {
                'id': 2,
                'name': 'Market Analysis Pro',
                'price': 0.0005,
                'currency': 'BTC',
                'description': 'Real-time market sentiment analysis and predictions using advanced ML algorithms',
                'category': 'Analytics',
                'rating': 4.6,
                'features': ['Sentiment Analysis', 'Price Predictions', 'News Integration', 'Social Media Monitoring'],
                'popular': False
            },
            {
                'id': 3,
                'name': 'Crypto Security Suite',
                'price': 0.0003,
                'currency': 'BTC',
                'description': 'Comprehensive security tools for cryptocurrency wallets and transactions',
                'category': 'Security',
                'rating': 4.9,
                'features': ['Wallet Security', 'Transaction Monitoring', 'Threat Detection', '2FA Integration'],
                'popular': False
            },
            {
                'id': 4,
                'name': 'Lightning Fast Executor',
                'price': 0.0008,
                'currency': 'BTC',
                'description': 'High-speed trade execution engine with minimal latency for professional traders',
                'category': 'Trading Tools',
                'rating': 4.7,
                'features': ['Ultra-Low Latency', 'Multi-Exchange Support', 'Order Types', 'Smart Routing'],
                'popular': True
            },
            {
                'id': 5,
                'name': 'DeFi Yield Optimizer',
                'price': 0.0012,
                'currency': 'BTC',
                'description': 'Automated yield farming and liquidity provision optimization across DeFi protocols',
                'category': 'DeFi',
                'rating': 4.5,
                'features': ['Yield Farming', 'Liquidity Optimization', 'Risk Assessment', 'Multi-Protocol Support'],
                'popular': False
            },
            {
                'id': 6,
                'name': 'Crypto Tax Calculator',
                'price': 0.0002,
                'currency': 'BTC',
                'description': 'Automated cryptocurrency tax calculation and reporting for multiple jurisdictions',
                'category': 'Utilities',
                'rating': 4.4,
                'features': ['Tax Calculations', 'Multi-Jurisdiction', 'Export Reports', 'Transaction History'],
                'popular': False
            }
        ]
        
        data = {'products': products}
        self.send_json_response(data)

    def handle_get_cart(self):
        # Mock cart data
        cart_items = [
            {
                'id': 1,
                'name': 'AI Trading Bot Premium',
                'price': 0.001,
                'currency': 'BTC',
                'quantity': 1,
                'description': 'Advanced AI-powered trading bot with portfolio optimization',
                'category': 'Trading Tools'
            },
            {
                'id': 2,
                'name': 'Market Analysis Pro',
                'price': 0.0005,
                'currency': 'BTC',
                'quantity': 2,
                'description': 'Real-time market sentiment analysis and predictions',
                'category': 'Analytics'
            }
        ]
        
        data = {
            'cart': cart_items,
            'total': 0.002,
            'currency': 'BTC'
        }
        self.send_json_response(data)

    def handle_add_to_cart(self, post_data):
        try:
            data = json.loads(post_data.decode())
            product_id = data.get('productId')
            quantity = data.get('quantity', 1)
            
            response = {
                'success': True,
                'message': f'Added product {product_id} to cart',
                'productId': product_id,
                'quantity': quantity
            }
            self.send_json_response(response)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 400)

    def handle_checkout(self, post_data):
        try:
            data = json.loads(post_data.decode())
            
            # Simulate payment processing
            response = {
                'success': True,
                'transactionId': f'tx_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'message': 'Payment processed successfully',
                'timestamp': datetime.now().isoformat()
            }
            self.send_json_response(response)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 400)

    def handle_ai_dashboard(self):
        data = {
            'ai_status': {
                'prediction_engine': 'active',
                'sentiment_analysis': 'active',
                'trading_bots': 'active'
            },
            'market_intelligence': {
                'market_fear_greed': 72,
                'market_mood': 'BULLISH',
                'market_sentiment': 0.58,
                'total_news_volume': 125,
                'total_social_mentions': 850
            },
            'market_signals': [
                {
                    'description': 'BTC showing strong upward momentum',
                    'signal_type': 'MOMENTUM_UP',
                    'strength': 0.85
                },
                {
                    'description': 'ETH experiencing increased trading volume',
                    'signal_type': 'HIGH_VOLUME',
                    'strength': 0.72
                }
            ],
            'predictions': {
                'BTC': {
                    'confidence': 0.85,
                    'current_price': 45000,
                    'predicted_price': 47500,
                    'direction': 'UP'
                }
            }
        }
        self.send_json_response(data)

    def handle_ai_status(self):
        data = {
            'status': 'operational',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'prediction_engine': 'active',
                'sentiment_analysis': 'active', 
                'trading_bots': 'active',
                'portfolio_optimization': 'active'
            }
        }
        self.send_json_response(data)

def main():
    port = int(os.environ.get('PORT', 5000))
    
    with socketserver.TCPServer(("", port), CORSRequestHandler) as httpd:
        print(f"Cryptons.com Marketplace Backend running on port {port}")
        print(f"Health check: http://localhost:{port}/health")
        print(f"API endpoints available at: http://localhost:{port}/api/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()

if __name__ == "__main__":
    main()