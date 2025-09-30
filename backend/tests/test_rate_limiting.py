"""
Tests for rate limiting
"""
import pytest
from src.rate_limiting import (
    RateLimitConfig,
    AdaptiveRateLimiter,
    DDoSProtection
)


@pytest.mark.unit
@pytest.mark.security
class TestRateLimitConfig:
    """Test rate limit configuration"""
    
    def test_config_has_limits(self):
        """Test that rate limit config has limits defined"""
        assert RateLimitConfig.DEFAULT_LIMITS is not None
        assert len(RateLimitConfig.DEFAULT_LIMITS) > 0
        assert RateLimitConfig.LIMITS is not None
        assert len(RateLimitConfig.LIMITS) > 0
    
    def test_endpoint_limits(self):
        """Test endpoint-specific limits"""
        # Check auth limits
        assert 'auth_login' in RateLimitConfig.LIMITS
        assert 'auth_register' in RateLimitConfig.LIMITS
        
        # Check trading limits
        assert 'trading_order' in RateLimitConfig.LIMITS
        assert 'trading_cancel' in RateLimitConfig.LIMITS
        
        # Check AI limits
        assert 'ai_prediction' in RateLimitConfig.LIMITS


@pytest.mark.integration
@pytest.mark.security
class TestAdaptiveRateLimiter:
    """Test adaptive rate limiter"""
    
    @pytest.fixture
    def limiter(self):
        """Create adaptive rate limiter instance"""
        return AdaptiveRateLimiter()
    
    def test_default_user_score(self, limiter):
        """Test default user score for new users"""
        score = limiter.get_user_score('new_user_123')
        assert 0.0 <= score <= 1.0
        assert score == 0.5  # Default score
    
    def test_adjust_score(self, limiter):
        """Test score adjustment"""
        user_id = 'test_user_score'
        
        # Increase score
        limiter.adjust_score(user_id, 0.2)
        score = limiter.get_user_score(user_id)
        assert score == 0.7
        
        # Decrease score
        limiter.adjust_score(user_id, -0.3)
        score = limiter.get_user_score(user_id)
        assert score == 0.4
    
    def test_score_bounds(self, limiter):
        """Test score stays within bounds"""
        user_id = 'test_user_bounds'
        
        # Try to exceed 1.0
        limiter.adjust_score(user_id, 1.0)
        score = limiter.get_user_score(user_id)
        assert score <= 1.0
        
        # Try to go below 0.0
        limiter.adjust_score(user_id, -2.0)
        score = limiter.get_user_score(user_id)
        assert score >= 0.0
    
    def test_adaptive_limit(self, limiter):
        """Test adaptive limit calculation"""
        user_id = 'test_user_adaptive'
        base_limit = 100
        
        # Low score = lower limit
        limiter.adjust_score(user_id, -0.5)  # Score becomes 0
        limit = limiter.get_adaptive_limit(base_limit, user_id)
        assert limit < base_limit
        
        # High score = higher limit
        limiter.adjust_score(user_id, 1.0)  # Score becomes 1.0
        limit = limiter.get_adaptive_limit(base_limit, user_id)
        assert limit > base_limit


@pytest.mark.integration
@pytest.mark.security
class TestDDoSProtection:
    """Test DDoS protection"""
    
    @pytest.fixture
    def protection(self):
        """Create DDoS protection instance"""
        return DDoSProtection()
    
    def test_is_suspicious_first_request(self, protection):
        """Test first request is not suspicious"""
        is_suspicious = protection.is_suspicious('192.168.1.1', threshold=10, window=60)
        assert is_suspicious is False
    
    def test_is_suspicious_threshold(self, protection):
        """Test suspicious activity detection"""
        ip = '192.168.1.100'
        threshold = 5
        
        # Make requests below threshold
        for _ in range(threshold - 1):
            is_suspicious = protection.is_suspicious(ip, threshold=threshold, window=60)
            assert is_suspicious is False
        
        # Next request should trigger threshold
        is_suspicious = protection.is_suspicious(ip, threshold=threshold, window=60)
        assert is_suspicious is True
    
    def test_block_and_check(self, protection):
        """Test IP blocking"""
        ip = '192.168.1.200'
        
        # Initially not blocked
        assert protection.is_blocked(ip) is False
        
        # Block IP
        protection.block_ip(ip, duration=10)
        
        # Should be blocked now
        assert protection.is_blocked(ip) is True
