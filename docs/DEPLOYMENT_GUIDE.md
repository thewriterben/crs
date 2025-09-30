# 🚀 Advanced AI Marketplace - Deployment Guide

## 📋 **Prerequisites**

### **System Requirements**
- Python 3.11+
- Node.js 18+
- npm or yarn
- Git (optional)

### **Development Environment**
- Ubuntu 22.04 (recommended)
- 4GB+ RAM
- 10GB+ storage

---

## 🔧 **Backend Deployment**

### **Step 1: Environment Setup**
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### **Step 2: Local Testing**
```bash
# Test the simple API server
python simple_ai_api.py

# Test the main Flask app
python src/main.py

# Verify API response
curl http://localhost:5000/api/ai/dashboard-data
```

### **Step 3: Production Deployment**

#### **Option A: Manus Platform (Recommended)**
```bash
# Ensure proper structure
mkdir -p src
cp main.py src/

# Deploy using Manus service
# (Requires Manus deployment tools)
```

#### **Option B: Manual Server Deployment**
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app

# Or with specific configuration
gunicorn --config gunicorn.conf.py src.main:app
```

#### **Option C: Docker Deployment**
```dockerfile
# Create Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.main:app"]
```

---

## 🎨 **Frontend Deployment**

### **Step 1: Setup React Environment**
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Or create new React app if needed
npx create-react-app ai-marketplace
cd ai-marketplace
```

### **Step 2: Configure API Endpoints**
```javascript
// Update API URLs in components
// NewCapabilitiesDashboard.jsx
const API_BASE_URL = 'https://your-backend-url.com';

// Update fetch calls
fetch(`${API_BASE_URL}/api/ai/dashboard-data`)
```

### **Step 3: Build for Production**
```bash
# Build the application
npm run build

# Test locally
npm run preview
```

### **Step 4: Deploy Frontend**

#### **Option A: Manus Platform**
```bash
# Deploy built files
# (Requires Manus deployment tools)
```

#### **Option B: Static Hosting**
```bash
# Deploy dist/ folder to:
# - Netlify
# - Vercel
# - AWS S3 + CloudFront
# - GitHub Pages
```

#### **Option C: Nginx Server**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

---

## 🔗 **Integration Setup**

### **CORS Configuration**
Ensure backend allows frontend domain:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://your-frontend-domain.com"])
```

### **Environment Variables**
```bash
# Backend .env
FLASK_ENV=production
API_KEY=your-api-key
DATABASE_URL=your-database-url

# Frontend .env
REACT_APP_API_URL=https://your-backend-url.com
REACT_APP_ENV=production
```

---

## 🧪 **Testing Deployment**

### **Backend API Tests**
```bash
# Health check
curl https://your-backend-url.com/

# AI dashboard data
curl https://your-backend-url.com/api/ai/dashboard-data

# Status endpoint
curl https://your-backend-url.com/api/ai/status
```

### **Frontend Tests**
```bash
# Check main page
curl https://your-frontend-url.com

# Verify routing
curl https://your-frontend-url.com/new-capabilities
```

### **Integration Tests**
1. Open frontend in browser
2. Navigate to AI Dashboard
3. Verify data loads from backend API
4. Test all dashboard tabs
5. Confirm real-time updates

---

## 🔧 **Configuration Files**

### **Backend: gunicorn.conf.py**
```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
```

### **Frontend: package.json**
```json
{
  "name": "ai-marketplace",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "react-router-dom": "^6.0.0"
  }
}
```

---

## 🚨 **Troubleshooting**

### **Common Backend Issues**

#### **Port Already in Use**
```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 <PID>
```

#### **Module Import Errors**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### **CORS Errors**
```python
# Update CORS configuration
CORS(app, origins="*")  # For development only
```

### **Common Frontend Issues**

#### **Build Failures**
```bash
# Clear cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### **Routing Issues**
```javascript
// Add to vite.config.js for SPA routing
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
  server: {
    historyApiFallback: true,
  },
}
```

---

## 📊 **Performance Optimization**

### **Backend Optimization**
```python
# Add caching
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.cached(timeout=60)
def get_dashboard_data():
    # Cached for 60 seconds
    return data
```

### **Frontend Optimization**
```javascript
// Lazy loading components
const AIDashboard = lazy(() => import('./components/AIDashboard'));

// Memoization for expensive calculations
const MemoizedComponent = memo(ExpensiveComponent);
```

---

## 🔐 **Security Considerations**

### **Backend Security**
```python
# Add rate limiting
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/ai/dashboard-data')
@limiter.limit("100 per minute")
def dashboard_data():
    return jsonify(data)
```

### **Frontend Security**
```javascript
// Sanitize user inputs
import DOMPurify from 'dompurify';

const cleanInput = DOMPurify.sanitize(userInput);
```

---

## 📈 **Monitoring & Maintenance**

### **Health Checks**
```bash
# Automated health check script
#!/bin/bash
curl -f https://your-backend-url.com/api/ai/status || exit 1
curl -f https://your-frontend-url.com || exit 1
```

### **Log Monitoring**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

---

## 🎯 **Production Checklist**

### **Pre-Deployment**
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] CORS properly configured
- [ ] API endpoints tested
- [ ] Frontend builds successfully
- [ ] Documentation updated

### **Post-Deployment**
- [ ] Health checks passing
- [ ] API responding correctly
- [ ] Frontend loading properly
- [ ] All features functional
- [ ] Performance metrics acceptable
- [ ] Monitoring configured

---

## 📞 **Support**

For deployment issues or questions:
1. Check this guide first
2. Review error logs
3. Test individual components
4. Verify configuration files
5. Check network connectivity

**Current Live Deployments:**
- Frontend: https://pdfumwkk.manus.space
- Backend: https://58hpi8c7q968.manus.space

---

*© 2025 Global AI Marketplace - Advanced AI Trading Platform*

