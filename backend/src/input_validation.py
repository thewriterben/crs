"""
Input validation middleware and utilities
Provides comprehensive validation for API requests
"""
from flask import request, jsonify
from functools import wraps
import re
from typing import Dict, List, Any, Optional
import bleach


class ValidationError(Exception):
    """Custom validation error"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


class InputValidator:
    """Input validation utilities"""
    
    # Regex patterns
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{3,30}$')
    PASSWORD_MIN_LENGTH = 8
    
    # Allowed HTML tags for sanitization
    ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'a']
    ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        if not email or not isinstance(email, str):
            return False
        return bool(InputValidator.EMAIL_PATTERN.match(email))
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username format"""
        if not username or not isinstance(username, str):
            return False
        return bool(InputValidator.USERNAME_PATTERN.match(username))
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, Optional[str]]:
        """
        Validate password strength
        Returns: (is_valid, error_message)
        """
        if not password or not isinstance(password, str):
            return False, "Password is required"
        
        if len(password) < InputValidator.PASSWORD_MIN_LENGTH:
            return False, f"Password must be at least {InputValidator.PASSWORD_MIN_LENGTH} characters"
        
        # Check for at least one uppercase, one lowercase, and one digit
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        
        return True, None
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Sanitize HTML to prevent XSS"""
        if not text:
            return ""
        return bleach.clean(
            text,
            tags=InputValidator.ALLOWED_TAGS,
            attributes=InputValidator.ALLOWED_ATTRIBUTES,
            strip=True
        )
    
    @staticmethod
    def validate_amount(amount: Any, min_value: float = 0.0, max_value: float = None) -> bool:
        """Validate numeric amount"""
        try:
            amount = float(amount)
            if amount < min_value:
                return False
            if max_value is not None and amount > max_value:
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_symbol(symbol: str, allowed_symbols: List[str] = None) -> bool:
        """Validate trading symbol"""
        if not symbol or not isinstance(symbol, str):
            return False
        
        # Basic format validation
        if not re.match(r'^[A-Z]{2,10}/[A-Z]{2,10}$', symbol):
            return False
        
        # Check against allowed list if provided
        if allowed_symbols and symbol not in allowed_symbols:
            return False
        
        return True
    
    @staticmethod
    def validate_order_type(order_type: str) -> bool:
        """Validate order type"""
        valid_types = ['market', 'limit', 'stop_loss', 'stop_limit', 'trailing_stop']
        return order_type in valid_types
    
    @staticmethod
    def validate_order_side(side: str) -> bool:
        """Validate order side"""
        return side in ['buy', 'sell']


def validate_json(*required_fields: str):
    """
    Decorator to validate JSON request body
    
    Usage:
        @validate_json('username', 'email', 'password')
        def register():
            data = request.json
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check if request has JSON
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
            
            data = request.json
            
            # Check required fields
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    'error': 'Missing required fields',
                    'missing_fields': missing_fields
                }), 400
            
            # Check for empty values
            empty_fields = [field for field in required_fields if not data.get(field)]
            if empty_fields:
                return jsonify({
                    'error': 'Fields cannot be empty',
                    'empty_fields': empty_fields
                }), 400
            
            return f(*args, **kwargs)
        return wrapper
    return decorator


def validate_registration():
    """Decorator to validate registration data"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.json
            
            # Validate email
            if not InputValidator.validate_email(data.get('email')):
                return jsonify({'error': 'Invalid email format'}), 400
            
            # Validate username
            if not InputValidator.validate_username(data.get('username')):
                return jsonify({
                    'error': 'Invalid username. Must be 3-30 characters, alphanumeric with hyphens/underscores'
                }), 400
            
            # Validate password
            is_valid, error = InputValidator.validate_password(data.get('password'))
            if not is_valid:
                return jsonify({'error': error}), 400
            
            return f(*args, **kwargs)
        return wrapper
    return decorator


def validate_order():
    """Decorator to validate trading order data"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.json
            
            # Validate symbol
            if not InputValidator.validate_symbol(data.get('symbol')):
                return jsonify({'error': 'Invalid trading symbol format'}), 400
            
            # Validate order type
            if not InputValidator.validate_order_type(data.get('order_type')):
                return jsonify({'error': 'Invalid order type'}), 400
            
            # Validate side
            if not InputValidator.validate_order_side(data.get('side')):
                return jsonify({'error': 'Invalid order side (must be buy or sell)'}), 400
            
            # Validate quantity
            if not InputValidator.validate_amount(data.get('quantity'), min_value=0.00000001):
                return jsonify({'error': 'Invalid quantity'}), 400
            
            # Validate price for limit orders
            if data.get('order_type') == 'limit':
                if not InputValidator.validate_amount(data.get('price'), min_value=0.01):
                    return jsonify({'error': 'Invalid price for limit order'}), 400
            
            return f(*args, **kwargs)
        return wrapper
    return decorator


def sanitize_output(data: Any) -> Any:
    """
    Sanitize output data to prevent XSS
    Recursively sanitizes strings in dictionaries and lists
    """
    if isinstance(data, dict):
        return {k: sanitize_output(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_output(item) for item in data]
    elif isinstance(data, str):
        return InputValidator.sanitize_html(data)
    return data


# SQL Injection prevention helpers
def escape_sql_like(value: str) -> str:
    """Escape special characters in LIKE queries"""
    return value.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')


def validate_pagination(max_per_page: int = 100):
    """
    Decorator to validate pagination parameters
    
    Usage:
        @validate_pagination(max_per_page=50)
        def list_items():
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            
            if page < 1:
                return jsonify({'error': 'Page must be >= 1'}), 400
            
            if per_page < 1 or per_page > max_per_page:
                return jsonify({
                    'error': f'Per page must be between 1 and {max_per_page}'
                }), 400
            
            return f(*args, **kwargs)
        return wrapper
    return decorator
