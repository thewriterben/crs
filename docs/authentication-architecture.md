# Authentication System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CRS Authentication System                       │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│                      │         │                      │
│   Frontend (React)   │◄───────►│  Backend (Flask)     │
│                      │  HTTPS  │                      │
└──────────────────────┘  /API   └──────────────────────┘
         │                                 │
         │                                 │
         ▼                                 ▼
┌──────────────────────┐         ┌──────────────────────┐
│  LocalStorage        │         │  SQLite Database     │
│  - access_token      │         │  - users             │
│  - refresh_token     │         │  - refresh_tokens    │
└──────────────────────┘         └──────────────────────┘
```

## Component Architecture

### Frontend Components

```
AuthContext (Global State)
    │
    ├── Login Component
    │   ├── Username Input
    │   ├── Password Input
    │   └── MFA Code Input (conditional)
    │
    ├── Register Component
    │   ├── Username Input
    │   ├── Email Input
    │   ├── Password Input
    │   ├── Confirm Password Input
    │   └── Password Strength Indicator
    │
    └── UserProfile Component
        ├── Profile Info Display
        ├── Email Update Form
        ├── Password Change Form
        └── MFA Management
```

### Backend Modules

```
main.py (Flask App)
    │
    ├── models.py
    │   ├── User Model
    │   │   ├── username
    │   │   ├── email
    │   │   ├── password_hash
    │   │   ├── mfa_enabled
    │   │   ├── mfa_secret
    │   │   └── Methods (set_password, check_password, etc.)
    │   │
    │   └── RefreshToken Model
    │       ├── user_id
    │       ├── token
    │       ├── expires_at
    │       └── revoked
    │
    ├── auth_utils.py
    │   ├── validate_email()
    │   ├── validate_password()
    │   ├── validate_username()
    │   ├── verify_mfa_code()
    │   └── token_required() decorator
    │
    └── auth_routes.py (Blueprint)
        ├── /register
        ├── /login
        ├── /logout
        ├── /refresh
        ├── /verify
        ├── /profile (GET/PUT)
        ├── /change-password
        └── /mfa/enable|disable
```

## Authentication Flow

### 1. Registration Flow

```
User                Frontend              Backend              Database
  │                    │                    │                     │
  ├─ Enter Details ───►│                    │                     │
  │                    ├─ Validate ────────►│                     │
  │                    │                    ├─ Hash Password ───►│
  │                    │                    ├─ Create User ──────►│
  │                    │◄─ Success ────────┤◄─ User ID ─────────┤
  │◄─ Show Success ───┤                    │                     │
  │                    │                    │                     │
```

### 2. Login Flow

```
User                Frontend              Backend              Database
  │                    │                    │                     │
  ├─ Enter Creds ─────►│                    │                     │
  │                    ├─ POST /login ─────►│                     │
  │                    │                    ├─ Verify User ──────►│
  │                    │                    │◄─ User Data ───────┤
  │                    │                    ├─ Check Password ───►│
  │                    │                    ├─ Generate Tokens ──►│
  │                    │                    ├─ Store Ref Token ──►│
  │                    │◄─ Tokens + User ──┤                     │
  │◄─ Logged In ───────┤                    │                     │
  │                    ├─ Store Tokens     │                     │
  │                    │   in LocalStorage  │                     │
  │                    │                    │                     │
```

### 3. Authenticated Request Flow

```
User                Frontend              Backend              Database
  │                    │                    │                     │
  ├─ Request Data ────►│                    │                     │
  │                    ├─ Add Auth Header ─►│                     │
  │                    │   (Bearer Token)   │                     │
  │                    │                    ├─ Verify JWT ───────►│
  │                    │                    │◄─ User ID ─────────┤
  │                    │                    ├─ Process Request ──►│
  │                    │◄─ Data ───────────┤◄─ Response ────────┤
  │◄─ Display Data ───┤                    │                     │
  │                    │                    │                     │
```

### 4. Token Refresh Flow

```
User                Frontend              Backend              Database
  │                    │                    │                     │
  │                    ├─ Access Token ────►│                     │
  │                    │   Expired!         ├─ Return 401 ───────│
  │                    │◄──────────────────┤                     │
  │                    │                    │                     │
  │                    ├─ POST /refresh ───►│                     │
  │                    │   (Ref Token)      │                     │
  │                    │                    ├─ Verify Ref Token ►│
  │                    │                    │◄─ Token Valid ─────┤
  │                    │                    ├─ Generate New ─────►│
  │                    │                    │   Access Token      │
  │                    │◄─ New Token ──────┤                     │
  │                    ├─ Store Token      │                     │
  │                    ├─ Retry Request ───►│                     │
  │◄─ Success ─────────┤◄─ Data ───────────┤                     │
  │                    │                    │                     │
