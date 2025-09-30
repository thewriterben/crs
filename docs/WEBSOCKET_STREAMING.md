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

```json
{
  "BTC": {
    "symbol": "BTC",
    "price": 45234.56,
    "change_24h": 2.45,
    "volume_24h": 28500000.00,
    "timestamp": "2024-01-15T10:30:00.000Z"
  },
  "ETH": { ... }
}
```

#### Sentiment Update Format

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

#### Trading Signal Format

```json
{
  "symbol": "BTC",
  "signal": "BUY",
  "strength": 0.85,
  "reason": "Strong momentum detected",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
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

## Troubleshooting

### Connection Issues

**Problem:** Client cannot connect to WebSocket server

**Solutions:**
1. Verify backend is running on port 5000
2. Check CORS settings allow your origin
3. Verify firewall allows WebSocket connections
4. Check browser console for specific errors

### Data Not Updating

**Problem:** Connected but no data received

**Solutions:**
1. Check backend logs for broadcast errors
2. Verify subscription was confirmed
3. Check network tab for WebSocket frames
4. Verify event listeners are registered

### Performance Issues

**Problem:** Updates causing lag or high CPU

**Solutions:**
1. Reduce update frequency in backend
2. Throttle state updates in React
3. Use React.memo() for expensive components
4. Consider virtualizing large data lists

## Future Enhancements

Potential improvements for the WebSocket implementation:

1. **Authentication:** Add token-based authentication for WebSocket connections
2. **Rate Limiting:** Implement per-client rate limits
3. **Compression:** Enable message compression for large payloads
4. **Persistence:** Store connection state for resuming
5. **Analytics:** Track connection metrics and performance
6. **Rooms:** Implement topic-based subscription rooms
7. **Binary Data:** Use binary protocols for maximum efficiency
8. **Heartbeat:** Add custom ping/pong for connection health

## API Reference

### WebSocket Service Methods

#### `connect()`
Establishes WebSocket connection to server.

#### `disconnect()`
Closes WebSocket connection and cleans up listeners.

#### `subscribe(symbols: string[])`
Subscribes to real-time updates for specified symbols.

#### `on(event: string, callback: Function): Function`
Registers event listener. Returns unsubscribe function.

#### `off(event: string, callback: Function)`
Removes event listener.

#### `isConnected(): boolean`
Returns current connection status.

### Hook Return Values

#### `isConnected: boolean`
True when WebSocket is connected.

#### `connectionStatus: string`
Current connection status ('connected', 'disconnected', 'error').

#### `marketData: Object`
Latest market data for all symbols.

#### `sentimentData: Object`
Latest sentiment analysis data.

#### `tradingSignals: Array`
Array of recent trading signals (max 10).

#### `lastUpdate: string`
ISO timestamp of last data update.

#### `connect(): void`
Manually connect to WebSocket.

#### `disconnect(): void`
Manually disconnect from WebSocket.

#### `subscribe(symbols: string[]): void`
Subscribe to additional symbols.

## License

This WebSocket implementation is part of the CRS project under MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review browser console logs
3. Check backend server logs
4. Open an issue on GitHub
