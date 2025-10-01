# Production Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Cryptons.com Cryptocurrency Marketplace to production environments. It covers security hardening, monitoring setup, and best practices.

## Prerequisites

### Required Software
- Docker and Docker Compose (recommended) OR
- Node.js 18+ and Python 3.11+
- PostgreSQL 13+ or MySQL 8+ (for production database)
- Redis 6+ (for caching and rate limiting)
- Nginx or similar reverse proxy (for SSL termination)

### Required Accounts/Services
- Domain name with DNS access
- SSL/TLS certificate (Let's Encrypt recommended)
- Email service (for notifications)
- Optional: Sentry account (for error tracking)
- Optional: Cloud storage (for backups)

---

## Table of Contents

1. [Docker Deployment (Recommended)](#docker-deployment)
2. [Manual Deployment](#manual-deployment)
3. [Security Configuration](#security-configuration)
4. [Database Setup](#database-setup)
5. [SSL/HTTPS Configuration](#ssl-configuration)
6. [Monitoring and Logging](#monitoring-and-logging)
7. [Backup and Recovery](#backup-and-recovery)
8. [Performance Optimization](#performance-optimization)
9. [Troubleshooting](#troubleshooting)

---

## Docker Deployment

### 1. Prepare Environment

```bash
# Clone repository
git clone https://github.com/thewriterben/crs.git
cd crs

# Copy environment template
cp .env.docker .env

# Edit environment variables
nano .env
```

### 2. Generate Secret Keys

```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT_SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update these values in `.env`:
```bash
SECRET_KEY=your-generated-secret-key
JWT_SECRET_KEY=your-generated-jwt-secret-key
```

### 3. Configure Database

For PostgreSQL (recommended):
```bash
# Update .env
DATABASE_URL=postgresql://username:password@postgres:5432/cryptons_db
```

### 4. Build and Run

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 5. Verify Deployment

```bash
# Check backend health
curl http://localhost:5000/api/health/liveness

# Check frontend
curl http://localhost:8080/health

# Check Redis
docker-compose exec redis redis-cli ping
```

---

## Manual Deployment

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy production environment
cp .env.production .env

# Edit configuration
nano .env

# Initialize database
python -c "from src.models import db; from src.main import app; app.app_context().push(); db.create_all()"

# Run with gunicorn
gunicorn --config gunicorn.conf.py src.main:app
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm ci --production

# Copy production environment
cp .env.production .env

# Edit configuration
nano .env

# Build for production
npm run build

# Serve with nginx or any static server
# (see nginx configuration section)
```

---

## Security Configuration

### 1. Environment Variables

**Critical Security Keys** (MUST be changed from defaults):
```bash
SECRET_KEY=<generate-random-32-char-string>
JWT_SECRET_KEY=<generate-random-32-char-string>
```

### 2. CORS Configuration

Restrict CORS to your frontend domain:
```bash
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 3. Rate Limiting

Configure rate limits based on your needs:
```bash
RATELIMIT_ENABLED=True
RATELIMIT_DEFAULT=200 per minute
RATELIMIT_STORAGE_URL=redis://redis:6379/1
```

### 4. Security Headers

Security headers are automatically configured via Flask-Talisman when `FLASK_ENV=production`.

Headers included:
- `Strict-Transport-Security` (HSTS)
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `Content-Security-Policy`

### 5. Session Security

```bash
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=3600
```

---

## Database Setup

### PostgreSQL (Recommended)

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE cryptons_marketplace;
CREATE USER cryptons_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE cryptons_marketplace TO cryptons_user;
\q
```

Update `.env`:
```bash
DATABASE_URL=postgresql://cryptons_user:secure_password@localhost:5432/cryptons_marketplace
```

### MySQL Alternative

```sql
CREATE DATABASE cryptons_marketplace CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'cryptons_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON cryptons_marketplace.* TO 'cryptons_user'@'localhost';
FLUSH PRIVILEGES;
```

Update `.env`:
```bash
DATABASE_URL=mysql://cryptons_user:secure_password@localhost:3306/cryptons_marketplace
```

---

## SSL Configuration

### Using Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
sudo systemctl status certbot.timer
```

### Nginx Configuration

Create `/etc/nginx/sites-available/cryptons`:

```nginx
upstream backend {
    server localhost:5000;
}

upstream frontend {
    server localhost:8080;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # API proxy
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/cryptons /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Monitoring and Logging

### Health Checks

The application provides several health check endpoints:

- **Liveness**: `GET /api/health/liveness` - Basic health check
- **Readiness**: `GET /api/health/readiness` - Database and Redis connectivity
- **Metrics**: `GET /api/health/metrics` - Application metrics
- **Info**: `GET /api/health/info` - Version and configuration info

### Log Configuration

#### Backend Logging

Configure in `.env`:
```bash
LOG_LEVEL=INFO
```

View logs:
```bash
# Docker
docker-compose logs -f backend

# Manual deployment
tail -f /var/log/cryptons/backend.log
```

#### Frontend Access Logs

Nginx logs location:
```bash
/var/log/nginx/access.log
/var/log/nginx/error.log
```

### Error Tracking with Sentry (Optional)

```bash
# Install Sentry SDK
pip install sentry-sdk[flask]

# Configure in .env
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
```

### Monitoring Tools

Recommended monitoring solutions:
- **Uptime monitoring**: UptimeRobot, Pingdom, or StatusCake
- **APM**: New Relic, DataDog, or Prometheus + Grafana
- **Error tracking**: Sentry or Rollbar
- **Log aggregation**: ELK Stack or Papertrail

---

## Backup and Recovery

### Database Backups

#### PostgreSQL

```bash
# Create backup script /usr/local/bin/backup-crs-db.sh
#!/bin/bash
BACKUP_DIR="/var/backups/cryptons"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

pg_dump -U cryptons_user cryptons_marketplace | gzip > $BACKUP_DIR/cryptons_db_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "cryptons_db_*.sql.gz" -mtime +30 -delete
```

Set up cron job:
```bash
# Daily backup at 2 AM
0 2 * * * /usr/local/bin/backup-crs-db.sh
```

#### Restore Database

```bash
# Extract and restore
gunzip < /var/backups/cryptons/cryptons_db_20240101_020000.sql.gz | psql -U cryptons_user cryptons_marketplace
```

### Application Backups

```bash
# Backup configuration and data
tar -czf crs-backup-$(date +%Y%m%d).tar.gz \
    backend/.env \
    backend/data/ \
    frontend/.env
```

---

## Performance Optimization

### Backend Optimization

1. **Enable Redis caching**:
```bash
CACHE_TYPE=RedisCache
REDIS_URL=redis://redis:6379/0
```

2. **Optimize gunicorn workers**:
```python
# gunicorn.conf.py
workers = (2 * cpu_count) + 1
worker_class = "gevent"  # or "eventlet" for async
```

3. **Database connection pooling**:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db?pool_size=20&max_overflow=10
```

### Frontend Optimization

1. **Enable Gzip compression** (already configured in nginx.conf)

2. **CDN for static assets** (optional):
   - CloudFlare
   - AWS CloudFront
   - Fastly

3. **Browser caching**: Configured in nginx for static assets

### Redis Optimization

```bash
# /etc/redis/redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
```

---

## Troubleshooting

### Common Issues

#### 1. Backend not starting

```bash
# Check logs
docker-compose logs backend

# Common causes:
# - Database connection failed
# - Missing environment variables
# - Port already in use

# Solutions:
docker-compose down
docker-compose up -d
```

#### 2. Frontend shows API errors

```bash
# Check CORS configuration
# Verify VITE_API_URL in frontend/.env
# Check backend logs for errors

# Test API directly
curl http://localhost:5000/api/health/liveness
```

#### 3. Database connection errors

```bash
# Test database connectivity
docker-compose exec backend python -c "from src.models import db; from src.main import app; app.app_context().push(); db.session.execute('SELECT 1')"

# Check PostgreSQL is running
docker-compose ps postgres
```

#### 4. Redis connection errors

```bash
# Test Redis
docker-compose exec redis redis-cli ping

# Should return: PONG
```

### Debug Mode

**WARNING**: Never enable debug mode in production!

For troubleshooting only:
```bash
FLASK_DEBUG=True  # Backend
VITE_DEBUG=true   # Frontend
```

### Getting Help

1. Check logs: `docker-compose logs -f`
2. Review health endpoints: `/api/health/*`
3. Check system resources: `docker stats`
4. Verify environment variables: `docker-compose config`

---

## Production Checklist

### Pre-Deployment
- [ ] Generate unique SECRET_KEY and JWT_SECRET_KEY
- [ ] Configure production database (PostgreSQL/MySQL)
- [ ] Set up Redis for caching
- [ ] Configure CORS for production domain
- [ ] Set up SSL/TLS certificates
- [ ] Configure rate limiting
- [ ] Set up monitoring and alerts
- [ ] Configure backups
- [ ] Test in staging environment

### Security
- [ ] All default keys changed
- [ ] HTTPS enabled and enforced
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] SQL injection protection verified
- [ ] XSS protection enabled
- [ ] CSRF protection enabled (for forms)

### Performance
- [ ] Redis caching enabled
- [ ] Response compression enabled
- [ ] Static assets cached
- [ ] Database queries optimized
- [ ] CDN configured (optional)

### Monitoring
- [ ] Health checks responding
- [ ] Logging configured
- [ ] Error tracking set up
- [ ] Uptime monitoring enabled
- [ ] Performance monitoring configured
- [ ] Alerts configured

### Post-Deployment
- [ ] Verify all endpoints working
- [ ] Test user registration/login
- [ ] Test payment processing
- [ ] Verify WebSocket connections
- [ ] Check mobile responsiveness
- [ ] Test under load
- [ ] Monitor logs for errors
- [ ] Verify backups working

---

## Support and Maintenance

### Regular Maintenance Tasks

**Daily**:
- Monitor error logs
- Check system health
- Review uptime alerts

**Weekly**:
- Review application metrics
- Check disk space
- Verify backups

**Monthly**:
- Update dependencies
- Security audit
- Performance review
- Backup testing

### Update Procedure

```bash
# 1. Backup current version
./scripts/backup.sh

# 2. Pull latest changes
git pull origin main

# 3. Update dependencies
docker-compose build --no-cache

# 4. Run migrations (if any)
docker-compose exec backend python scripts/migrate.py

# 5. Restart services
docker-compose down
docker-compose up -d

# 6. Verify deployment
./scripts/verify-deployment.sh
```

---

## Additional Resources

- [Security Best Practices](./SECURITY_BEST_PRACTICES.md)
- [API Documentation](./API_DOCUMENTATION.md)
- [Troubleshooting Guide](./TROUBLESHOOTING.md)
- [Development Setup](./development-setup.md)
- [Performance Optimization](./PERFORMANCE_OPTIMIZATION.md)

---

**Last Updated**: January 2025
**Version**: 1.0.0
