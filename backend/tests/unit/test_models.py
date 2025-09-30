"""
Unit tests for database models
"""
import pytest
from datetime import datetime, timedelta
from src.models import db, User, RefreshToken


@pytest.mark.unit
class TestUserModel:
    """Test cases for User model"""
    
    def test_create_user(self, app):
        """Test creating a new user"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
            assert user.is_active is True
            assert user.mfa_enabled is False
    
    def test_set_password(self, app):
        """Test password hashing"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('mypassword')
            
            assert user.password_hash is not None
            assert user.password_hash != 'mypassword'
            assert len(user.password_hash) > 0
    
    def test_check_password(self, app):
        """Test password verification"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('correctpassword')
            
            assert user.check_password('correctpassword') is True
            assert user.check_password('wrongpassword') is False
    
    def test_enable_mfa(self, app):
        """Test enabling MFA"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            secret = user.enable_mfa()
            
            assert user.mfa_enabled is True
            assert user.mfa_secret is not None
            assert secret == user.mfa_secret
            assert len(secret) == 32  # 16 bytes in hex = 32 chars
    
    def test_disable_mfa(self, app):
        """Test disabling MFA"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.enable_mfa()
            user.disable_mfa()
            
            assert user.mfa_enabled is False
            assert user.mfa_secret is None
    
    def test_to_dict(self, app):
        """Test converting user to dictionary"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            
            user_dict = user.to_dict()
            
            assert user_dict['username'] == 'testuser'
            assert user_dict['email'] == 'test@example.com'
            assert user_dict['is_active'] is True
            assert user_dict['mfa_enabled'] is False
            assert 'password_hash' not in user_dict
    
    def test_unique_username(self, app):
        """Test unique username constraint"""
        with app.app_context():
            user1 = User(username='testuser', email='test1@example.com')
            user1.set_password('password')
            db.session.add(user1)
            db.session.commit()
            
            user2 = User(username='testuser', email='test2@example.com')
            user2.set_password('password')
            db.session.add(user2)
            
            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit()


@pytest.mark.unit
class TestRefreshTokenModel:
    """Test cases for RefreshToken model"""
    
    def test_create_refresh_token(self, app):
        """Test creating a refresh token"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            
            token = RefreshToken(
                user_id=user.id,
                token='test-token-123',
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
            db.session.add(token)
            db.session.commit()
            
            assert token.id is not None
            assert token.user_id == user.id
            assert token.revoked is False
    
    def test_is_valid_token(self, app):
        """Test token validity check"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            
            # Valid token
            valid_token = RefreshToken(
                user_id=user.id,
                token='valid-token',
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
            db.session.add(valid_token)
            db.session.commit()
            
            assert valid_token.is_valid() is True
            
            # Expired token
            expired_token = RefreshToken(
                user_id=user.id,
                token='expired-token',
                expires_at=datetime.utcnow() - timedelta(days=1)
            )
            db.session.add(expired_token)
            db.session.commit()
            
            assert expired_token.is_valid() is False
    
    def test_revoke_token(self, app):
        """Test token revocation"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            
            token = RefreshToken(
                user_id=user.id,
                token='token-to-revoke',
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
            db.session.add(token)
            db.session.commit()
            
            assert token.is_valid() is True
            
            token.revoke()
            db.session.commit()
            
            assert token.revoked is True
            assert token.is_valid() is False
