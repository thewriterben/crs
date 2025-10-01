#!/usr/bin/env python3
"""
Environment Variable Validation Script
Validates required environment variables before backend startup.
This helps prevent deployment errors due to missing or incorrect configuration.
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class ValidationError:
    """Represents a validation error"""
    def __init__(self, var_name: str, message: str, severity: str = "error"):
        self.var_name = var_name
        self.message = message
        self.severity = severity  # "error", "warning", "info"


class EnvValidator:
    """Environment variable validator"""
    
    # Required environment variables for production
    REQUIRED_PRODUCTION = {
        'SECRET_KEY': {
            'description': 'Flask secret key for session management',
            'validator': 'validate_secret_key',
            'example': 'Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"'
        },
        'JWT_SECRET_KEY': {
            'description': 'JWT token signing key',
            'validator': 'validate_secret_key',
            'example': 'Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"'
        },
        'DATABASE_URL': {
            'description': 'Database connection URL',
            'validator': 'validate_database_url',
            'example': 'postgresql://user:pass@localhost:5432/dbname or sqlite:///marketplace.db'
        },
    }
    
    # Optional but recommended environment variables
    OPTIONAL_VARS = {
        'FLASK_ENV': {
            'description': 'Flask environment (development/production)',
            'validator': 'validate_flask_env',
            'default': 'development',
            'example': 'development or production'
        },
        'FLASK_DEBUG': {
            'description': 'Enable Flask debug mode (NEVER enable in production!)',
            'validator': 'validate_boolean',
            'default': 'False',
            'example': 'True or False'
        },
        'PORT': {
            'description': 'API server port',
            'validator': 'validate_port',
            'default': '5000',
            'example': '5000'
        },
        'CORS_ORIGINS': {
            'description': 'Allowed CORS origins (comma-separated)',
            'validator': 'validate_cors_origins',
            'default': '*',
            'example': 'http://localhost:5173,https://example.com'
        },
        'REDIS_URL': {
            'description': 'Redis connection URL for caching and sessions',
            'validator': 'validate_redis_url',
            'default': 'redis://localhost:6379/0',
            'example': 'redis://localhost:6379/0'
        },
    }
    
    # PostgreSQL specific variables (used when DATABASE_URL is PostgreSQL)
    POSTGRES_VARS = {
        'POSTGRES_USER': {
            'description': 'PostgreSQL username',
            'default': 'cryptons_user'
        },
        'POSTGRES_PASSWORD': {
            'description': 'PostgreSQL password',
            'default': 'change_this_password'
        },
        'POSTGRES_HOST': {
            'description': 'PostgreSQL host',
            'default': 'localhost'
        },
        'POSTGRES_PORT': {
            'description': 'PostgreSQL port',
            'default': '5432'
        },
        'POSTGRES_DB': {
            'description': 'PostgreSQL database name',
            'default': 'cryptons_db'
        },
    }
    
    def __init__(self, env_file: Optional[str] = None, strict: bool = False):
        """
        Initialize validator
        
        Args:
            env_file: Path to .env file (optional)
            strict: If True, treat warnings as errors
        """
        self.env_file = env_file
        self.strict = strict
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
        self.info: List[ValidationError] = []
        self.env_vars = self._load_env_vars()
    
    def _load_env_vars(self) -> Dict[str, str]:
        """Load environment variables from file and system"""
        env_vars = dict(os.environ)
        
        # Try to load from .env file if specified or if it exists
        env_file_path = self.env_file or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), '.env'
        )
        
        if os.path.exists(env_file_path):
            try:
                from dotenv import load_dotenv
                load_dotenv(env_file_path)
                # Reload env vars after loading .env
                env_vars = dict(os.environ)
                self.info.append(
                    ValidationError(
                        'ENV_FILE',
                        f'Loaded environment variables from {env_file_path}',
                        'info'
                    )
                )
            except ImportError:
                self.warnings.append(
                    ValidationError(
                        'ENV_FILE',
                        'python-dotenv not installed, cannot load .env file',
                        'warning'
                    )
                )
        
        return env_vars
    
    def validate_secret_key(self, var_name: str, value: str) -> Optional[ValidationError]:
        """Validate secret key strength"""
        if not value:
            return ValidationError(var_name, 'Secret key cannot be empty')
        
        # Check for default/weak values
        weak_values = [
            'dev-secret-key',
            'change-in-production',
            'your-secret-key-here',
            'secret',
            'password',
            '123456'
        ]
        
        if any(weak in value.lower() for weak in weak_values):
            return ValidationError(
                var_name,
                f'Using default or weak secret key. {self.REQUIRED_PRODUCTION[var_name]["example"]}',
                'warning' if self.env_vars.get('FLASK_ENV') == 'development' else 'error'
            )
        
        # Check minimum length
        if len(value) < 32:
            return ValidationError(
                var_name,
                f'Secret key is too short ({len(value)} chars). Recommended: 32+ characters',
                'warning'
            )
        
        return None
    
    def validate_database_url(self, var_name: str, value: str) -> Optional[ValidationError]:
        """Validate database URL format"""
        if not value:
            return ValidationError(var_name, 'Database URL cannot be empty')
        
        # Parse database URL
        try:
            parsed = urlparse(value)
            
            # Check for valid schemes
            valid_schemes = ['postgresql', 'postgres', 'sqlite', 'mysql']
            if parsed.scheme not in valid_schemes:
                return ValidationError(
                    var_name,
                    f'Unsupported database scheme: {parsed.scheme}. '
                    f'Supported: {", ".join(valid_schemes)}'
                )
            
            # Warn about SQLite in production
            if parsed.scheme == 'sqlite' and self.env_vars.get('FLASK_ENV') == 'production':
                return ValidationError(
                    var_name,
                    'Using SQLite in production is not recommended. Consider PostgreSQL.',
                    'warning'
                )
            
            # For PostgreSQL, check if credentials are present
            if parsed.scheme in ['postgresql', 'postgres']:
                if not parsed.username or not parsed.password:
                    return ValidationError(
                        var_name,
                        'PostgreSQL URL missing username or password',
                        'warning'
                    )
        
        except Exception as e:
            return ValidationError(var_name, f'Invalid database URL format: {str(e)}')
        
        return None
    
    def validate_flask_env(self, var_name: str, value: str) -> Optional[ValidationError]:
        """Validate Flask environment"""
        if not value:
            return None  # Will use default
        
        valid_envs = ['development', 'production', 'testing']
        if value not in valid_envs:
            return ValidationError(
                var_name,
                f'Invalid Flask environment: {value}. '
                f'Must be one of: {", ".join(valid_envs)}'
            )
        
        return None
    
    def validate_boolean(self, var_name: str, value: str) -> Optional[ValidationError]:
        """Validate boolean value"""
        if not value:
            return None  # Will use default
        
        valid_bools = ['true', 'false', '1', '0', 'yes', 'no']
        if value.lower() not in valid_bools:
            return ValidationError(
                var_name,
                f'Invalid boolean value: {value}. '
                f'Must be one of: {", ".join(valid_bools)}'
            )
        
        # Warn if debug is enabled in production
        if var_name == 'FLASK_DEBUG' and value.lower() in ['true', '1', 'yes']:
            if self.env_vars.get('FLASK_ENV') == 'production':
                return ValidationError(
                    var_name,
                    'FLASK_DEBUG is enabled in production! This is a SECURITY RISK!',
                    'error'
                )
        
        return None
    
    def validate_port(self, var_name: str, value: str) -> Optional[ValidationError]:
        """Validate port number"""
        if not value:
            return None  # Will use default
        
        try:
            port = int(value)
            if port < 1 or port > 65535:
                return ValidationError(
                    var_name,
                    f'Port {port} is out of valid range (1-65535)'
                )
        except ValueError:
            return ValidationError(var_name, f'Invalid port number: {value}')
        
        return None
    
    def validate_cors_origins(self, var_name: str, value: str) -> Optional[ValidationError]:
        """Validate CORS origins"""
        if not value:
            return None  # Will use default
        
        # Warn about wildcard in production
        if value == '*' and self.env_vars.get('FLASK_ENV') == 'production':
            return ValidationError(
                var_name,
                'Using wildcard (*) for CORS in production is not recommended. '
                'Specify exact origins.',
                'warning'
            )
        
        # Validate each origin
        if value != '*':
            origins = [o.strip() for o in value.split(',')]
            for origin in origins:
                try:
                    parsed = urlparse(origin)
                    if not parsed.scheme or not parsed.netloc:
                        return ValidationError(
                            var_name,
                            f'Invalid origin URL: {origin}'
                        )
                except Exception:
                    return ValidationError(
                        var_name,
                        f'Invalid origin URL: {origin}'
                    )
        
        return None
    
    def validate_redis_url(self, var_name: str, value: str) -> Optional[ValidationError]:
        """Validate Redis URL"""
        if not value:
            return None  # Will use default
        
        try:
            parsed = urlparse(value)
            if parsed.scheme not in ['redis', 'rediss']:
                return ValidationError(
                    var_name,
                    f'Invalid Redis URL scheme: {parsed.scheme}. Must be redis:// or rediss://'
                )
        except Exception as e:
            return ValidationError(var_name, f'Invalid Redis URL format: {str(e)}')
        
        return None
    
    def validate_all(self) -> bool:
        """
        Validate all environment variables
        
        Returns:
            True if validation passed (no errors), False otherwise
        """
        is_production = self.env_vars.get('FLASK_ENV') == 'production'
        
        # Validate required variables (especially in production)
        for var_name, config in self.REQUIRED_PRODUCTION.items():
            value = self.env_vars.get(var_name)
            
            if not value:
                if is_production:
                    self.errors.append(
                        ValidationError(
                            var_name,
                            f'Required in production: {config["description"]}. {config["example"]}'
                        )
                    )
                else:
                    self.warnings.append(
                        ValidationError(
                            var_name,
                            f'Not set (will use default). {config["description"]}. {config["example"]}',
                            'warning'
                        )
                    )
            else:
                # Run validator
                validator_name = config.get('validator')
                if validator_name:
                    validator = getattr(self, validator_name)
                    error = validator(var_name, value)
                    if error:
                        if error.severity == 'error':
                            self.errors.append(error)
                        elif error.severity == 'warning':
                            self.warnings.append(error)
                        else:
                            self.info.append(error)
        
        # Validate optional variables
        for var_name, config in self.OPTIONAL_VARS.items():
            value = self.env_vars.get(var_name)
            
            if value:
                # Run validator if present
                validator_name = config.get('validator')
                if validator_name:
                    validator = getattr(self, validator_name)
                    error = validator(var_name, value)
                    if error:
                        if error.severity == 'error':
                            self.errors.append(error)
                        elif error.severity == 'warning':
                            self.warnings.append(error)
                        else:
                            self.info.append(error)
        
        # Check PostgreSQL variables if using PostgreSQL
        db_url = self.env_vars.get('DATABASE_URL', '')
        if db_url.startswith('postgres'):
            for var_name, config in self.POSTGRES_VARS.items():
                value = self.env_vars.get(var_name)
                if not value and is_production:
                    self.warnings.append(
                        ValidationError(
                            var_name,
                            f'{config["description"]} not set (will use default: {config["default"]})',
                            'warning'
                        )
                    )
        
        # Return True only if no errors (or no errors+warnings in strict mode)
        return len(self.errors) == 0 and (not self.strict or len(self.warnings) == 0)
    
    def print_results(self):
        """Print validation results"""
        print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
        print(f"{Colors.BOLD}Environment Variable Validation Report{Colors.END}")
        print(f"{Colors.BOLD}{'=' * 70}{Colors.END}\n")
        
        # Print info messages
        if self.info:
            print(f"{Colors.CYAN}{Colors.BOLD}ℹ️  Information:{Colors.END}")
            for info in self.info:
                print(f"{Colors.CYAN}  • {info.message}{Colors.END}")
            print()
        
        # Print warnings
        if self.warnings:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  Warnings:{Colors.END}")
            for warning in self.warnings:
                print(f"{Colors.YELLOW}  • [{warning.var_name}] {warning.message}{Colors.END}")
            print()
        
        # Print errors
        if self.errors:
            print(f"{Colors.RED}{Colors.BOLD}❌ Errors:{Colors.END}")
            for error in self.errors:
                print(f"{Colors.RED}  • [{error.var_name}] {error.message}{Colors.END}")
            print()
        
        # Print summary
        print(f"{Colors.BOLD}{'=' * 70}{Colors.END}")
        
        if not self.errors and not self.warnings:
            print(f"{Colors.GREEN}{Colors.BOLD}✅ All environment variables are valid!{Colors.END}\n")
            return True
        elif not self.errors:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  Validation completed with {len(self.warnings)} warning(s){Colors.END}\n")
            return True
        else:
            print(f"{Colors.RED}{Colors.BOLD}❌ Validation failed with {len(self.errors)} error(s) and {len(self.warnings)} warning(s){Colors.END}\n")
            return False


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate environment variables for Cryptons.com backend',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate current environment
  python validate_env.py
  
  # Validate specific .env file
  python validate_env.py --env-file /path/to/.env
  
  # Strict mode (treat warnings as errors)
  python validate_env.py --strict
  
  # Show all environment variables
  python validate_env.py --show-vars
        """
    )
    
    parser.add_argument(
        '--env-file',
        help='Path to .env file to validate',
        default=None
    )
    
    parser.add_argument(
        '--strict',
        help='Treat warnings as errors',
        action='store_true'
    )
    
    parser.add_argument(
        '--show-vars',
        help='Show all detected environment variables',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    # Create validator
    validator = EnvValidator(env_file=args.env_file, strict=args.strict)
    
    # Show variables if requested
    if args.show_vars:
        print(f"\n{Colors.BOLD}Detected Environment Variables:{Colors.END}\n")
        for key in sorted(validator.env_vars.keys()):
            # Only show Cryptons.com-related variables
            if any(prefix in key for prefix in ['FLASK', 'SECRET', 'JWT', 'DATABASE', 'REDIS', 'CORS', 'POSTGRES', 'PORT', 'API']):
                value = validator.env_vars[key]
                # Mask sensitive values
                if any(sensitive in key for sensitive in ['SECRET', 'PASSWORD', 'KEY']):
                    display_value = '*' * min(len(value), 8) if value else '(not set)'
                else:
                    display_value = value[:50] + '...' if len(value) > 50 else value
                print(f"  {key}: {display_value}")
        print()
    
    # Run validation
    validator.validate_all()
    
    # Print results
    success = validator.print_results()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
