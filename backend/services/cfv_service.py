"""
CFV (Crypto Fair Value) Service

Integrates with cfv-calculator and cfv-metrics-agent APIs to calculate
fair values and determine discounts for supported cryptocurrencies.
"""

import os
import time
import requests
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta


class CFVService:
    """Service for calculating Crypto Fair Value and discounts"""
    
    # 12 DGF (Digital Gold Foundation) supported cryptocurrencies
    SUPPORTED_CRYPTOS = {
        'XNO': {'name': 'Nano', 'category': 'Payment'},
        'NEAR': {'name': 'NEAR Protocol', 'category': 'Smart Contract Platform'},
        'ICP': {'name': 'Internet Computer', 'category': 'Smart Contract Platform'},
        'EGLD': {'name': 'MultiversX', 'category': 'Smart Contract Platform'},
        'DGB': {'name': 'DigiByte', 'category': 'Payment'},
        'DASH': {'name': 'Dash', 'category': 'Payment'},
        'XCH': {'name': 'Chia', 'category': 'Layer 1'},
        'XEC': {'name': 'eCash', 'category': 'Payment'},
        'XMR': {'name': 'Monero', 'category': 'Privacy'},
        'RVN': {'name': 'Ravencoin', 'category': 'Asset Transfer'},
        'DGD': {'name': 'Digital Gold', 'category': 'Digital Gold'},
        'BTC-LN': {'name': 'Bitcoin Lightning', 'category': 'Payment'}
    }
    
    # Discount tiers based on undervaluation percentage
    DISCOUNT_TIERS = [
        {'threshold': 50, 'discount': 10},  # ≥50% undervalued: 10% discount
        {'threshold': 30, 'discount': 7},   # 30-49% undervalued: 7% discount
        {'threshold': 15, 'discount': 5},   # 15-29% undervalued: 5% discount
        {'threshold': 0, 'discount': 2}     # <15% undervalued: 2% discount
    ]
    
    def __init__(self, 
                 calculator_url: str = None,
                 agent_url: str = None,
                 cache_ttl: int = None,
                 discount_enabled: bool = True,
                 max_discount: float = 10):
        """
        Initialize CFV Service
        
        Args:
            calculator_url: URL for cfv-calculator API
            agent_url: URL for cfv-metrics-agent API
            cache_ttl: Cache time-to-live in seconds (default: 300)
            discount_enabled: Whether discounts are enabled
            max_discount: Maximum discount percentage allowed
        """
        self.calculator_url = calculator_url or os.getenv('CFV_CALCULATOR_URL', 'http://localhost:3000')
        self.agent_url = agent_url or os.getenv('CFV_AGENT_URL', 'http://localhost:3001')
        self.cache_ttl = cache_ttl or int(os.getenv('CFV_CACHE_TTL', '300'))  # 5 minutes default
        self.discount_enabled = discount_enabled and os.getenv('CFV_DISCOUNT_ENABLED', 'true').lower() == 'true'
        self.max_discount = min(max_discount, float(os.getenv('CFV_MAX_DISCOUNT', '10')))
        
        # Cache for CFV calculations
        self._cache = {}
        
    def is_supported(self, symbol: str) -> bool:
        """
        Check if a cryptocurrency is supported
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'XNO', 'NEAR')
            
        Returns:
            True if supported, False otherwise
        """
        return symbol.upper() in self.SUPPORTED_CRYPTOS
    
    def get_supported_coins(self) -> list:
        """
        Get list of supported cryptocurrencies
        
        Returns:
            List of supported coin information
        """
        return [
            {
                'symbol': symbol,
                'name': info['name'],
                'category': info['category']
            }
            for symbol, info in self.SUPPORTED_CRYPTOS.items()
        ]
    
    def calculate_cfv(self, symbol: str, force_refresh: bool = False) -> Optional[Dict]:
        """
        Calculate CFV for a cryptocurrency
        
        Args:
            symbol: Cryptocurrency symbol
            force_refresh: Force refresh cache
            
        Returns:
            CFV calculation result or None if failed
        """
        symbol = symbol.upper()
        
        if not self.is_supported(symbol):
            raise ValueError(f"Unsupported cryptocurrency: {symbol}")
        
        # Check cache
        if not force_refresh and symbol in self._cache:
            cached_data, cached_time = self._cache[symbol]
            if time.time() - cached_time < self.cache_ttl:
                return cached_data
        
        try:
            # Try cfv-calculator API first
            response = requests.get(
                f"{self.calculator_url}/api/cfv/{symbol}",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                # Cache the result
                self._cache[symbol] = (data, time.time())
                return data
            
            # Fallback to cfv-metrics-agent API
            response = requests.get(
                f"{self.agent_url}/api/metrics/{symbol}",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                # Cache the result
                self._cache[symbol] = (data, time.time())
                return data
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching CFV for {symbol}: {e}")
            
            # Return mock data for development/testing
            return self._get_mock_cfv_data(symbol)
        
        return None
    
    def _get_mock_cfv_data(self, symbol: str) -> Dict:
        """
        Generate mock CFV data for development/testing
        
        Args:
            symbol: Cryptocurrency symbol
            
        Returns:
            Mock CFV data
        """
        # Mock data with varying undervaluation levels for testing
        mock_undervaluation = {
            'XNO': 65,  # Highly undervalued
            'NEAR': 45,  # Moderately undervalued
            'ICP': 25,  # Slightly undervalued
            'EGLD': 10,  # Minimally undervalued
            'DGB': 55,  # Highly undervalued
            'DASH': 35,  # Moderately undervalued
            'XCH': 20,  # Slightly undervalued
            'XEC': 60,  # Highly undervalued
            'XMR': 40,  # Moderately undervalued
            'RVN': 30,  # Moderately undervalued
            'DGD': 50,  # Highly undervalued
            'BTC-LN': 15  # Slightly undervalued
        }
        
        undervaluation = mock_undervaluation.get(symbol, 25)
        current_price = 100.0  # Mock current price
        fair_value = current_price * (1 + undervaluation / 100)
        
        return {
            'symbol': symbol,
            'currentPrice': current_price,
            'fairValue': fair_value,
            'valuationPercent': undervaluation,
            'valuationStatus': self._get_valuation_status(undervaluation),
            'calculatedAt': datetime.utcnow().isoformat(),
            'source': 'mock'
        }
    
    def _get_valuation_status(self, valuation_percent: float) -> str:
        """
        Determine valuation status based on percentage
        
        Args:
            valuation_percent: Valuation percentage (positive = undervalued)
            
        Returns:
            Valuation status string
        """
        if valuation_percent >= 15:
            return 'undervalued'
        elif valuation_percent <= -15:
            return 'overvalued'
        else:
            return 'fair'
    
    def calculate_discount(self, symbol: str) -> Tuple[float, Dict]:
        """
        Calculate discount based on CFV undervaluation
        
        Args:
            symbol: Cryptocurrency symbol
            
        Returns:
            Tuple of (discount_percentage, cfv_metrics)
        """
        if not self.discount_enabled:
            return 0.0, {}
        
        cfv_data = self.calculate_cfv(symbol)
        
        if not cfv_data:
            return 0.0, {}
        
        valuation_percent = cfv_data.get('valuationPercent', 0)
        
        # Only apply discounts for undervalued coins
        if valuation_percent <= 0:
            return 0.0, {
                'valuationStatus': cfv_data.get('valuationStatus', 'fair'),
                'valuationPercent': valuation_percent,
                'calculatedAt': cfv_data.get('calculatedAt'),
                'fairValue': cfv_data.get('fairValue')
            }
        
        # Determine discount tier
        discount = 0.0
        for tier in self.DISCOUNT_TIERS:
            if valuation_percent >= tier['threshold']:
                discount = tier['discount']
                break
        
        # Apply max discount cap
        discount = min(discount, self.max_discount)
        
        cfv_metrics = {
            'valuationStatus': cfv_data.get('valuationStatus', 'undervalued'),
            'valuationPercent': valuation_percent,
            'calculatedAt': cfv_data.get('calculatedAt'),
            'fairValue': cfv_data.get('fairValue'),
            'currentPrice': cfv_data.get('currentPrice')
        }
        
        return discount, cfv_metrics
    
    def get_payment_info(self, symbol: str, amount_usd: float) -> Dict:
        """
        Get payment information with CFV discount applied
        
        Args:
            symbol: Cryptocurrency symbol
            amount_usd: Amount in USD
            
        Returns:
            Payment information including discount
        """
        symbol = symbol.upper()
        
        if not self.is_supported(symbol):
            raise ValueError(f"Unsupported cryptocurrency: {symbol}")
        
        # Calculate discount
        discount_percent, cfv_metrics = self.calculate_discount(symbol)
        
        # Apply discount
        original_price = amount_usd
        discounted_price = amount_usd * (1 - discount_percent / 100)
        discount_amount = original_price - discounted_price
        
        # Get current price for conversion
        cfv_data = self.calculate_cfv(symbol)
        current_price = cfv_data.get('currentPrice', 100.0) if cfv_data else 100.0
        
        # Calculate crypto amount
        amount_crypto = discounted_price / current_price
        
        return {
            'symbol': symbol,
            'name': self.SUPPORTED_CRYPTOS[symbol]['name'],
            'category': self.SUPPORTED_CRYPTOS[symbol]['category'],
            'originalPriceUSD': original_price,
            'discountPercent': discount_percent,
            'discountAmount': discount_amount,
            'finalPriceUSD': discounted_price,
            'amountCrypto': amount_crypto,
            'currentPrice': current_price,
            'cfvMetrics': cfv_metrics
        }
    
    def clear_cache(self, symbol: str = None):
        """
        Clear CFV cache
        
        Args:
            symbol: Specific symbol to clear, or None to clear all
        """
        if symbol:
            symbol = symbol.upper()
            if symbol in self._cache:
                del self._cache[symbol]
        else:
            self._cache.clear()
