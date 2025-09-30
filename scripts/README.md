# Deployment Scripts

This directory contains utility scripts for deploying and managing the CRS Cryptocurrency Marketplace.

## Available Scripts

### Backend Scripts (Python)

#### validate_env.py

Validates environment variables before backend startup to prevent deployment errors.

**Location**: `backend/scripts/validate_env.py`

**Usage**:
```bash
cd backend

# Validate current environment
python scripts/validate_env.py

# Validate specific .env file
python scripts/validate_env.py --env-file /path/to/.env

# Show all detected environment variables (sensitive values masked)
python scripts/validate_env.py --show-vars

# Strict mode (treat warnings as errors)
python scripts/validate_env.py --strict
```

**What It Validates**:
- Required environment variables (SECRET_KEY, JWT_SECRET_KEY, DATABASE_URL)
- Secret key strength (detects weak or default keys)
- Database URL format and scheme validity
- Flask environment configuration
- Port numbers and boolean values
- CORS origins configuration
- Redis connection strings
- Security issues (debug mode in production, wildcard CORS, etc.)

**Exit Codes**:
- `0` - Validation passed
- `1` - Validation failed (errors found)

**Features**:
- Color-coded output for easy reading
- Detailed error messages with suggestions
- Distinguishes between errors and warnings
- Production vs development mode awareness
- Automatic .env file loading (requires python-dotenv)

**Example Output**:
```bash
======================================================================
Environment Variable Validation Report
======================================================================

ℹ️  Information:
  • Loaded environment variables from /path/to/.env

⚠️  Warnings:
  • [CORS_ORIGINS] Using wildcard (*) for CORS in production is not recommended.

❌ Errors:
  • [SECRET_KEY] Using default or weak secret key.
    Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"

======================================================================
❌ Validation failed with 1 error(s) and 1 warning(s)
```

**Best Practices**:
1. Run validation before starting the backend in production
2. Fix all errors before deployment
3. Address warnings to improve security
4. Use `--strict` mode in CI/CD pipelines
5. Keep sensitive values in `.env` files, not in code

---

### Deployment Scripts (Shell)

### health-check.sh

Comprehensive health check script that verifies all services are running correctly.

**Usage**:
```bash
./scripts/health-check.sh
```

**Checks**:
- Docker container status
- Backend API endpoints (liveness, readiness, info)
- Frontend availability
- Redis connectivity
- Database connectivity
- System resources (disk, memory, CPU)

**Output**: Color-coded status for each check with detailed metrics.

### generate-keys.sh

Generates secure random keys for production deployment.

**Usage**:
```bash
./scripts/generate-keys.sh
```

**Generates**:
- `SECRET_KEY` - Flask secret key for session management
- `JWT_SECRET_KEY` - JWT token signing key

**Important**: 
- Never commit generated keys to version control
- Use different keys for each environment
- Regenerate keys after security incidents

## Quick Start

### Initial Setup

1. Make scripts executable:
```bash
chmod +x scripts/*.sh
```

2. Generate production keys:
```bash
./scripts/generate-keys.sh
```

3. Copy keys to your `.env` file:
```bash
# Edit .env and add the generated keys
nano .env
```

### Health Checks

Run health checks after deployment:
```bash
./scripts/health-check.sh
```

Expected output:
```
🏥 CRS Health Check Starting...
==================================

📦 Docker Services
------------------
Checking Docker service backend... ✓ Running
Checking Docker service frontend... ✓ Running
Checking Docker service redis... ✓ Running

🔧 Backend Health
------------------
Checking Backend Liveness... ✓ OK (HTTP 200)
Checking Backend Readiness... ✓ OK (HTTP 200)
Checking Backend Info... ✓ OK (HTTP 200)

🎨 Frontend Health
------------------
Checking Frontend... ✓ OK (HTTP 200)
Checking Frontend Root... ✓ OK (HTTP 200)

💾 Redis Health
------------------
Redis Connection: ✓ OK

🗄️  Database Health
------------------
Database Connection: ✓ OK

💿 Disk Space
------------------
Available: 50G (20% used)

🧠 Memory Usage
------------------
Available: 2.5G / 8.0G

📊 Container Stats
------------------
NAME              CPU %     MEM USAGE
crs-backend       5.2%      256MB
crs-frontend      1.1%      64MB
crs-redis         0.5%      32MB

==================================
✅ Health check complete!
```

## Troubleshooting

### Health Check Fails

If health checks fail:

1. Check Docker services:
```bash
docker-compose ps
```

2. View logs:
```bash
docker-compose logs -f
```

3. Restart services:
```bash
docker-compose restart
```

### Permission Denied

If you get "Permission denied" errors:

```bash
chmod +x scripts/*.sh
```

### Script Not Found

Ensure you're in the project root directory:

```bash
cd /path/to/crs
./scripts/health-check.sh
```

## Additional Scripts (Coming Soon)

Future utility scripts planned:
- `deploy.sh` - Automated deployment with rollback
- `backup.sh` - Database and configuration backup
- `restore.sh` - Restore from backup
- `update.sh` - Update dependencies
- `monitor.sh` - Continuous monitoring

## Contributing

When adding new scripts:

1. Follow the existing naming convention (lowercase with hyphens)
2. Make scripts executable: `chmod +x script-name.sh`
3. Add comprehensive comments
4. Update this README
5. Test in development environment first

## Security Notes

- Scripts may contain or generate sensitive information
- Never commit `.env` files or generated keys
- Review script output before sharing logs
- Use secure file permissions (600 for sensitive files)
- Regularly rotate generated keys

---

**Last Updated**: January 2025
