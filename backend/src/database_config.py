"""
Database configuration for PostgreSQL and migration utilities
"""
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Database configuration
class DatabaseConfig:
    """Database configuration class"""
    
    # PostgreSQL configuration (production)
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'cryptons_user')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'change_this_password')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'cryptons_db')
    
    # Build PostgreSQL URL
    POSTGRESQL_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    # SQLite configuration (development/testing)
    SQLITE_URL = os.environ.get('DATABASE_URL', 'sqlite:///marketplace.db')
    
    # Use PostgreSQL in production, SQLite otherwise
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 
                                             POSTGRESQL_URL if os.environ.get('FLASK_ENV') == 'production' 
                                             else SQLITE_URL)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get('SQL_ECHO', 'false').lower() == 'true'
    
    # Connection pool settings for PostgreSQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.environ.get('DB_POOL_SIZE', 10)),
        'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', 3600)),
        'pool_pre_ping': True,
        'max_overflow': int(os.environ.get('DB_MAX_OVERFLOW', 20)),
    }


class RedisConfig:
    """Redis configuration for caching and sessions"""
    
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Cache configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Session configuration
    SESSION_TYPE = 'redis'
    SESSION_REDIS = REDIS_URL
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = REDIS_URL


def init_database(app):
    """
    Initialize database with app
    
    Args:
        app: Flask application instance
    
    Returns:
        tuple: (db, migrate) instances
    """
    from src.models import db
    
    # Apply database configuration
    app.config.update(
        SQLALCHEMY_DATABASE_URI=DatabaseConfig.SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=DatabaseConfig.SQLALCHEMY_TRACK_MODIFICATIONS,
        SQLALCHEMY_ECHO=DatabaseConfig.SQLALCHEMY_ECHO,
        SQLALCHEMY_ENGINE_OPTIONS=DatabaseConfig.SQLALCHEMY_ENGINE_OPTIONS
    )
    
    # Initialize database
    db.init_app(app)
    
    # Initialize migration support
    migrate = Migrate(app, db)
    
    return db, migrate


def init_redis(app):
    """
    Initialize Redis for caching and sessions
    
    Args:
        app: Flask application instance
    """
    from flask_caching import Cache
    from flask_session import Session
    
    # Apply Redis configuration
    app.config.update(
        CACHE_TYPE=RedisConfig.CACHE_TYPE,
        CACHE_REDIS_URL=RedisConfig.CACHE_REDIS_URL,
        CACHE_DEFAULT_TIMEOUT=RedisConfig.CACHE_DEFAULT_TIMEOUT,
        SESSION_TYPE=RedisConfig.SESSION_TYPE,
        SESSION_REDIS=RedisConfig.SESSION_REDIS,
        SESSION_PERMANENT=RedisConfig.SESSION_PERMANENT,
        SESSION_USE_SIGNER=RedisConfig.SESSION_USE_SIGNER,
    )
    
    # Initialize cache
    cache = Cache(app)
    
    # Initialize session
    Session(app)
    
    return cache
