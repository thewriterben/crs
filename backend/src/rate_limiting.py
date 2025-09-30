"""
Advanced rate limiting configuration and utilities
Provides multi-tier rate limiting with Redis backend
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request, jsonify
import redis
import os
from typing import Optional, Callable


class RateLimitConfig:
    """Rate limiting configuration"""
    
    # Redis URL for rate limiting
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Default rate limits
    DEFAULT_LIMITS = ["200 per day", "50 per hour"]
    
    # Endpoint-specific limits
    LIMITS = {
        # Authentication endpoints
        'auth_register': ["5 per hour"],
        'auth_login': ["10 per minute", "50 per hour"],
        'auth_refresh': ["20 per minute"],
        
        # Trading endpoints
        'trading_order': ["100 per minute", "1000 per hour"],
        'trading_cancel': ["200 per minute"],
        'trading_query': ["500 per minute"],
        
        # Market data endpoints
        'market_data': ["1000 per minute"],
        'market_history': ["200 per minute"],
        
        # AI/ML endpoints
        'ai_prediction': ["50 per hour"],
        'ai_analysis': ["100 per hour"],
        
        # User endpoints
        'user_profile': ["100 per minute"],
        'user_update': ["20 per hour"],
    }
    
    # Exempted IP addresses (for internal services)
    EXEMPT_IPS = os.environ.get('RATE_LIMIT_EXEMPT_IPS', '').split(',')
    
    # Headers to include in rate limit response
    HEADERS_ENABLED = True
    HEADER_LIMIT = "X-RateLimit-Limit"
    HEADER_REMAINING = "X-RateLimit-Remaining"
    HEADER_RESET = "X-RateLimit-Reset"


def get_rate_limit_key():
    """
    Custom key function for rate limiting
    Uses IP address and user ID (if authenticated)
    """
    # Try to get user ID from JWT token
    user_id = None
    try:
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()
    except:
        pass
    
    # Combine IP and user ID for the key
    ip = get_remote_address()
    if user_id:
        return f"{ip}:{user_id}"
    return ip


def is_rate_limit_exempt():
    """Check if the current request should be exempt from rate limiting"""
    ip = get_remote_address()
    return ip in RateLimitConfig.EXEMPT_IPS


def init_rate_limiter(app):
    """
    Initialize rate limiter with Flask app
    
    Args:
        app: Flask application instance
    
    Returns:
        Limiter instance
    """
    limiter = Limiter(
        app=app,
        key_func=get_rate_limit_key,
        storage_uri=RateLimitConfig.REDIS_URL,
        default_limits=RateLimitConfig.DEFAULT_LIMITS,
        headers_enabled=RateLimitConfig.HEADERS_ENABLED,
        strategy="fixed-window",  # or "moving-window" for more accuracy
    )
    
    # Custom error handler for rate limit exceeded
    @app.errorhandler(429)
    def rate_limit_handler(e):
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': str(e.description),
            'retry_after': e.description
        }), 429
    
    return limiter


# Adaptive rate limiting based on user behavior
class AdaptiveRateLimiter:
    """
    Adaptive rate limiter that adjusts limits based on user behavior
    """
    
    def __init__(self, redis_url: str = None):
        self.redis_url = redis_url or RateLimitConfig.REDIS_URL
        self.redis_client = redis.from_url(self.redis_url)
    
    def get_user_score(self, user_id: str) -> float:
        """
        Get user trust score (0-1)
        Higher score = more trusted user = higher rate limits
        """
        score_key = f"user_score:{user_id}"
        score = self.redis_client.get(score_key)
        
        if score is None:
            return 0.5  # Default score for new users
        
        return float(score)
    
    def adjust_score(self, user_id: str, delta: float):
        """Adjust user trust score"""
        current_score = self.get_user_score(user_id)
        new_score = max(0.0, min(1.0, current_score + delta))
        
        score_key = f"user_score:{user_id}"
        self.redis_client.set(score_key, new_score, ex=30*24*3600)  # 30 days
    
    def get_adaptive_limit(self, base_limit: int, user_id: str) -> int:
        """
        Calculate adaptive limit based on user score
        
        Args:
            base_limit: Base rate limit
            user_id: User identifier
        
        Returns:
            Adjusted rate limit
        """
        score = self.get_user_score(user_id)
        # Scale limit from 50% to 200% based on score
        multiplier = 0.5 + (score * 1.5)
        return int(base_limit * multiplier)


# DDoS protection helper
class DDoSProtection:
    """Simple DDoS protection using Redis"""
    
    def __init__(self, redis_url: str = None):
        self.redis_url = redis_url or RateLimitConfig.REDIS_URL
        self.redis_client = redis.from_url(self.redis_url)
    
    def is_suspicious(self, ip: str, threshold: int = 1000, window: int = 60) -> bool:
        """
        Check if IP is making suspiciously high number of requests
        
        Args:
            ip: IP address
            threshold: Request threshold
            window: Time window in seconds
        
        Returns:
            True if suspicious activity detected
        """
        key = f"ddos:{ip}"
        count = self.redis_client.get(key)
        
        if count is None:
            self.redis_client.setex(key, window, 1)
            return False
        
        count = int(count)
        if count >= threshold:
            return True
        
        self.redis_client.incr(key)
        return False
    
    def block_ip(self, ip: str, duration: int = 3600):
        """
        Temporarily block an IP address
        
        Args:
            ip: IP address to block
            duration: Block duration in seconds
        """
        key = f"blocked:{ip}"
        self.redis_client.setex(key, duration, 1)
    
    def is_blocked(self, ip: str) -> bool:
        """Check if IP is blocked"""
        key = f"blocked:{ip}"
        return bool(self.redis_client.get(key))


# Rate limit decorator helpers
def apply_rate_limit(limit_key: str):
    """
    Apply rate limit from configuration
    
    Usage:
        @app.route('/api/endpoint')
        @apply_rate_limit('trading_order')
        def endpoint():
            ...
    """
    def decorator(f):
        limit = RateLimitConfig.LIMITS.get(limit_key, RateLimitConfig.DEFAULT_LIMITS)
        # Note: This requires the limiter to be initialized
        # Use with Flask-Limiter's @limiter.limit() decorator
        return f
    return decorator
