"""
Integration tests for CFV API

Tests the CFV API endpoints including:
- Supported coins endpoint
- CFV calculation endpoint
- Payment info endpoint
- Order creation
- Payment creation and confirmation
"""

import pytest
import json
from datetime import datetime, timedelta


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def sample_order_data():
    """Sample order data for testing"""
    return {
        'user_id': 1,
        'items': [
            {
                'product_id': 'test_prod_1',
                'name': 'Test Product 1',
                'quantity': 2,
                'price': 50.0
            },
            {
                'product_id': 'test_prod_2',
                'name': 'Test Product 2',
                'quantity': 1,
                'price': 30.0
            }
        ],
        'cryptocurrency': 'XNO',
        'shipping_address': {
            'name': 'Test User',
            'street': '123 Test St',
            'city': 'Test City',
            'state': 'TS',
            'zip': '12345',
            'country': 'USA'
        },
        'shipping_method': 'standard',
        'shipping_cost': 10.0
    }


class TestCFVCoinsEndpoint:
    """Test /api/cfv/coins endpoint"""
    
    def test_get_supported_coins(self, client):
        """Test getting list of supported coins"""
        response = client.get('/api/cfv/coins')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'coins' in data
        assert 'count' in data
        assert data['count'] == 12
        
        # Verify all coins have required fields
        for coin in data['coins']:
            assert 'symbol' in coin
            assert 'name' in coin
            assert 'category' in coin
            assert 'discount' in coin
    
    def test_coins_sorted_by_discount(self, client):
        """Test that coins are sorted by discount (highest first)"""
        response = client.get('/api/cfv/coins')
        data = json.loads(response.data)
        
        discounts = [coin['discount'] for coin in data['coins']]
        
        # Check if sorted in descending order
        assert discounts == sorted(discounts, reverse=True)


class TestCFVCalculateEndpoint:
    """Test /api/cfv/calculate/:symbol endpoint"""
    
    def test_calculate_cfv_valid_coin(self, client):
        """Test CFV calculation for valid cryptocurrency"""
        response = client.get('/api/cfv/calculate/XNO')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['symbol'] == 'XNO'
        assert 'cfv' in data
        assert 'discount' in data
        assert 'metrics' in data
        
        # Verify CFV data structure
        cfv = data['cfv']
        assert 'currentPrice' in cfv
        assert 'fairValue' in cfv
        assert 'valuationPercent' in cfv
        assert 'valuationStatus' in cfv
    
    def test_calculate_cfv_invalid_coin(self, client):
        """Test CFV calculation for invalid cryptocurrency"""
        response = client.get('/api/cfv/calculate/INVALID')
        
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
    
    def test_calculate_cfv_with_refresh(self, client):
        """Test CFV calculation with cache refresh"""
        # First call
        response1 = client.get('/api/cfv/calculate/XNO')
        assert response1.status_code == 200
        
        # Second call with refresh
        response2 = client.get('/api/cfv/calculate/XNO?refresh=true')
        assert response2.status_code == 200
        
        # Both should succeed
        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        assert data1['success'] is True
        assert data2['success'] is True


