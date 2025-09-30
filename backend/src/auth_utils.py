"""
Authentication utilities and helpers
"""
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
import pyotp
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate password strength
    - At least 8 characters
    - Contains uppercase and lowercase
    - Contains at least one number
    - Contains at least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"

def validate_username(username):
    """
    Validate username
    - 3-80 characters
    - Alphanumeric with underscores and hyphens
    """
    if len(username) < 3 or len(username) > 80:
        return False, "Username must be between 3 and 80 characters"
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"
    
    return True, "Username is valid"

def generate_mfa_code(secret):
    """Generate MFA code from secret"""
    totp = pyotp.TOTP(secret)
    return totp.now()

def verify_mfa_code(secret, code):
    """Verify MFA code"""
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)

def token_required(optional=False):
    """
    Decorator to protect routes with JWT authentication
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request(optional=optional)
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Invalid or expired token', 'message': str(e)}), 401
        return wrapper
    return decorator

def get_current_user_id():
    """Get current user ID from JWT token"""
    return get_jwt_identity()

def get_token_claims():
    """Get JWT token claims"""
    return get_jwt()
