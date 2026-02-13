# CFV API Documentation

Comprehensive API reference for the Crypto Fair Value (CFV) integrated payment system.

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Base URL](#base-url)
- [Endpoints](#endpoints)
  - [CFV Coins](#cfv-coins)
  - [CFV Calculation](#cfv-calculation)
  - [Payment Information](#payment-information)
  - [Orders](#orders)
  - [Payments](#payments)
- [Response Schemas](#response-schemas)
- [Error Handling](#error-handling)

## Overview

The CFV API provides endpoints for cryptocurrency payment processing with integrated Crypto Fair Value calculations. The system supports 12 Digital Gold Foundation (DGF) tracked cryptocurrencies and applies dynamic discounts based on fair value analysis.

### Supported Cryptocurrencies

| Symbol | Name | Category |
|--------|------|----------|
| XNO | Nano | Payment |
| NEAR | NEAR Protocol | Smart Contract Platform |
| ICP | Internet Computer | Smart Contract Platform |
| EGLD | MultiversX | Smart Contract Platform |
| DGB | DigiByte | Payment |
| DASH | Dash | Payment |
| XCH | Chia | Layer 1 |
| XEC | eCash | Payment |
| XMR | Monero | Privacy |
| RVN | Ravencoin | Asset Transfer |
| DGD | Digital Gold | Digital Gold |
| BTC-LN | Bitcoin Lightning | Payment |

## Authentication

Currently, the API does not require authentication for most endpoints. In production, implement JWT-based authentication for user-specific operations.

**Future Authentication Header:**
```
Authorization: Bearer <your_jwt_token>
```

## Base URL

```
Development: http://localhost:5000
Production: https://api.yourdomain.com
```

## Endpoints

### CFV Coins

#### Get Supported Coins

Get a list of all supported DGF cryptocurrencies with their current CFV data and discount information.

**Endpoint:** `GET /api/cfv/coins`

**Request:**
```http
GET /api/cfv/coins HTTP/1.1
Host: localhost:5000
```

**Response:** `200 OK`
```json
{
  "success": true,
  "coins": [
    {
      "symbol": "XNO",
      "name": "Nano",
      "category": "Payment",
      "discount": 10,
      "cfv": {
        "symbol": "XNO",
        "currentPrice": 100.0,
        "fairValue": 165.0,
        "valuationPercent": 65,
        "valuationStatus": "undervalued",
        "calculatedAt": "2026-02-13T05:39:14.129Z",
        "source": "mock"
      }
    }
  ],
  "count": 12
}
```

---

### CFV Calculation

#### Calculate CFV for a Coin

Calculate the Crypto Fair Value for a specific cryptocurrency.

**Endpoint:** `GET /api/cfv/calculate/:symbol`

**Parameters:**
- `symbol` (path): Cryptocurrency symbol (e.g., XNO, NEAR)
- `refresh` (query, optional): Force refresh cache (true/false)

**Request:**
```http
GET /api/cfv/calculate/XNO?refresh=false HTTP/1.1
Host: localhost:5000
```

**Response:** `200 OK`
```json
{
  "success": true,
  "symbol": "XNO",
  "cfv": {
    "symbol": "XNO",
    "currentPrice": 100.0,
    "fairValue": 165.0,
    "valuationPercent": 65,
    "valuationStatus": "undervalued",
    "calculatedAt": "2026-02-13T05:39:14.129Z",
    "source": "mock"
  },
  "discount": 10,
  "metrics": {
    "valuationStatus": "undervalued",
    "valuationPercent": 65,
    "calculatedAt": "2026-02-13T05:39:14.129Z",
    "fairValue": 165.0,
    "currentPrice": 100.0
  }
}
```

**Error Response:** `400 Bad Request`
```json
{
  "success": false,
  "error": "Unsupported cryptocurrency: INVALID"
}
```

---

### Payment Information

#### Get Payment Info with CFV Discount

Calculate payment information with CFV discount applied for a specific cryptocurrency and amount.

**Endpoint:** `POST /api/cfv/payment-info/:symbol`

**Parameters:**
- `symbol` (path): Cryptocurrency symbol

**Request Body:**
```json
{
  "amount_usd": 100.0
}
```

**Request:**
```http
POST /api/cfv/payment-info/XNO HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "amount_usd": 100.0
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "payment_info": {
    "symbol": "XNO",
    "name": "Nano",
    "category": "Payment",
    "originalPriceUSD": 100.0,
    "discountPercent": 10,
    "discountAmount": 10.0,
    "finalPriceUSD": 90.0,
    "amountCrypto": 0.9,
    "currentPrice": 100.0,
    "cfvMetrics": {
      "valuationStatus": "undervalued",
      "valuationPercent": 65,
      "calculatedAt": "2026-02-13T05:39:14.129Z",
      "fairValue": 165.0,
      "currentPrice": 100.0
    }
  }
}
```

**Error Response:** `400 Bad Request`
```json
{
  "success": false,
  "error": "amount_usd is required"
}
```

---

### Orders

#### Create Order with CFV Discount

Create a new e-commerce order with CFV discount applied.

**Endpoint:** `POST /api/orders`

**Request Body:**
```json
{
  "user_id": 1,
  "items": [
    {
      "product_id": "prod_123",
      "name": "Product Name",
      "quantity": 2,
      "price": 50.0
    }
  ],
  "cryptocurrency": "XNO",
  "shipping_address": {
    "name": "John Doe",
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "country": "USA"
  },
  "shipping_method": "standard",
  "shipping_cost": 10.0
}
```

**Request:**
```http
POST /api/orders HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "user_id": 1,
  "items": [...],
  "cryptocurrency": "XNO",
  "shipping_cost": 10.0
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "order": {
    "order_id": "ORD-A1B2C3D4E5F6",
    "user_id": 1,
    "items": [...],
    "subtotal": 100.0,
    "original_price_usd": 110.0,
    "cfv_discount": 10,
    "cfv_metrics": {
      "valuationStatus": "undervalued",
      "valuationPercent": 65,
      "calculatedAt": "2026-02-13T05:39:14.129Z",
      "fairValue": 165.0,
      "currentPrice": 100.0
    },
    "total": 99.0,
    "status": "pending",
    "shipping_cost": 10.0,
    "created_at": "2026-02-13T05:39:14.129Z",
    "updated_at": "2026-02-13T05:39:14.129Z"
  }
}
```

**Error Response:** `400 Bad Request`
```json
{
  "success": false,
  "error": "items is required"
}
```

---

### Payments

#### Create Payment

Create a cryptocurrency payment for an existing order.

**Endpoint:** `POST /api/payments/create`

**Request Body:**
```json
{
  "order_id": "ORD-A1B2C3D4E5F6",
  "cryptocurrency": "XNO",
  "metadata": {
    "customer_ip": "192.168.1.1",
    "user_agent": "Mozilla/5.0..."
  }
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "payment": {
    "payment_id": "abc123def456",
    "order_id": 1,
    "user_id": 1,
    "cryptocurrency": "XNO",
    "amount_crypto": 0.99,
    "amount_usd": 99.0,
    "fair_value": 165.0,
    "cfv_discount": 10,
    "cfv_metrics": {
      "valuationStatus": "undervalued",
      "valuationPercent": 65,
      "calculatedAt": "2026-02-13T05:39:14.129Z",
      "fairValue": 165.0,
      "currentPrice": 100.0
    },
    "payment_address": "nano_abc123...",
    "transaction_hash": null,
    "confirmations": 0,
    "network_fee": 0.00099,
    "total_amount": 0.99099,
    "status": "pending",
    "created_at": "2026-02-13T05:39:14.129Z",
    "expires_at": "2026-02-13T05:54:14.129Z",
    "confirmed_at": null,
    "completed_at": null,
    "metadata": {...}
  }
}
```

---

#### Get Payment by Order ID

Retrieve payment information for a specific order.

**Endpoint:** `GET /api/payments/order/:order_id`

**Parameters:**
- `order_id` (path): Order ID

**Request:**
```http
GET /api/payments/order/ORD-A1B2C3D4E5F6 HTTP/1.1
Host: localhost:5000
```

**Response:** `200 OK`
```json
{
  "success": true,
  "order": {
    "order_id": "ORD-A1B2C3D4E5F6",
    "user_id": 1,
    "total": 99.0,
    "status": "pending",
    ...
  },
  "payments": [
    {
      "payment_id": "abc123def456",
      "status": "pending",
      ...
    }
  ]
}
```

**Error Response:** `404 Not Found`
```json
{
  "success": false,
  "error": "Order not found"
}
```

---

#### Confirm Payment

Confirm a payment with a blockchain transaction hash.

**Endpoint:** `POST /api/payments/confirm`

**Request Body:**
```json
{
  "payment_id": "abc123def456",
  "transaction_hash": "0x1234567890abcdef..."
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "payment": {
    "payment_id": "abc123def456",
    "status": "completed",
    "transaction_hash": "0x1234567890abcdef...",
    "confirmations": 1,
    "confirmed_at": "2026-02-13T05:40:14.129Z",
    "completed_at": "2026-02-13T05:40:14.129Z",
    ...
  },
  "order": {
    "order_id": "ORD-A1B2C3D4E5F6",
    "status": "paid",
    "paid_at": "2026-02-13T05:40:14.129Z",
    ...
  }
}
```

**Error Response:** `400 Bad Request`
```json
{
  "success": false,
  "error": "Payment has expired"
}
```

---

## Response Schemas

### CFV Data

```typescript
{
  symbol: string;           // Cryptocurrency symbol
  currentPrice: number;     // Current market price
  fairValue: number;        // Calculated fair value
  valuationPercent: number; // Percentage difference (positive = undervalued)
  valuationStatus: string;  // "undervalued" | "fair" | "overvalued"
  calculatedAt: string;     // ISO 8601 timestamp
  source: string;          // Data source ("api" | "mock")
}
```

### CFV Metrics

```typescript
{
  valuationStatus: string;  // Valuation status
  valuationPercent: number; // Valuation percentage
  calculatedAt: string;     // ISO 8601 timestamp
  fairValue: number;        // Fair value
  currentPrice: number;     // Current price
}
```

### Order

```typescript
{
  order_id: string;              // Unique order ID
  user_id: number;               // User ID
  items: Array<{                 // Order items
    product_id: string;
    name: string;
    quantity: number;
    price: number;
  }>;
  subtotal: number;              // Subtotal before shipping
  original_price_usd: number;    // Price before CFV discount
  cfv_discount: number;          // Discount percentage applied
  cfv_metrics: CFVMetrics;       // CFV calculation data
  total: number;                 // Final total after discount
  status: string;                // Order status
  shipping_address: object;      // Shipping address
  shipping_method: string;       // Shipping method
  shipping_cost: number;         // Shipping cost
  tracking_number?: string;      // Tracking number (if shipped)
  created_at: string;            // ISO 8601 timestamp
  updated_at: string;            // ISO 8601 timestamp
  paid_at?: string;              // ISO 8601 timestamp
}
```

### Payment

```typescript
{
  payment_id: string;            // Unique payment ID
  order_id: number;              // Associated order ID
  user_id: number;               // User ID
  cryptocurrency: string;        // Cryptocurrency symbol
  amount_crypto: number;         // Amount in cryptocurrency
  amount_usd: number;            // USD equivalent
  fair_value?: number;           // CFV fair value
  cfv_discount: number;          // Discount percentage applied
  cfv_metrics: CFVMetrics;       // CFV calculation data
  payment_address: string;       // Payment address
  transaction_hash?: string;     // Blockchain transaction hash
  confirmations: number;         // Number of confirmations
  network_fee: number;           // Network fee
  total_amount: number;          // Total including fee
  status: string;                // Payment status
  created_at: string;            // ISO 8601 timestamp
  expires_at: string;            // ISO 8601 timestamp
  confirmed_at?: string;         // ISO 8601 timestamp
  completed_at?: string;         // ISO 8601 timestamp
  metadata?: object;             // Additional metadata
}
```

---

## Error Handling

All API endpoints return consistent error responses.

### Error Response Format

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error occurred |

### Common Errors

**Unsupported Cryptocurrency:**
```json
{
  "success": false,
  "error": "Unsupported cryptocurrency: INVALID"
}
```

**Missing Required Field:**
```json
{
  "success": false,
  "error": "amount_usd is required"
}
```

**Resource Not Found:**
```json
{
  "success": false,
  "error": "Order not found"
}
```

**Payment Expired:**
```json
{
  "success": false,
  "error": "Payment has expired"
}
```

**Invalid Order Status:**
```json
{
  "success": false,
  "error": "Order is already paid"
}
```

---

## Discount Tiers

The system applies tiered discounts based on the cryptocurrency's undervaluation:

| Undervaluation | Discount |
|----------------|----------|
| ≥ 50% | 10% |
| 30-49% | 7% |
| 15-29% | 5% |
| < 15% | 2% |
| Overvalued (< 0%) | 0% |

---

## Rate Limiting

**Future Implementation:**
- 100 requests per minute per IP
- 1000 requests per hour per user

---

## Changelog

### Version 1.0.0 (2026-02-13)
- Initial release
- Support for 12 DGF cryptocurrencies
- CFV-based discount system
- Order and payment management endpoints
