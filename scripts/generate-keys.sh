#!/bin/bash
# Generate secure keys for production deployment

echo "🔐 Cryptons.com Key Generator"
echo "===================="
echo ""

echo "Copy these values to your .env file:"
echo ""

echo "# Security Keys (Generated $(date))"
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
echo "JWT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"

echo ""
echo "⚠️  IMPORTANT: Keep these keys secure and never commit them to version control!"
echo ""
