# CFV Integration Guide

Complete guide for integrating Crypto Fair Value (CFV) calculations into the cryptocurrency reservation system.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Service Dependencies](#service-dependencies)
- [Configuration Guide](#configuration-guide)
- [Integration Steps](#integration-steps)
- [API Integration](#api-integration)
- [Frontend Integration](#frontend-integration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

The CFV integration consists of several components working together:

```
┌─────────────────┐
│   Frontend      │
│  (React App)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│   CFV API       │────▶│   CFV Service    │
│  (Flask)        │     │  (Python Class)  │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌──────────────────┐
│   Database      │     │  External APIs   │
│  (PostgreSQL)   │     │  - cfv-calculator│
└─────────────────┘     │  - cfv-agent     │
                        └──────────────────┘
```

### Components

1. **CFV Service** (`backend/services/cfv_service.py`)
   - Calculates fair values
   - Determines discount tiers
   - Caches results
   - Validates cryptocurrencies

2. **CFV API** (`backend/api/cfv_api.py`)
   - REST endpoints
   - Order management
   - Payment processing
   - Response formatting

3. **Database Models** (`backend/src/trading_models.py`)
   - EcommerceOrder model
   - Payment model
   - CFV metrics storage

4. **Frontend Components**
   - CryptoPaymentSelector
   - Payment gateway integration
   - Real-time discount display

## Service Dependencies

### External Services

The CFV system integrates with two external services:

#### 1. CFV Calculator API
- **Repository:** https://github.com/thewriterben/cfv-calculator
- **Default URL:** http://localhost:3000
- **Purpose:** Calculate fair values using Digital Gold Standard formula
- **Endpoints:**
  - `GET /api/cfv/:symbol` - Get CFV calculation

#### 2. CFV Metrics Agent
- **Repository:** https://github.com/thewriterben/cfv-metrics-agent
- **Default URL:** http://localhost:3001
- **Purpose:** Aggregate metrics and provide valuation data
- **Endpoints:**
  - `GET /api/metrics/:symbol` - Get aggregated metrics

### Starting External Services

**Using Docker:**
```bash
# CFV Calculator
cd /path/to/cfv-calculator
docker-compose up -d

# CFV Metrics Agent
cd /path/to/cfv-metrics-agent
docker-compose up -d
```

**Using NPM:**
```bash
# CFV Calculator
cd /path/to/cfv-calculator
npm install
npm start

# CFV Metrics Agent
cd /path/to/cfv-metrics-agent
npm install
npm start
```

## Configuration Guide

### Environment Variables

Add to `backend/.env`:

```bash
# CFV Service URLs
CFV_CALCULATOR_URL=http://localhost:3000
CFV_AGENT_URL=http://localhost:3001

# Cache Configuration
CFV_CACHE_TTL=300000  # 5 minutes in milliseconds

# Discount Configuration
CFV_DISCOUNT_ENABLED=true
CFV_MAX_DISCOUNT=10  # Maximum discount percentage

# Supported Cryptocurrencies
SUPPORTED_CRYPTOS=XNO,NEAR,ICP,EGLD,DGB,DASH,XCH,XEC,XMR,RVN,DGD,BTC-LN

# Database
DATABASE_URL=postgresql://localhost/cryptons_db
```

### Production Configuration

For production, update `backend/.env.production`:

```bash
# Production CFV Service URLs
CFV_CALCULATOR_URL=https://cfv-calculator.yourdomain.com
CFV_AGENT_URL=https://cfv-agent.yourdomain.com

# Stricter cache settings
CFV_CACHE_TTL=180000  # 3 minutes

# Production database
DATABASE_URL=postgresql://user:pass@prod-db.host/cryptons_db

# Security
SECRET_KEY=your_production_secret_key_here
```

## Integration Steps

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Required packages:
- `requests` - For API calls
- `flask` - Web framework
- `flask-sqlalchemy` - Database ORM
- `psycopg2-binary` - PostgreSQL driver

### Step 2: Run Database Migrations

```bash
cd backend
python migrations/add_cfv_models.py upgrade
python migrations/add_cfv_models.py validate
```

### Step 3: Register CFV API Blueprint

In `backend/app.py`, register the CFV API:

```python
from api.cfv_api import cfv_api

def create_app():
    app = Flask(__name__)
    
    # ... existing configuration ...
    
    # Register CFV API
    app.register_blueprint(cfv_api)
    
    return app
```

### Step 4: Initialize Database

```python
from app import create_app
from src.models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database initialized!")
```

### Step 5: Start the Application

```bash
cd backend
python main.py
```

Verify the server is running:
```bash
curl http://localhost:5000/api/cfv/coins
```

## API Integration

### Using the CFV API

#### Get Supported Coins

```javascript
fetch('http://localhost:5000/api/cfv/coins')
  .then(response => response.json())
  .then(data => {
    console.log('Supported coins:', data.coins);
  });
```

#### Calculate CFV for a Coin

```javascript
fetch('http://localhost:5000/api/cfv/calculate/XNO')
  .then(response => response.json())
  .then(data => {
    console.log('CFV Data:', data.cfv);
    console.log('Discount:', data.discount + '%');
  });
```

#### Get Payment Info with Discount

```javascript
fetch('http://localhost:5000/api/cfv/payment-info/XNO', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    amount_usd: 100.0
  })
})
  .then(response => response.json())
  .then(data => {
    console.log('Original Price:', data.payment_info.originalPriceUSD);
    console.log('Discount:', data.payment_info.discountPercent + '%');
    console.log('Final Price:', data.payment_info.finalPriceUSD);
  });
```

#### Create Order with CFV Discount

```javascript
const orderData = {
  user_id: 1,
  items: [
    {
      product_id: 'prod_123',
      name: 'Product Name',
      quantity: 2,
      price: 50.0
    }
  ],
  cryptocurrency: 'XNO',
  shipping_cost: 10.0,
  shipping_address: {
    name: 'John Doe',
    street: '123 Main St',
    city: 'New York',
    state: 'NY',
    zip: '10001',
    country: 'USA'
  },
  shipping_method: 'standard'
};

fetch('http://localhost:5000/api/orders', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(orderData)
})
  .then(response => response.json())
  .then(data => {
    console.log('Order created:', data.order);
    console.log('CFV Discount applied:', data.order.cfv_discount + '%');
  });
```

## Frontend Integration

### Payment Selector Component

Example React component for cryptocurrency selection:

```jsx
import React, { useState, useEffect } from 'react';

function CryptoPaymentSelector({ amount, onSelect }) {
  const [coins, setCoins] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5000/api/cfv/coins')
      .then(response => response.json())
      .then(data => {
        setCoins(data.coins);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="crypto-selector">
      {coins.map(coin => (
        <div key={coin.symbol} className="crypto-option">
          <h3>{coin.name} ({coin.symbol})</h3>
          <p>Category: {coin.category}</p>
          
          {coin.cfv && (
            <div className="cfv-info">
              <p>Fair Value: ${coin.cfv.fairValue.toFixed(2)}</p>
              <p>Current Price: ${coin.cfv.currentPrice.toFixed(2)}</p>
              <p>Status: {coin.cfv.valuationStatus}</p>
            </div>
          )}
          
          {coin.discount > 0 && (
            <div className="discount-badge">
              {coin.discount}% OFF
            </div>
          )}
          
          <button onClick={() => onSelect(coin)}>
            Pay with {coin.symbol}
          </button>
        </div>
      ))}
    </div>
  );
}

export default CryptoPaymentSelector;
```

### Order Creation Flow

```jsx
async function createOrderWithPayment(items, cryptocurrency, shippingInfo) {
  // 1. Create order
  const orderResponse = await fetch('http://localhost:5000/api/orders', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      items,
      cryptocurrency,
      shipping_address: shippingInfo.address,
      shipping_method: shippingInfo.method,
      shipping_cost: shippingInfo.cost
    })
  });
  
  const orderData = await orderResponse.json();
  const order = orderData.order;
  
  // 2. Create payment
  const paymentResponse = await fetch('http://localhost:5000/api/payments/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      order_id: order.order_id,
      cryptocurrency
    })
  });
  
  const paymentData = await paymentResponse.json();
  const payment = paymentData.payment;
  
  // 3. Display payment information to user
  displayPaymentInfo(payment);
  
  return { order, payment };
}
```

## Testing

### Unit Tests

Test the CFV service:

```python
# backend/tests/test_cfv_service.py
import pytest
from services.cfv_service import CFVService

def test_supported_cryptocurrencies():
    service = CFVService()
    
    # Test supported coin
    assert service.is_supported('XNO')
    assert service.is_supported('NEAR')
    
    # Test unsupported coin
    assert not service.is_supported('INVALID')

def test_discount_calculation():
    service = CFVService()
    
    # Test high undervaluation (should get 10% discount)
    discount, metrics = service.calculate_discount('XNO')
    assert discount == 10
    assert metrics['valuationStatus'] == 'undervalued'

def test_payment_info():
    service = CFVService()
    
    payment_info = service.get_payment_info('XNO', 100.0)
    
    assert payment_info['symbol'] == 'XNO'
    assert payment_info['originalPriceUSD'] == 100.0
    assert payment_info['discountPercent'] > 0
    assert payment_info['finalPriceUSD'] < 100.0
```

Run tests:
```bash
cd backend
pytest tests/test_cfv_service.py -v
```

### Integration Tests

Test API endpoints:

```bash
# Test supported coins endpoint
curl http://localhost:5000/api/cfv/coins

# Test CFV calculation
curl http://localhost:5000/api/cfv/calculate/XNO

# Test payment info
curl -X POST http://localhost:5000/api/cfv/payment-info/XNO \
  -H "Content-Type: application/json" \
  -d '{"amount_usd": 100.0}'
```

## Deployment

### Docker Deployment

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - CFV_CALCULATOR_URL=http://cfv-calculator:3000
      - CFV_AGENT_URL=http://cfv-agent:3001
      - DATABASE_URL=postgresql://db:5432/cryptons
    depends_on:
      - db
      - cfv-calculator
      - cfv-agent

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: cryptons
      POSTGRES_USER: cryptons
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  cfv-calculator:
    image: thewriterben/cfv-calculator:latest
    ports:
      - "3000:3000"

  cfv-agent:
    image: thewriterben/cfv-metrics-agent:latest
    ports:
      - "3001:3001"

volumes:
  postgres_data:
```

Deploy:
```bash
docker-compose up -d
```

## Troubleshooting

### Common Issues

#### 1. External API Connection Failed

**Error:** `Error fetching CFV for XNO: Connection refused`

**Solutions:**
- Check if external services are running
- Verify URLs in environment variables
- Test connectivity: `curl http://localhost:3000/health`

#### 2. Database Connection Error

**Error:** `sqlalchemy.exc.OperationalError: could not connect to server`

**Solutions:**
- Verify DATABASE_URL is correct
- Ensure PostgreSQL is running
- Check database permissions

#### 3. CFV Cache Not Working

**Symptoms:** Slow API responses, excessive external API calls

**Solutions:**
- Verify CFV_CACHE_TTL is set
- Check cache size with: `service._cache`
- Clear cache: `service.clear_cache()`

#### 4. Incorrect Discount Calculation

**Symptoms:** Discounts don't match expected tiers

**Solutions:**
- Verify CFV data is accurate
- Check CFV_MAX_DISCOUNT setting
- Ensure CFV_DISCOUNT_ENABLED is true
- Review discount tier logic in CFVService

### Debug Mode

Enable detailed logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('cfv_service')
```

### Health Check

Create a health check endpoint:

```python
@cfv_api.route('/api/cfv/health', methods=['GET'])
def health_check():
    try:
        # Test CFV service
        service = CFVService()
        cfv_data = service.calculate_cfv('XNO')
        
        return jsonify({
            'status': 'healthy',
            'cfv_service': 'operational',
            'cache_size': len(service._cache),
            'sample_calculation': cfv_data is not None
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500
```

---

**Last Updated:** 2026-02-13  
**Version:** 1.0.0
