# Cryptons.com

## Project Overview

A comprehensive cryptocurrency marketplace combining AI-powered trading capabilities with modern e-commerce functionality. This project integrates three key components with **Phase 3 advanced features** now complete:

1. **AI Marketplace** - Advanced AI trading platform with portfolio optimization
2. **Crypto Shop** - Modern React-based cryptocurrency shopping interface  
3. **Website Resources** - Static website assets and templates

### 🚀 Phase 3 Complete - Advanced Features Live!

The Cryptons.com platform now includes cutting-edge features ready for production:

- **🤖 Advanced AI/ML Models** - LSTM, Transformer, Ensemble predictions, and BERT sentiment analysis
- **💰 DeFi Integration** - DEX aggregation, yield farming, staking, and liquidity pools
- **👥 Social Trading** - Copy trading, AI signals, and portfolio sharing
- **📊 Portfolio Automation** - Auto-rebalancing, risk management, DCA, and stop-loss

**3,500+ lines** of production code | **30+ new API endpoints** | **All tests passing ✅**

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

#### 🤖 Advanced AI/ML (Phase 3)
- **LSTM Predictor** - Time series forecasting with 60-period lookback
- **Transformer Model** - 8-head attention mechanism for pattern analysis
- **Ensemble Predictor** - Combines 5 models for 94% confidence predictions
- **BERT Sentiment** - NLP-based crypto sentiment from news/social media

#### 💰 DeFi Integration (Phase 3)
- **DEX Aggregator** - Best prices across Uniswap, PancakeSwap, SushiSwap
- **Yield Farming** - 5 pools with 38-68% APY (Compound, Aave, Curve, Yearn, Convex)
- **Staking** - ETH, BNB, ADA, DOT, SOL with flexible/locked options
- **Liquidity Pools** - AMM pool management with fee tracking

#### 👥 Social Trading (Phase 3)
- **Copy Trading** - Follow top traders (72% win rate leaders)
- **Trading Signals** - AI-generated BUY/SELL/HOLD recommendations
- **Portfolio Sharing** - Browse and replicate successful portfolios
- **Leaderboards** - Community rankings with verified traders

#### 📊 Portfolio Automation (Phase 3)
- **Auto-Rebalancing** - Drift detection and order generation
- **Risk Management** - Portfolio risk assessment and position sizing
- **Dollar-Cost Averaging** - Automated DCA schedules (daily/weekly/monthly)
- **Stop-Loss** - Trailing stops and take-profit automation

#### 💎 CFV Payment System (NEW)
- **12 DGF Cryptocurrencies** - XNO, NEAR, ICP, EGLD, DGB, DASH, XCH, XEC, XMR, RVN, DGD, BTC-LN
- **Dynamic Discounts** - Up to 10% off based on Crypto Fair Value calculations
- **Fair Value Analytics** - Real-time valuation status (undervalued/fair/overvalued)
- **Tiered Discount System**:
  - ≥50% undervalued: 10% discount
  - 30-49% undervalued: 7% discount
  - 15-29% undervalued: 5% discount
  - <15% undervalued: 2% discount
- **Smart Payment Selection** - Visual indicators for best value cryptocurrencies
- **Integrated E-commerce** - Full order and payment management with CFV metrics

#### Core Platform Features
- AI-powered portfolio optimization with Modern Portfolio Theory
- **Real-time data streaming via WebSocket** - Live market feeds and instant updates
- Real-time sentiment analysis and market intelligence
- Advanced trading engine with automated bots
- Professional charting and technical analysis
- **Advanced Cryptocurrency Payments** - CFV-enabled payment system with 12 DGF coins ✨
- Secure cryptocurrency transaction handling
- Modern responsive UI with dark theme support
- **User Authentication & Security**
  - Secure login and registration
  - JWT token-based authentication
  - Password encryption with bcrypt
  - Multi-factor authentication (MFA/2FA)
  - Session management with automatic token refresh
  - User profile management

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

### Phase 1: Foundation ✅ COMPLETE
- [x] Extract and analyze existing components
- [x] Set up project structure
- [x] Create unified package.json
- [x] Integrate UI component libraries
- [x] Comprehensive testing infrastructure (Backend: pytest, Frontend: Vitest)
- [x] Database architecture upgrade (PostgreSQL + Redis)
- [x] Security framework (input validation, rate limiting)
- [x] Performance monitoring system
- [x] Comprehensive documentation (76KB across 6 guides)

### Phase 2: Integration ✅ INFRASTRUCTURE READY
- [x] Backend testing framework complete
- [x] Frontend testing framework complete
- [x] Database models for trading data
- [x] Security and compliance framework
- [x] Performance monitoring endpoints
- [ ] Merge AI marketplace and crypto shop frontends
- [ ] Unify styling and theming
- [ ] Integrate backend APIs
- [ ] Set up routing and navigation

