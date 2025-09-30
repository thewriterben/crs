"""
Tests for trading engine
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from trading.advanced_trading_engine import AdvancedOrderManager, TradingAPI


@pytest.mark.unit
@pytest.mark.trading
class TestAdvancedOrderManager:
    """Test advanced order manager"""
    
    @pytest.fixture
    def order_manager(self):
        """Create order manager instance"""
        return AdvancedOrderManager()
    
    def test_initialization(self, order_manager):
        """Test order manager initialization"""
        assert order_manager is not None
        assert len(order_manager.market_data) > 0
        assert len(order_manager.order_books) > 0
    
    def test_place_market_order(self, order_manager):
        """Test placing market order"""
        order_data = {
            'user_id': 'user123',
            'symbol': 'BTC/USDT',
            'order_type': 'market',
            'side': 'buy',
            'quantity': 0.1
        }
        
        result = order_manager.place_order(order_data)
        
        assert result['success'] is True
        assert 'order_id' in result
        assert 'order' in result
        assert result['order']['status'] in ['filled', 'partially_filled']
    
    def test_place_limit_order(self, order_manager):
        """Test placing limit order"""
        order_data = {
            'user_id': 'user123',
            'symbol': 'ETH/USDT',
            'order_type': 'limit',
            'side': 'buy',
            'quantity': 1.0,
            'price': 3000.0
        }
        
        result = order_manager.place_order(order_data)
        
        assert result['success'] is True
        assert 'order_id' in result
        assert result['order']['order_type'] == 'limit'
    
    def test_cancel_order(self, order_manager):
        """Test canceling an order"""
        # First place an order
        order_data = {
            'user_id': 'user123',
            'symbol': 'BTC/USDT',
            'order_type': 'limit',
            'side': 'buy',
            'quantity': 0.1,
            'price': 45000.0
        }
        
        place_result = order_manager.place_order(order_data)
        order_id = place_result['order_id']
        
        # Then cancel it
        cancel_result = order_manager.cancel_order(order_id, 'user123')
        
        assert cancel_result['success'] is True
        assert cancel_result['order']['status'] == 'cancelled'
    
    def test_get_order_status(self, order_manager):
        """Test getting order status"""
        # Place an order
        order_data = {
            'user_id': 'user123',
            'symbol': 'BTC/USDT',
            'order_type': 'market',
            'side': 'buy',
            'quantity': 0.1
        }
        
        place_result = order_manager.place_order(order_data)
        order_id = place_result['order_id']
        
        # Get status
        status = order_manager.get_order_status(order_id)
        
        assert status['success'] is True
        assert 'order' in status
        assert status['order']['order_id'] == order_id


@pytest.mark.integration
@pytest.mark.trading
class TestTradingAPI:
    """Test trading API"""
    
    @pytest.fixture
    def trading_api(self):
        """Create trading API instance"""
        return TradingAPI()
    
    def test_trading_api_initialization(self, trading_api):
        """Test trading API initialization"""
        assert trading_api is not None
        assert trading_api.order_manager is not None
        assert trading_api.algo_trading is not None
    
    def test_get_order_book(self, trading_api):
        """Test getting order book"""
        result = trading_api.get_order_book('BTC/USDT')
        
        assert result['success'] is True
        assert 'order_book' in result
        assert 'bids' in result['order_book']
        assert 'asks' in result['order_book']
