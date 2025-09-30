#!/usr/bin/env python3
"""
Unified API Server for Advanced AI Marketplace Capabilities
Integrates portfolio optimization, advanced charting, news analysis, and trading features
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import sys
import os

# Import all the new capability modules
from portfolio_optimizer import PortfolioAPI
from advanced_charting import ChartingAPI
from ai_news_analyzer import NewsAnalysisAPI
from advanced_trading_engine import TradingAPI

app = Flask(__name__)
CORS(app, origins="*")

# Initialize all API modules
portfolio_api = PortfolioAPI()
charting_api = ChartingAPI()
news_api = NewsAnalysisAPI()
trading_api = TradingAPI()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'portfolio_optimization': 'active',
            'advanced_charting': 'active',
            'news_analysis': 'active',
            'advanced_trading': 'active'
        }
    })

# Portfolio Optimization Endpoints
@app.route('/api/portfolio/optimize', methods=['POST'])
def optimize_portfolio():
    """Optimize portfolio allocation"""
    try:
        data = request.get_json()
        assets = data.get('assets')
        method = data.get('method', 'max_sharpe')
        
        result = portfolio_api.get_optimized_portfolio(assets, method)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio/efficient-frontier', methods=['POST'])
def get_efficient_frontier():
    """Get efficient frontier data"""
    try:
        data = request.get_json()
        assets = data.get('assets')
        
        result = portfolio_api.get_efficient_frontier(assets)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio/risk-analysis', methods=['POST'])
def analyze_portfolio_risk():
    """Analyze portfolio risk metrics"""
    try:
        data = request.get_json()
        portfolio_weights = data.get('portfolio_weights')
        portfolio_value = data.get('portfolio_value', 100000)
        
        result = portfolio_api.analyze_portfolio_risk(portfolio_weights, portfolio_value)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Advanced Charting Endpoints
@app.route('/api/charts/data/<symbol>', methods=['GET'])
def get_chart_data(symbol):
    """Get comprehensive chart data with indicators"""
    try:
        timeframe = request.args.get('timeframe', '1h')
        periods = int(request.args.get('periods', 100))
        
        result = charting_api.get_chart_data(symbol, timeframe, periods)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/charts/multi-timeframe/<symbol>', methods=['GET'])
def get_multi_timeframe_analysis(symbol):
    """Get multi-timeframe analysis"""
    try:
        result = charting_api.get_multi_timeframe_analysis(symbol)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/charts/market-structure/<symbol>', methods=['GET'])
def get_market_structure(symbol):
    """Get market structure analysis"""
    try:
        result = charting_api.get_market_structure(symbol)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# News Analysis Endpoints
@app.route('/api/news/analysis', methods=['GET'])
def get_news_analysis():
    """Get comprehensive news analysis"""
    try:
        hours_back = int(request.args.get('hours_back', 24))
        
        result = news_api.get_news_analysis(hours_back)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/news/crypto-summary/<crypto>', methods=['GET'])
def get_crypto_news_summary(crypto):
    """Get news summary for specific cryptocurrency"""
    try:
        result = news_api.get_crypto_news_summary(crypto)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Advanced Trading Endpoints
@app.route('/api/trading/place-order', methods=['POST'])
def place_order():
    """Place a trading order"""
    try:
        order_data = request.get_json()
        result = trading_api.place_order(order_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trading/cancel-order', methods=['POST'])
def cancel_order():
    """Cancel a trading order"""
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        user_id = data.get('user_id')
        
        result = trading_api.cancel_order(order_id, user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trading/order-book/<symbol>', methods=['GET'])
def get_order_book(symbol):
    """Get order book for a symbol"""
    try:
        result = trading_api.get_order_book(symbol)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trading/market-data', methods=['GET'])
def get_market_data():
    """Get market data"""
    try:
        symbol = request.args.get('symbol')
        result = trading_api.get_market_data(symbol)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trading/algo-strategy', methods=['POST'])
def execute_algo_strategy():
    """Execute algorithmic trading strategy"""
    try:
        data = request.get_json()
        strategy_type = data.get('strategy_type')
        params = data.get('params')
        
        result = trading_api.execute_algo_strategy(strategy_type, params)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trading/statistics/<user_id>', methods=['GET'])
def get_trading_statistics(user_id):
    """Get trading statistics for a user"""
    try:
        result = trading_api.get_trading_statistics(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Comprehensive Dashboard Endpoint
@app.route('/api/dashboard/comprehensive', methods=['GET'])
def get_comprehensive_dashboard():
    """Get comprehensive dashboard data combining all features"""
    try:
        user_id = request.args.get('user_id', 'demo_user')
        
        # Get data from all modules
        portfolio_data = portfolio_api.get_optimized_portfolio(['BTC', 'ETH', 'ADA', 'DOT', 'LINK'])
        chart_data = charting_api.get_chart_data('BTC', '1h', 50)
        news_data = news_api.get_news_analysis(24)
        trading_stats = trading_api.get_trading_statistics(user_id)
        market_data = trading_api.get_market_data()
        
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'portfolio_optimization': {
                'optimal_allocation': portfolio_data['optimization_result']['weights'],
                'expected_return': portfolio_data['optimization_result']['expected_return'],
                'volatility': portfolio_data['optimization_result']['volatility'],
                'sharpe_ratio': portfolio_data['optimization_result']['sharpe_ratio'],
                'risk_metrics': portfolio_data['risk_metrics']
            },
            'market_analysis': {
                'btc_price': chart_data['ohlcv_data'][-1]['close'],
                'btc_trend': chart_data['technical_indicators']['sma_20'][-1] > chart_data['technical_indicators']['sma_50'][-1],
                'rsi': chart_data['technical_indicators']['rsi'][-1],
                'macd': chart_data['technical_indicators']['macd'][-1]
            },
            'news_sentiment': {
                'overall_sentiment': news_data['overall_sentiment_label'],
                'market_signals': len(news_data['market_signals']),
                'trending_topics': list(news_data['trending_topics'].keys())[:5]
            },
            'trading_performance': trading_stats['statistics'] if trading_stats['success'] else {},
            'market_data': market_data['market_data'] if market_data['success'] else {},
            'active_features': {
                'portfolio_optimization': True,
                'advanced_charting': True,
                'ai_news_analysis': True,
                'algorithmic_trading': True,
                'risk_management': True,
                'pattern_recognition': True
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Feature Status Endpoint
@app.route('/api/features/status', methods=['GET'])
def get_feature_status():
    """Get status of all advanced features"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'advanced_features': {
            'portfolio_optimization': {
                'status': 'active',
                'description': 'Modern Portfolio Theory optimization with risk metrics',
                'capabilities': [
                    'Sharpe ratio maximization',
                    'Risk-return optimization',
                    'Monte Carlo simulation',
                    'Value at Risk calculation',
                    'Portfolio rebalancing'
                ]
            },
            'advanced_charting': {
                'status': 'active',
                'description': 'Professional-grade technical analysis and charting',
                'capabilities': [
                    'Advanced technical indicators',
                    'Pattern recognition',
                    'Multi-timeframe analysis',
                    'Volume profile analysis',
                    'Fibonacci retracements'
                ]
            },
            'ai_news_analysis': {
                'status': 'active',
                'description': 'AI-powered news sentiment and market intelligence',
                'capabilities': [
                    'Real-time sentiment analysis',
                    'Market impact assessment',
                    'Trending topic detection',
                    'News-based trading signals',
                    'Multi-source aggregation'
                ]
            },
            'advanced_trading': {
                'status': 'active',
                'description': 'Sophisticated trading engine with algorithmic strategies',
                'capabilities': [
                    'Advanced order types (OCO, Iceberg, Trailing Stop)',
                    'Algorithmic trading (TWAP, VWAP)',
                    'Order management system',
                    'Trade execution optimization',
                    'Performance analytics'
                ]
            }
        },
        'integration_status': {
            'api_unified': True,
            'frontend_ready': True,
            'real_time_data': True,
            'cross_feature_compatibility': True
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Unified AI Marketplace API Server...")
    print("📊 Portfolio Optimization: Ready")
    print("📈 Advanced Charting: Ready") 
    print("📰 AI News Analysis: Ready")
    print("💹 Advanced Trading: Ready")
    print("🔗 All systems integrated and operational!")
    print("🌐 Server starting on http://0.0.0.0:5010")
    
    app.run(host='0.0.0.0', port=5010, debug=True)

