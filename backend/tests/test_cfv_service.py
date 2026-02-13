"""
Unit tests for CFV Service

Tests the Crypto Fair Value service functionality including:
- Cryptocurrency validation
- CFV calculation
- Discount calculation
- Payment info generation
- Caching mechanism
"""

import pytest
from services.cfv_service import CFVService


class TestCFVService:
    """Test suite for CFV Service"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = CFVService(
            calculator_url='http://localhost:3000',
            agent_url='http://localhost:3001',
            cache_ttl=300,
            discount_enabled=True,
            max_discount=10
        )
    
    def test_supported_cryptocurrencies(self):
        """Test cryptocurrency validation"""
        # Test supported coins
        assert self.service.is_supported('XNO')
        assert self.service.is_supported('NEAR')
        assert self.service.is_supported('ICP')
        assert self.service.is_supported('EGLD')
        assert self.service.is_supported('DGB')
        assert self.service.is_supported('DASH')
        assert self.service.is_supported('XCH')
        assert self.service.is_supported('XEC')
        assert self.service.is_supported('XMR')
        assert self.service.is_supported('RVN')
        assert self.service.is_supported('DGD')
        assert self.service.is_supported('BTC-LN')
        
        # Test case insensitive
        assert self.service.is_supported('xno')
        assert self.service.is_supported('Near')
        
        # Test unsupported coins
        assert not self.service.is_supported('BTC')
        assert not self.service.is_supported('ETH')
        assert not self.service.is_supported('INVALID')
    
    def test_get_supported_coins(self):
        """Test getting list of supported coins"""
        coins = self.service.get_supported_coins()
        
        # Should return 12 DGF coins
        assert len(coins) == 12
        
        # Check structure
        for coin in coins:
            assert 'symbol' in coin
            assert 'name' in coin
            assert 'category' in coin
        
        # Verify specific coins
        symbols = [coin['symbol'] for coin in coins]
        assert 'XNO' in symbols
        assert 'NEAR' in symbols
        assert 'BTC-LN' in symbols
    
    def test_calculate_cfv(self):
        """Test CFV calculation"""
        # Calculate CFV for XNO
        cfv_data = self.service.calculate_cfv('XNO')
        
        assert cfv_data is not None
        assert 'symbol' in cfv_data
        assert 'currentPrice' in cfv_data
        assert 'fairValue' in cfv_data
        assert 'valuationPercent' in cfv_data
        assert 'valuationStatus' in cfv_data
        assert 'calculatedAt' in cfv_data
        
        # Verify data types
        assert isinstance(cfv_data['currentPrice'], (int, float))
        assert isinstance(cfv_data['fairValue'], (int, float))
        assert isinstance(cfv_data['valuationPercent'], (int, float))
        assert cfv_data['valuationStatus'] in ['undervalued', 'fair', 'overvalued']
    
    def test_calculate_cfv_invalid_coin(self):
        """Test CFV calculation with invalid cryptocurrency"""
        with pytest.raises(ValueError, match="Unsupported cryptocurrency"):
            self.service.calculate_cfv('INVALID')
    
    def test_discount_calculation_high_undervaluation(self):
        """Test discount for highly undervalued coin (>=50%)"""
        # XNO is mocked at 65% undervaluation
        discount, metrics = self.service.calculate_discount('XNO')
        
        # Should get 10% discount
        assert discount == 10
        assert metrics['valuationStatus'] == 'undervalued'
        assert metrics['valuationPercent'] >= 50
    
    def test_discount_calculation_moderate_undervaluation(self):
        """Test discount for moderately undervalued coin (30-49%)"""
        # NEAR is mocked at 45% undervaluation
        discount, metrics = self.service.calculate_discount('NEAR')
        
        # Should get 7% discount
        assert discount == 7
        assert metrics['valuationStatus'] == 'undervalued'
        assert 30 <= metrics['valuationPercent'] < 50
    
    def test_discount_calculation_slight_undervaluation(self):
        """Test discount for slightly undervalued coin (15-29%)"""
        # ICP is mocked at 25% undervaluation
        discount, metrics = self.service.calculate_discount('ICP')
        
        # Should get 5% discount
        assert discount == 5
        assert metrics['valuationStatus'] == 'undervalued'
        assert 15 <= metrics['valuationPercent'] < 30
    
    def test_discount_calculation_minimal_undervaluation(self):
        """Test discount for minimally undervalued coin (<15%)"""
        # EGLD is mocked at 10% undervaluation
        discount, metrics = self.service.calculate_discount('EGLD')
        
        # Should get 2% discount
        assert discount == 2
        assert 0 < metrics['valuationPercent'] < 15
    
    def test_discount_disabled(self):
        """Test discount calculation when discounts are disabled"""
        service = CFVService(discount_enabled=False)
        discount, metrics = service.calculate_discount('XNO')
        
        assert discount == 0.0
    
    def test_max_discount_cap(self):
        """Test maximum discount cap"""
        service = CFVService(max_discount=5)
        discount, _ = service.calculate_discount('XNO')
        
        # Even though XNO would get 10%, max is capped at 5%
        assert discount <= 5
    
    def test_payment_info(self):
        """Test payment info generation"""
        payment_info = self.service.get_payment_info('XNO', 100.0)
        
        # Verify structure
        assert payment_info['symbol'] == 'XNO'
        assert payment_info['name'] == 'Nano'
        assert payment_info['category'] == 'Payment'
        assert payment_info['originalPriceUSD'] == 100.0
        assert 'discountPercent' in payment_info
        assert 'discountAmount' in payment_info
        assert 'finalPriceUSD' in payment_info
        assert 'amountCrypto' in payment_info
        assert 'currentPrice' in payment_info
        assert 'cfvMetrics' in payment_info
        
        # Verify calculations
        discount_percent = payment_info['discountPercent']
        expected_final_price = 100.0 * (1 - discount_percent / 100)
        assert abs(payment_info['finalPriceUSD'] - expected_final_price) < 0.01
        
        expected_discount_amount = 100.0 - expected_final_price
        assert abs(payment_info['discountAmount'] - expected_discount_amount) < 0.01
    
    def test_payment_info_invalid_coin(self):
        """Test payment info with invalid cryptocurrency"""
        with pytest.raises(ValueError, match="Unsupported cryptocurrency"):
            self.service.get_payment_info('INVALID', 100.0)
    
    def test_cache_functionality(self):
        """Test CFV caching mechanism"""
        # First call - should cache
        cfv_data_1 = self.service.calculate_cfv('XNO')
        
        # Second call - should return from cache
        cfv_data_2 = self.service.calculate_cfv('XNO')
        
        # Should be identical
        assert cfv_data_1 == cfv_data_2
        
        # Cache should have entry
        assert 'XNO' in self.service._cache
    
    def test_cache_force_refresh(self):
        """Test cache force refresh"""
        # First call
        cfv_data_1 = self.service.calculate_cfv('XNO')
        
        # Force refresh
        cfv_data_2 = self.service.calculate_cfv('XNO', force_refresh=True)
        
        # Data should still be valid
        assert cfv_data_2 is not None
        assert 'symbol' in cfv_data_2
    
    def test_clear_cache(self):
        """Test cache clearing"""
        # Add some data to cache
        self.service.calculate_cfv('XNO')
        self.service.calculate_cfv('NEAR')
        
        assert len(self.service._cache) == 2
        
        # Clear specific coin
        self.service.clear_cache('XNO')
        assert 'XNO' not in self.service._cache
        assert 'NEAR' in self.service._cache
        
        # Clear all
        self.service.clear_cache()
        assert len(self.service._cache) == 0
    
    def test_valuation_status(self):
        """Test valuation status determination"""
        # Test undervalued
        assert self.service._get_valuation_status(20) == 'undervalued'
        assert self.service._get_valuation_status(50) == 'undervalued'
        
        # Test fair
        assert self.service._get_valuation_status(10) == 'fair'
        assert self.service._get_valuation_status(0) == 'fair'
        assert self.service._get_valuation_status(-10) == 'fair'
        
        # Test overvalued
        assert self.service._get_valuation_status(-20) == 'overvalued'
        assert self.service._get_valuation_status(-50) == 'overvalued'
    
    def test_all_supported_coins_have_cfv(self):
        """Test that all supported coins can calculate CFV"""
        for symbol in self.service.SUPPORTED_CRYPTOS.keys():
            cfv_data = self.service.calculate_cfv(symbol)
            assert cfv_data is not None
            assert cfv_data['symbol'] == symbol
    
    def test_discount_tiers_coverage(self):
        """Test all discount tiers are properly defined"""
        # Verify discount tiers are sorted by threshold (descending)
        tiers = self.service.DISCOUNT_TIERS
        
        assert len(tiers) == 4
        assert tiers[0]['threshold'] == 50
        assert tiers[0]['discount'] == 10
        assert tiers[1]['threshold'] == 30
        assert tiers[1]['discount'] == 7
        assert tiers[2]['threshold'] == 15
        assert tiers[2]['discount'] == 5
        assert tiers[3]['threshold'] == 0
        assert tiers[3]['discount'] == 2


class TestCFVIntegration:
    """Integration tests for CFV service"""
    
    def test_complete_payment_flow(self):
        """Test complete payment flow with CFV"""
        service = CFVService()
        
        # 1. Get supported coins
        coins = service.get_supported_coins()
        assert len(coins) > 0
        
        # 2. Select a coin (XNO)
        selected_coin = 'XNO'
        assert service.is_supported(selected_coin)
        
        # 3. Calculate CFV
        cfv_data = service.calculate_cfv(selected_coin)
        assert cfv_data is not None
        
        # 4. Calculate discount
        discount, metrics = service.calculate_discount(selected_coin)
        assert discount >= 0
        
        # 5. Get payment info
        payment_info = service.get_payment_info(selected_coin, 100.0)
        assert payment_info['discountPercent'] == discount
        assert payment_info['symbol'] == selected_coin
        
        # 6. Verify discount applied correctly
        if discount > 0:
            assert payment_info['finalPriceUSD'] < payment_info['originalPriceUSD']
            expected_savings = 100.0 * (discount / 100)
            assert abs(payment_info['discountAmount'] - expected_savings) < 0.01


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
