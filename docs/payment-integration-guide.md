# Cryptocurrency Payment Processing Integration Guide

## Overview

The Cryptons.com platform now includes comprehensive cryptocurrency payment processing capabilities, supporting multiple cryptocurrencies including Bitcoin (BTC), Ethereum (ETH), Tether (USDT), and Binance Coin (BNB).

## Features

### ✅ Implemented Features

1. **Multi-Currency Support**
   - Bitcoin (BTC)
   - Ethereum (ETH)
   - Tether (USDT)
   - Binance Coin (BNB)

2. **Payment Methods**
   - Direct cryptocurrency transfer
   - Wallet connection (MetaMask, Trust Wallet, etc.)
   - QR code payment support

3. **Transaction Management**
   - Payment creation and tracking
   - Transaction verification
   - Status monitoring
   - Expiration handling (15-minute timeout)

4. **Wallet Integration**
   - Multiple wallet provider support
   - Secure wallet connection
   - Session management

5. **Security Features**
   - 256-bit SSL encryption
   - Blockchain verified transactions
   - No personal data storage
   - Address validation

## Architecture

### Backend Components

```
backend/
├── payments/
│   ├── __init__.py
│   ├── crypto_payment_processor.py  # Main payment processing logic
│   ├── transaction_verifier.py      # Blockchain transaction verification
│   └── wallet_manager.py            # Wallet connection management
└── api/
    └── payment_api_server.py        # REST API endpoints
```

### Frontend Components

```
frontend/
├── src/
│   ├── components/
│   │   └── shop/
│   │       └── PaymentGateway.jsx   # Payment UI component
│   └── lib/
│       └── paymentApi.js            # API client library
└── .env.example                     # Configuration template
```

## API Endpoints

### Payment Endpoints

#### 1. Get Supported Currencies
```
GET /api/payments/currencies
```

Response:
```json
{
  "success": true,
  "currencies": [
    {
      "code": "BTC",
      "name": "Bitcoin",
      "decimals": 8,
      "network_fee": 0.0001,
      "confirmation_time": 600
    }
  ]
}
```

#### 2. Create Payment
```
POST /api/payments/create
```

Request:
```json
{
  "amount": 0.001,
  "currency": "BTC",
  "order_id": "order_123",
  "metadata": {}
}
```

Response:
```json
{
  "success": true,
  "payment": {
    "payment_id": "abc123",
    "payment_address": "bc1q...",
    "amount": 0.001,
    "network_fee": 0.0001,
    "total_amount": 0.0011,
    "currency": "BTC",
    "status": "pending",
    "expires_at": "2024-01-01T12:00:00",
    "created_at": "2024-01-01T11:45:00"
  }
}
```

#### 3. Check Payment Status
```
GET /api/payments/{payment_id}/status
```

Response:
```json
{
  "success": true,
  "status": {
    "payment_id": "abc123",
    "status": "completed",
    "confirmations": 3,
    "transaction_hash": "0x...",
    "amount": 0.001,
    "currency": "BTC"
  }
}
```

#### 4. Verify Payment
```
POST /api/payments/{payment_id}/verify
```

Request:
```json
{
  "transaction_hash": "0x..."
}
```

Response:
```json
{
  "success": true,
  "payment": {
    "payment_id": "abc123",
    "status": "completed",
    "transaction_hash": "0x...",
    "confirmations": 1
  }
}
```

### Wallet Endpoints

#### 5. Connect Wallet
```
POST /api/payments/wallet/connect
```

Request:
```json
{
  "wallet_type": "metamask",
  "address": "0x...",
  "signature": "..."
}
```

#### 6. Get Supported Wallets
```
GET /api/payments/wallets
```

Response:
```json
{
  "success": true,
  "wallets": [
    {
      "id": "metamask",
      "name": "MetaMask",
      "supported_currencies": ["ETH", "USDT", "BNB"],
      "type": "browser_extension"
    }
  ]
}
```

## Frontend Integration

### Using the Payment Gateway Component

```jsx
import PaymentGateway from '@/components/shop/PaymentGateway.jsx';

function Checkout() {
  const handlePaymentComplete = (paymentInfo) => {
    console.log('Payment completed:', paymentInfo);
    // Handle successful payment
  };

  return (
    <PaymentGateway
      orderTotal={0.001}
      currency="BTC"
      orderId="order_123"
      onPaymentComplete={handlePaymentComplete}
    />
  );
}
```

### Using the Payment API Client

```javascript
import { 
  createPayment, 
  verifyPayment, 
  getSupportedCurrencies 
} from '@/lib/paymentApi.js';

// Get supported currencies
const currencies = await getSupportedCurrencies();

// Create a payment
const payment = await createPayment(0.001, 'BTC', 'order_123');

// Verify a payment
const verified = await verifyPayment(payment.payment_id, txHash);
```

