"""
Unit tests for authentication module
"""
import pytest
from src.models import User


@pytest.mark.unit
@pytest.mark.auth
class TestUser:
    """Test User model"""
    
    def test_user_creation(self, app, db_session):
        """Test user creation"""
        user = User(username='newuser', email='new@example.com')
        user.set_password('password123')
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.username == 'newuser'
        assert user.email == 'new@example.com'
        assert user.password_hash is not None
        assert user.is_active is True
        assert user.mfa_enabled is False
    
    def test_password_hashing(self, app, db_session):
        """Test password hashing and verification"""
        user = User(username='user1', email='user1@example.com')
        user.set_password('mypassword')
        
        assert user.check_password('mypassword') is True
        assert user.check_password('wrongpassword') is False
    
    def test_mfa_enable(self, app, db_session):
        """Test MFA enabling"""
        user = User(username='user2', email='user2@example.com')
        user.set_password('password')
        
        secret = user.enable_mfa()
        
        assert user.mfa_enabled is True
        assert user.mfa_secret is not None
        assert secret == user.mfa_secret
        assert len(secret) == 32
    
    def test_mfa_disable(self, app, db_session):
        """Test MFA disabling"""
        user = User(username='user3', email='user3@example.com')
        user.set_password('password')
        user.enable_mfa()
        
        user.disable_mfa()
        
        assert user.mfa_enabled is False
        assert user.mfa_secret is None
    
    def test_user_to_dict(self, app, test_user):
        """Test user to dictionary conversion"""
        user_dict = test_user.to_dict()
        
        assert 'id' in user_dict
        assert 'username' in user_dict
        assert 'email' in user_dict
        assert 'password_hash' not in user_dict
        assert user_dict['username'] == 'testuser'
