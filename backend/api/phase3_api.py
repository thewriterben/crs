#!/usr/bin/env python3
"""
Phase 3 API Server - Enhanced Features
Provides endpoints for advanced AI models, DeFi integration, social trading, and portfolio automation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import datetime
from typing import Dict, List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Phase 3 modules
from ai.advanced_models import (
    LSTMPredictor, TransformerPredictor, EnsemblePredictor, BERTSentimentAnalyzer
)
from defi.defi_integration import (
    DEXAggregator, YieldFarmingManager, StakingManager, LiquidityPoolManager
)

# Import social trading and portfolio automation modules
from social.social_trading import CopyTradingSystem, TradingSignalsGenerator, PortfolioSharingSystem
from portfolio.portfolio_automation import (
    PortfolioRebalancer, RiskManagementSystem, DollarCostAveragingSystem, StopLossAutomation
)

# Initialize social trading systems
copy_trading = CopyTradingSystem()
trading_signals = TradingSignalsGenerator()
portfolio_sharing = PortfolioSharingSystem()

# Initialize portfolio automation systems
portfolio_rebalancer = PortfolioRebalancer()
risk_manager = RiskManagementSystem()
dca_system = DollarCostAveragingSystem()
stop_loss_automation = StopLossAutomation()


# ==================== Social Trading Endpoints ====================



app = Flask(__name__)
CORS(app)

# Initialize Phase 3 systems
lstm_predictor = LSTMPredictor(lookback_period=60)
transformer_predictor = TransformerPredictor(n_heads=8)
ensemble_predictor = EnsemblePredictor()
bert_sentiment = BERTSentimentAnalyzer()

dex_aggregator = DEXAggregator()
yield_farming = YieldFarmingManager()
staking_manager = StakingManager()
liquidity_manager = LiquidityPoolManager()

# ==================== Advanced AI Model Endpoints ====================

@app.route('/api/phase3/ai/lstm/predict', methods=['POST'])
def lstm_predict():
    """Get LSTM model prediction"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'BTC')
        historical_data = data.get('historical_data', [])
        
        # For demo, use simulated data if not provided
        if not historical_data:
            import numpy as np
            # Generate sample data
            historical_data = np.random.randn(100, 5) * 100 + 45000
        else:
            import numpy as np
            historical_data = np.array(historical_data)
        
        # Train if not trained
        if not lstm_predictor.is_trained:
            train_result = lstm_predictor.train(historical_data)
        
        # Predict
        prediction = lstm_predictor.predict(historical_data)
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'model': 'LSTM',
            'prediction': prediction.prediction,
            'confidence': prediction.confidence,
            'feature_importance': prediction.feature_importance,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/ai/transformer/predict', methods=['POST'])
