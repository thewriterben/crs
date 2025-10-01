# Backend Scripts

This directory contains utility scripts for the Cryptons.com backend.

## Available Scripts

### validate_env.py

Validates environment variables before backend startup to prevent deployment errors.

**Usage:**
```bash
# Validate current environment
python scripts/validate_env.py

# Validate specific .env file
python scripts/validate_env.py --env-file /path/to/.env

# Show all detected environment variables (sensitive values masked)
python scripts/validate_env.py --show-vars

# Strict mode (treat warnings as errors)
python scripts/validate_env.py --strict
```

**What it validates:**
- Required environment variables (SECRET_KEY, JWT_SECRET_KEY, DATABASE_URL)
- Secret key strength (detects weak or default keys)
- Database URL format and scheme validity
- Flask environment configuration
- Port numbers and boolean values
- CORS origins configuration
- Redis connection strings
- Security issues (debug mode in production, wildcard CORS, etc.)

**Exit codes:**
- `0` - Validation passed (no errors)
- `1` - Validation failed (errors found)

See [../../docs/development-setup.md](../../docs/development-setup.md#environment-variable-validation) for more details.

---

### init_database.py

Initializes and manages database tables.

**Usage:**
```bash
# Initialize database with tables
python scripts/init_database.py init

# Drop and recreate all tables (WARNING: deletes all data!)
python scripts/init_database.py reset

# Show all database tables and columns
python scripts/init_database.py show
```

**Features:**
- Creates all database tables based on models
- Creates default trading pairs (BTC/USDT, ETH/USDT, etc.)
- Provides safe reset functionality with confirmation
- Shows database schema for debugging

---

## Development Workflow

1. **Before starting development:**
   ```bash
   # Validate environment configuration
   python scripts/validate_env.py
   
   # Initialize database if needed
   python scripts/init_database.py init
   ```

2. **During development:**
   - Run `validate_env.py` after changing .env files
   - Use `init_database.py show` to inspect database schema
   
3. **Before deployment:**
   - Run `validate_env.py --strict` to ensure production readiness
   - Verify all errors and warnings are addressed

## Contributing

When adding new scripts:

1. Make scripts executable: `chmod +x script_name.py`
2. Add comprehensive docstrings
3. Include usage examples in this README
4. Follow the existing code style
5. Add appropriate error handling

## Security Notes

- Scripts may access sensitive environment variables
- Never commit `.env` files or generated secrets
- Review script output before sharing logs
- Use appropriate file permissions for sensitive data

---

**Last Updated:** January 2025
