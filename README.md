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

### Phase 3: Enhancement 🚧 IN PROGRESS
- [x] AI/ML enhancement strategy documented
- [x] DeFi integration framework designed
- [x] Security implementation guide complete
- [x] KYC/AML compliance framework documented
- [ ] Deploy advanced AI models (LSTM, Transformers)
- [ ] Implement DeFi integrations (DEX, yield farming, staking)
- [ ] Add social trading features
- [ ] Portfolio rebalancing automation

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

# Run development server
python src/main.py
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

### Upgrade & Architecture
- **[Comprehensive Upgrade Roadmap](docs/COMPREHENSIVE_UPGRADE_ROADMAP.md)** (13KB) - Complete upgrade plan across 8 areas
- **[Implementation Summary](docs/IMPLEMENTATION_COMPLETE.md)** (26KB) - Detailed implementation summary
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
- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference
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

## Contributing

1. Follow existing code structure and conventions
2. Ensure security best practices for crypto operations
3. Maintain compatibility between AI and shop components
4. Update documentation for any new features

## License

MIT License - See LICENSE file for details

---

*A revolutionary cryptocurrency marketplace powered by AI technology*