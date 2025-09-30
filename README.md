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
- Real-time sentiment analysis and market intelligence
- Advanced trading engine with automated bots
- Professional charting and technical analysis
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
- [ ] Add cryptocurrency payment processing
- [x] Implement user authentication
- [ ] Add real-time data streaming
- [ ] Performance optimization

### Phase 4: Deployment
- [ ] Production build configuration
- [ ] Security hardening
- [ ] Monitoring and analytics
- [ ] Documentation completion

## Quick Start

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

# Set environment variables (optional)
export SECRET_KEY='your-secret-key'
export JWT_SECRET_KEY='your-jwt-secret-key'

# Run the backend server
cd src
python main.py
```

### Authentication Setup

The application includes a complete user authentication system with the following features:

#### Backend Configuration

1. **Environment Variables**: Set these in your environment or `.env` file:
   ```bash
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   DATABASE_URL=sqlite:///marketplace.db  # Default SQLite database
   ```

2. **Database**: The authentication system uses SQLAlchemy with SQLite by default. The database is automatically created on first run.

#### Authentication Features

- **Registration**: New users can register with username, email, and password
- **Login**: Secure login with JWT token generation
- **Password Security**: Passwords are hashed using bcrypt
- **JWT Tokens**: Access tokens (1 hour) and refresh tokens (30 days)
- **Token Refresh**: Automatic token refresh to maintain sessions
- **MFA Support**: Optional multi-factor authentication using TOTP
- **Profile Management**: Users can update email and change passwords
- **Session Management**: Automatic logout on token expiration

#### API Endpoints

Authentication endpoints are available at:

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get tokens
- `POST /api/auth/logout` - Logout and revoke tokens
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/verify` - Verify token validity
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile
- `POST /api/auth/change-password` - Change password
- `POST /api/auth/mfa/enable` - Enable MFA
- `POST /api/auth/mfa/disable` - Disable MFA

#### Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

#### Frontend Integration

The frontend includes:
- `AuthContext` for global authentication state
- Login and Registration components
- User Profile component with password change and MFA management
- Automatic token refresh
- Protected routes requiring authentication

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