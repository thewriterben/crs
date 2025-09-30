"""
Tests for AI prediction engine
"""
import pytest
import sys
import os

# Add ai directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai.ai_prediction_engine import AIPredictionEngine


@pytest.mark.unit
@pytest.mark.ai
class TestAIPredictionEngine:
    """Test AI prediction engine"""
    
    @pytest.fixture
    def engine(self):
        """Create prediction engine instance"""
        return AIPredictionEngine()
    
    def test_engine_initialization(self, engine):
        """Test engine initializes correctly"""
        assert engine is not None
        assert hasattr(engine, 'generate_predictions')
    
    def test_generate_predictions_structure(self, engine):
        """Test prediction output structure"""
        predictions = engine.generate_predictions('BTC')
        
        assert predictions is not None
        assert 'symbol' in predictions
        assert 'predictions' in predictions
        assert 'model_consensus' in predictions
        assert predictions['symbol'] == 'BTC'
    
    def test_predictions_have_required_fields(self, engine):
        """Test predictions contain required fields"""
        predictions = engine.generate_predictions('ETH')
        
        pred_list = predictions.get('predictions', [])
        assert len(pred_list) > 0
        
        for pred in pred_list:
            assert 'model' in pred
            assert 'prediction' in pred
            assert 'confidence' in pred
            assert 'timestamp' in pred
    
    def test_model_consensus(self, engine):
        """Test model consensus calculation"""
        predictions = engine.generate_predictions('BTC')
        consensus = predictions.get('model_consensus', {})
        
        assert 'predicted_price' in consensus
        assert 'confidence' in consensus
        assert 'direction' in consensus
        assert consensus['direction'] in ['bullish', 'bearish', 'neutral']
    
    def test_multiple_symbols(self, engine):
        """Test predictions for multiple symbols"""
        symbols = ['BTC', 'ETH', 'USDT']
        
        for symbol in symbols:
            predictions = engine.generate_predictions(symbol)
            assert predictions['symbol'] == symbol
            assert len(predictions['predictions']) > 0
