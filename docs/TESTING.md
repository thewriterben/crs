# Testing Infrastructure Documentation

## Overview

This document describes the comprehensive testing infrastructure implemented for the CRS Cryptocurrency Marketplace. The testing ecosystem covers both frontend (React/Vite) and backend (Flask/Python) components with unit tests, integration tests, and automated CI/CD testing.

## Table of Contents

- [Frontend Testing](#frontend-testing)
- [Backend Testing](#backend-testing)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [CI/CD Integration](#cicd-integration)
- [Writing New Tests](#writing-new-tests)
- [Best Practices](#best-practices)

---

## Frontend Testing

### Technology Stack

- **Test Framework**: Vitest (fast, Vite-native testing framework)
- **React Testing**: @testing-library/react
- **DOM Assertions**: @testing-library/jest-dom
- **User Interactions**: @testing-library/user-event
- **Test Environment**: jsdom

### Configuration

The frontend testing is configured in `frontend/vitest.config.js`:

```javascript
{
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/tests/setup/test-setup.js'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80,
    }
  }
}
```

### Test Structure

```
frontend/src/tests/
├── setup/
│   ├── test-setup.js          # Global test configuration
│   └── test-utils.jsx         # Custom render utilities
├── __tests__/
│   ├── components/
│   │   ├── ui/                # UI component tests
│   │   ├── ai/                # AI component tests (to be added)
│   │   └── auth/              # Auth component tests (to be added)
│   ├── hooks/                 # Custom hooks tests
│   ├── contexts/              # Context tests (to be added)
│   └── utils/                 # Utility function tests
```

### Available Tests

#### Component Tests
- **Button.test.jsx** - Tests for button component variants, states, and interactions
- **Card.test.jsx** - Tests for card component and its subcomponents

#### Hook Tests
- **useMobile.test.js** - Tests for mobile detection hook

#### Utility Tests
- **utils.test.js** - Tests for className merging utility

### Frontend Test Commands

```bash
# Run tests in watch mode
npm run test

# Run tests once
npm run test:run

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

---

## Backend Testing

### Technology Stack

- **Test Framework**: pytest
- **Flask Testing**: pytest-flask
- **Mocking**: pytest-mock
- **Coverage**: pytest-cov

### Configuration

The backend testing is configured in `backend/pytest.ini`:

```ini
[pytest]
testpaths = tests
addopts = 
    -v
    --strict-markers
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80

markers =
    unit: Unit tests
    integration: Integration tests
    auth: Authentication tests
    api: API endpoint tests
```

### Test Structure

```
backend/tests/
├── conftest.py                # Pytest fixtures and configuration
├── unit/
│   ├── test_models.py         # Database model tests
│   └── test_auth_utils.py     # Auth utility tests (to be added)
├── integration/
│   ├── test_auth_routes.py    # Authentication endpoint tests
│   └── test_api_endpoints.py  # API endpoint tests
└── fixtures/
    └── (shared test data)
```

### Available Tests

#### Unit Tests
- **test_models.py** - Tests for User and RefreshToken models including:
  - User creation and validation
  - Password hashing and verification
  - MFA enable/disable functionality
  - Refresh token validation and revocation

#### Integration Tests
- **test_auth_routes.py** - Tests for authentication endpoints:
  - User registration (success, duplicate, validation)
  - User login (success, wrong password, non-existent user)
  - Profile access (authenticated, unauthenticated)
  - Logout functionality

- **test_api_endpoints.py** - Tests for health check endpoints:
  - Liveness check
  - Readiness check
  - Health info

### Backend Test Commands

```bash
# Activate virtual environment
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_models.py

# Run tests by marker
pytest -m unit          # Run only unit tests
pytest -m integration   # Run only integration tests
pytest -m auth          # Run only auth tests

# Run with coverage
pytest --cov=src --cov-report=html

# Run with verbose output
pytest -v

# Run specific test
pytest tests/unit/test_models.py::TestUserModel::test_create_user
```

---

## Running Tests

### Running All Tests

From the project root:

```bash
# Run both frontend and backend tests
npm test

# Run with coverage
npm run test:coverage
```

### Running Frontend Tests Only

```bash
npm run test:frontend

# With coverage
npm run test:frontend:coverage
```

### Running Backend Tests Only

```bash
npm run test:backend

# With coverage
npm run test:backend:coverage
```

---

## Test Coverage

### Coverage Goals

- **Minimum Coverage**: 80% for lines, functions, branches, and statements
- **Target Coverage**: 90%+ for critical paths (authentication, payment processing)

### Viewing Coverage Reports

#### Frontend

After running `npm run test:coverage` in the frontend directory:

```bash
# Open HTML coverage report
open coverage/index.html  # macOS
xdg-open coverage/index.html  # Linux
start coverage/index.html  # Windows
```

#### Backend

After running pytest with coverage:

```bash
cd backend

# View terminal report
pytest --cov=src --cov-report=term-missing

# Generate and open HTML report
pytest --cov=src --cov-report=html
open htmlcov/index.html  # macOS
```

### Coverage Exclusions

Files excluded from coverage:
- Test files (`*test*.py`, `*.test.js`)
- Configuration files
- Build artifacts (`dist/`, `venv/`)
- Node modules

---

## CI/CD Integration

### GitHub Actions Workflow

The CI/CD pipeline (`.github/workflows/ci-cd.yml`) includes automated testing:

#### Frontend Pipeline
1. **Linting** - ESLint code quality checks
2. **Testing** - Run Vitest test suite
3. **Coverage** - Generate and upload coverage reports
4. **Build** - Build production bundle

#### Backend Pipeline
1. **Linting** - flake8 and pylint checks
2. **Testing** - Run pytest test suite
3. **Coverage** - Generate and upload coverage reports

#### Deployment Check
- Runs only when all tests pass
- Required for merging to main branch

### Test Status Badges

Add these to your README.md:

```markdown
![Tests](https://github.com/thewriterben/crs/workflows/CI/CD%20Pipeline/badge.svg)
![Coverage](https://codecov.io/gh/thewriterben/crs/branch/main/graph/badge.svg)
```

---

## Writing New Tests

### Frontend Test Template

```javascript
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MyComponent } from '@/components/MyComponent'

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />)
    expect(screen.getByText('Expected Text')).toBeInTheDocument()
  })

  it('handles user interaction', async () => {
    const handleClick = vi.fn()
    render(<MyComponent onClick={handleClick} />)
    
    await userEvent.click(screen.getByRole('button'))
    expect(handleClick).toHaveBeenCalled()
  })
})
```

### Backend Test Template

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

@pytest.mark.integration
class TestMyEndpoint:
    def test_endpoint_success(self, client):
        """Test successful endpoint call"""
        response = client.get('/api/my-endpoint')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'expected_field' in data
```

