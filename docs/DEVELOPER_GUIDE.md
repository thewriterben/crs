# Developer Guide

Complete developer guide for contributing to the Cryptons.com Cryptocurrency Marketplace project, including Phase 3 advanced features.

**Version**: 3.0.0  
**Last Updated**: September 30, 2024

---

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Phase 3 Module Development](#phase-3-module-development)
- [API Development](#api-development)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

- **Node.js**: >= 18.0.0
- **Python**: >= 3.8.0
- **npm**: >= 8.0.0
- **Git**: Latest version
- **Docker**: (Optional) For production-like environment
- **PostgreSQL**: 15+ (for production) or SQLite (for development)
- **Redis**: 7+ (for caching and sessions)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/thewriterben/crs.git
cd crs

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Run tests to verify setup
cd ../backend
PYTHONPATH=$(pwd) python tests/test_phase3.py
```

---

## Development Setup

### Backend Development

#### 1. Virtual Environment

Always use a virtual environment for Python development:

```bash
cd backend
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

#### 2. Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///crs.db
# For PostgreSQL: postgresql://user:password@localhost:5432/crs

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=http://localhost:5173

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
```

#### 3. Run Backend Server

```bash
# Standard Flask server
python src/main.py

# Or with auto-reload
FLASK_ENV=development python src/main.py

# Phase 3 API server
PYTHONPATH=$(pwd) python api/phase3_api.py
```

### Frontend Development

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Run Development Server

```bash
npm run dev
# Opens at http://localhost:5173
```

#### 3. Build for Production

```bash
npm run build
# Output in frontend/dist/
```

### Docker Development

For a production-like environment:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Project Structure

```
crs/
├── backend/                      # Backend API server
│   ├── ai/                       # AI/ML modules
│   │   ├── __init__.py
│   │   ├── advanced_models.py    # Phase 3: LSTM, Transformer, Ensemble, BERT
│   │   ├── ai_prediction_engine.py
│   │   └── sentiment_analysis_system.py
│   │
│   ├── defi/                     # Phase 3: DeFi integration
│   │   ├── __init__.py
│   │   └── defi_integration.py   # DEX, Farming, Staking, Liquidity
│   │
│   ├── social/                   # Phase 3: Social trading
│   │   ├── __init__.py
│   │   └── social_trading.py     # Copy trading, Signals, Portfolios
│   │
│   ├── portfolio/                # Phase 3: Portfolio automation
│   │   ├── __init__.py
│   │   └── portfolio_automation.py  # Rebalancing, Risk, DCA, Stop-Loss
│   │
│   ├── api/                      # API endpoints
│   │   ├── ai_api_server.py
│   │   ├── payment_api_server.py
│   │   ├── phase3_api.py         # Phase 3 API (30+ endpoints)
│   │   └── unified_api_server.py
│   │
│   ├── src/                      # Core application
│   │   ├── auth/                 # Authentication
│   │   ├── models/               # Database models
│   │   └── utils/                # Utility functions
│   │
│   ├── tests/                    # Test suite
│   │   ├── test_phase3.py        # Phase 3 tests
│   │   └── ...
│   │
│   └── requirements.txt          # Python dependencies
│
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── pages/                # Page components
│   │   ├── hooks/                # Custom hooks
│   │   └── lib/                  # Utilities
│   └── package.json
│
├── docs/                         # Documentation
│   ├── API_REFERENCE.md          # Complete API reference
│   ├── DEVELOPER_GUIDE.md        # This file
│   └── ...
│
├── scripts/                      # Utility scripts
│   ├── demo_phase3.py            # Phase 3 demo
│   └── start_phase3_api.sh       # API launcher
│
└── docker-compose.yml            # Docker orchestration
```

---

## Coding Standards

### Python Code Style

We follow PEP 8 with these additional guidelines:

#### 1. Formatting

Use **Black** for automatic formatting:

```bash
# Format single file
black backend/ai/advanced_models.py

# Format entire backend
black backend/

# Check without modifying
black --check backend/
```

#### 2. Linting

Use **flake8** for linting:

```bash
# Lint backend
flake8 backend/ --max-line-length=100 --exclude=venv

# With specific rules
flake8 backend/ --max-line-length=100 --ignore=E203,W503
```

#### 3. Type Hints

Always use type hints for function parameters and return values:

```python
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

def calculate_risk(
    positions: List[Dict[str, float]], 
    threshold: float = 0.05
) -> Tuple[float, str]:
    """
    Calculate portfolio risk score.
    
    Args:
        positions: List of position dictionaries
        threshold: Risk threshold (default: 0.05)
        
    Returns:
        Tuple of (risk_score, risk_level)
    """
    risk_score = sum(p['volatility'] * p['value'] for p in positions)
    risk_level = "high" if risk_score > 7 else "medium" if risk_score > 3 else "low"
    return risk_score, risk_level
```

#### 4. Dataclasses

Use dataclasses for structured data:

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TradingSignal:
    """Trading signal with AI-generated recommendations."""
    asset: str
    action: str  # BUY, SELL, HOLD
    confidence: float
    currentPrice: float
    targetPrice: float
    stopLoss: float
    timestamp: datetime
```

#### 5. Error Handling

Always handle errors appropriately:

```python
from flask import jsonify

@app.route('/api/endpoint', methods=['POST'])
def endpoint():
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'required_field' not in data:
            return jsonify({
                'error': 'Missing required field',
                'code': 'MISSING_PARAMS'
            }), 400
        
        # Process request
        result = process_data(data)
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'code': 'INVALID_PARAMS'
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'code': 'SERVER_ERROR'
        }), 500
```

### JavaScript/React Code Style

#### 1. ESLint Configuration

Use the provided `.eslintrc.js` configuration:

```bash
# Lint frontend
cd frontend
npm run lint

# Auto-fix issues
npm run lint -- --fix
```

#### 2. Component Structure

Follow this structure for React components:

```javascript
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

/**
 * Component description
 * 
 * @param {Object} props - Component props
 * @param {string} props.title - Title to display
 * @param {Function} props.onUpdate - Update callback
 */
const MyComponent = ({ title, onUpdate }) => {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    // Effect logic
  }, []);
  
  const handleClick = () => {
    // Event handler
  };
  
  return (
    <div>
      <h1>{title}</h1>
      {/* Component content */}
    </div>
  );
};

MyComponent.propTypes = {
  title: PropTypes.string.isRequired,
  onUpdate: PropTypes.func.isRequired,
};

export default MyComponent;
```

#### 3. Naming Conventions

- **Components**: PascalCase (e.g., `UserProfile`, `TradingDashboard`)
- **Functions**: camelCase (e.g., `calculateRisk`, `fetchData`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`, `MAX_RETRIES`)
- **Files**: kebab-case (e.g., `user-profile.js`, `trading-dashboard.js`)

---

## Testing Guidelines

### Backend Testing

#### 1. Test Structure

Place tests in `backend/tests/` with naming convention `test_*.py`:

```python
# backend/tests/test_defi.py
import pytest
from defi.defi_integration import DEXAggregator

def test_dex_quote():
    """Test DEX quote generation."""
    dex = DEXAggregator()
    quote = dex.get_quote("ETH", "USDT", 1.0)
    
    assert quote is not None
    assert len(quote) > 0
    assert all('dex' in q for q in quote)
    assert all('amountOut' in q for q in quote)

def test_dex_quote_invalid_token():
    """Test DEX quote with invalid token."""
    dex = DEXAggregator()
    quote = dex.get_quote("INVALID", "USDT", 1.0)
    
    assert quote == []
```

#### 2. Running Tests

```bash
# Run all tests
cd backend
PYTHONPATH=$(pwd) pytest

# Run specific test file
PYTHONPATH=$(pwd) pytest tests/test_phase3.py

# Run with coverage
PYTHONPATH=$(pwd) pytest --cov=. --cov-report=html

# Run specific test
PYTHONPATH=$(pwd) pytest tests/test_defi.py::test_dex_quote
```

#### 3. Test Fixtures

Use pytest fixtures for reusable test data:

```python
@pytest.fixture
def sample_portfolio():
    """Sample portfolio for testing."""
    return {
        'positions': [
            {'asset': 'BTC', 'value': 50000.0, 'volatility': 0.65},
            {'asset': 'ETH', 'value': 30000.0, 'volatility': 0.72},
            {'asset': 'USDT', 'value': 20000.0, 'volatility': 0.01}
        ]
    }

def test_risk_calculation(sample_portfolio):
    """Test risk calculation with sample portfolio."""
    from portfolio.portfolio_automation import RiskManagementSystem
    
    risk = RiskManagementSystem()
    result = risk.assess_risk(sample_portfolio['positions'])
    
    assert result['riskScore'] > 0
    assert result['riskLevel'] in ['low', 'medium', 'high']
```

### Frontend Testing

#### 1. Component Tests

Use Vitest and React Testing Library:

```javascript
// frontend/src/components/TradingSignal.test.jsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import TradingSignal from './TradingSignal';

describe('TradingSignal', () => {
  it('renders signal correctly', () => {
    const signal = {
      asset: 'BTC',
      action: 'BUY',
      confidence: 0.87,
      currentPrice: 52000
    };
    
    render(<TradingSignal signal={signal} />);
    
    expect(screen.getByText('BTC')).toBeInTheDocument();
    expect(screen.getByText('BUY')).toBeInTheDocument();
    expect(screen.getByText('87%')).toBeInTheDocument();
  });
});
```

#### 2. Running Tests

```bash
cd frontend

# Run all tests
npm test

# Run with UI
npm run test:ui

# Generate coverage
npm run test:coverage
```

---

## Phase 3 Module Development

### Adding New AI Models

To add a new AI model to the advanced models module:

```python
# backend/ai/advanced_models.py

@dataclass
class MyNewModel:
    """Description of the new model."""
    name: str = "MyNewModel"
    
    def predict(self, data: List[float]) -> List[float]:
        """
        Generate predictions using the new model.
        
        Args:
            data: Historical price data
            
        Returns:
            List of predicted prices
        """
        # Model implementation
        predictions = self._process_data(data)
        return predictions
    
    def _process_data(self, data: List[float]) -> List[float]:
        """Internal processing logic."""
        # Implementation
        pass
```

Then add the endpoint in `backend/api/phase3_api.py`:

```python
@app.route('/api/phase3/ai/mynewmodel/predict', methods=['POST'])
def predict_mynewmodel():
    """MyNewModel price predictions."""
    try:
        data = request.get_json()
        
        if not data or 'symbol' not in data or 'data' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        model = MyNewModel()
        predictions = model.predict(data['data'])
        
        return jsonify({
            'predictions': predictions,
            'model': 'MyNewModel',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Adding New DeFi Protocols

To integrate a new DeFi protocol:

```python
# backend/defi/defi_integration.py

@dataclass
class NewProtocolIntegration:
    """Integration with New DeFi Protocol."""
    protocol_name: str = "NewProtocol"
    
    def get_opportunities(self) -> List[Dict]:
        """Get farming/staking opportunities."""
        return [
            {
                'poolId': 'new_001',
                'protocol': self.protocol_name,
                'asset': 'TOKEN',
                'apy': 45.0,
                'tvl': 1000000,
                'riskLevel': 'medium'
            }
        ]
    
    def deposit(self, pool_id: str, amount: float) -> Dict:
        """Deposit to protocol."""
        # Implementation
        pass
```

### Adding Social Trading Features

To add new social trading features:

```python
# backend/social/social_trading.py

class NewSocialFeature:
    """New social trading feature."""
    
    def __init__(self):
        self.name = "NewFeature"
    
    def execute(self, params: Dict) -> Dict:
        """Execute the feature."""
        # Implementation
        return {
            'status': 'success',
            'result': {}
        }
```

---

## API Development

### Creating New Endpoints

Follow this pattern for new API endpoints:

```python
from flask import Flask, request, jsonify
from datetime import datetime

@app.route('/api/phase3/category/action', methods=['POST'])
def new_endpoint():
    """
    Endpoint description.
    
    Request Body:
        param1 (str): Description
        param2 (float): Description
        
    Returns:
        JSON response with result
    """
    try:
        # 1. Parse request
        data = request.get_json()
        
        # 2. Validate input
        if not data or 'param1' not in data:
            return jsonify({
                'error': 'Missing required parameter: param1',
                'code': 'MISSING_PARAMS'
            }), 400
        
        # 3. Process request
        result = process_logic(data['param1'], data.get('param2', 0))
        
        # 4. Return response
        return jsonify({
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'code': 'INVALID_PARAMS'
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'code': 'SERVER_ERROR'
        }), 500
```

### API Documentation

Document all endpoints in `docs/API_REFERENCE.md` following this format:

```markdown
#### Endpoint Name

Description of what the endpoint does.

**Endpoint**: `POST /api/phase3/category/action`

**Request Body**:
```json
{
  "param1": "value",
  "param2": 123.45
}
```

**Response** (200 OK):
```json
{
  "result": "success",
  "timestamp": "2024-09-30T12:00:00Z"
}
```
```

---

## Contributing

### Git Workflow

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

3. **Make your changes**
   - Write clean, well-documented code
   - Follow coding standards
   - Add tests for new features

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   PYTHONPATH=$(pwd) pytest
   
   # Frontend tests
   cd frontend
   npm test
   ```

5. **Commit with descriptive messages**
   ```bash
   git add .
   git commit -m "Add new DeFi protocol integration
   
   - Implement NewProtocol class
   - Add API endpoints for deposits/withdrawals
   - Include comprehensive tests
   - Update documentation"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/my-new-feature
   ```

7. **Create Pull Request**
   - Provide clear description
   - Reference any related issues
   - Ensure CI/CD passes

### Code Review Process

- All PRs require at least one approval
- CI/CD must pass (tests, linting, security scans)
- Documentation must be updated
- Breaking changes require migration guide

### Commit Message Guidelines

Follow the conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Example**:
```
feat(defi): add Curve Finance integration

- Implement CurveProtocol class
- Add endpoints for pool deposits
- Include APY calculations
- Add comprehensive test coverage

Closes #123
```

---

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'defi'`

**Solution**:
```bash
# Set PYTHONPATH
export PYTHONPATH=/path/to/crs/backend:$PYTHONPATH

# Or run with PYTHONPATH
cd backend
PYTHONPATH=$(pwd) python tests/test_phase3.py
```

#### 2. Database Connection Issues

**Problem**: Cannot connect to PostgreSQL

**Solution**:
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Or start with Docker Compose
docker-compose up -d postgres

# Check connection
psql -h localhost -U cryptons_user -d cryptons_db
```

#### 3. Redis Connection Issues

**Problem**: Cannot connect to Redis

**Solution**:
```bash
# Start Redis
docker-compose up -d redis

# Test connection
redis-cli ping
```

#### 4. Frontend Build Errors

**Problem**: Build fails with dependency errors

**Solution**:
```bash
# Clean install
cd frontend
rm -rf node_modules package-lock.json
npm install

# Clear cache
npm cache clean --force
```

### Debug Mode

Enable debug mode for detailed error messages:

```python
# backend/.env
FLASK_DEBUG=True
FLASK_ENV=development
```

```bash
# Run with debug logging
PYTHONPATH=$(pwd) python -m pdb api/phase3_api.py
```

### Getting Help

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Search [GitHub Issues](https://github.com/thewriterben/crs/issues)
- Create a new issue with:
  - Clear description of the problem
  - Steps to reproduce
  - Expected vs actual behavior
  - System information
  - Error messages/logs

---

## Resources

### Documentation

- [README.md](../README.md) - Project overview
- [API_REFERENCE.md](API_REFERENCE.md) - Complete API reference
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Deployment instructions
- [PHASE_3_IMPLEMENTATION.md](PHASE_3_IMPLEMENTATION.md) - Phase 3 details

### External Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Testing Best Practices](https://docs.pytest.org/en/stable/)

---

**Version**: 3.0.0  
**Last Updated**: September 30, 2024  
**Maintainers**: Cryptons.com Development Team
