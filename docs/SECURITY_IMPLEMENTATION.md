# Security Implementation Guide

This document provides comprehensive security implementation guidelines for the CRS cryptocurrency marketplace.

## Table of Contents

1. [Input Validation](#input-validation)
2. [Rate Limiting](#rate-limiting)
3. [Authentication & Authorization](#authentication--authorization)
4. [Data Protection](#data-protection)
5. [API Security](#api-security)
6. [Security Testing](#security-testing)
7. [Compliance](#compliance)

---

## Input Validation

### Overview

All user inputs must be validated and sanitized to prevent injection attacks and XSS vulnerabilities.

### Implementation

#### Using Validation Decorators

```python
from src.input_validation import validate_json, validate_registration, validate_order

@app.route('/api/auth/register', methods=['POST'])
@validate_json('username', 'email', 'password')
@validate_registration()
def register():
    data = request.json
    # Data is validated and safe to use
    ...
```

#### Manual Validation

```python
from src.input_validation import InputValidator

# Validate email
if not InputValidator.validate_email(email):
    return jsonify({'error': 'Invalid email'}), 400

# Validate password
is_valid, error = InputValidator.validate_password(password)
if not is_valid:
    return jsonify({'error': error}), 400

# Sanitize HTML
clean_text = InputValidator.sanitize_html(user_input)
```

### Validation Rules

#### Email
- Must match RFC 5322 format
- Maximum length: 254 characters
- Case-insensitive

#### Username
- 3-30 characters
- Alphanumeric, hyphens, and underscores only
- No spaces or special characters

#### Password
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- Recommended: Include special characters

#### Trading Orders
- Symbol: Format `BASE/QUOTE` (e.g., `BTC/USDT`)
- Order type: `market`, `limit`, `stop_loss`, `stop_limit`, `trailing_stop`
- Side: `buy` or `sell`
- Quantity: Positive number, minimum 0.00000001
- Price: Positive number (for limit orders)

### XSS Prevention

All user-generated content is automatically sanitized using `bleach`:

```python
from src.input_validation import sanitize_output

# Sanitize before returning to client
data = get_user_data()
safe_data = sanitize_output(data)
return jsonify(safe_data)
```

**Allowed HTML tags:**
- `<p>`, `<br>`, `<strong>`, `<em>`, `<u>`, `<a>`

**Allowed attributes:**
- `<a>`: `href`, `title`

### SQL Injection Prevention

**Always use parameterized queries:**

```python
# GOOD - Parameterized query
user = User.query.filter_by(username=username).first()

# BAD - Never use string formatting
# user = User.query.filter(f"username = '{username}'").first()
```

**For LIKE queries:**

```python
from src.input_validation import escape_sql_like

search_term = escape_sql_like(user_input)
results = Model.query.filter(Model.name.like(f'%{search_term}%')).all()
```

---

## Rate Limiting

### Overview

Multi-tier rate limiting protects against abuse and DDoS attacks.

### Configuration

Rate limits are defined in `src/rate_limiting.py`:

```python
LIMITS = {
    'auth_login': ["10 per minute", "50 per hour"],
    'trading_order': ["100 per minute", "1000 per hour"],
    'market_data': ["1000 per minute"],
    'ai_prediction': ["50 per hour"],
}
```

### Implementation

#### Initialize Rate Limiter

```python
from src.rate_limiting import init_rate_limiter

app = Flask(__name__)
limiter = init_rate_limiter(app)
```

#### Apply Rate Limits

```python
from flask_limiter import Limiter

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    ...
```

### Adaptive Rate Limiting

Adjusts limits based on user behavior:

```python
from src.rate_limiting import AdaptiveRateLimiter

adaptive = AdaptiveRateLimiter()

# Increase score for good behavior
adaptive.adjust_score(user_id, 0.1)

# Get adjusted limit
limit = adaptive.get_adaptive_limit(base_limit=100, user_id=user_id)
```

### DDoS Protection

```python
from src.rate_limiting import DDoSProtection

ddos = DDoSProtection()

# Check for suspicious activity
if ddos.is_suspicious(ip_address, threshold=1000, window=60):
    ddos.block_ip(ip_address, duration=3600)
    return jsonify({'error': 'Too many requests'}), 429
```

### Rate Limit Headers

Responses include rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1640000000
```

---

## Authentication & Authorization

### JWT Token Security

**Configuration:**

```python
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')  # Strong, random key
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
```

**Best Practices:**

1. **Never log tokens**: Exclude from logs and error messages
2. **Use HTTPS only**: Never transmit tokens over HTTP
3. **Short expiration**: Access tokens expire in 1 hour
4. **Refresh tokens**: Implement token refresh mechanism
5. **Token revocation**: Blacklist compromised tokens

### Password Security

**Hashing:**

```python
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Hash password
password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

# Verify password
is_valid = bcrypt.check_password_hash(password_hash, password)
```

**Requirements:**

- Bcrypt with default work factor (12)
- No password reuse (implement password history)
- Password reset tokens expire in 1 hour
- Rate limit password reset attempts

### Multi-Factor Authentication (MFA)

**Implementation:**

```python
# Enable MFA
secret = user.enable_mfa()
qr_code = generate_qr_code(secret)

# Verify MFA code
is_valid = verify_totp(secret, user_code)
```

**MFA Methods:**

1. TOTP (Time-based One-Time Password)
2. SMS verification
3. Email verification
4. Hardware keys (FIDO2/WebAuthn)

---

## Data Protection

### Encryption at Rest

**Database Encryption:**

```python
# Use PostgreSQL with encryption
DATABASE_URL = postgresql://user:pass@host:5432/db?sslmode=require

# Encrypt sensitive fields
from cryptography.fernet import Fernet

cipher = Fernet(encryption_key)
encrypted_data = cipher.encrypt(sensitive_data.encode())
```

### Encryption in Transit

**HTTPS Only:**

```python
from flask_talisman import Talisman

Talisman(app, 
    force_https=True,
    strict_transport_security=True,
    session_cookie_secure=True
)
```

### Sensitive Data Handling

**Never log sensitive data:**
- Passwords
- API keys
- Private keys
- Personal information

**Mask sensitive data:**

```python
def mask_email(email):
    parts = email.split('@')
    return f"{parts[0][:2]}***@{parts[1]}"

def mask_phone(phone):
    return f"***-***-{phone[-4:]}"
```

---

## API Security

### CORS Configuration

```python
from flask_cors import CORS

CORS(app, 
    origins=os.environ.get('CORS_ORIGINS', '').split(','),
    methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=['Content-Type', 'Authorization'],
    supports_credentials=True
)
```

### Security Headers

```python
from flask_talisman import Talisman

Talisman(app,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
    },
    force_https=True,
    strict_transport_security=True,
    session_cookie_secure=True,
    session_cookie_httponly=True,
    session_cookie_samesite='Lax'
)
```

### API Versioning

```python
@app.route('/api/v1/endpoint')
def endpoint_v1():
    ...

@app.route('/api/v2/endpoint')
def endpoint_v2():
    ...
```

---

## Security Testing

### Automated Security Scanning

**GitHub Actions:**

```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    scan-ref: '.'
```

### Penetration Testing Checklist

- [ ] SQL injection testing
- [ ] XSS vulnerability testing
- [ ] CSRF protection testing
- [ ] Authentication bypass attempts
- [ ] Rate limiting effectiveness
- [ ] Session management security
- [ ] API endpoint security
- [ ] File upload security

### Security Audit Log

```python
from src.trading_models import AuditLog

def log_security_event(user_id, event_type, action, details):
    log = AuditLog(
        user_id=user_id,
        event_type=event_type,
        action=action,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        details=details,
        status='success'
    )
    db.session.add(log)
    db.session.commit()
```

---

## Compliance

### GDPR Compliance

**Data Privacy:**

1. **Right to Access**: Provide user data export
2. **Right to Deletion**: Implement account deletion
3. **Data Minimization**: Only collect necessary data
4. **Consent Management**: Explicit user consent for data processing
5. **Data Breach Notification**: Notify within 72 hours

**Implementation:**

```python
@app.route('/api/user/data-export', methods=['GET'])
@jwt_required()
def export_user_data():
    user_id = get_jwt_identity()
    user_data = compile_user_data(user_id)
    return send_file(user_data, as_attachment=True)

@app.route('/api/user/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    anonymize_user_data(user_id)
    return jsonify({'message': 'Account deleted'}), 200
```

### PCI DSS Compliance

See [KYC_AML_COMPLIANCE.md](./KYC_AML_COMPLIANCE.md) for payment security requirements.

### KYC/AML Compliance

See [KYC_AML_COMPLIANCE.md](./KYC_AML_COMPLIANCE.md) for identity verification requirements.

---

## Security Incident Response

### Incident Response Plan

1. **Detection**: Monitor logs and alerts
2. **Containment**: Isolate affected systems
3. **Eradication**: Remove threat
4. **Recovery**: Restore services
5. **Lessons Learned**: Document and improve

### Security Contacts

- **Security Team**: security@crs-marketplace.com
- **Bug Bounty**: [security policy link]
- **Emergency Contact**: [24/7 contact]

---

## Security Checklist

### Development

- [ ] Input validation on all user inputs
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output sanitization)
- [ ] CSRF protection enabled
- [ ] Secure password hashing (bcrypt)
- [ ] JWT token security
- [ ] Rate limiting configured
- [ ] Security headers configured
- [ ] HTTPS enforced
- [ ] Secrets in environment variables

### Deployment

- [ ] Change default credentials
- [ ] Generate strong secret keys
- [ ] Configure CORS properly
- [ ] Enable security monitoring
- [ ] Set up automated backups
- [ ] Configure firewall rules
- [ ] Enable audit logging
- [ ] Set up intrusion detection
- [ ] Document security procedures
- [ ] Train team on security practices

---

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)
