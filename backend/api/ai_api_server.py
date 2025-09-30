#!/usr/bin/env python3
"""
Unified AI API Server for Advanced AI Features
Combines prediction engine, trading bots, and sentiment analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import threading
import time

# Import AI modules
from ai_prediction_engine import PredictionAPI
from trading_bot_system import TradingBotManager
from sentiment_analysis_system import SentimentAPI

app = Flask(__name__)
CORS(app)

# Initialize AI systems
prediction_api = PredictionAPI()
bot_manager = TradingBotManager()
sentiment_api = SentimentAPI()

# Global state
ai_status = {
    'prediction_engine': 'active',
    'trading_bots': 'active',
    'sentiment_analysis': 'active',
    'last_update': datetime.now().isoformat()
}

@app.route('/api/ai/status', methods=['GET'])
def get_ai_status():
    """Get overall AI system status"""
    return jsonify({
        'status': 'operational',
        'systems': ai_status,
        'active_bots': len(bot_manager.get_all_bots()),
        'timestamp': datetime.now().isoformat()
    })

# Prediction Engine Endpoints
@app.route('/api/ai/prediction/<symbol>', methods=['GET'])
def get_prediction(symbol):
    """Get price prediction for a symbol"""
    timeframe = request.args.get('timeframe', '1h')
    try:
        prediction = prediction_api.get_prediction(symbol.upper(), timeframe)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/predictions/batch', methods=['POST'])
def get_batch_predictions():
    """Get predictions for multiple symbols"""
    data = request.get_json()
    symbols = data.get('symbols', [])
    timeframe = data.get('timeframe', '1h')
    
    predictions = {}
    for symbol in symbols:
        try:
            prediction = prediction_api.get_prediction(symbol.upper(), timeframe)
            predictions[symbol] = prediction
        except Exception as e:
            predictions[symbol] = {'error': str(e)}
    
    return jsonify(predictions)

@app.route('/api/ai/market-signals', methods=['GET'])
def get_market_signals():
    """Get current market signals"""
    try:
        signals = prediction_api.get_market_signals()
        return jsonify(signals)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/model-performance', methods=['GET'])
def get_model_performance():
    """Get AI model performance metrics"""
    try:
        performance = prediction_api.get_model_performance()
        return jsonify(performance)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Trading Bot Endpoints
@app.route('/api/ai/bots', methods=['GET'])
def get_all_bots():
    """Get all trading bots"""
    try:
        bots = bot_manager.get_all_bots()
        return jsonify(bots)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/bots', methods=['POST'])
def create_bot():
    """Create a new trading bot"""
    data = request.get_json()
    
    try:
        bot_id = bot_manager.create_bot(
            name=data['name'],
            strategy_name=data['strategy'],
            symbols=data['symbols'],
            initial_balance=data.get('initial_balance', 10000),
            strategy_params=data.get('strategy_params')
        )
        
        return jsonify({
            'bot_id': bot_id,
            'message': 'Bot created successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/bots/<bot_id>', methods=['GET'])
def get_bot_details(bot_id):
    """Get detailed information about a specific bot"""
    try:
        details = bot_manager.get_bot_details(bot_id)
        if details is None:
            return jsonify({'error': 'Bot not found'}), 404
        return jsonify(details)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/bots/<bot_id>/start', methods=['POST'])
def start_bot(bot_id):
    """Start a trading bot"""
    try:
        bot_manager.start_bot(bot_id)
        return jsonify({'message': 'Bot started successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/bots/<bot_id>/stop', methods=['POST'])
def stop_bot(bot_id):
    """Stop a trading bot"""
    try:
        bot_manager.stop_bot(bot_id)
        return jsonify({'message': 'Bot stopped successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/bots/<bot_id>/pause', methods=['POST'])
def pause_bot(bot_id):
    """Pause a trading bot"""
    try:
        bot_manager.pause_bot(bot_id)
        return jsonify({'message': 'Bot paused successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/bots/<bot_id>/resume', methods=['POST'])
def resume_bot(bot_id):
    """Resume a trading bot"""
    try:
        bot_manager.resume_bot(bot_id)
        return jsonify({'message': 'Bot resumed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/bots/<bot_id>', methods=['DELETE'])
def delete_bot(bot_id):
    """Delete a trading bot"""
    try:
        bot_manager.delete_bot(bot_id)
        return jsonify({'message': 'Bot deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/strategies', methods=['GET'])
def get_available_strategies():
    """Get available trading strategies"""
    try:
        strategies = bot_manager.get_available_strategies()
        return jsonify(strategies)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Sentiment Analysis Endpoints
@app.route('/api/ai/sentiment/<symbol>', methods=['GET'])
def get_sentiment_analysis(symbol):
    """Get sentiment analysis for a symbol"""
    try:
        sentiment = sentiment_api.get_sentiment_analysis(symbol.upper())
        return jsonify(sentiment)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/sentiment/batch', methods=['POST'])
def get_batch_sentiment():
    """Get sentiment analysis for multiple symbols"""
    data = request.get_json()
    symbols = data.get('symbols', [])
    
    try:
        sentiment_summary = sentiment_api.get_sentiment_summary([s.upper() for s in symbols])
        return jsonify(sentiment_summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/market-intelligence', methods=['GET'])
def get_market_intelligence():
    """Get overall market intelligence"""
    try:
        intelligence = sentiment_api.get_market_intelligence()
        return jsonify(intelligence)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/trending-topics', methods=['GET'])
def get_trending_topics():
    """Get trending topics in cryptocurrency"""
    try:
        topics = sentiment_api.get_trending_topics()
        return jsonify(topics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/analyze-text', methods=['POST'])
def analyze_custom_text():
    """Analyze sentiment of custom text"""
    data = request.get_json()
    text = data.get('text', '')
    symbol = data.get('symbol')
    
    try:
        analysis = sentiment_api.analyze_custom_text(text, symbol)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Combined AI Insights Endpoints
@app.route('/api/ai/insights/<symbol>', methods=['GET'])
def get_combined_insights(symbol):
    """Get combined AI insights for a symbol"""
    try:
        # Get prediction
        prediction = prediction_api.get_prediction(symbol.upper(), '1h')
        
        # Get sentiment
        sentiment = sentiment_api.get_sentiment_analysis(symbol.upper())
        
        # Combine insights
        combined_insights = {
            'symbol': symbol.upper(),
            'prediction': prediction,
            'sentiment': sentiment,
            'ai_recommendation': _generate_ai_recommendation(prediction, sentiment),
            'confidence_score': _calculate_combined_confidence(prediction, sentiment),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(combined_insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/dashboard-data', methods=['GET'])
def get_dashboard_data():
    """Get comprehensive AI dashboard data"""
    try:
        # Get market overview
        symbols = ['BTC', 'ETH', 'DGD', 'ADA', 'SOL']
        
        # Get predictions for all symbols
        predictions = {}
        for symbol in symbols:
            predictions[symbol] = prediction_api.get_prediction(symbol, '1h')
        
        # Get sentiment summary
        sentiment_summary = sentiment_api.get_sentiment_summary(symbols)
        
        # Get market intelligence
        market_intelligence = sentiment_api.get_market_intelligence()
        
        # Get trading bots status
        bots = bot_manager.get_all_bots()
        
        # Get trending topics
        trending_topics = sentiment_api.get_trending_topics()
        
        # Get market signals
        market_signals = prediction_api.get_market_signals()
        
        dashboard_data = {
            'predictions': predictions,
            'sentiment_summary': sentiment_summary,
            'market_intelligence': market_intelligence,
            'trading_bots': {
                'total_bots': len(bots),
                'active_bots': len([b for b in bots if b['status'] == 'active']),
                'bots': bots[:5]  # Top 5 bots
            },
            'trending_topics': trending_topics[:5],  # Top 5 topics
            'market_signals': market_signals[:10],  # Top 10 signals
            'ai_status': ai_status,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(dashboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _generate_ai_recommendation(prediction, sentiment):
    """Generate combined AI recommendation"""
    if 'error' in prediction or 'error' in sentiment:
        return 'INSUFFICIENT_DATA'
    
    pred_rec = prediction.get('recommendation', 'HOLD')
    sent_score = sentiment.get('overall_sentiment', 0)
    
    # Combine prediction and sentiment
    if pred_rec in ['STRONG_BUY', 'BUY'] and sent_score > 0.2:
        return 'STRONG_BUY'
    elif pred_rec in ['STRONG_BUY', 'BUY'] and sent_score > -0.2:
        return 'BUY'
    elif pred_rec in ['STRONG_SELL', 'SELL'] and sent_score < -0.2:
        return 'STRONG_SELL'
    elif pred_rec in ['STRONG_SELL', 'SELL'] and sent_score < 0.2:
        return 'SELL'
    else:
        return 'HOLD'

def _calculate_combined_confidence(prediction, sentiment):
    """Calculate combined confidence score"""
    if 'error' in prediction or 'error' in sentiment:
        return 0.0
    
    pred_conf = prediction.get('confidence', 0)
    sent_conf = sentiment.get('confidence', 0)
    
    # Weighted average (prediction 60%, sentiment 40%)
    combined_conf = (pred_conf * 0.6) + (sent_conf * 0.4)
    return round(combined_conf, 3)

def update_ai_status():
    """Background task to update AI system status"""
    while True:
        try:
            ai_status['last_update'] = datetime.now().isoformat()
            time.sleep(60)  # Update every minute
        except Exception as e:
            print(f"Error updating AI status: {e}")
            time.sleep(60)

if __name__ == '__main__':
    # Start background status updater
    status_thread = threading.Thread(target=update_ai_status, daemon=True)
    status_thread.start()
    
    print("Starting AI API Server...")
    print("Available endpoints:")
    print("- GET /api/ai/status - AI system status")
    print("- GET /api/ai/prediction/<symbol> - Price predictions")
    print("- GET /api/ai/sentiment/<symbol> - Sentiment analysis")
    print("- GET /api/ai/bots - Trading bots management")
    print("- GET /api/ai/dashboard-data - Complete dashboard data")
    
    app.run(host='0.0.0.0', port=5003, debug=True)

