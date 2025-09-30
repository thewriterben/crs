"""
Database models for authentication
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import secrets

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # MFA fields
    mfa_enabled = db.Column(db.Boolean, default=False)
    mfa_secret = db.Column(db.String(32))
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verify password against hash"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def enable_mfa(self):
        """Enable MFA and generate secret"""
        self.mfa_enabled = True
        self.mfa_secret = secrets.token_hex(16)
        return self.mfa_secret
    
    def disable_mfa(self):
        """Disable MFA"""
        self.mfa_enabled = False
        self.mfa_secret = None
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'mfa_enabled': self.mfa_enabled
        }

class RefreshToken(db.Model):
    """Refresh token model for JWT token management"""
    __tablename__ = 'refresh_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='refresh_tokens')
    
    def is_valid(self):
        """Check if token is valid"""
        return not self.revoked and datetime.utcnow() < self.expires_at
    
    def revoke(self):
        """Revoke the token"""
        self.revoked = True