def transformer_predict():
    """Get Transformer model prediction"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'BTC')
        historical_data = data.get('historical_data', [])
        
        # For demo, use simulated data if not provided
        if not historical_data:
            import numpy as np
            historical_data = np.random.randn(100, 5) * 100 + 45000
        else:
            import numpy as np
            historical_data = np.array(historical_data)
        
        # Train if not trained
        if not transformer_predictor.is_trained:
            train_result = transformer_predictor.train(historical_data)
        
        # Predict
        prediction = transformer_predictor.predict(historical_data)
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'model': 'Transformer',
            'prediction': prediction.prediction,
            'confidence': prediction.confidence,
            'feature_importance': prediction.feature_importance,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/ai/ensemble/predict', methods=['POST'])
def ensemble_predict():
    """Get ensemble prediction from all models"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'BTC')
        historical_data = data.get('historical_data', [])
        features = data.get('features', [])
        
        # For demo, use simulated data if not provided
        if not historical_data:
            import numpy as np
            historical_data = np.random.randn(100, 5) * 100 + 45000
            features = np.random.randn(100, 14)  # 14 features
        else:
            import numpy as np
            historical_data = np.array(historical_data)
            features = np.array(features)
        
        # Train ensemble if not trained
        if not ensemble_predictor.is_trained:
            train_result = ensemble_predictor.train(historical_data, features)
        
        # Get current features (last row)
        current_features = features[-1] if len(features) > 0 else features
        
        # Predict
        result = ensemble_predictor.predict(historical_data, current_features)
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'ensemble_prediction': result['ensemble_prediction'],
            'confidence': result['confidence'],
            'individual_predictions': result['individual_predictions'],
            'model_agreement': result['model_agreement'],
            'variance': result['variance'],
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/ai/sentiment/analyze', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment using BERT-style analyzer"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        texts = data.get('texts', [])
        
        if texts:
            # Batch analysis
            result = bert_sentiment.batch_analyze(texts)
        else:
            # Single text analysis
            result = bert_sentiment.analyze(text)
        
        return jsonify({
            'success': True,
            **result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== DeFi Integration Endpoints ====================

@app.route('/api/phase3/defi/dex/quote', methods=['GET'])
def get_dex_quote():
    """Get DEX swap quote"""
    try:
        token_in = request.args.get('tokenIn', 'ETH')
        token_out = request.args.get('tokenOut', 'USDT')
        amount_in = float(request.args.get('amountIn', 1.0))
        dex = request.args.get('dex', None)
        
        quotes = dex_aggregator.get_quote(token_in, token_out, amount_in, dex)
        
        # Convert dataclasses to dict
        quotes_dict = [
            {
                'token_in': q.token_in,
                'token_out': q.token_out,
                'amount_in': q.amount_in,
                'amount_out': q.amount_out,
                'price': q.price,
                'price_impact': q.price_impact,
                'gas_estimate': q.gas_estimate,
                'dex_name': q.dex_name
            }
            for q in quotes
        ]
        
        return jsonify({
            'success': True,
            'quotes': quotes_dict,
            'best_quote': quotes_dict[0] if quotes_dict else None,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/defi/dex/swap', methods=['POST'])
def execute_dex_swap():
    """Execute DEX swap"""
    try:
        data = request.get_json()
        token_in = data.get('tokenIn')
        token_out = data.get('tokenOut')
        amount_in = float(data.get('amountIn'))
        dex_name = data.get('dex', 'Uniswap')
        user_address = data.get('userAddress', '0x0000000000000000000000000000000000000000')
        slippage = float(data.get('slippage', 0.01))
        
        # Get quote
        quotes = dex_aggregator.get_quote(token_in, token_out, amount_in, dex_name)
        best_quote = quotes[0]
        
        # Execute swap
        result = dex_aggregator.execute_swap(best_quote, user_address, slippage)
        
        return jsonify({
            'success': True,
            **result
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/defi/farming/opportunities', methods=['GET'])
def get_farming_opportunities():
    """Get yield farming opportunities"""
    try:
        min_apy = float(request.args.get('minApy', 0))
        risk_level = request.args.get('riskLevel', None)
        
        opportunities = yield_farming.get_opportunities(min_apy, risk_level)
        
        return jsonify({
            'success': True,
            'opportunities': opportunities,
            'count': len(opportunities),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/defi/farming/deposit', methods=['POST'])
def deposit_to_farm():
    """Deposit to yield farm"""
    try:
        data = request.get_json()
        farm_id = data.get('farmId')
        amount = float(data.get('amount'))
        user_id = data.get('userId', 'demo_user')
        
        position = yield_farming.deposit(farm_id, amount, user_id)
        
        return jsonify({
            'success': True,
            'position': {
                'farm_id': position.farm_id,
                'pool_name': position.pool_name,
                'deposited_amount': position.deposited_amount,
                'current_value': position.current_value,
                'rewards_earned': position.rewards_earned,
                'apy': position.apy,
                'start_date': position.start_date.isoformat()
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/defi/farming/positions', methods=['GET'])
def get_farming_positions():
    """Get user's farming positions"""
    try:
        user_id = request.args.get('userId', 'demo_user')
        
        positions = yield_farming.get_positions(user_id)
        
        positions_dict = [
            {
                'farm_id': p.farm_id,
                'pool_name': p.pool_name,
                'deposited_amount': p.deposited_amount,
                'current_value': p.current_value,
                'rewards_earned': p.rewards_earned,
                'apy': p.apy,
                'start_date': p.start_date.isoformat()
            }
            for p in positions
        ]
        
        return jsonify({
            'success': True,
            'positions': positions_dict,
            'count': len(positions_dict),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/defi/staking/options', methods=['GET'])
def get_staking_options():
    """Get available staking options"""
    try:
        options = staking_manager.get_staking_options()
        
        return jsonify({
            'success': True,
            'staking_options': options,
            'count': len(options),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/defi/staking/stake', methods=['POST'])
def stake_tokens():
    """Stake tokens"""
    try:
        data = request.get_json()
        token = data.get('token')
        amount = float(data.get('amount'))
        user_id = data.get('userId', 'demo_user')
        
        position = staking_manager.stake(token, amount, user_id)
        
        return jsonify({
            'success': True,
            'position': {
                'staking_id': position.staking_id,
                'token': position.token,
                'amount': position.amount,
                'rewards': position.rewards,
                'apy': position.apy,
                'lock_period': position.lock_period,
                'unlock_date': position.unlock_date.isoformat()
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/defi/staking/positions', methods=['GET'])
def get_staking_positions():
    """Get user's staking positions"""
    try:
        user_id = request.args.get('userId', 'demo_user')
        
        positions = staking_manager.get_stakes(user_id)
        
        positions_dict = [
            {
                'staking_id': p.staking_id,
                'token': p.token,
                'amount': p.amount,
                'rewards': p.rewards,
                'apy': p.apy,
                'lock_period': p.lock_period,
                'unlock_date': p.unlock_date.isoformat()
            }
            for p in positions
        ]
        
        return jsonify({
            'success': True,
            'positions': positions_dict,
            'count': len(positions_dict),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/defi/liquidity/pools', methods=['GET'])
def get_liquidity_pools():
    """Get available liquidity pools"""
    try:
        pools = liquidity_manager.get_pools()
        
        return jsonify({
            'success': True,
            'pools': pools,
            'count': len(pools),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/defi/liquidity/add', methods=['POST'])
def add_liquidity():
    """Add liquidity to pool"""
    try:
        data = request.get_json()
        pool_id = data.get('poolId')
        amount0 = float(data.get('amount0'))
        amount1 = float(data.get('amount1'))
        user_id = data.get('userId', 'demo_user')
        
        result = liquidity_manager.add_liquidity(pool_id, amount0, amount1, user_id)
        
        # Convert datetime to string
        if 'position' in result and 'entry_date' in result['position']:
            result['position']['entry_date'] = result['position']['entry_date'].isoformat()
        
        return jsonify({
            **result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/defi/liquidity/positions', methods=['GET'])
def get_liquidity_positions():
    """Get user's liquidity positions"""
    try:
        user_id = request.args.get('userId', 'demo_user')
        
        positions = liquidity_manager.get_positions(user_id)
        
        # Convert datetime objects
        for pos in positions:
            if 'entry_date' in pos:
                pos['entry_date'] = pos['entry_date'].isoformat()
        
        return jsonify({
            'success': True,
            'positions': positions,
            'count': len(positions),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/social/traders/top', methods=['GET'])
def get_top_traders():
    """Get top performing traders"""
    try:
        limit = int(request.args.get('limit', 10))
        traders = copy_trading.get_top_traders(limit=limit)
        
        return jsonify({
            'success': True,
            'traders': traders,
            'count': len(traders),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/social/traders/follow', methods=['POST'])
def follow_trader():
    """Follow a trader for copy trading"""
    try:
        data = request.get_json()
        follower_id = data.get('followerId', 'demo_user')
        trader_id = data.get('traderId')
        copy_amount = float(data.get('copyAmount', 1000))
        
        result = copy_trading.follow_trader(follower_id, trader_id, copy_amount)
        
        return jsonify({
            **result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/social/signals', methods=['GET'])
def get_trading_signals():
    """Get AI-generated trading signals"""
    try:
        symbol = request.args.get('symbol', None)
        signals = trading_signals.get_signals(symbol=symbol)
        
        # Convert datetime objects to strings
        for signal in signals:
            if 'created_at' in signal and isinstance(signal['created_at'], datetime):
                signal['created_at'] = signal['created_at'].isoformat()
        
        return jsonify({
            'success': True,
            'signals': signals,
            'count': len(signals),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/social/portfolios/featured', methods=['GET'])
def get_featured_portfolios():
    """Get featured portfolios"""
    try:
        sort_by = request.args.get('sortBy', 'followers')
        portfolios = portfolio_sharing.get_featured_portfolios(sort_by=sort_by)
        
        return jsonify({
            'success': True,
            'portfolios': portfolios,
            'count': len(portfolios),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Portfolio Automation Endpoints ====================

@app.route('/api/phase3/portfolio/rebalance/analyze', methods=['POST'])
def analyze_rebalance():
    """Analyze portfolio for rebalancing needs"""
    try:
        data = request.get_json()
        current_allocation = data.get('currentAllocation', {})
        target_allocation = data.get('targetAllocation', {})
        
        analysis = portfolio_rebalancer.analyze_portfolio(current_allocation, target_allocation)
        
        return jsonify({
            'success': True,
            **analysis
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/portfolio/rebalance/orders', methods=['POST'])
def generate_rebalance_orders():
    """Generate orders to rebalance portfolio"""
    try:
        data = request.get_json()
        portfolio_value = float(data.get('portfolioValue', 100000))
        drifts = data.get('drifts', {})
        
        orders = portfolio_rebalancer.generate_rebalance_orders(portfolio_value, drifts)
        
        return jsonify({
            'success': True,
            'orders': orders,
            'count': len(orders),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/portfolio/risk/assess', methods=['POST'])
def assess_portfolio_risk():
    """Assess portfolio risk"""
    try:
        data = request.get_json()
        positions = data.get('positions', [])
        
        assessment = risk_manager.assess_portfolio_risk(positions)
        
        return jsonify({
            'success': True,
            **assessment,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/portfolio/position-size', methods=['POST'])
def calculate_position_size():
    """Calculate optimal position size"""
    try:
        data = request.get_json()
        portfolio_value = float(data.get('portfolioValue', 100000))
        risk_per_trade = float(data.get('riskPerTrade', 0.02))
        stop_loss_pct = float(data.get('stopLossPct', 0.05))
        
        result = risk_manager.calculate_position_size(portfolio_value, risk_per_trade, stop_loss_pct)
        
        return jsonify({
            'success': True,
            **result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/portfolio/dca/create', methods=['POST'])
def create_dca_schedule():
    """Create DCA schedule"""
    try:
        data = request.get_json()
        user_id = data.get('userId', 'demo_user')
        asset = data.get('asset')
        amount = float(data.get('amount'))
        frequency = data.get('frequency', 'weekly')
        duration = int(data.get('durationMonths', 12))
        
        schedule = dca_system.create_dca_schedule(user_id, asset, amount, frequency, duration)
        
        # Convert datetime objects
        schedule['started_at'] = schedule['started_at'].isoformat()
        schedule['next_execution'] = schedule['next_execution'].isoformat()
        
        return jsonify({
            'success': True,
            'schedule': schedule,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/portfolio/dca/schedules', methods=['GET'])
def get_dca_schedules():
    """Get active DCA schedules"""
    try:
        user_id = request.args.get('userId', 'demo_user')
        schedules = dca_system.get_active_schedules(user_id)
        
        return jsonify({
            'success': True,
            'schedules': schedules,
            'count': len(schedules),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/portfolio/stop-loss/create', methods=['POST'])
def create_stop_loss():
    """Create trailing stop loss order"""
    try:
        data = request.get_json()
        position_id = data.get('positionId')
        symbol = data.get('symbol')
        entry_price = float(data.get('entryPrice'))
        trailing_pct = float(data.get('trailingPct', 0.05))
        take_profit_pct = data.get('takeProfitPct')
        
        if take_profit_pct:
            take_profit_pct = float(take_profit_pct)
        
        order = stop_loss_automation.create_trailing_stop(
            position_id, symbol, entry_price, trailing_pct, take_profit_pct
        )
        
        # Convert datetime
        order['created_at'] = order['created_at'].isoformat()
        
        return jsonify({
            'success': True,
            'order': order,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/phase3/portfolio/stop-loss/active', methods=['GET'])
def get_active_stops():
    """Get active stop loss orders"""
    try:
        position_id = request.args.get('positionId', None)
        orders = stop_loss_automation.get_active_stops(position_id=position_id)
        
        return jsonify({
            'success': True,
            'orders': orders,
            'count': len(orders),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Status and Health Endpoints ====================

@app.route('/api/phase3/status', methods=['GET'])
def get_phase3_status():
    """Get Phase 3 features status"""
    return jsonify({
        'status': 'operational',
        'features': {
            'advanced_ai_models': {
                'lstm': 'active',
                'transformer': 'active',
                'ensemble': 'active',
                'bert_sentiment': 'active'
            },
            'defi_integration': {
                'dex_aggregator': 'active',
                'yield_farming': 'active',
                'staking': 'active',
                'liquidity_pools': 'active'
            },
            'social_trading': 'planned',
            'portfolio_automation': 'planned'
        },
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/phase3/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '3.0.0',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("Starting Phase 3 API Server...")
    print("\n=== Available Endpoints ===")
    print("\nAdvanced AI Models:")
    print("  POST /api/phase3/ai/lstm/predict - LSTM predictions")
    print("  POST /api/phase3/ai/transformer/predict - Transformer predictions")
    print("  POST /api/phase3/ai/ensemble/predict - Ensemble predictions")
    print("  POST /api/phase3/ai/sentiment/analyze - BERT sentiment analysis")
    print("\nDeFi Integration:")
    print("  GET  /api/phase3/defi/dex/quote - Get DEX quotes")
    print("  POST /api/phase3/defi/dex/swap - Execute DEX swap")
    print("  GET  /api/phase3/defi/farming/opportunities - Yield farming opportunities")
    print("  POST /api/phase3/defi/farming/deposit - Deposit to farm")
    print("  GET  /api/phase3/defi/farming/positions - Get farming positions")
    print("  GET  /api/phase3/defi/staking/options - Staking options")
    print("  POST /api/phase3/defi/staking/stake - Stake tokens")
    print("  GET  /api/phase3/defi/staking/positions - Get staking positions")
    print("  GET  /api/phase3/defi/liquidity/pools - Liquidity pools")
    print("  POST /api/phase3/defi/liquidity/add - Add liquidity")
    print("  GET  /api/phase3/defi/liquidity/positions - Get liquidity positions")
    print("\nSocial Trading:")
    print("  GET  /api/phase3/social/traders/top - Top traders")
    print("  POST /api/phase3/social/traders/follow - Follow trader")
    print("  GET  /api/phase3/social/signals - Trading signals")
    print("  GET  /api/phase3/social/portfolios/featured - Featured portfolios")
    print("\nPortfolio Automation:")
    print("  POST /api/phase3/portfolio/rebalance/analyze - Analyze rebalancing")
    print("  POST /api/phase3/portfolio/rebalance/orders - Generate orders")
    print("  POST /api/phase3/portfolio/risk/assess - Assess risk")
    print("  POST /api/phase3/portfolio/position-size - Calculate position size")
    print("  POST /api/phase3/portfolio/dca/create - Create DCA schedule")
    print("  GET  /api/phase3/portfolio/dca/schedules - Get DCA schedules")
    print("  POST /api/phase3/portfolio/stop-loss/create - Create stop loss")
    print("  GET  /api/phase3/portfolio/stop-loss/active - Get active stops")
    print("\nStatus:")
    print("  GET  /api/phase3/status - Feature status")
    print("  GET  /api/phase3/health - Health check")
    print("\nServer running on http://0.0.0.0:5006")
    
    app.run(host='0.0.0.0', port=5006, debug=True)
