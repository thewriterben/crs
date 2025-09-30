"""
Pytest configuration and shared fixtures
"""
import os
import sys
import pytest
from flask import Flask

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    # Import here to avoid circular imports
    from flask import Flask
    from flask_jwt_extended import JWTManager
    from datetime import timedelta
    
    # Create Flask app
    test_app = Flask(__name__)
    
    # Test configuration
    test_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-secret-key',
        'JWT_SECRET_KEY': 'test-jwt-secret-key',
        'JWT_ACCESS_TOKEN_EXPIRES': timedelta(hours=1),
        'JWT_REFRESH_TOKEN_EXPIRES': timedelta(days=30),
        'WTF_CSRF_ENABLED': False,
    })
    
    # Initialize extensions
    from src.models import db, bcrypt
    from src.auth_routes import auth_bp
    from src.health_routes import health_bp
    
    db.init_app(test_app)
    bcrypt.init_app(test_app)
    jwt = JWTManager(test_app)
    
    # Register blueprints
    test_app.register_blueprint(auth_bp)
    test_app.register_blueprint(health_bp)
    
    # Create database tables
    with test_app.app_context():
        db.create_all()
    
    yield test_app
    
    # Cleanup
    with test_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers(client):
    """Create authorization headers for authenticated requests."""
    # Register and login a test user
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPassword123!'
    })
    
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'TestPassword123!'
    })
    
    data = response.get_json()
    access_token = data.get('access_token')
    
    return {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPassword123!'
    }


@pytest.fixture
def sample_invalid_user_data():
    """Sample invalid user data for testing."""
    return {
        'username': '',
        'email': 'invalid-email',
        'password': '123'  # Too short
    }
