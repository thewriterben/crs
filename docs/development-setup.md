# Development Setup Guide

## Prerequisites

Before setting up the CRS (Cryptocurrency Marketplace) development environment, ensure you have the following installed:

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **Git**
- **A modern web browser**

## Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/thewriterben/crs.git
cd crs
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`

### 3. Backend Setup (New Terminal)
```bash
cd backend
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
python main.py
```
The backend API will be available at `http://localhost:5000`

## Detailed Setup Instructions

### Frontend Development

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Available Scripts
- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint for code quality

#### Environment Configuration
Create a `.env` file in the frontend directory:
```env
VITE_API_BASE_URL=http://localhost:5000
VITE_APP_TITLE=Cryptocurrency Marketplace
VITE_ENABLE_AI_FEATURES=true
```

### Backend Development

#### Virtual Environment Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the backend directory:
```env
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000
DATABASE_URL=sqlite:///marketplace.db
SECRET_KEY=your-secret-key-here
AI_MODELS_PATH=./ai/models/
```

#### Running the Backend
```bash
# Development mode with auto-reload
python main.py

# Or using Flask CLI
flask run --debug

# Or using Gunicorn for production-like testing
gunicorn -c gunicorn.conf.py app:app
```

## Project Structure Deep Dive

### Frontend Structure
```
frontend/
├── public/                  # Static assets
│   ├── favicon.ico
│   └── assets/
├── src/
│   ├── components/
│   │   ├── ai/             # AI marketplace components
│   │   │   ├── AIDashboard.jsx
│   │   │   ├── AIDashboard.css
│   │   │   ├── NewCapabilitiesDashboard.jsx
│   │   │   └── NewCapabilitiesDashboard.css
│   │   ├── shop/           # E-commerce components (to be created)
│   │   └── ui/             # Base UI components (Radix UI)
│   │       ├── button.jsx
│   │       ├── card.jsx
│   │       ├── dialog.jsx
│   │       └── ... (50+ components)
│   ├── pages/              # Application pages (to be created)
│   ├── hooks/              # Custom React hooks
│   │   └── use-mobile.js
│   ├── lib/                # Utility functions
│   │   └── utils.js
│   ├── App.jsx             # Main application component
│   ├── main.jsx            # React entry point
│   └── index.css           # Global styles
├── components.json         # Shadcn/ui configuration
├── jsconfig.json           # JavaScript configuration
├── eslint.config.js        # ESLint rules
├── vite.config.js          # Vite configuration
└── package.json            # Dependencies and scripts
```

### Backend Structure
```
backend/
├── ai/                     # AI and ML modules
│   ├── ai_prediction_engine.py    # ML prediction models
│   ├── portfolio_optimizer.py     # Portfolio optimization
│   ├── sentiment_analysis_system.py # News sentiment analysis
│   └── ai_news_analyzer.py        # AI news processing
├── trading/                # Trading engine components
│   ├── trading_bot_system.py      # Automated trading bots
│   ├── advanced_trading_engine.py # Trading operations
│   └── advanced_charting.py       # Technical analysis
├── api/                    # API endpoints
│   ├── unified_api_server.py      # Main API server
│   ├── ai_api_server.py           # AI-specific endpoints
│   └── simple_ai_api.py           # Simplified API
├── src/
│   └── main.py             # Primary Flask application
├── app.py                  # Alternative Flask entry point
├── requirements.txt        # Python dependencies
└── gunicorn.conf.py        # Production server configuration
```

## Development Workflow

### 1. Feature Development
1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make changes in the appropriate component directories
3. Test locally with both frontend and backend running
4. Commit changes: `git commit -m "Add your feature"`
5. Push and create a pull request

### 2. Component Development
#### Adding New UI Components
```bash
cd frontend
# Add new Radix UI component (if needed)
npm install @radix-ui/react-your-component

# Create component in appropriate directory
touch src/components/ui/your-component.jsx
```

#### Adding New AI Features
```bash
cd backend
# Create new AI module
touch ai/your_ai_module.py

# Add API endpoint
# Edit api/unified_api_server.py to include new routes
```

### 3. Testing

#### Frontend Testing
```bash
cd frontend
npm run lint          # Check code quality
npm run build         # Test production build
npm run preview       # Test production build locally
```

#### Backend Testing
```bash
cd backend
python -m pytest tests/              # Run unit tests (when added)
python -c "import app; print('OK')"  # Quick import test
```

## Environment Variables Reference

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:5000      # Backend API URL
VITE_APP_TITLE=Cryptocurrency Marketplace    # Application title
VITE_ENABLE_AI_FEATURES=true                 # Enable AI components
VITE_ENABLE_SHOP_FEATURES=true               # Enable shop components
VITE_DEBUG=true                              # Enable debug mode
```

### Backend (.env)
```env
FLASK_ENV=development           # Flask environment
FLASK_DEBUG=True               # Enable debug mode
API_PORT=5000                  # API server port
DATABASE_URL=sqlite:///marketplace.db  # Database connection
SECRET_KEY=your-secret-key-here         # Flask secret key
AI_MODELS_PATH=./ai/models/             # AI models directory
CORS_ORIGINS=http://localhost:5173      # Allowed CORS origins
```

## Troubleshooting

### Common Issues

#### Frontend
1. **Port 5173 already in use**
   ```bash
   # Kill process using the port
   lsof -ti:5173 | xargs kill -9
   # Or use a different port
   npm run dev -- --port 3000
   ```

2. **Node modules issues**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Tailwind styles not loading**
   - Check if Tailwind CSS is properly configured in `vite.config.js`
   - Ensure `@tailwind` directives are in `src/index.css`

#### Backend
1. **Port 5000 already in use**
   ```bash
   # Find and kill process
   lsof -ti:5000 | xargs kill -9
   # Or change port in main.py
   ```

2. **Python import errors**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **CORS errors**
   - Check CORS configuration in Flask app
   - Ensure frontend origin is allowed in backend

### Performance Tips

1. **Frontend Optimization**
   - Use React.lazy() for code splitting
   - Optimize images and assets
   - Enable Vite's build optimizations

2. **Backend Optimization**
   - Use caching for AI model predictions
   - Implement API response caching
   - Consider using Redis for session storage

## IDE Setup

### VS Code Recommended Extensions
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- Python
- Pylance
- GitLens
- Thunder Client (for API testing)

### VS Code Settings
Create `.vscode/settings.json`:
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "tailwindCSS.includeLanguages": {
    "javascript": "javascript",
    "html": "HTML"
  }
}
```

## Next Steps

1. **Set up the development environment** following this guide
2. **Review the integration architecture** document
3. **Start with frontend component integration**
4. **Test AI features** with the backend APIs
5. **Begin implementing new shop features**

For more detailed information, see:
- [Integration Architecture](./integration-architecture.md)
- [API Documentation](./ai_features_summary.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)