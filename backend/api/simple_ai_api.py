#!/usr/bin/env python3
"""
Simple AI API Server for Testing
"""

from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/ai/dashboard-data', methods=['GET'])
def get_dashboard_data():
    return jsonify({
        'predictions': {
            'BTC': {
                'symbol': 'BTC',
                'current_price': 45000,
                'predicted_price': 47000,
                'price_change': 2000,
                'price_change_percent': 4.44,
                'confidence': 0.85,
                'recommendation': 'BUY',
                'model_consensus': {
                    'random_forest': 46500,
                    'gradient_boost': 47200,
                    'linear_regression': 47300
                }
            },
            'ETH': {
                'symbol': 'ETH',
                'current_price': 2800,
                'predicted_price': 2950,
                'price_change': 150,
                'price_change_percent': 5.36,
                'confidence': 0.78,
                'recommendation': 'BUY',
                'model_consensus': {
                    'random_forest': 2920,
                    'gradient_boost': 2960,
                    'linear_regression': 2970
                }
            }
        },
        'sentiment_summary': {
            'BTC': {
                'overall_sentiment': 0.65,
                'sentiment_label': 'POSITIVE',
                'sentiment_trend': 'IMPROVING',
                'news_volume': 25,
                'social_mentions': 150,
                'confidence': 0.82
            },
            'ETH': {
                'overall_sentiment': 0.58,
                'sentiment_label': 'POSITIVE',
                'sentiment_trend': 'STABLE',
                'news_volume': 18,
                'social_mentions': 120,
                'confidence': 0.75
            }
        },
        'market_intelligence': {
            'market_mood': 'BULLISH',
            'market_sentiment': 0.58,
            'market_fear_greed': 72,
            'total_news_volume': 125,
            'total_social_mentions': 850
        },
        'trading_bots': {
            'total_bots': 3,
            'active_bots': 2,
            'bots': [
                {
                    'name': 'BTC Momentum Bot',
                    'status': 'active',
                    'strategy': 'Momentum Strategy',
                    'current_balance': 12500,
                    'total_pnl': 2500,
                    'total_trades': 45,
                    'active_positions': 2
                },
                {
                    'name': 'ETH Mean Reversion Bot',
                    'status': 'active',
                    'strategy': 'Mean Reversion Strategy',
                    'current_balance': 8750,
                    'total_pnl': 1250,
                    'total_trades': 32,
                    'active_positions': 1
                }
            ]
        },
        'trending_topics': [
            {
                'topic': 'AI Trading Revolution',
                'mentions': 2500,
                'sentiment': 0.75,
                'sentiment_label': 'POSITIVE'
            },
            {
                'topic': 'DeFi Integration',
                'mentions': 1800,
                'sentiment': 0.68,
                'sentiment_label': 'POSITIVE'
            },
            {
                'topic': 'Regulatory Clarity',
                'mentions': 1200,
                'sentiment': 0.45,
                'sentiment_label': 'NEUTRAL'
            }
        ],
        'market_signals': [
            {
                'signal_type': 'MOMENTUM_UP',
                'strength': 0.85,
                'description': 'BTC showing strong upward momentum'
            },
            {
                'signal_type': 'HIGH_VOLUME',
                'strength': 0.72,
                'description': 'ETH experiencing increased trading volume'
            }
        ],
        'ai_status': {
            'prediction_engine': 'active',
            'trading_bots': 'active',
            'sentiment_analysis': 'active'
        },
        'timestamp': '2025-07-18T15:47:00.000Z'
    })

@app.route('/api/ai/status', methods=['GET'])
def get_ai_status():
    return jsonify({
        'status': 'operational',
        'systems': {
            'prediction_engine': 'active',
            'trading_bots': 'active',
            'sentiment_analysis': 'active'
        },
        'active_bots': 2,
        'timestamp': '2025-07-18T15:47:00.000Z'
    })

if __name__ == '__main__':
    print('Starting simple AI API server on port 5005...')
    app.run(host='0.0.0.0', port=5005, debug=False)

