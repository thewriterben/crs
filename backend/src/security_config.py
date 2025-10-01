"""
Security configuration and middleware for Cryptons.com Backend
Implements security headers, rate limiting, and CORS policies
"""
import os
from flask import Flask
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_compress import Compress
from flask_cors import CORS

# Initialize extensions
cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per minute", "2000 per hour"],
    storage_uri=os.environ.get('RATELIMIT_STORAGE_URL', 'memory://'),
    storage_options={}
)
compress = Compress()

def configure_security(app: Flask) -> None:
    """
    Configure security settings for the Flask application
    
    Args:
        app: Flask application instance
    """
    # CORS Configuration
    allowed_origins = os.environ.get('CORS_ORIGINS', '*').split(',')
    CORS(app, 
         origins=allowed_origins,
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Security Headers (only in production with HTTPS)
    if app.config.get('FLASK_ENV') == 'production':
        csp = {
            'default-src': ['\'self\''],
            'script-src': ['\'self\'', '\'unsafe-inline\''],
            'style-src': ['\'self\'', '\'unsafe-inline\''],
            'img-src': ['\'self\'', 'data:', 'https:'],
            'font-src': ['\'self\'', 'data:'],
            'connect-src': ['\'self\''],
        }
        
        Talisman(app,
                 force_https=True,
                 strict_transport_security=True,
                 content_security_policy=csp,
                 session_cookie_secure=True,
                 session_cookie_http_only=True)
    
    # Rate Limiting
    limiter.init_app(app)
    
    # Response Compression
    compress.init_app(app)
    
    # Caching Configuration
    cache_config = {
        'CACHE_TYPE': os.environ.get('CACHE_TYPE', 'SimpleCache'),
        'CACHE_DEFAULT_TIMEOUT': 300,
    }
    
    if cache_config['CACHE_TYPE'] == 'RedisCache':
        cache_config['CACHE_REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    cache.init_app(app, config=cache_config)
    
    # Additional security configurations
    app.config.update(
        SESSION_COOKIE_SECURE=app.config.get('FLASK_ENV') == 'production',
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=int(os.environ.get('PERMANENT_SESSION_LIFETIME', 3600)),
        MAX_CONTENT_LENGTH=int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    )

def get_rate_limiter():
    """Get the rate limiter instance"""
    return limiter

def get_cache():
    """Get the cache instance"""
    return cache