```

### 5. MFA Flow

```
User                Frontend              Backend              Database
  │                    │                    │                     │
  ├─ Login (user/pass)►│                    │                     │
  │                    ├─ POST /login ─────►│                     │
  │                    │                    ├─ Verify User ──────►│
  │                    │                    │◄─ MFA Enabled ─────┤
  │                    │◄─ MFA Required ───┤                     │
  │◄─ Show MFA Form ──┤                    │                     │
  │                    │                    │                     │
  ├─ Enter MFA Code ──►│                    │                     │
  │                    ├─ POST /login ─────►│                     │
  │                    │   (with MFA)       │                     │
  │                    │                    ├─ Verify Code ──────►│
  │                    │                    │◄─ Valid ───────────┤
  │                    │                    ├─ Generate Tokens ──►│
  │                    │◄─ Tokens + User ──┤                     │
  │◄─ Logged In ───────┤                    │                     │
  │                    │                    │                     │
```

## Security Layers

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: Transport Security (HTTPS in production)              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 2: CORS Configuration (Restrict Origins)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 3: Input Validation (Email, Password, Username)          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 4: Authentication (JWT Verification)                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 5: Authorization (User Permissions)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 6: Data Protection (Bcrypt, SQLAlchemy ORM)             │
└─────────────────────────────────────────────────────────────────┘
```

## Token Management

### Access Token
- **Duration:** 1 hour
- **Purpose:** Authenticate API requests
- **Storage:** localStorage (Frontend)
- **Transmission:** Authorization header
- **Contains:** User ID, expiration time

### Refresh Token
- **Duration:** 30 days
- **Purpose:** Generate new access tokens
- **Storage:** localStorage (Frontend) + Database (Backend)
- **Transmission:** Authorization header
- **Features:** Can be revoked, tracked in database

### Token Lifecycle

```
┌────────────────┐
│  User Logs In  │
└────────┬───────┘
         │
         ▼
┌────────────────────────┐
│ Generate Access Token  │
│ (1 hour expiry)        │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ Generate Refresh Token │
│ (30 day expiry)        │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ Store in LocalStorage  │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ Make API Requests      │
└────────┬───────────────┘
         │
         ▼
    ┌────────┐
    │ Valid? │
    └────┬───┴──────┐
      Yes│          │No (Expired)
         │          │
         ▼          ▼
    ┌────────┐  ┌────────────┐
    │Success │  │Use Refresh │
    └────────┘  │Token       │
                └────┬───────┘
                     │
                     ▼
                ┌────────────┐
                │New Access  │
                │Token       │
                └────┬───────┘
                     │
                     ▼
                ┌────────────┐
                │Retry       │
                │Request     │
                └────────────┘
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    mfa_secret VARCHAR(32)
);
```

### Refresh Tokens Table
```sql
CREATE TABLE refresh_tokens (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## API Request/Response Examples

### Register
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

### Authenticated Request
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Error Handling

```
┌─────────────────┐
│  Request Error  │
└────────┬────────┘
         │
         ▼
    ┌────────────────┐
    │ Network Error? │
    └────┬───────┬───┘
      Yes│       │No
         │       │
         ▼       ▼
    ┌────────┐ ┌────────────────┐
    │ Retry  │ │ HTTP Status    │
    │ Logic  │ │ Code Check     │
    └────────┘ └────┬───────────┘
                    │
                    ▼
              ┌─────────────┐
              │   Status?   │
              └─────┬───┬───┴─────┐
                    │   │         │
                 400│ 401│       500│
                    │   │         │
                    ▼   ▼         ▼
              ┌──────┬──────┬────────┐
              │ Bad  │Auth  │Server  │
              │Request│Error │ Error  │
              └──────┴──────┴────────┘
                    │
                    ▼
              ┌──────────────┐
              │Display Error │
              │to User       │
              └──────────────┘
```

## Summary

This authentication system provides:

✅ **Complete user lifecycle management**
✅ **Secure password storage and validation**
✅ **JWT-based stateless authentication**
✅ **Token refresh mechanism**
✅ **Multi-factor authentication support**
✅ **Comprehensive error handling**
✅ **Production-ready security practices**
✅ **Full API documentation**
✅ **Clean, maintainable code structure**
