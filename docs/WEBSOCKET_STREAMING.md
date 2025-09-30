# Real-time Data Streaming with WebSockets

This document describes the WebSocket implementation for real-time data streaming in the CRS (Cryptocurrency Marketplace) application.

## Overview

The application now supports real-time data streaming using WebSocket technology, enabling:
- **Live market data feeds** - Real-time cryptocurrency price updates
- **Instant price updates** - Sub-second price change notifications  
- **Event-driven notifications** - Trading signals and sentiment analysis alerts
- **Low-latency communication** - Direct bidirectional communication between client and server

## Architecture

### Backend (Flask-SocketIO)

**Location:** `/backend/websocket_service.py`

The backend WebSocket service is built using Flask-SocketIO and provides:

#### WebSocket Events

| Event | Direction | Description | Interval |
|-------|-----------|-------------|----------|
| `connect` | Server → Client | Client connection established | On connect |
| `disconnect` | Server → Client | Client disconnection | On disconnect |
| `subscribe` | Client → Server | Subscribe to specific symbols | On demand |
| `market_update` | Server → Client | Live market price data | 2 seconds |
| `sentiment_update` | Server → Client | Sentiment analysis data | 10 seconds |
| `trading_signal` | Server → Client | Trading signals/alerts | 15 seconds |
| `connection_status` | Server → Client | Connection status updates | On status change |

#### Market Data Format

The `market_update` event provides real-time price data for multiple cryptocurrencies:

```json
{
  "BTC": {
    "symbol": "BTC",
    "price": 45234.56,
    "change_24h": 2.45,
    "volume_24h": 28500000.00,
    "timestamp": "2024-01-15T10:30:00.000Z"
  },
  "ETH": {
    "symbol": "ETH",
    "price": 2567.89,
    "change_24h": -1.23,
    "volume_24h": 15200000.00,
    "timestamp": "2024-01-15T10:30:00.000Z"
  },
  "ADA": {
    "symbol": "ADA",
    "price": 0.456789,
    "change_24h": 5.67,
    "volume_24h": 3400000.00,
    "timestamp": "2024-01-15T10:30:00.000Z"
  }
}
```

**Field Descriptions:**
- `symbol` (string): Cryptocurrency ticker symbol
- `price` (number): Current market price in USD
- `change_24h` (number): Percentage change in the last 24 hours
- `volume_24h` (number): Trading volume in USD for the last 24 hours
- `timestamp` (string): ISO 8601 formatted timestamp of the data point

**Example Usage:**
```javascript
socket.on('market_update', (data) => {
  const btcPrice = data.BTC.price;
  const priceChange = data.BTC.change_24h;
  
  console.log(`BTC: $${btcPrice} (${priceChange > 0 ? '+' : ''}${priceChange}%)`);
  
  // Update UI
  updatePriceDisplay('BTC', btcPrice, priceChange);
});
```

#### Sentiment Update Format

The `sentiment_update` event provides market sentiment analysis:

