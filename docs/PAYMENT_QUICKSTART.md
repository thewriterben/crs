# Cryptocurrency Payment Processing - Quick Start Guide

## Overview

This implementation adds comprehensive cryptocurrency payment processing to the CRS platform with support for Bitcoin, Ethereum, USDT, and BNB.

## What's Been Implemented

### Backend (Python/Flask)

1. **Payment Processing Module** (`backend/payments/`)
   - `crypto_payment_processor.py` - Core payment logic
   - `transaction_verifier.py` - Blockchain verification
   - `wallet_manager.py` - Wallet connection handling

2. **API Endpoints** (`backend/api/payment_api_server.py`)
   - `/api/payments/currencies` - Get supported currencies
   - `/api/payments/create` - Create new payment
   - `/api/payments/{id}/status` - Check payment status
   - `/api/payments/{id}/verify` - Verify transaction
   - `/api/payments/wallet/connect` - Connect wallet
   - `/api/payments/wallets` - Get supported wallets

### Frontend (React)

1. **Updated PaymentGateway Component** (`frontend/src/components/shop/PaymentGateway.jsx`)
   - Real-time backend integration
   - Multi-currency support (BTC, ETH)
   - Payment address generation
   - Transaction verification
   - 15-minute expiration timer
   - Error handling and loading states

2. **API Client Library** (`frontend/src/lib/paymentApi.js`)
   - Clean API interface for all payment operations
   - Error handling and validation

## Quick Start

### 1. Start the Backend

```bash
cd backend

# Install dependencies (if not already installed)
pip install Flask Flask-CORS

# Start the server
python3 main.py
```

The server will start on `http://localhost:5000`

### 2. Test the API

```bash
# Get supported currencies
curl http://localhost:5000/api/payments/currencies

# Create a payment
curl -X POST http://localhost:5000/api/payments/create \
  -H "Content-Type: application/json" \
  -d '{"amount": 0.001, "currency": "BTC", "order_id": "test_123"}'

# Get supported wallets
curl http://localhost:5000/api/payments/wallets
```

### 3. Run the Frontend (Optional)

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:5000" > .env

# Start dev server
npm run dev
```

## Supported Features

### ✅ Cryptocurrencies
- Bitcoin (BTC) - 8 decimals, ~10 min confirmation
- Ethereum (ETH) - 18 decimals, ~3 min confirmation
- Tether (USDT) - 6 decimals, ~3 min confirmation
- Binance Coin (BNB) - 18 decimals, ~1 min confirmation

### ✅ Payment Methods
- Direct cryptocurrency transfer with QR code
- Wallet connection (MetaMask, Trust Wallet, Coinbase Wallet, WalletConnect)

### ✅ Payment Flow
1. Create payment request with amount and currency
2. Generate unique payment address
3. Display QR code and address to user
4. User sends cryptocurrency
5. Verify transaction on blockchain
6. Confirm payment completion

### ✅ Security Features
- Unique payment addresses per transaction
- Transaction verification
- 15-minute payment expiration
- Network fee calculation
- Status tracking and monitoring

## Architecture

```
┌─────────────────┐
│   Frontend      │
│   (React)       │
│   PaymentGateway│
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   Backend       │
│   Payment API   │
├─────────────────┤
│ Payment         │
│ Processor       │
├─────────────────┤
│ Transaction     │
│ Verifier        │
├─────────────────┤
│ Wallet          │
│ Manager         │
└─────────────────┘
```

## Testing Results

### ✅ Backend Tests Passed
- [x] Health check endpoint working
- [x] API status showing crypto_payments feature enabled
- [x] Get supported currencies (4 currencies)
- [x] Create payment for BTC (unique address generated)
- [x] Create payment for ETH (unique address generated)
- [x] Get supported wallets (4 wallet providers)
- [x] Payment status checking
- [x] Transaction verification
- [x] Payment state transitions (pending → processing → completed)

### Example Payment Created

```json
{
  "payment_id": "71d0bd4fc9d2a242",
  "currency": "BTC",
  "amount": 0.001,
  "network_fee": 0.0001,
  "total_amount": 0.0011,
  "payment_address": "bc1q56c44bf1f56c8b3aca637043465937512a622a19",
  "status": "pending",
  "expires_at": "2025-09-30T02:29:03.053478"
}
```

## Development vs Production

### Current Implementation (Development)
- ✅ Mock payment address generation
- ✅ Simulated transaction verification
- ✅ All payment logic and state management
- ✅ API endpoints fully functional
- ⚠️ Does not connect to real blockchain networks

### For Production Deployment
To use in production, you need to:

1. **Integrate with Payment Gateway**
   - CoinGate, BTCPay Server, Coinbase Commerce, or NOWPayments
   - Update `crypto_payment_processor.py` to use their APIs

2. **Add Blockchain Verification**
   - Use BlockCypher, Etherscan, BSCScan APIs
   - Update `transaction_verifier.py` with real blockchain queries

3. **Security Configuration**
   - Add API keys to `.env` files
   - Enable HTTPS
   - Configure CORS properly
   - Add rate limiting
   - Implement webhook handlers

4. **Web3 Wallet Integration**
   - Add Web3.js or Ethers.js for wallet connections
   - Implement actual wallet signing
   - Handle MetaMask/WalletConnect flows

## File Changes Summary

### New Files Created
```
backend/payments/__init__.py
backend/payments/crypto_payment_processor.py
backend/payments/transaction_verifier.py
backend/payments/wallet_manager.py
backend/api/payment_api_server.py
backend/.env.example
frontend/src/lib/paymentApi.js
frontend/.env.example
frontend/src/pages/PaymentTestPage.jsx
docs/payment-integration-guide.md
docs/PAYMENT_QUICKSTART.md
```

### Modified Files
```
backend/main.py - Added payment API routes
frontend/src/components/shop/PaymentGateway.jsx - Connected to backend
```

## Next Steps

To fully complete the integration:

1. **Install Frontend Dependencies** (if testing UI)
   ```bash
   cd frontend && npm install
   ```

2. **Configure Environment Variables**
   - Copy `.env.example` to `.env` in both frontend and backend
   - Update API URLs for your environment

3. **Add to Application**
   - Import PaymentGateway component where needed
   - Pass order amount, currency, and order ID
   - Handle onPaymentComplete callback

4. **Production Setup** (when ready)
   - Choose a payment gateway provider
   - Add their API credentials
   - Update verification logic to query real blockchains
   - Enable HTTPS and security features

## Documentation

See `docs/payment-integration-guide.md` for comprehensive documentation including:
- Complete API reference
- Security considerations
- Production deployment guide
- Testing checklist
- Future enhancements

## Support

For issues:
1. Check backend logs: `python3 main.py` output
2. Test API endpoints with curl
3. Check browser console for frontend errors
4. Review the integration guide in `docs/`

## License

MIT License - Part of the CRS Cryptocurrency Marketplace project
