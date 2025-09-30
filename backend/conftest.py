"""
Pytest configuration and fixtures for CRS backend tests
"""
import pytest
import sys
import os
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import create_app
from src.models import db, User


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret-key',
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False,
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    """Create database session for testing"""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.rollback()
        db.drop_all()


@pytest.fixture
def test_user(app, db_session):
    """Create a test user"""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.set_password('testpassword123')
        db_session.add(user)
        db_session.commit()
        return user


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers with JWT token"""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword123'
    })
    assert response.status_code == 200
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def sample_market_data():
    """Sample market data for testing"""
    return {
        'BTC': {
            'price': 50000.0,
            'volume': 1000000.0,
            'change_24h': 0.05
        },
        'ETH': {
            'price': 3000.0,
            'volume': 500000.0,
            'change_24h': -0.02
        }
    }


@pytest.fixture
def sample_portfolio():
    """Sample portfolio data for testing"""
    return {
        'assets': [
            {'symbol': 'BTC', 'quantity': 0.5, 'avg_price': 48000.0},
            {'symbol': 'ETH', 'quantity': 2.0, 'avg_price': 2900.0}
        ],
        'total_value': 30000.0,
        'cash': 5000.0
    }
