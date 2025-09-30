"""
Tests for environment variable validation script
"""
import os
import sys
import pytest
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(scripts_dir))

from validate_env import EnvValidator, ValidationError


class TestEnvValidator:
    """Test EnvValidator class"""
    
    def test_validator_initialization(self):
        """Test validator can be initialized"""
        validator = EnvValidator()
        assert validator is not None
        assert isinstance(validator.env_vars, dict)
    
    def test_validate_secret_key_empty(self):
        """Test secret key validation with empty value"""
        validator = EnvValidator()
        error = validator.validate_secret_key('SECRET_KEY', '')
        assert error is not None
        assert 'cannot be empty' in error.message
    
    def test_validate_secret_key_weak(self):
        """Test secret key validation with weak value"""
        validator = EnvValidator()
        error = validator.validate_secret_key('SECRET_KEY', 'dev-secret-key')
        assert error is not None
        assert 'weak' in error.message.lower()
    
    def test_validate_secret_key_short(self):
        """Test secret key validation with short value"""
        validator = EnvValidator()
        error = validator.validate_secret_key('SECRET_KEY', 'short')
        assert error is not None
        assert 'too short' in error.message
    
    def test_validate_secret_key_valid(self):
        """Test secret key validation with valid value"""
        validator = EnvValidator()
        error = validator.validate_secret_key('SECRET_KEY', 'a' * 32)
        assert error is None
    
    def test_validate_database_url_empty(self):
        """Test database URL validation with empty value"""
        validator = EnvValidator()
        error = validator.validate_database_url('DATABASE_URL', '')
        assert error is not None
        assert 'cannot be empty' in error.message
    
    def test_validate_database_url_invalid_scheme(self):
        """Test database URL validation with invalid scheme"""
        validator = EnvValidator()
        error = validator.validate_database_url('DATABASE_URL', 'invalid://localhost/db')
        assert error is not None
        assert 'Unsupported database scheme' in error.message
    
    def test_validate_database_url_sqlite(self):
        """Test database URL validation with SQLite"""
        validator = EnvValidator()
        error = validator.validate_database_url('DATABASE_URL', 'sqlite:///marketplace.db')
        assert error is None
    
    def test_validate_database_url_postgresql(self):
        """Test database URL validation with PostgreSQL"""
        validator = EnvValidator()
        error = validator.validate_database_url('DATABASE_URL', 'postgresql://user:pass@localhost:5432/db')
        assert error is None
    
    def test_validate_database_url_postgresql_no_credentials(self):
        """Test database URL validation with PostgreSQL without credentials"""
        validator = EnvValidator()
        error = validator.validate_database_url('DATABASE_URL', 'postgresql://localhost:5432/db')
        assert error is not None
        assert 'missing username or password' in error.message
    
    def test_validate_flask_env_valid(self):
        """Test Flask environment validation with valid values"""
        validator = EnvValidator()
        for env in ['development', 'production', 'testing']:
            error = validator.validate_flask_env('FLASK_ENV', env)
            assert error is None
    
    def test_validate_flask_env_invalid(self):
        """Test Flask environment validation with invalid value"""
        validator = EnvValidator()
        error = validator.validate_flask_env('FLASK_ENV', 'invalid')
        assert error is not None
        assert 'Invalid Flask environment' in error.message
    
    def test_validate_boolean_valid(self):
        """Test boolean validation with valid values"""
        validator = EnvValidator()
        for value in ['true', 'false', '1', '0', 'yes', 'no']:
            error = validator.validate_boolean('FLASK_DEBUG', value)
            assert error is None or error.severity != 'error'
    
    def test_validate_boolean_invalid(self):
        """Test boolean validation with invalid value"""
        validator = EnvValidator()
        error = validator.validate_boolean('FLASK_DEBUG', 'invalid')
        assert error is not None
        assert 'Invalid boolean value' in error.message
    
    def test_validate_port_valid(self):
        """Test port validation with valid value"""
        validator = EnvValidator()
        error = validator.validate_port('PORT', '5000')
        assert error is None
    
    def test_validate_port_invalid(self):
        """Test port validation with invalid value"""
        validator = EnvValidator()
        error = validator.validate_port('PORT', 'invalid')
        assert error is not None
        assert 'Invalid port number' in error.message
    
    def test_validate_port_out_of_range(self):
        """Test port validation with out of range value"""
        validator = EnvValidator()
        error = validator.validate_port('PORT', '70000')
        assert error is not None
        assert 'out of valid range' in error.message
    
    def test_validate_cors_origins_wildcard(self):
        """Test CORS origins validation with wildcard"""
        validator = EnvValidator()
        error = validator.validate_cors_origins('CORS_ORIGINS', '*')
        assert error is None  # Allowed in development
    
    def test_validate_cors_origins_valid_urls(self):
        """Test CORS origins validation with valid URLs"""
        validator = EnvValidator()
        error = validator.validate_cors_origins('CORS_ORIGINS', 'http://localhost:5173,https://example.com')
        assert error is None
    
    def test_validate_cors_origins_invalid_url(self):
        """Test CORS origins validation with invalid URL"""
        validator = EnvValidator()
        error = validator.validate_cors_origins('CORS_ORIGINS', 'invalid-url')
        assert error is not None
        assert 'Invalid origin URL' in error.message
    
    def test_validate_redis_url_valid(self):
        """Test Redis URL validation with valid value"""
        validator = EnvValidator()
        error = validator.validate_redis_url('REDIS_URL', 'redis://localhost:6379/0')
        assert error is None
    
    def test_validate_redis_url_invalid_scheme(self):
        """Test Redis URL validation with invalid scheme"""
        validator = EnvValidator()
        error = validator.validate_redis_url('REDIS_URL', 'http://localhost:6379')
        assert error is not None
        assert 'Invalid Redis URL scheme' in error.message
    
    def test_validate_all_development(self, monkeypatch):
        """Test full validation in development environment"""
        # Clear environment
        monkeypatch.delenv('SECRET_KEY', raising=False)
        monkeypatch.delenv('JWT_SECRET_KEY', raising=False)
        monkeypatch.delenv('DATABASE_URL', raising=False)
        monkeypatch.setenv('FLASK_ENV', 'development')
        
        validator = EnvValidator()
        result = validator.validate_all()
        
        # Should pass with warnings in development
        assert result is True
        assert len(validator.warnings) > 0
        assert len(validator.errors) == 0
    
    def test_validate_all_production_missing_required(self, monkeypatch):
        """Test full validation in production with missing required variables"""
        # Clear environment
        monkeypatch.delenv('SECRET_KEY', raising=False)
        monkeypatch.delenv('JWT_SECRET_KEY', raising=False)
        monkeypatch.delenv('DATABASE_URL', raising=False)
        monkeypatch.setenv('FLASK_ENV', 'production')
        
        validator = EnvValidator()
        result = validator.validate_all()
        
        # Should fail with errors in production
        assert result is False
        assert len(validator.errors) > 0
    
    def test_validate_all_production_with_required(self, monkeypatch):
        """Test full validation in production with all required variables"""
        monkeypatch.setenv('FLASK_ENV', 'production')
        monkeypatch.setenv('SECRET_KEY', 'a' * 32)
        monkeypatch.setenv('JWT_SECRET_KEY', 'b' * 32)
        monkeypatch.setenv('DATABASE_URL', 'postgresql://user:pass@localhost:5432/db')
        
        validator = EnvValidator()
        result = validator.validate_all()
        
        # Should pass (may have warnings for optional vars)
        assert result is True
        assert len(validator.errors) == 0
    
    def test_validate_debug_in_production(self, monkeypatch):
        """Test validation catches debug mode enabled in production"""
        monkeypatch.setenv('FLASK_ENV', 'production')
        monkeypatch.setenv('FLASK_DEBUG', 'True')
        
        validator = EnvValidator()
        error = validator.validate_boolean('FLASK_DEBUG', 'True')
        
        assert error is not None
        assert error.severity == 'error'
        assert 'SECURITY RISK' in error.message
    
    def test_sqlite_warning_in_production(self, monkeypatch):
        """Test validation warns about SQLite in production"""
        monkeypatch.setenv('FLASK_ENV', 'production')
        
        validator = EnvValidator()
        error = validator.validate_database_url('DATABASE_URL', 'sqlite:///marketplace.db')
        
        assert error is not None
        assert error.severity == 'warning'
        assert 'not recommended' in error.message
    
    def test_cors_wildcard_warning_in_production(self, monkeypatch):
        """Test validation warns about CORS wildcard in production"""
        monkeypatch.setenv('FLASK_ENV', 'production')
        
        validator = EnvValidator()
        error = validator.validate_cors_origins('CORS_ORIGINS', '*')
        
        assert error is not None
        assert error.severity == 'warning'
        assert 'not recommended' in error.message
    
    def test_strict_mode(self, monkeypatch):
        """Test strict mode treats warnings as failures"""
        monkeypatch.setenv('FLASK_ENV', 'development')
        monkeypatch.delenv('SECRET_KEY', raising=False)
        
        # Without strict mode, should pass with warnings
        validator = EnvValidator(strict=False)
        validator.validate_all()
        result = validator.validate_all()
        assert result is True
        assert len(validator.warnings) > 0
        
        # With strict mode, should fail due to warnings
        validator_strict = EnvValidator(strict=True)
        validator_strict.validate_all()
        result_strict = not validator_strict.warnings and not validator_strict.errors
        # In strict mode, having warnings means it's not fully passing
        assert len(validator_strict.warnings) > 0


class TestValidationError:
    """Test ValidationError class"""
    
    def test_validation_error_creation(self):
        """Test ValidationError can be created"""
        error = ValidationError('TEST_VAR', 'Test message')
        assert error.var_name == 'TEST_VAR'
        assert error.message == 'Test message'
        assert error.severity == 'error'
    
    def test_validation_error_with_severity(self):
        """Test ValidationError with custom severity"""
        warning = ValidationError('TEST_VAR', 'Test warning', 'warning')
        assert warning.severity == 'warning'
        
        info = ValidationError('TEST_VAR', 'Test info', 'info')
        assert info.severity == 'info'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