---

## Best Practices

### General Testing Principles

1. **Test Behavior, Not Implementation**
   - Focus on what the component does, not how it does it
   - Test from the user's perspective

2. **Keep Tests Isolated**
   - Each test should be independent
   - Use fixtures for shared setup
   - Clean up after tests

3. **Use Descriptive Names**
   - Test names should describe what they're testing
   - Use the pattern: `test_<action>_<expected_result>`

4. **Test Edge Cases**
   - Test both success and failure paths
   - Test boundary conditions
   - Test error handling

5. **Maintain Test Coverage**
   - Aim for 80%+ coverage
   - Focus on critical paths
   - Don't sacrifice quality for coverage numbers

### Frontend Best Practices

1. **Use Testing Library Queries**
   - Prefer `getByRole`, `getByLabelText`, `getByText`
   - Avoid `getByTestId` unless necessary
   - Use accessible queries

2. **User-Centric Testing**
   - Use `userEvent` for interactions (not `fireEvent`)
   - Test what users see and do
   - Test accessibility

3. **Async Testing**
   - Use `waitFor` for async operations
   - Use `findBy` queries for async elements
   - Be patient with async tests

4. **Mock Wisely**
   - Mock external dependencies (APIs, services)
   - Don't mock what you're testing
   - Keep mocks simple

### Backend Best Practices

1. **Use Fixtures**
   - Create reusable fixtures in `conftest.py`
   - Use fixture scopes appropriately
   - Share fixtures across test files

2. **Test Database Operations**
   - Use in-memory database for tests
   - Clean up after each test
   - Test transactions and rollbacks

3. **Test API Contracts**
   - Test request/response formats
   - Test status codes
   - Test error responses

4. **Use Markers**
   - Mark tests by type (`@pytest.mark.unit`)
   - Mark slow tests (`@pytest.mark.slow`)
   - Run specific test categories

---

## Troubleshooting

### Common Issues

#### Frontend

**Issue**: Tests fail with "Cannot find module"
```bash
# Solution: Check path aliases in vitest.config.js
# Ensure @ alias points to ./src
```

**Issue**: "window.matchMedia is not a function"
```bash
# Solution: Already mocked in test-setup.js
# Check that setupFiles is configured in vitest.config.js
```

#### Backend

**Issue**: "No module named 'src'"
```bash
# Solution: Check sys.path in conftest.py
# Ensure backend directory is in Python path
```

**Issue**: Database connection errors
```bash
# Solution: Tests use in-memory SQLite
# Check app context in fixtures
```

### Getting Help

1. Check the test output for detailed error messages
2. Review the test documentation
3. Check existing tests for examples
4. Open an issue on GitHub with:
   - Test output
   - Steps to reproduce
   - Environment details

---

## Next Steps

### Planned Test Additions

1. **Frontend**
   - AI dashboard component tests
   - Authentication component tests
   - WebSocket hook tests
   - Payment flow E2E tests

2. **Backend**
   - AI prediction engine tests
   - WebSocket service tests
   - Payment processing tests
   - Performance/load tests

3. **E2E Testing**
   - Consider adding Playwright for full E2E testing
   - Test critical user journeys
   - Test cross-browser compatibility

### Continuous Improvement

- Monitor test execution time
- Maintain test coverage above 80%
- Regular test maintenance
- Update tests when features change
- Add performance benchmarks

---

## Resources

- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-flask Documentation](https://pytest-flask.readthedocs.io/)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

---

**Last Updated**: January 2025
**Version**: 1.0.0
