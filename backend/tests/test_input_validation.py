"""
Tests for input validation
"""
import pytest
from src.input_validation import (
    InputValidator,
    ValidationError,
    sanitize_output,
    escape_sql_like
)


@pytest.mark.unit
@pytest.mark.security
class TestInputValidator:
    """Test input validator"""
    
    def test_validate_email_valid(self):
        """Test valid email validation"""
        valid_emails = [
            'user@example.com',
            'test.user@example.com',
            'test+tag@example.co.uk',
            'user123@test-domain.com'
        ]
        for email in valid_emails:
            assert InputValidator.validate_email(email) is True
    
    def test_validate_email_invalid(self):
        """Test invalid email validation"""
        invalid_emails = [
            'notanemail',
            '@example.com',
            'user@',
            'user@.com',
            'user @example.com',
            '',
            None
        ]
        for email in invalid_emails:
            assert InputValidator.validate_email(email) is False
    
    def test_validate_username_valid(self):
        """Test valid username validation"""
        valid_usernames = [
            'user123',
            'test_user',
            'test-user',
            'abc',
            'user_123-test'
        ]
        for username in valid_usernames:
            assert InputValidator.validate_username(username) is True
    
    def test_validate_username_invalid(self):
        """Test invalid username validation"""
        invalid_usernames = [
            'ab',  # too short
            'a' * 31,  # too long
            'user name',  # space
            'user@name',  # invalid char
            'user.name',  # invalid char
            '',
            None
        ]
        for username in invalid_usernames:
            assert InputValidator.validate_username(username) is False
    
    def test_validate_password_valid(self):
        """Test valid password validation"""
        valid_passwords = [
            'Password123',
            'Test1234',
            'SecureP@ss1'
        ]
        for password in valid_passwords:
            is_valid, error = InputValidator.validate_password(password)
            assert is_valid is True
            assert error is None
    
    def test_validate_password_invalid(self):
        """Test invalid password validation"""
        invalid_cases = [
            ('short1A', 'too short'),
            ('nouppercase1', 'no uppercase'),
            ('NOLOWERCASE1', 'no lowercase'),
            ('NoDigitsHere', 'no digit'),
            ('', 'empty'),
            (None, 'none')
        ]
        for password, _ in invalid_cases:
            is_valid, error = InputValidator.validate_password(password)
            assert is_valid is False
            assert error is not None
    
    def test_sanitize_html(self):
        """Test HTML sanitization"""
        # Test XSS prevention
        dangerous = '<script>alert("XSS")</script><p>Safe text</p>'
        cleaned = InputValidator.sanitize_html(dangerous)
        assert '<script>' not in cleaned
        assert 'Safe text' in cleaned
        
        # Test allowed tags
        safe = '<p>Text with <strong>bold</strong></p>'
        cleaned = InputValidator.sanitize_html(safe)
        assert '<p>' in cleaned
        assert '<strong>' in cleaned
    
    def test_validate_amount(self):
        """Test amount validation"""
        # Valid amounts
        assert InputValidator.validate_amount(10.5) is True
        assert InputValidator.validate_amount('10.5') is True
        assert InputValidator.validate_amount(100, min_value=0, max_value=200) is True
        
        # Invalid amounts
        assert InputValidator.validate_amount(-10) is False
        assert InputValidator.validate_amount(300, max_value=200) is False
        assert InputValidator.validate_amount('not a number') is False
    
    def test_validate_symbol(self):
        """Test trading symbol validation"""
        # Valid symbols
        valid_symbols = ['BTC/USDT', 'ETH/USD', 'AAPL/USD']
        for symbol in valid_symbols:
            assert InputValidator.validate_symbol(symbol) is True
        
        # Invalid symbols
        invalid_symbols = ['btc/usdt', 'BTC', 'BTC-USDT', 'BTC/usdt']
        for symbol in invalid_symbols:
            assert InputValidator.validate_symbol(symbol) is False
    
    def test_validate_order_type(self):
        """Test order type validation"""
        valid_types = ['market', 'limit', 'stop_loss']
        for order_type in valid_types:
            assert InputValidator.validate_order_type(order_type) is True
        
        assert InputValidator.validate_order_type('invalid_type') is False
    
    def test_validate_order_side(self):
        """Test order side validation"""
        assert InputValidator.validate_order_side('buy') is True
        assert InputValidator.validate_order_side('sell') is True
        assert InputValidator.validate_order_side('hold') is False


@pytest.mark.unit
@pytest.mark.security
class TestSanitization:
    """Test sanitization functions"""
    
    def test_sanitize_output_string(self):
        """Test output sanitization for strings"""
        dangerous = '<script>alert("XSS")</script>Safe'
        cleaned = sanitize_output(dangerous)
        assert '<script>' not in cleaned
        assert 'Safe' in cleaned
    
    def test_sanitize_output_dict(self):
        """Test output sanitization for dictionaries"""
        data = {
            'name': '<script>XSS</script>John',
            'description': '<p>Safe text</p>'
        }
        cleaned = sanitize_output(data)
        assert '<script>' not in cleaned['name']
        assert 'John' in cleaned['name']
        assert '<p>' in cleaned['description']
    
    def test_sanitize_output_list(self):
        """Test output sanitization for lists"""
        data = ['<script>XSS</script>Text', 'Safe text']
        cleaned = sanitize_output(data)
        assert '<script>' not in cleaned[0]
        assert 'Text' in cleaned[0]
    
    def test_escape_sql_like(self):
        """Test SQL LIKE escaping"""
        dangerous = 'test%_value'
        escaped = escape_sql_like(dangerous)
        assert '\\%' in escaped
        assert '\\_' in escaped