```json
{
  "overall_sentiment": "BULLISH",
  "market_fear_greed": 72,
  "market_mood": "BULLISH",
  "confidence": 0.85,
  "trending_topics": ["bitcoin", "ethereum", "defi"],
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Field Descriptions:**
- `overall_sentiment` (string): General market sentiment - one of: `POSITIVE`, `NEUTRAL`, `NEGATIVE`, `BULLISH`, `BEARISH`
- `market_fear_greed` (number): Fear & Greed Index (0-100, where 0 is extreme fear, 100 is extreme greed)
- `market_mood` (string): Current market mood - one of: `BULLISH`, `BEARISH`, `NEUTRAL`
- `confidence` (number): Confidence level of the analysis (0.0-1.0)
- `trending_topics` (array): List of currently trending topics in crypto discussions
- `timestamp` (string): ISO 8601 formatted timestamp

**Example Usage:**
```javascript
socket.on('sentiment_update', (data) => {
  const fearGreed = data.market_fear_greed;
  const sentiment = data.overall_sentiment;
  
  // Determine sentiment color
  const sentimentColor = fearGreed > 70 ? 'green' : 
                        fearGreed < 30 ? 'red' : 'yellow';
  
  console.log(`Market Sentiment: ${sentiment} (${fearGreed}/100)`);
  console.log(`Trending: ${data.trending_topics.join(', ')}`);
  
  // Update sentiment indicator
  updateSentimentIndicator(sentiment, fearGreed, sentimentColor);
});
```

#### Trading Signal Format

The `trading_signal` event provides automated trading recommendations:

```json
{
  "symbol": "BTC",
  "signal": "STRONG_BUY",
  "strength": 0.92,
  "reason": "Strong momentum detected",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Field Descriptions:**
- `symbol` (string): Cryptocurrency ticker symbol for the signal
- `signal` (string): Trading recommendation - one of: `STRONG_BUY`, `BUY`, `HOLD`, `SELL`, `STRONG_SELL`
- `strength` (number): Signal strength/confidence (0.5-1.0, where 1.0 is highest confidence)
- `reason` (string): Human-readable explanation for the signal
- `timestamp` (string): ISO 8601 formatted timestamp

**Possible Reasons:**
- "Strong momentum detected"
- "Volume surge observed"
- "Breakout pattern forming"
- "Support level reached"
- "Resistance level approaching"

**Example Usage:**
```javascript
socket.on('trading_signal', (signal) => {
  console.log(`${signal.signal} ${signal.symbol} - Strength: ${signal.strength}`);
  console.log(`Reason: ${signal.reason}`);
  
  // Filter for high-confidence signals
  if (signal.strength > 0.8) {
    showNotification(`${signal.signal} signal for ${signal.symbol}`, signal.reason);
  }
  
  // Add to signal history
  addToSignalHistory(signal);
});
```

### Frontend (socket.io-client)

#### WebSocket Service

**Location:** `/frontend/src/lib/websocket.js`

A singleton service that manages the WebSocket connection:

```javascript
import websocketService from '@/lib/websocket.js';

// Connect to server
websocketService.connect();

// Subscribe to symbols
websocketService.subscribe(['BTC', 'ETH', 'ADA']);

// Listen for events
const unsubscribe = websocketService.on('market_update', (data) => {
  console.log('Market update:', data);
});

// Cleanup
unsubscribe();
websocketService.disconnect();
```

#### React Hook

**Location:** `/frontend/src/hooks/useWebSocket.js`

A custom React hook for easy integration:

```javascript
import { useWebSocket } from '@/hooks/useWebSocket.js';

function MyComponent() {
  const { 
    isConnected,
    marketData,
    sentimentData,
    tradingSignals,
    lastUpdate,
    subscribe 
  } = useWebSocket({ 
    autoConnect: true,
    symbols: ['BTC', 'ETH']
  });

  return (
    <div>
      <p>Status: {isConnected ? 'Connected' : 'Disconnected'}</p>
      <p>BTC Price: ${marketData.BTC?.price}</p>
    </div>
  );
}
```

## Integration Examples

### AIDashboard Component

The main AI dashboard now displays real-time data with live connection status:

```javascript
const { isConnected, marketData, sentimentData } = useWebSocket({ 
  autoConnect: true, 
  symbols: ['BTC', 'ETH', 'ADA', 'DOT', 'LINK'] 
});

// Updates automatically merge with existing dashboard data
useEffect(() => {
  if (marketData && Object.keys(marketData).length > 0) {
    setDashboardData(prev => ({
      ...prev,
      predictions: updatePrices(prev.predictions, marketData)
    }));
  }
}, [marketData]);
```

### Visual Indicators

Both dashboard components now include connection status indicators:

```jsx
<div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
  <span className="status-indicator"></span>
  {isConnected ? 'Live' : 'Offline'}
</div>
```

The indicator:
- Shows green with pulsing animation when connected
- Shows red when disconnected
- Updates in real-time as connection changes

## Setup Instructions

### Backend Setup

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python app.py
   ```

   The server will:
   - Start on port 5000
   - Enable WebSocket support automatically
   - Begin broadcasting real-time data
   - Log connection events

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Access the application:**
   - Open browser to `http://localhost:5173`
   - Check browser console for WebSocket connection logs
   - Verify "Live" indicator appears in dashboard headers

## Connection Management

### Auto-reconnection

The client automatically handles reconnection with:
- **Initial delay:** 1 second
- **Maximum delay:** 5 seconds
- **Maximum attempts:** 5
- **Exponential backoff:** Yes

### Error Handling

Connection errors are logged and status is updated:
```javascript
// Connection status values:
// - 'connected': Successfully connected
// - 'disconnected': Connection lost
// - 'error': Connection failed
```

## Performance Considerations

### Update Frequencies

To balance real-time updates with performance:
- **Market data:** Every 2 seconds (highly frequent)
- **Sentiment data:** Every 10 seconds (moderate)
- **Trading signals:** Every 15 seconds (periodic)

### Data Efficiency

- Only subscribed symbols receive updates
- Data is compressed using WebSocket binary frames
- Reconnection uses exponential backoff
- Updates merge with existing state (no full refresh)

## Testing

### Backend Testing

```bash
cd backend
python test_websocket_setup.py
```

This validates:
- WebSocket service module exists
- Integration with Flask app
- Required dependencies listed

### Frontend Testing

```bash
cd frontend
node test_websocket_frontend.mjs
```

This validates:
- WebSocket client service
- React hook implementation
- Dependencies installed
- Component integrations

### Manual Testing

1. Start backend server
2. Start frontend dev server
3. Open browser console
4. Check for connection messages:
   ```
   ✓ WebSocket connected
   Subscription confirmed: ["BTC", "ETH", ...]
   ```
5. Watch for data updates in console
6. Verify dashboard updates in real-time

## Browser Compatibility

WebSocket is supported in:
- ✓ Chrome 16+
- ✓ Firefox 11+
- ✓ Safari 7+
- ✓ Edge 12+
- ✓ Opera 12.1+

Fallback to polling is automatic via socket.io.

## Authentication

The CRS WebSocket implementation supports token-based authentication using JWT (JSON Web Tokens) to secure real-time connections. This section describes how to authenticate WebSocket connections.

### Authentication Flow

1. **Obtain Access Token**: User logs in via REST API and receives a JWT access token
2. **Connect with Token**: Client includes token when establishing WebSocket connection
3. **Token Verification**: Server validates token before accepting connection
4. **Automatic Reconnection**: Client uses stored token for automatic reconnections

### Token-Based Authentication

WebSocket connections can be authenticated using JWT tokens obtained from the authentication API.

#### Backend Implementation

To enable authentication on WebSocket connections, modify the connection handler:

```python
from flask_socketio import SocketIO, emit, disconnect
from flask_jwt_extended import decode_token
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

@socketio.on('connect')
def handle_connect(auth):
    """Handle client connection with authentication"""
    try:
        # Extract token from auth parameter
        token = auth.get('token') if auth else None
        
        if not token:
            print('Connection rejected: No token provided')
            disconnect()
            return False
        
        # Verify JWT token
        try:
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
            print(f'Authenticated user {user_id} connected')
            
            # Send connection confirmation with user info
            emit('connection_status', {
                'status': 'connected',
                'message': 'Authenticated connection established',
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            })
            return True
            
        except ExpiredSignatureError:
            print('Connection rejected: Token expired')
            emit('auth_error', {'error': 'Token expired'})
            disconnect()
            return False
            
        except InvalidTokenError:
            print('Connection rejected: Invalid token')
            emit('auth_error', {'error': 'Invalid token'})
            disconnect()
            return False
            
    except Exception as e:
        print(f'Connection error: {e}')
        disconnect()
        return False
```

#### JavaScript Client Authentication

Connect to WebSocket with authentication token:

```javascript
import { io } from 'socket.io-client';

// Obtain token from login API
const accessToken = localStorage.getItem('access_token');

// Connect with authentication
const socket = io('http://localhost:5000', {
  auth: {
    token: accessToken
  },
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: 5
});

// Handle authentication errors
socket.on('auth_error', (data) => {
  console.error('Authentication failed:', data.error);
  
  if (data.error === 'Token expired') {
    // Refresh token and reconnect
    refreshTokenAndReconnect();
  }
});

// Handle successful connection
socket.on('connection_status', (data) => {
  console.log('Connected:', data.message);
  console.log('User ID:', data.user_id);
});

// Refresh token and reconnect
async function refreshTokenAndReconnect() {
  try {
    const response = await fetch('http://localhost:5000/api/auth/refresh', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        refresh_token: localStorage.getItem('refresh_token')
      })
    });
    
    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    
    // Reconnect with new token
    socket.auth.token = data.access_token;
    socket.connect();
  } catch (error) {
    console.error('Token refresh failed:', error);
  }
}
```

#### Python Client Authentication

Example Python client with authentication:

```python
import socketio
import requests
import time

# Socket.IO client
sio = socketio.Client()

# Login and get token
def login(username, password):
    """Login and retrieve access token"""
    response = requests.post('http://localhost:5000/api/auth/login', json={
        'username': username,
        'password': password
    })
    
    if response.status_code == 200:
        data = response.json()
        return data['access_token'], data['refresh_token']
    else:
        raise Exception(f'Login failed: {response.text}')

# Event handlers
@sio.on('connection_status')
def on_connection_status(data):
    print(f"Connected: {data['message']}")
    print(f"User ID: {data.get('user_id')}")

@sio.on('market_update')
def on_market_update(data):
    print(f"Market Update: {data}")

@sio.on('sentiment_update')
def on_sentiment_update(data):
    print(f"Sentiment Update: {data}")

@sio.on('trading_signal')
def on_trading_signal(data):
    print(f"Trading Signal: {data}")

@sio.on('auth_error')
def on_auth_error(data):
    print(f"Authentication error: {data['error']}")
    sio.disconnect()

# Connect with authentication
def connect_authenticated(username, password):
    """Connect to WebSocket with authentication"""
    try:
        # Get access token
        access_token, refresh_token = login(username, password)
        print(f"Login successful, connecting to WebSocket...")
        
        # Connect with token
        sio.connect('http://localhost:5000', auth={'token': access_token})
        
        # Subscribe to symbols
        sio.emit('subscribe', {'symbols': ['BTC', 'ETH', 'ADA']})
        
        # Keep connection alive
        sio.wait()
        
    except Exception as e:
        print(f"Error: {e}")

# Usage
if __name__ == '__main__':
    connect_authenticated('your_username', 'your_password')
```

### Connection Flow with Authentication

```
┌─────────┐                 ┌─────────┐                 ┌──────────┐
│ Client  │                 │ Auth    │                 │ WebSocket│
│         │                 │ API     │                 │ Server   │
└────┬────┘                 └────┬────┘                 └────┬─────┘
     │                           │                           │
     │  POST /api/auth/login     │                           │
     │─────────────────────────>│                           │
     │                           │                           │
     │  {access_token, ...}      │                           │
     │<─────────────────────────│                           │
     │                           │                           │
     │  Connect with token       │                           │
     │───────────────────────────────────────────────────────>│
     │                           │                           │
     │                           │   Verify token            │
     │                           │<──────────────────────────│
     │                           │                           │
     │                           │   Token valid             │
     │                           │───────────────────────────>│
     │                           │                           │
     │  connection_status        │                           │
     │<───────────────────────────────────────────────────────│
     │                           │                           │
     │  subscribe                │                           │
     │───────────────────────────────────────────────────────>│
     │                           │                           │
     │  subscription_confirmed   │                           │
     │<───────────────────────────────────────────────────────│
     │                           │                           │
     │  market_update (stream)   │                           │
     │<───────────────────────────────────────────────────────│
     │                           │                           │
```

### Security Best Practices

1. **Always use HTTPS/WSS in production** to encrypt token transmission
2. **Store tokens securely** (HttpOnly cookies or secure storage)
3. **Implement token refresh** before expiration to maintain connection
4. **Use short-lived access tokens** (1 hour recommended)
5. **Validate tokens on every connection attempt**
6. **Log authentication failures** for security monitoring
7. **Rate limit connection attempts** to prevent brute force attacks

## Security Considerations

### CORS Configuration

Backend allows all origins in development:
```python
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*")
```

For production, restrict to specific domains:
```python
CORS(app, origins=["https://yourdomain.com"])
socketio = SocketIO(app, cors_allowed_origins=["https://yourdomain.com"])
```

### Data Validation

All incoming data should be validated before use:
- Verify symbol formats
- Check data types
- Sanitize user inputs
- Limit subscription lists

### Token Security

When implementing authentication:
- Use HTTPS/WSS in production to encrypt tokens in transit
- Never expose tokens in URLs or logs
- Implement token rotation for long-lived connections
- Clear tokens on logout
- Monitor for suspicious authentication patterns

## Troubleshooting

### Connection Issues

**Problem:** Client cannot connect to WebSocket server

**Solutions:**
1. Verify backend is running on port 5000
2. Check CORS settings allow your origin
3. Verify firewall allows WebSocket connections
4. Check browser console for specific errors
5. Ensure WebSocket URL is correct (ws:// or wss://)

**Debug Commands:**
```bash
# Check if backend is running
curl http://localhost:5000/health

# Test WebSocket connection
wscat -c ws://localhost:5000/socket.io/

# Check backend logs
tail -f backend.log
```

### Authentication Issues

**Problem:** Connection rejected with authentication error

**Symptoms:**
- `auth_error` event received
- Connection immediately closed
- "Token expired" or "Invalid token" messages

**Solutions:**

1. **Token Expired:**
   ```javascript
   socket.on('auth_error', async (data) => {
     if (data.error === 'Token expired') {
       // Refresh the token
       const newToken = await refreshAccessToken();
       socket.auth.token = newToken;
       socket.connect();
     }
   });
   ```

2. **Invalid Token:**
   - Verify token is correctly stored and retrieved
   - Check token format (should be JWT)
   - Ensure token is not corrupted
   - Verify token was issued by the correct server

3. **Missing Token:**
   ```javascript
   // Always check if token exists before connecting
   const token = localStorage.getItem('access_token');
   if (!token) {
     console.error('No access token found');
     redirectToLogin();
   } else {
     socket = io(url, { auth: { token } });
   }
   ```

4. **Token Not Being Sent:**
   - Verify auth object in connection options:
   ```javascript
   const socket = io('http://localhost:5000', {
     auth: {
       token: accessToken  // Make sure this is set
     }
   });
   ```

**Debug Steps:**
```javascript
// Log token before connecting
console.log('Connecting with token:', token ? 'present' : 'missing');
console.log('Token length:', token?.length);

// Monitor auth errors
socket.on('auth_error', (data) => {
  console.error('Auth Error:', data);
  console.log('Current token:', localStorage.getItem('access_token'));
});
```

### Data Not Updating

**Problem:** Connected but no data received

**Solutions:**
1. Check backend logs for broadcast errors
2. Verify subscription was confirmed
3. Check network tab for WebSocket frames
4. Verify event listeners are registered
5. Ensure symbols are valid cryptocurrency tickers

**Debug Code:**
```javascript
// Verify subscription
socket.emit('subscribe', { symbols: ['BTC', 'ETH'] });

socket.on('subscription_confirmed', (data) => {
  console.log('Subscription confirmed:', data.symbols);
});

// Monitor all events
socket.onAny((eventName, ...args) => {
  console.log(`Event: ${eventName}`, args);
});
```

### Performance Issues

**Problem:** Updates causing lag or high CPU

**Solutions:**
1. Reduce update frequency in backend
2. Throttle state updates in React
3. Use React.memo() for expensive components
4. Consider virtualizing large data lists
5. Debounce UI updates

**Example Throttling:**
```javascript
import { throttle } from 'lodash';

// Throttle market updates to once per second
const throttledUpdate = throttle((data) => {
  setMarketData(data);
}, 1000);

socket.on('market_update', throttledUpdate);
```

**Example Memoization:**
```javascript
const MarketDataDisplay = React.memo(({ symbol, price, change }) => {
  return (
    <div>
      {symbol}: ${price} ({change}%)
    </div>
  );
});
```

### Reconnection Issues

**Problem:** WebSocket not reconnecting after disconnection

**Solutions:**

1. **Verify Reconnection Options:**
   ```javascript
   const socket = io('http://localhost:5000', {
     reconnection: true,
     reconnectionAttempts: 5,
     reconnectionDelay: 1000,
     reconnectionDelayMax: 5000
   });
   ```

2. **Monitor Reconnection Events:**
   ```javascript
   socket.on('reconnect', (attemptNumber) => {
     console.log('Reconnected after', attemptNumber, 'attempts');
   });
   
   socket.on('reconnect_attempt', (attemptNumber) => {
     console.log('Attempting to reconnect:', attemptNumber);
   });
   
   socket.on('reconnect_error', (error) => {
     console.error('Reconnection error:', error);
   });
   
   socket.on('reconnect_failed', () => {
     console.error('Reconnection failed after all attempts');
   });
   ```

3. **Manual Reconnection with Token Refresh:**
   ```javascript
   socket.on('reconnect_failed', async () => {
     // Refresh token and try again
     const newToken = await refreshAccessToken();
     socket.auth.token = newToken;
     socket.connect();
   });
   ```

### Subscription Issues

**Problem:** Not receiving updates for specific symbols

**Solutions:**

1. **Verify Symbol Format:**
   ```javascript
   // Correct format - uppercase ticker symbols
   socket.emit('subscribe', { symbols: ['BTC', 'ETH', 'ADA'] });
   
   // Incorrect formats
   // ✗ socket.emit('subscribe', { symbols: ['bitcoin'] });
   // ✗ socket.emit('subscribe', { symbols: ['btc'] });
   ```

2. **Check Subscription Confirmation:**
   ```javascript
   socket.emit('subscribe', { symbols: ['BTC', 'ETH'] });
   
   socket.once('subscription_confirmed', (data) => {
     console.log('Confirmed subscription:', data.symbols);
     // If symbols don't match what you requested, there's an issue
   });
   ```

3. **Listen for Market Updates:**
   ```javascript
   socket.on('market_update', (data) => {
     const subscribedSymbols = Object.keys(data);
     console.log('Receiving data for:', subscribedSymbols);
   });
   ```

### CORS Errors

**Problem:** CORS policy blocking WebSocket connection

**Solutions:**

1. **Development - Allow All Origins:**
   ```python
   # backend/app.py
   from flask_cors import CORS
   CORS(app, origins="*")
   socketio = SocketIO(app, cors_allowed_origins="*")
   ```

2. **Production - Specify Origins:**
   ```python
   allowed_origins = [
     "https://yourdomain.com",
     "https://www.yourdomain.com"
   ]
   CORS(app, origins=allowed_origins)
   socketio = SocketIO(app, cors_allowed_origins=allowed_origins)
   ```

3. **Check Browser Console:**
   - Look for CORS-specific error messages
   - Verify the Origin header in request
   - Ensure server is sending correct CORS headers

### Common Error Messages

#### "WebSocket connection failed"
- **Cause:** Server not running or unreachable
- **Fix:** Start backend server, check URL and port

#### "Token expired"
- **Cause:** JWT access token has expired
- **Fix:** Implement token refresh mechanism

#### "Invalid token"
- **Cause:** Token format incorrect or token verification failed
- **Fix:** Ensure token is valid JWT from authentication API

#### "Connection timeout"
- **Cause:** Server not responding within timeout period
- **Fix:** Check server health, network connectivity

#### "Transport close"
- **Cause:** Connection unexpectedly closed
- **Fix:** Check server logs, ensure stable network connection

### Getting Help

If issues persist:

1. **Enable Debug Logging:**
   ```javascript
   // Client-side
   localStorage.debug = 'socket.io-client:socket';
   
   // Or for all socket.io logs
   localStorage.debug = '*';
   ```

2. **Check Server Logs:**
   ```bash
   # Backend logs should show connection attempts
   python app.py
   ```

3. **Use Browser DevTools:**
   - Network tab → WS/WebSocket filter
   - Console for JavaScript errors
   - Application tab → Local Storage (check tokens)

4. **Test with Simple Client:**
   ```bash
   # Install wscat
   npm install -g wscat
   
   # Test connection
   wscat -c "ws://localhost:5000/socket.io/?EIO=4&transport=websocket"
   ```

5. **Open GitHub Issue:**
   - Include error messages
   - Provide steps to reproduce
   - Share relevant code snippets
   - Mention browser and version

## Future Enhancements

Potential improvements for the WebSocket implementation:

1. **Authentication Implementation:** ✓ Documentation complete - Ready for implementation
   - Token-based authentication with JWT
   - Connection-level security
   - Token refresh mechanisms
   - See [Authentication](#authentication) section for implementation guide

2. **Rate Limiting:** Implement per-client rate limits
   - Prevent abuse of WebSocket connections
   - Throttle excessive subscription requests
   - Limit message frequency per client

3. **Compression:** Enable message compression for large payloads
   - Reduce bandwidth usage
   - Improve performance for mobile clients
   - Use WebSocket permessage-deflate extension

4. **Persistence:** Store connection state for resuming
   - Allow clients to resume after disconnection
   - Replay missed messages
   - Maintain subscription state across reconnections

5. **Analytics:** Track connection metrics and performance
   - Monitor active connections
   - Track message delivery rates
   - Measure latency and performance metrics
   - Connection duration and patterns

6. **Rooms:** Implement topic-based subscription rooms
   - Group clients by interest (e.g., specific coin pairs)
   - Reduce unnecessary message broadcasting
   - More efficient resource usage

7. **Binary Data:** Use binary protocols for maximum efficiency
   - Switch from JSON to MessagePack or Protocol Buffers
   - Reduce payload size
   - Improve parsing performance

8. **Heartbeat:** Add custom ping/pong for connection health
   - Detect dead connections faster
   - Custom health check messages
   - Proactive connection management

9. **Message Queue Integration:** Add message broker support
   - Integrate with Redis Pub/Sub or RabbitMQ
   - Enable horizontal scaling across multiple servers
   - Improve reliability and fault tolerance

10. **Selective Subscriptions:** Fine-grained subscription control
    - Subscribe to specific data fields only
    - Reduce unnecessary data transfer
    - Custom subscription filters

## API Reference

### WebSocket Events

#### Server-to-Client Events

##### `connection_status`
Emitted when connection status changes.

**Payload:**
```json
{
  "status": "connected",
  "message": "Connected to real-time data stream",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "user_id": 123  // Only present if authenticated
}
```

**Example:**
```javascript
socket.on('connection_status', (data) => {
  console.log(`Status: ${data.status} - ${data.message}`);
  if (data.user_id) {
    console.log(`Authenticated as user ${data.user_id}`);
  }
});
```

##### `market_update`
Emitted every 2 seconds with real-time market data for all symbols.

**Payload:** See [Market Data Format](#market-data-format)

**Example:**
```javascript
socket.on('market_update', (data) => {
  Object.keys(data).forEach(symbol => {
    const coin = data[symbol];
    console.log(`${symbol}: $${coin.price} (${coin.change_24h}%)`);
  });
});
```

##### `sentiment_update`
Emitted every 10 seconds with market sentiment analysis.

**Payload:** See [Sentiment Update Format](#sentiment-update-format)

**Example:**
```javascript
socket.on('sentiment_update', (data) => {
  console.log(`Market Mood: ${data.market_mood}`);
  console.log(`Fear & Greed: ${data.market_fear_greed}`);
});
```

##### `trading_signal`
Emitted every 15 seconds with trading recommendations.

**Payload:** See [Trading Signal Format](#trading-signal-format)

**Example:**
```javascript
socket.on('trading_signal', (signal) => {
  if (signal.signal === 'STRONG_BUY' && signal.strength > 0.9) {
    console.log(`High confidence ${signal.signal} for ${signal.symbol}`);
  }
});
```

##### `subscription_confirmed`
Emitted after successful subscription request.

**Payload:**
```json
{
  "symbols": ["BTC", "ETH", "ADA"],
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Example:**
```javascript
socket.on('subscription_confirmed', (data) => {
  console.log(`Subscribed to: ${data.symbols.join(', ')}`);
});
```

##### `auth_error`
Emitted when authentication fails (only if authentication is enabled).

**Payload:**
```json
{
  "error": "Token expired",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Example:**
```javascript
socket.on('auth_error', (data) => {
  console.error(`Authentication failed: ${data.error}`);
  // Attempt to refresh token or redirect to login
});
```

#### Client-to-Server Events

##### `subscribe`
Request subscription to specific cryptocurrency symbols.

**Payload:**
```json
{
  "symbols": ["BTC", "ETH", "ADA", "DOT"]
}
```

**Example:**
```javascript
socket.emit('subscribe', {
  symbols: ['BTC', 'ETH', 'ADA']
});
```

**Response:** Server emits `subscription_confirmed` event

##### `disconnect`
Client-initiated disconnection (handled automatically by socket.io).

**Example:**
```javascript
socket.disconnect();
```

### WebSocket Service Methods

#### `connect(url?: string, options?: object)`
Establishes WebSocket connection to server.

**Parameters:**
- `url` (optional): Server URL (defaults to `http://localhost:5000`)
- `options` (optional): Socket.IO connection options

**Options:**
```javascript
{
  auth: {
    token: 'your_jwt_token'  // For authenticated connections
  },
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: 5,
  transports: ['websocket', 'polling']
}
```

**Example:**
```javascript
import websocketService from '@/lib/websocket.js';

websocketService.connect('http://localhost:5000', {
  auth: { token: localStorage.getItem('access_token') },
  reconnection: true
});
```

#### `disconnect()`
Closes WebSocket connection and cleans up listeners.

**Example:**
```javascript
websocketService.disconnect();
```

#### `subscribe(symbols: string[])`
Subscribes to real-time updates for specified symbols.

**Parameters:**
- `symbols`: Array of cryptocurrency ticker symbols

**Example:**
```javascript
websocketService.subscribe(['BTC', 'ETH', 'ADA', 'DOT', 'LINK']);
```

#### `on(event: string, callback: Function): Function`
Registers event listener. Returns unsubscribe function.

**Parameters:**
- `event`: Event name to listen for
- `callback`: Function to call when event is received

**Returns:** Unsubscribe function

**Example:**
```javascript
const unsubscribe = websocketService.on('market_update', (data) => {
  console.log('Market data:', data);
});

// Later, to unsubscribe:
unsubscribe();
```

#### `off(event: string, callback: Function)`
Removes event listener.

**Parameters:**
- `event`: Event name
- `callback`: Callback function to remove

**Example:**
```javascript
const handleMarketUpdate = (data) => {
  console.log(data);
};

websocketService.on('market_update', handleMarketUpdate);
// Later...
websocketService.off('market_update', handleMarketUpdate);
```

#### `isConnected(): boolean`
Returns current connection status.

**Returns:** `true` if connected, `false` otherwise

**Example:**
```javascript
if (websocketService.isConnected()) {
  console.log('WebSocket is connected');
} else {
  console.log('WebSocket is disconnected');
}
```

### React Hook: useWebSocket

A custom React hook for easy WebSocket integration in React components.

#### Usage

```javascript
import { useWebSocket } from '@/hooks/useWebSocket.js';

function MyComponent() {
  const {
    isConnected,
    connectionStatus,
    marketData,
    sentimentData,
    tradingSignals,
    lastUpdate,
    connect,
    disconnect,
    subscribe
  } = useWebSocket(options);
  
  // Your component logic
}
```

#### Options

```javascript
{
  autoConnect: true,        // Automatically connect on mount
  symbols: ['BTC', 'ETH'],  // Initial symbols to subscribe to
  token: 'jwt_token'        // Authentication token (optional)
}
```

### Hook Return Values

#### `isConnected: boolean`
True when WebSocket is connected.

**Example:**
```javascript
<div className={isConnected ? 'status-online' : 'status-offline'}>
  {isConnected ? 'Live' : 'Offline'}
</div>
```

#### `connectionStatus: string`
Current connection status: `'connected'`, `'disconnected'`, or `'error'`.

**Example:**
```javascript
if (connectionStatus === 'error') {
  showErrorNotification('Connection failed. Retrying...');
}
```

#### `marketData: Object`
Latest market data for all symbols. Updates automatically with `market_update` events.

**Example:**
```javascript
const btcPrice = marketData.BTC?.price;
const ethPrice = marketData.ETH?.price;
```

#### `sentimentData: Object`
Latest sentiment analysis data. Updates automatically with `sentiment_update` events.

**Example:**
```javascript
const fearGreed = sentimentData?.market_fear_greed;
const mood = sentimentData?.market_mood;
```

#### `tradingSignals: Array`
Array of recent trading signals (max 10, newest first).

**Example:**
```javascript
{tradingSignals.map(signal => (
  <div key={signal.timestamp}>
    {signal.signal} {signal.symbol} - {signal.reason}
  </div>
))}
```

#### `lastUpdate: string`
ISO timestamp of last data update.

**Example:**
```javascript
<p>Last updated: {new Date(lastUpdate).toLocaleTimeString()}</p>
```

#### `connect(): void`
Manually connect to WebSocket.

**Example:**
```javascript
<button onClick={connect}>Connect</button>
```

#### `disconnect(): void`
Manually disconnect from WebSocket.

**Example:**
```javascript
<button onClick={disconnect}>Disconnect</button>
```

#### `subscribe(symbols: string[]): void`
Subscribe to additional symbols.

**Example:**
```javascript
<button onClick={() => subscribe(['SOL', 'AVAX'])}>
  Add SOL & AVAX
</button>
```

## License

This WebSocket implementation is part of the CRS project under MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review browser console logs
3. Check backend server logs
4. Open an issue on GitHub
