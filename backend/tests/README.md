# Backend Tests

This directory contains the test suite for the Cryptons.com Cryptocurrency Marketplace backend.

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py

# Run tests by marker
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m auth          # Auth tests only
```

## Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── unit/                    # Unit tests
│   ├── test_models.py      # Database model tests
│   └── test_auth_utils.py  # Auth utility tests
├── integration/             # Integration tests
│   ├── test_auth_routes.py # Authentication endpoint tests
│   └── test_api_endpoints.py # API endpoint tests
└── fixtures/                # Shared test data and fixtures
```

## Current Test Coverage

### Unit Tests
- ✅ User model creation and validation
- ✅ Password hashing and verification
- ✅ MFA enable/disable functionality
- ✅ RefreshToken validation and revocation

### Integration Tests
- ✅ User registration (success, validation, duplicates)
- ✅ User login (success, wrong password, non-existent user)
- ✅ Profile access (authenticated, unauthenticated)
- ✅ Logout functionality
- ✅ Health check endpoints

**Total: 30+ tests**

## Fixtures

### Available Fixtures

```python
@pytest.fixture
def app():
    """Create a test Flask application"""
    
@pytest.fixture
def client(app):
    """Create a test client"""
    
@pytest.fixture
def auth_headers(client):
    """Create authorization headers for authenticated requests"""
    
@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
```

## Writing Tests

### Unit Test Example

```python
import pytest
from src.models import db, MyModel

@pytest.mark.unit
class TestMyModel:
    def test_create_model(self, app):
        """Test model creation"""
        with app.app_context():
            instance = MyModel(field='value')
            db.session.add(instance)
            db.session.commit()
            
            assert instance.id is not None
            assert instance.field == 'value'
```

### Integration Test Example

```python
import pytest

@pytest.mark.integration
@pytest.mark.api
class TestMyEndpoint:
    def test_endpoint_success(self, client):
        """Test successful endpoint call"""
        response = client.get('/api/my-endpoint')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'expected_field' in data
```

### Authenticated Test Example

```python
def test_protected_endpoint(self, client, auth_headers):
    """Test protected endpoint with authentication"""
    response = client.get('/api/protected', headers=auth_headers)
    
    assert response.status_code == 200
```

## Test Markers

Use markers to categorize tests:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.auth` - Authentication tests
- `@pytest.mark.api` - API endpoint tests
- `@pytest.mark.slow` - Slow running tests

Run specific markers:

```bash
pytest -m unit          # Run only unit tests
pytest -m "not slow"    # Skip slow tests
```

## Coverage

View coverage report:

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Open report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Best Practices

1. **Use Fixtures**: Reuse test setup with fixtures
2. **Test Database Operations**: Use in-memory database
3. **Test API Contracts**: Verify request/response formats
4. **Keep Tests Isolated**: Each test should be independent
5. **Use Markers**: Categorize tests for easy running
6. **Test Error Cases**: Test both success and failure paths

## Troubleshooting

### Module Import Errors

If you get "No module named 'src'" errors:

```bash
# Ensure you're in the backend directory
cd backend

# Activate virtual environment
source venv/bin/activate
```

### Database Errors

Tests use an in-memory SQLite database. If you get database errors:

1. Check that the app fixture properly initializes the database
2. Ensure db.create_all() is called in the fixture
3. Verify cleanup (db.drop_all()) happens after tests

## Resources

- [Full Testing Documentation](../../docs/TESTING.md)
- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-flask Documentation](https://pytest-flask.readthedocs.io/)

---

For more detailed information, see the [main testing documentation](../../docs/TESTING.md).
