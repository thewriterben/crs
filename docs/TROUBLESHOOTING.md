# Troubleshooting Guide

## Overview

This guide helps diagnose and resolve common issues in the CRS Cryptocurrency Marketplace.

---

## Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Backend Issues](#backend-issues)
3. [Frontend Issues](#frontend-issues)
4. [Database Issues](#database-issues)
5. [Docker Issues](#docker-issues)
6. [Performance Issues](#performance-issues)
7. [Security Issues](#security-issues)
8. [Getting Help](#getting-help)

---

## Quick Diagnostics

### Health Check Commands

```bash
# Check all services
docker-compose ps

# Backend health
curl http://localhost:5000/api/health/liveness
curl http://localhost:5000/api/health/readiness

# Frontend health
curl http://localhost:8080/health

# Redis health
docker-compose exec redis redis-cli ping

# Database health (PostgreSQL)
docker-compose exec postgres pg_isready
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f redis

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Check Resource Usage

```bash
# Docker stats
docker stats

# System resources
df -h              # Disk space
free -h            # Memory
top                # CPU usage
```

---

## Backend Issues

### Issue: Backend Won't Start

**Symptoms**:
- Container exits immediately
- Connection refused errors
- Import errors

**Diagnosis**:
```bash
# Check logs
docker-compose logs backend

# Try running directly
docker-compose run --rm backend python src/main.py
```

**Solutions**:

1. **Missing Dependencies**:
```bash
docker-compose build --no-cache backend
docker-compose up -d backend
```

2. **Port Already in Use**:
```bash
# Find process using port 5000
lsof -i :5000
# or
netstat -tulpn | grep :5000

# Kill process
kill -9 <PID>
```

3. **Database Connection Failed**:
```bash
# Check DATABASE_URL in .env
# Verify database is running
docker-compose ps postgres

# Test connection
docker-compose exec backend python -c "from src.models import db; from src.main import app; app.app_context().push(); db.session.execute('SELECT 1')"
```

4. **Missing Environment Variables**:
```bash
# Check .env file exists
ls -la .env

# Verify required variables
docker-compose config | grep -A 20 backend

# Use the environment validation script
cd backend
python scripts/validate_env.py

# Or validate a specific .env file
python scripts/validate_env.py --env-file /path/to/.env

# Show all environment variables (with sensitive values masked)
python scripts/validate_env.py --show-vars
```

**What the validation script checks:**
- Required variables: SECRET_KEY, JWT_SECRET_KEY, DATABASE_URL
- Secret key strength (detects weak/default keys)
- Database connection URL format
- Security issues (debug mode in production, CORS wildcards)
- Valid port numbers, boolean values, URLs

**Common validation errors:**
- `SECRET_KEY not set` - Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- `Weak secret key` - Replace default keys with secure random values
- `Invalid DATABASE_URL` - Check connection string format
- `Debug mode in production` - Set `FLASK_DEBUG=False` in production

See [development-setup.md](./development-setup.md#environment-variable-validation) for more details.

### Issue: 500 Internal Server Error

**Diagnosis**:
```bash
# Check detailed error logs
docker-compose logs backend | tail -50

# Enable debug mode (development only!)
# In .env: FLASK_DEBUG=True
```

**Common Causes**:
1. Database connection lost
2. Unhandled exception in code
3. Missing required configuration
4. Redis connection failed

**Solutions**:
```bash
# Restart backend
docker-compose restart backend

# Check database
docker-compose exec postgres psql -U crs_user -d crs_marketplace -c "SELECT 1"

# Check Redis
docker-compose exec redis redis-cli ping
```

### Issue: Authentication Failures

**Symptoms**:
- Login returns 401
- Token validation fails
- "Invalid credentials" errors

**Diagnosis**:
```bash
# Check JWT configuration
docker-compose exec backend python -c "import os; print(os.getenv('JWT_SECRET_KEY'))"

# Verify user exists
docker-compose exec backend python -c "from src.models import User, db; from src.main import app; app.app_context().push(); print(User.query.all())"
```

**Solutions**:

1. **Secret Key Mismatch**:
```bash
# Ensure JWT_SECRET_KEY is set and consistent
# Restart backend after changing
docker-compose restart backend
```

2. **Token Expired**:
```bash
# Client should refresh token
# Check JWT_ACCESS_TOKEN_EXPIRES in .env
```

3. **Password Issue**:
```bash
# Reset password for user
docker-compose exec backend python scripts/reset_password.py username@example.com
```

### Issue: Rate Limiting Errors

**Symptoms**:
- 429 Too Many Requests
- "Rate limit exceeded" messages

**Diagnosis**:
```bash
# Check rate limit configuration
grep RATELIMIT .env

# Check Redis for rate limit data
docker-compose exec redis redis-cli keys "*limiter*"
```

**Solutions**:

1. **Increase Limits** (if legitimate traffic):
```bash
# In .env
RATELIMIT_DEFAULT=500 per minute
```

2. **Reset Rate Limits**:
```bash
# Clear Redis rate limit keys
docker-compose exec redis redis-cli FLUSHDB
```

3. **Whitelist IP**:
```python
# In security_config.py
limiter.exempt(lambda: request.remote_addr == 'trusted.ip.address')
```

---

## Frontend Issues

### Issue: Frontend Won't Build

**Symptoms**:
- Build fails with errors
- Dependency issues
- Out of memory errors

**Diagnosis**:
```bash
# Check logs
docker-compose logs frontend

# Try building directly
cd frontend
npm run build
```

**Solutions**:

1. **Clear Cache**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
npm run build
```

2. **Memory Issues**:
```bash
# Increase Node memory
NODE_OPTIONS="--max-old-space-size=4096" npm run build
```

3. **Dependency Conflicts**:
```bash
# Use exact versions
npm ci --legacy-peer-deps
```

### Issue: API Connection Errors

**Symptoms**:
- Network errors in browser console
- CORS errors
- Failed to fetch

**Diagnosis**:
```bash
# Check frontend environment
cat frontend/.env

# Test API directly
curl http://localhost:5000/api/ai/status

# Check browser console (F12)
# Look for CORS or network errors
```

**Solutions**:

1. **CORS Error**:
```bash
# Update backend .env
CORS_ORIGINS=http://localhost:8080,http://localhost:5173

# Restart backend
docker-compose restart backend
```

2. **Wrong API URL**:
```bash
# Update frontend/.env
VITE_API_URL=http://localhost:5000

# Rebuild frontend
docker-compose up -d --build frontend
```

3. **Network Connectivity**:
```bash
# Test from container
docker-compose exec frontend wget -O- http://backend:5000/api/health/liveness
```

### Issue: Blank Page / White Screen

**Symptoms**:
- Browser shows blank page
- Console shows errors
- Assets not loading

**Diagnosis**:
```bash
# Check nginx logs
docker-compose logs frontend

# Check browser console (F12)
# Look for JavaScript errors

# Verify build completed
ls -la frontend/dist/
```

**Solutions**:

1. **Rebuild Application**:
```bash
docker-compose up -d --build frontend
```

2. **Clear Browser Cache**:
```
Ctrl+Shift+R (Chrome/Firefox)
Cmd+Shift+R (Mac)
```

3. **Check Nginx Configuration**:
```bash
docker-compose exec frontend nginx -t
```

---

## Database Issues

### Issue: Cannot Connect to Database

**Symptoms**:
- Connection refused
- Authentication failed
- Database does not exist

**Diagnosis**:
```bash
# Check database container
docker-compose ps postgres

# Try connecting manually
docker-compose exec postgres psql -U crs_user -d crs_marketplace

# Check DATABASE_URL
echo $DATABASE_URL
```

**Solutions**:

1. **Database Not Running**:
```bash
docker-compose up -d postgres
```

2. **Wrong Credentials**:
```bash
# Verify credentials in .env match docker-compose.yml
# Update DATABASE_URL if needed
```

3. **Database Doesn't Exist**:
```bash
# Create database
docker-compose exec postgres createdb -U crs_user crs_marketplace
```

### Issue: Migration Errors

**Symptoms**:
- Table doesn't exist
- Column missing
- Schema mismatch

**Solutions**:

1. **Recreate Tables**:
```bash
docker-compose exec backend python -c "from src.models import db; from src.main import app; app.app_context().push(); db.create_all()"
```

2. **Check Schema**:
```bash
docker-compose exec postgres psql -U crs_user -d crs_marketplace -c "\dt"
```

### Issue: Database Performance

**Symptoms**:
- Slow queries
- High CPU usage
- Timeouts

**Diagnosis**:
```bash
# Check slow queries (PostgreSQL)
docker-compose exec postgres psql -U crs_user -d crs_marketplace -c "SELECT query, calls, total_time, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"
```

**Solutions**:

1. **Add Indexes**:
```sql
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_token_user ON refresh_tokens(user_id);
```

2. **Optimize Queries**:
```python
# Use select_related to reduce queries
User.query.options(joinedload(User.tokens)).all()
```

3. **Increase Resources**:
```yaml
# docker-compose.yml
postgres:
  deploy:
    resources:
      limits:
        memory: 2G
      reservations:
        memory: 1G
```

---

## Docker Issues

### Issue: Container Keeps Restarting

**Diagnosis**:
```bash
# Check restart count
docker-compose ps

# View exit code and logs
docker-compose logs --tail=50 <service>
```

**Common Causes**:
1. Application crashes
2. Health check failures
3. Resource limits exceeded

**Solutions**:
```bash
# Disable restart policy temporarily
docker-compose up --no-recreate <service>

# Check resources
docker stats

# Review health check
docker inspect <container> | grep -A 10 Healthcheck
```

### Issue: Out of Disk Space

**Symptoms**:
- No space left on device
- Cannot write to disk
- Build failures

**Diagnosis**:
```bash
# Check disk usage
df -h

# Check Docker disk usage
docker system df
```

**Solutions**:
```bash
# Clean up unused images
docker image prune -a

# Clean up volumes
docker volume prune

# Clean up everything
docker system prune -a --volumes

# WARNING: This removes all unused data!
```

### Issue: Network Issues

**Symptoms**:
- Cannot connect between containers
- DNS resolution fails
- Timeout errors

**Diagnosis**:
```bash
# List networks
docker network ls

# Inspect network
docker network inspect crs_crs-network

# Test connectivity
docker-compose exec backend ping frontend
```

**Solutions**:
```bash
# Recreate network
docker-compose down
docker-compose up -d
```

---

## Performance Issues

### Issue: Slow Response Times

**Diagnosis**:
```bash
# Check application metrics
curl http://localhost:5000/api/health/metrics

# Monitor in real-time
docker stats
```

**Solutions**:

1. **Enable Caching**:
```bash
# In .env
CACHE_TYPE=RedisCache
REDIS_URL=redis://redis:6379/0
```

2. **Optimize Database**:
```sql
-- Add indexes
-- Optimize queries
-- Use connection pooling
```

3. **Scale Workers**:
```python
# gunicorn.conf.py
workers = 8  # Increase based on CPU cores
```

### Issue: High Memory Usage

**Diagnosis**:
```bash
# Check memory usage
docker stats --no-stream

# Check backend metrics
curl http://localhost:5000/api/health/metrics | jq '.process.memory_rss_mb'
```

**Solutions**:

1. **Set Memory Limits**:
```yaml
# docker-compose.yml
backend:
  deploy:
    resources:
      limits:
        memory: 512M
```

2. **Optimize Code**:
```python
# Clear caches periodically
# Use generators instead of lists
# Close database connections
```

### Issue: High CPU Usage

**Diagnosis**:
```bash
# Identify process
docker stats

# Check application metrics
curl http://localhost:5000/api/health/metrics | jq '.process.cpu_percent'
```

**Solutions**:

1. **Optimize Algorithms**:
   - Profile code
   - Reduce complexity
   - Add caching

2. **Use Async Workers**:
```python
# gunicorn.conf.py
worker_class = "gevent"
```

---

## Security Issues

### Issue: Suspicious Activity Detected

**Actions**:

1. **Immediate**:
```bash
# Block IP address
sudo ufw deny from <suspicious-ip>

# Disable affected user account
docker-compose exec backend python scripts/disable_user.py user@example.com
```

2. **Investigation**:
```bash
# Review logs
docker-compose logs backend | grep <suspicious-ip>

# Check authentication attempts
docker-compose logs backend | grep "Failed login"
```

3. **Recovery**:
```bash
# Rotate credentials
# Update security rules
# Apply patches
```

### Issue: Suspected Data Breach

**Immediate Steps**:
1. Isolate affected systems
2. Preserve evidence (logs, etc.)
3. Notify stakeholders
4. Contact security team
5. Follow incident response plan

---

## Getting Help

### Information to Gather

When seeking help, provide:

1. **System Information**:
```bash
docker-compose version
docker version
uname -a
```

2. **Logs**:
```bash
docker-compose logs --tail=100 > logs.txt
```

3. **Configuration** (sanitized):
```bash
docker-compose config > config.yml
# Remove sensitive data before sharing!
```

4. **Error Messages**:
- Exact error text
- Stack traces
- Status codes

### Support Channels

1. **Documentation**: Check docs/ directory
2. **GitHub Issues**: [github.com/thewriterben/crs/issues](https://github.com/thewriterben/crs/issues)
3. **Community**: Discussion forums
4. **Email**: support@yourdomain.com

### Before Reporting

- [ ] Checked logs
- [ ] Reviewed documentation
- [ ] Searched existing issues
- [ ] Tried basic troubleshooting
- [ ] Gathered relevant information

---

## Preventive Measures

### Regular Maintenance

```bash
# Daily
./scripts/check-health.sh

# Weekly
./scripts/update-dependencies.sh
./scripts/backup-database.sh

# Monthly
./scripts/security-audit.sh
./scripts/performance-review.sh
```

### Monitoring Setup

```bash
# Set up alerts for:
- Service downtime
- High error rates
- Disk space low
- Memory usage high
- Failed authentication attempts
```

---

**Last Updated**: January 2025
**Version**: 1.0.0