## Configuration

### Frontend Configuration

Create a `.env` file in the `frontend` directory:

```env
VITE_API_URL=http://localhost:5000
VITE_DEBUG=true
```

For production, set the appropriate API URL:
```env
VITE_API_URL=https://api.yourapp.com
VITE_DEBUG=false
```

### Backend Configuration

Create a `.env` file in the `backend` directory:

```env
FLASK_APP=main.py
FLASK_ENV=development
PORT=5000
SECRET_KEY=your_secret_key_here
```

## Payment Flow

### Standard Payment Flow

1. **User initiates payment**
   - Frontend calls `createPayment()` with amount and currency
   - Backend generates unique payment address
   - Payment expires in 15 minutes

2. **User sends cryptocurrency**
   - Frontend displays payment address and QR code
   - User sends exact amount to the address
   - User submits transaction hash

3. **Transaction verification**
   - Frontend calls `verifyPayment()` with transaction hash
   - Backend verifies transaction on blockchain
   - Payment status updated to 'processing' or 'completed'

4. **Payment completion**
   - Backend confirms sufficient blockchain confirmations
   - Payment status updated to 'completed'
   - `onPaymentComplete` callback triggered

### Wallet Connection Flow

1. **User selects wallet method**
   - Frontend initiates wallet connection
   - User connects MetaMask, Trust Wallet, etc.

2. **Wallet authorization**
   - User approves connection in wallet
   - Frontend receives wallet address and signature

3. **Payment execution**
   - Payment transaction initiated through wallet
   - User confirms transaction in wallet
   - Transaction hash returned

4. **Verification and completion**
   - Same as standard flow from step 3

## Security Considerations

### Development vs Production

**Current Implementation (Development)**
- Mock payment addresses generated
- Simulated transaction verification
- No actual blockchain queries
- Suitable for testing and development

**Production Requirements**
- Integrate with actual payment gateway providers:
  - CoinGate
  - BTCPay Server
  - Coinbase Commerce
  - NOWPayments

- Implement real blockchain verification:
  - Query blockchain explorers (BlockCypher, Etherscan)
  - Run full nodes for verification
  - Monitor transaction confirmations

- Security measures:
  - Secure key management
  - Rate limiting
  - IP whitelisting
  - Webhook signature verification
  - HTTPS only in production

### Best Practices

1. **Never store private keys**
   - Use payment gateway providers
   - Generate unique addresses per transaction
   - Use HD wallet derivation

2. **Verify transactions independently**
   - Don't trust client-side data
   - Query blockchain directly
   - Wait for sufficient confirmations

3. **Handle edge cases**
   - Payment timeouts
   - Partial payments
   - Overpayments
   - Network congestion

4. **Monitor and alert**
   - Track payment success rates
   - Alert on failed verifications
   - Monitor blockchain confirmations

## Testing

### Backend Testing

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py

# Test endpoints
curl http://localhost:5000/api/payments/currencies
```

### Frontend Testing

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Access the payment gateway
# Navigate to the shop checkout page
```

### Manual Testing Checklist

- [ ] Create payment for BTC
- [ ] Create payment for ETH
- [ ] Verify payment address generation
- [ ] Test payment expiration (15 min timeout)
- [ ] Verify transaction with mock hash
- [ ] Check payment status updates
- [ ] Test wallet connection
- [ ] Test error handling
- [ ] Verify responsive design
- [ ] Test countdown timer

## Production Deployment

### Environment Setup

1. **Configure payment gateway**
   - Sign up for payment provider (e.g., CoinGate)
   - Obtain API credentials
   - Add credentials to `.env`

2. **Configure blockchain APIs**
   - Sign up for blockchain explorers
   - Get API keys for verification
   - Add to backend configuration

3. **Update API endpoints**
   - Modify `crypto_payment_processor.py` to use real APIs
   - Update `transaction_verifier.py` for blockchain queries
   - Implement webhook handlers for payment notifications

4. **Security hardening**
   - Enable HTTPS
   - Configure CORS properly
   - Set up rate limiting
   - Implement request signing

### Monitoring

- Set up logging for all payment transactions
- Monitor payment success/failure rates
- Track blockchain confirmation times
- Alert on anomalies

## Future Enhancements

- [ ] Add more cryptocurrencies (LTC, ADA, DOT)
- [ ] Implement Lightning Network support
- [ ] Add automatic price conversion from fiat
- [ ] Implement refund functionality
- [ ] Add payment history and receipts
- [ ] Support for stablecoins (USDC, DAI)
- [ ] Multi-signature wallet support
- [ ] Advanced fraud detection
- [ ] Webhook notifications
- [ ] Payment analytics dashboard

## Support

For issues or questions:
- Check the API response errors
- Review server logs
- Consult documentation
- Open an issue on GitHub

## License

MIT License - See LICENSE file for details