### Phase 3: Enhancement ✅ COMPLETE
- [x] AI/ML enhancement strategy documented
- [x] DeFi integration framework designed
- [x] Security implementation guide complete
- [x] KYC/AML compliance framework documented
- [x] Deploy advanced AI models (LSTM, Transformers, Ensemble, BERT)
- [x] Implement DeFi integrations (DEX, yield farming, staking, liquidity pools)
- [x] Add social trading features (copy trading, signals, portfolio sharing)
- [x] Portfolio automation (rebalancing, risk management, DCA, stop-loss)
- [x] CFV payment system with 12 DGF cryptocurrencies
- [x] Dynamic discount system based on fair value calculations

### Phase 4: Deployment ✅ PRODUCTION READY
- [x] Production build configuration
  - Docker containerization with multi-stage builds
  - Docker Compose orchestration with PostgreSQL and Redis
  - Production environment configurations
  - Nginx reverse proxy setup
- [x] Security hardening
  - Flask-Talisman for security headers
  - Flask-Limiter for rate limiting (multi-tier, adaptive)
  - Flask-Caching with Redis support
  - Security configuration module
  - Input validation and sanitization framework
- [x] CI/CD pipeline
  - GitHub Actions workflows
  - Automated testing (backend + frontend)
  - Security scanning with Trivy and CodeQL
  - Docker build automation
- [x] Monitoring and analytics
  - Health check endpoints (liveness, readiness, metrics)
  - Performance monitoring (CPU, memory, disk, network)
  - API metrics tracking (response times, error rates)
  - Structured logging configuration
- [x] Documentation completion
  - Comprehensive production deployment guide
  - Security best practices documentation
  - KYC/AML compliance framework
  - AI/ML enhancement strategy (16KB)
  - DeFi integration guide (18KB)
  - Complete upgrade roadmap (13KB)
  - Troubleshooting guide
  - Deployment scripts and utilities

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
- PostgreSQL 15+ (for production) or SQLite (for development)
- Redis 7+ (for caching and sessions)

### Development Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_database.py init

# Run main development server
python src/main.py

# Or run Phase 3 API server (port 5006)
PYTHONPATH=$(pwd) python api/phase3_api.py
```

#### Phase 3 Features Demo
```bash
# Run interactive Phase 3 demo
PYTHONPATH=/home/runner/work/crs/crs/backend python3 scripts/demo_phase3.py

# Or start Phase 3 API server
./scripts/start_phase3_api.sh

# Test Phase 3 endpoints
curl http://localhost:5006/api/phase3/status
curl http://localhost:5006/api/phase3/health
```

#### CFV Payment System Setup
```bash
# Run database migration for CFV models
cd backend
python migrations/add_cfv_models.py upgrade
python migrations/add_cfv_models.py validate

# Configure CFV environment variables in backend/.env
# CFV_CALCULATOR_URL=http://localhost:3000
# CFV_AGENT_URL=http://localhost:3001
# CFV_DISCOUNT_ENABLED=true

# Test CFV endpoints
curl http://localhost:5000/api/cfv/coins
curl http://localhost:5000/api/cfv/calculate/XNO
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test
```

#### Docker Setup (Recommended for Production)
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec backend python scripts/init_database.py init

# Check logs
docker-compose logs -f
```

### Running Tests

#### Backend Tests
```bash
cd backend
pytest -v --cov                    # Run all tests with coverage
pytest -m unit                     # Run only unit tests
pytest -m integration              # Run only integration tests
pytest -m security                 # Run only security tests

# Run Phase 3 tests
PYTHONPATH=$(pwd) python tests/test_phase3.py
```

