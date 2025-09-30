# Cryptocurrency Marketplace (CRS)

## Project Overview

A comprehensive cryptocurrency marketplace combining AI-powered trading capabilities with modern e-commerce functionality. This project integrates three key components:

1. **AI Marketplace** - Advanced AI trading platform with portfolio optimization
2. **Crypto Shop** - Modern React-based cryptocurrency shopping interface  
3. **Website Resources** - Static website assets and templates

## Architecture

### Frontend
- **Framework**: React 18+ with Vite
- **UI Library**: Tailwind CSS + Radix UI components
- **State Management**: React hooks and context
- **Routing**: React Router DOM
- **Charts**: Recharts for data visualization

### Backend
- **Framework**: Flask 3.1.1 (Python)
- **AI/ML**: scikit-learn, pandas, numpy
- **Features**: Portfolio optimization, sentiment analysis, trading bots
- **API**: RESTful with CORS support

### Key Features
- AI-powered portfolio optimization with Modern Portfolio Theory
- **Real-time data streaming via WebSocket** - Live market feeds and instant updates
- Real-time sentiment analysis and market intelligence
- Advanced trading engine with automated bots
- Professional charting and technical analysis
- **Cryptocurrency payment processing (BTC, ETH, USDT, BNB)** ✨
- Secure cryptocurrency transaction handling
- Modern responsive UI with dark theme support

## Project Structure

```
crs/
├── frontend/                 # Main React application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   │   ├── ai/          # AI marketplace components
│   │   │   ├── shop/        # Crypto shop components
│   │   │   └── ui/          # Base UI components
│   │   ├── pages/           # Application pages
│   │   ├── hooks/           # Custom React hooks
│   │   └── lib/             # Utility functions
│   └── package.json
├── backend/                  # Flask API server
│   ├── ai/                  # AI and ML modules
│   ├── trading/             # Trading engine components
│   ├── api/                 # API endpoints
│   └── requirements.txt
├── static-assets/           # Static website resources
├── docs/                    # Documentation
└── deployment/             # Deployment configurations
```

## Development Roadmap

### Phase 1: Foundation ✓
- [x] Extract and analyze existing components
- [x] Set up project structure
- [ ] Create unified package.json
- [ ] Integrate UI component libraries

### Phase 2: Integration
- [ ] Merge AI marketplace and crypto shop frontends
- [ ] Unify styling and theming
- [ ] Integrate backend APIs
- [ ] Set up routing and navigation

### Phase 3: Enhancement
- [ ] Implement user authentication

### Phase 4: Deployment
- [ ] Production build configuration
- [ ] Security hardening
- [ ] Monitoring and analytics
- [ ] Documentation completion

## Performance Features

This platform includes comprehensive performance optimizations:

- **Backend Caching**: Flask-Caching with Redis support for API responses
- **Response Compression**: Automatic gzip compression reduces bandwidth by 70-80%
- **Rate Limiting**: Prevents API abuse with configurable limits
- **Code Splitting**: React lazy loading reduces initial bundle size by ~40%
- **Memoization**: Optimized React components with useCallback and useMemo
- **Service Worker**: Asset caching for faster subsequent loads
- **Build Optimization**: Terser minification, chunk splitting, and tree shaking

See [PERFORMANCE_OPTIMIZATION.md](docs/PERFORMANCE_OPTIMIZATION.md) for detailed information.

## Quick Start

### Prerequisites
- Node.js >= 18.0.0
- Python >= 3.8.0
- npm >= 8.0.0

### Development Setup
```bash
# Install frontend dependencies
cd frontend
npm install
npm run dev

# Setup backend (in separate terminal)
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The application will start with:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- WebSocket: ws://localhost:5000/socket.io

### WebSocket Features
The application includes real-time data streaming:
- Live market price updates (every 2 seconds)
- Sentiment analysis updates (every 10 seconds)
- Trading signals (every 15 seconds)
- Connection status indicators

See [WebSocket Documentation](docs/WEBSOCKET_STREAMING.md) for detailed information.

### Build for Production
```bash
# Frontend
npm run build

# Backend
python -m gunicorn app:app
```

## Contributing

1. Follow existing code structure and conventions
2. Ensure security best practices for crypto operations
3. Maintain compatibility between AI and shop components
4. Update documentation for any new features

## License

MIT License - See LICENSE file for details

---

*A revolutionary cryptocurrency marketplace powered by AI technology*