class TestPaymentInfoEndpoint:
    """Test /api/cfv/payment-info/:symbol endpoint"""
    
    def test_get_payment_info_valid(self, client):
        """Test getting payment info with valid data"""
        response = client.post(
            '/api/cfv/payment-info/XNO',
            data=json.dumps({'amount_usd': 100.0}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'payment_info' in data
        
        payment_info = data['payment_info']
        assert payment_info['symbol'] == 'XNO'
        assert payment_info['originalPriceUSD'] == 100.0
        assert 'discountPercent' in payment_info
        assert 'finalPriceUSD' in payment_info
        assert 'amountCrypto' in payment_info
        
        # Verify discount calculation
        discount = payment_info['discountPercent']
        expected_final = 100.0 * (1 - discount / 100)
        assert abs(payment_info['finalPriceUSD'] - expected_final) < 0.01
    
    def test_get_payment_info_missing_amount(self, client):
        """Test getting payment info without amount"""
        response = client.post(
            '/api/cfv/payment-info/XNO',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'amount_usd' in data['error']
    
    def test_get_payment_info_negative_amount(self, client):
        """Test getting payment info with negative amount"""
        response = client.post(
            '/api/cfv/payment-info/XNO',
            data=json.dumps({'amount_usd': -100.0}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False


class TestOrdersEndpoint:
    """Test /api/orders endpoint"""
    
    def test_create_order_valid(self, client, sample_order_data):
        """Test creating a valid order"""
        response = client.post(
            '/api/orders',
            data=json.dumps(sample_order_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'order' in data
        
        order = data['order']
        assert 'order_id' in order
        assert order['user_id'] == 1
        assert order['subtotal'] == 130.0  # 2*50 + 1*30
        assert order['original_price_usd'] == 140.0  # subtotal + shipping
        assert 'cfv_discount' in order
        assert 'cfv_metrics' in order
        assert order['status'] == 'pending'
    
    def test_create_order_missing_items(self, client):
        """Test creating order without items"""
        response = client.post(
            '/api/orders',
            data=json.dumps({'cryptocurrency': 'XNO'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'items' in data['error']
    
    def test_create_order_invalid_crypto(self, client, sample_order_data):
        """Test creating order with invalid cryptocurrency"""
        sample_order_data['cryptocurrency'] = 'INVALID'
        
        response = client.post(
            '/api/orders',
            data=json.dumps(sample_order_data),
            content_type='application/json'
        )
        
        # Should still create order but with 0% discount
        # Or return error - depends on implementation
        data = json.loads(response.data)
        # Implementation specific


class TestPaymentsEndpoint:
    """Test payment creation and confirmation endpoints"""
    
    def test_create_payment_valid(self, client, sample_order_data):
        """Test creating a payment for an order"""
        # First create an order
        order_response = client.post(
            '/api/orders',
            data=json.dumps(sample_order_data),
            content_type='application/json'
        )
        
        order_data = json.loads(order_response.data)
        order_id = order_data['order']['order_id']
        
        # Create payment
        payment_response = client.post(
            '/api/payments/create',
            data=json.dumps({
                'order_id': order_id,
                'cryptocurrency': 'XNO'
            }),
            content_type='application/json'
        )
        
        assert payment_response.status_code == 201
        
        data = json.loads(payment_response.data)
        assert data['success'] is True
        assert 'payment' in data
        
        payment = data['payment']
        assert 'payment_id' in payment
        assert payment['cryptocurrency'] == 'XNO'
        assert payment['status'] == 'pending'
        assert 'payment_address' in payment
        assert 'expires_at' in payment
    
    def test_create_payment_order_not_found(self, client):
        """Test creating payment for non-existent order"""
        response = client.post(
            '/api/payments/create',
            data=json.dumps({
                'order_id': 'INVALID-ORDER-ID',
                'cryptocurrency': 'XNO'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'not found' in data['error'].lower()
    
    def test_get_payment_by_order(self, client, sample_order_data):
        """Test getting payment by order ID"""
        # Create order
        order_response = client.post(
            '/api/orders',
            data=json.dumps(sample_order_data),
            content_type='application/json'
        )
        
        order_data = json.loads(order_response.data)
        order_id = order_data['order']['order_id']
        
        # Get payment info
        response = client.get(f'/api/payments/order/{order_id}')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'order' in data
        assert 'payments' in data
    
    def test_confirm_payment(self, client, sample_order_data):
        """Test confirming a payment"""
        # Create order and payment
        order_response = client.post(
            '/api/orders',
            data=json.dumps(sample_order_data),
            content_type='application/json'
        )
        
        order_data = json.loads(order_response.data)
        order_id = order_data['order']['order_id']
        
        payment_response = client.post(
            '/api/payments/create',
            data=json.dumps({
                'order_id': order_id,
                'cryptocurrency': 'XNO'
            }),
            content_type='application/json'
        )
        
        payment_data = json.loads(payment_response.data)
        payment_id = payment_data['payment']['payment_id']
        
        # Confirm payment
        confirm_response = client.post(
            '/api/payments/confirm',
            data=json.dumps({
                'payment_id': payment_id,
                'transaction_hash': '0x1234567890abcdef'
            }),
            content_type='application/json'
        )
        
        assert confirm_response.status_code == 200
        
        data = json.loads(confirm_response.data)
        assert data['success'] is True
        assert data['payment']['status'] == 'completed'
        assert data['order']['status'] == 'paid'
    
    def test_confirm_payment_not_found(self, client):
        """Test confirming non-existent payment"""
        response = client.post(
            '/api/payments/confirm',
            data=json.dumps({
                'payment_id': 'INVALID',
                'transaction_hash': '0x123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['success'] is False


class TestCFVDiscount:
    """Test CFV discount calculations across all coins"""
    
    def test_all_coins_have_discount_info(self, client):
        """Test that all coins return discount information"""
        coins_response = client.get('/api/cfv/coins')
        data = json.loads(coins_response.data)
        
        for coin in data['coins']:
            # Each coin should have discount info
            assert 'discount' in coin
            assert isinstance(coin['discount'], (int, float))
            assert 0 <= coin['discount'] <= 10  # Max 10% discount
    
    def test_undervalued_coins_have_discount(self, client):
        """Test that undervalued coins have non-zero discount"""
        coins_response = client.get('/api/cfv/coins')
        data = json.loads(coins_response.data)
        
        for coin in data['coins']:
            if coin.get('cfv') and coin['cfv'].get('valuationStatus') == 'undervalued':
                # Undervalued coins should have discount
                assert coin['discount'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