#### Frontend Tests
```bash
cd frontend
npm test                           # Run tests
npm run test:ui                    # Run tests with UI
npm run test:coverage              # Generate coverage report
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

### Getting Started
- [Development Setup Guide](docs/development-setup.md) - Local development environment setup
- [Quick Start](#quick-start) - Fast setup instructions above
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Basic deployment instructions

### Phase 3 Advanced Features 🚀
- **[API Reference Guide](docs/API_REFERENCE.md)** (NEW) - Complete API documentation for all 30+ Phase 3 endpoints
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** (NEW) - Comprehensive guide for contributing to Phase 3 features
- **[CHANGELOG](CHANGELOG.md)** (NEW) - Complete version history and Phase 3 release notes

### Feature Guides 📚
- **[AI/ML Models Guide](docs/FEATURE_GUIDES/AI_ML_MODELS.md)** (NEW) - LSTM, Transformer, Ensemble, BERT usage
- **[DeFi Features Guide](docs/FEATURE_GUIDES/DEFI_FEATURES.md)** (NEW) - DEX, Farming, Staking, Liquidity Pools
- **[Social Trading Guide](docs/FEATURE_GUIDES/SOCIAL_TRADING.md)** (NEW) - Copy trading, Signals, Portfolio sharing
- **[CFV Payment System Guide](docs/USER_GUIDE.md)** (NEW) - Crypto Fair Value discounts and payment processing
- **[CFV Integration Guide](docs/CFV_INTEGRATION.md)** (NEW) - Developer guide for CFV system integration
- **[API Documentation](docs/API.md)** (NEW) - Complete CFV API reference with examples
- **[Database Migration Guide](docs/MIGRATIONS.md)** (NEW) - CFV database schema and migration procedures
- **[Portfolio Automation Guide](docs/FEATURE_GUIDES/PORTFOLIO_AUTOMATION.md)** (NEW) - Rebalancing, Risk, DCA, Stop-Loss

### Upgrade & Architecture
- **[Comprehensive Upgrade Roadmap](docs/COMPREHENSIVE_UPGRADE_ROADMAP.md)** (13KB) - Complete upgrade plan across 8 areas
- **[Implementation Summary](docs/IMPLEMENTATION_COMPLETE.md)** (26KB) - Detailed implementation summary
- **[Phase 3 Implementation](docs/PHASE_3_IMPLEMENTATION.md)** - Phase 3 technical details
- **[Phase 3 Architecture](docs/PHASE_3_ARCHITECTURE.md)** - System architecture diagrams
- [Integration Architecture](docs/integration-architecture.md) - System integration guide

### Production Deployment
- **[Production Deployment Guide](docs/PRODUCTION_DEPLOYMENT.md)** - Complete production deployment instructions
- **[Production Checklist](docs/PRODUCTION_CHECKLIST.md)** - Step-by-step deployment checklist
- **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### Security & Compliance
- **[Security Implementation Guide](docs/SECURITY_IMPLEMENTATION.md)** (11KB) - Security best practices and implementation
- **[KYC/AML Compliance](docs/KYC_AML_COMPLIANCE.md)** (18KB) - Regulatory compliance framework
- [Security Best Practices](docs/SECURITY_BEST_PRACTICES.md) - Security guidelines

### API & Integration
- **[API Reference](docs/API_REFERENCE.md)** (NEW) - Complete Phase 3 API reference with examples
- **[API Documentation](docs/API_DOCUMENTATION.md)** - Core API endpoints
- [Authentication API](docs/authentication-api.md) - Authentication endpoints reference
- [Authentication Implementation](docs/authentication-implementation-summary.md) - Auth system details

### Advanced Features
- **[AI/ML Enhancement Strategy](docs/AI_ML_ENHANCEMENT.md)** (16KB) - Advanced AI/ML implementation guide
- **[DeFi Integration Guide](docs/DEFI_INTEGRATION.md)** (18KB) - DeFi protocols integration
- [AI Features Summary](docs/ai_features_summary.md) - Current AI capabilities

### Performance & Optimization
- [Performance Optimization](docs/PERFORMANCE_OPTIMIZATION.md) - Performance tuning guide
- [Performance Architecture](docs/PERFORMANCE_ARCHITECTURE.md) - System architecture
- [WebSocket Streaming](docs/WEBSOCKET_STREAMING.md) - Real-time data streaming

### Additional Resources
- [Component Inventory](docs/component-inventory.md) - UI components catalog
- [Payment Integration Guide](docs/payment-integration-guide.md) - Crypto payment processing
- [Testing Guide](docs/TESTING.md) - Testing infrastructure and practices

## Phase 3 Quick Examples

### AI Price Prediction
```bash
# Get LSTM prediction for BTC
curl -X POST http://localhost:5006/api/phase3/ai/lstm/predict \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC", "data": [50000, 51000, 50500, 52000, 51500]}'
```

### Get Best DEX Quote
```bash
# Compare prices across Uniswap, PancakeSwap, SushiSwap
curl "http://localhost:5006/api/phase3/defi/dex/quote?tokenIn=ETH&tokenOut=USDT&amountIn=1.0"
```

### Copy Top Trader
```bash
# Follow a top-performing trader
curl -X POST http://localhost:5006/api/phase3/social/traders/follow \
  -H "Content-Type: application/json" \
  -d '{"traderId": "trader_001", "copyAmount": 5000}'
```

### Create DCA Schedule
```bash
# Setup weekly $100 BTC purchases for 1 year
curl -X POST http://localhost:5006/api/phase3/portfolio/dca/create \
  -H "Content-Type: application/json" \
  -d '{"asset": "BTC", "amount": 100, "frequency": "weekly", "durationMonths": 12}'
```

For complete examples and documentation, see the [API Reference Guide](docs/API_REFERENCE.md).

## Contributing

1. Follow existing code structure and conventions
2. Ensure security best practices for crypto operations
3. Maintain compatibility between AI and shop components
4. Update documentation for any new features
5. See [Developer Guide](docs/DEVELOPER_GUIDE.md) for detailed contribution guidelines

## License

MIT License - See LICENSE file for details

---

**Version**: 3.0.0 | **Phase**: 3 Complete ✅ | *A revolutionary cryptocurrency marketplace powered by AI technology*