"""
Authentication routes and endpoints
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from datetime import datetime, timedelta
from .models import db, User, RefreshToken
from .auth_utils import (
    validate_email, 
    validate_password, 
    validate_username,
    verify_mfa_code,
    token_required
)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Import rate limiter
try:
    from .security_config import get_rate_limiter
    limiter = get_rate_limiter()
except ImportError:
    limiter = None

def rate_limit(limit_string):
    """Decorator factory for rate limiting"""
    def decorator(f):
        if limiter:
            return limiter.limit(limit_string)(f)
        return f
    return decorator

@auth_bp.route('/register', methods=['POST'])
@rate_limit("5 per minute")
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        username = data['username']
        email = data['email']
        password = data['password']
        
        # Validate username
        valid, message = validate_username(username)
        if not valid:
            return jsonify({'error': message}), 400
        
        # Validate email
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password
        valid, message = validate_password(password)
        if not valid:
            return jsonify({'error': message}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
@rate_limit("10 per minute")
def login():
    """Login user and return JWT tokens"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['username', 'password']):
            return jsonify({'error': 'Missing username or password'}), 400
        
        username = data['username']
        password = data['password']
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Check if MFA is enabled
        if user.mfa_enabled:
            mfa_code = data.get('mfa_code')
            if not mfa_code:
                return jsonify({'error': 'MFA code required', 'mfa_required': True}), 401
            
            if not verify_mfa_code(user.mfa_secret, mfa_code):
                return jsonify({'error': 'Invalid MFA code'}), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token_value = create_refresh_token(identity=user.id)
        
        # Store refresh token
        refresh_token = RefreshToken(
            user_id=user.id,
            token=refresh_token_value,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.session.add(refresh_token)
        db.session.commit()
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token_value,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token"""
    try:
        user_id = get_jwt_identity()
        
        # Create new access token
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Token refresh failed', 'message': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user and revoke refresh token"""
    try:
        jti = get_jwt()['jti']
        user_id = get_jwt_identity()
        
        # Revoke all refresh tokens for this user
        RefreshToken.query.filter_by(user_id=user_id, revoked=False).update({'revoked': True})
        db.session.commit()
        
        return jsonify({'message': 'Logout successful'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Logout failed', 'message': str(e)}), 500

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify():
    """Verify JWT token and return user info"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'valid': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Token verification failed', 'message': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get profile', 'message': str(e)}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update email if provided
        if 'email' in data:
            if not validate_email(data['email']):
                return jsonify({'error': 'Invalid email format'}), 400
            
            # Check if email is already taken
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'Email already in use'}), 409
            
            user.email = data['email']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile', 'message': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if not data or not all(k in data for k in ['current_password', 'new_password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Verify current password
        if not user.check_password(data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Validate new password
        valid, message = validate_password(data['new_password'])
        if not valid:
            return jsonify({'error': message}), 400
        
        # Update password
        user.set_password(data['new_password'])
        
        # Revoke all existing refresh tokens
        RefreshToken.query.filter_by(user_id=user_id, revoked=False).update({'revoked': True})
        
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to change password', 'message': str(e)}), 500

@auth_bp.route('/mfa/enable', methods=['POST'])
@jwt_required()
def enable_mfa():
    """Enable MFA for user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.mfa_enabled:
            return jsonify({'error': 'MFA already enabled'}), 400
        
        # Generate MFA secret
        secret = user.enable_mfa()
        db.session.commit()
        
        return jsonify({
            'message': 'MFA enabled successfully',
            'secret': secret
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to enable MFA', 'message': str(e)}), 500

@auth_bp.route('/mfa/disable', methods=['POST'])
@jwt_required()
def disable_mfa():
    """Disable MFA for user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Verify password before disabling MFA
        if not data or 'password' not in data:
            return jsonify({'error': 'Password required'}), 400
        
        if not user.check_password(data['password']):
            return jsonify({'error': 'Invalid password'}), 401
        
        user.disable_mfa()
        db.session.commit()
        
        return jsonify({'message': 'MFA disabled successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to disable MFA', 'message': str(e)}), 500
