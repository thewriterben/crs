# Deployment Scripts

This directory contains utility scripts for deploying and managing the CRS Cryptocurrency Marketplace.

## Available Scripts

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
