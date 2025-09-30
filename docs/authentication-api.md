# Authentication API Documentation

## Overview

The CRS Marketplace authentication system provides secure user management with JWT token-based authentication, password encryption, and optional multi-factor authentication.

## Base URL

- Development: `http://localhost:5000/api/auth`
- Production: `/api/auth`

## Authentication Flow

1. User registers or logs in
2. Server returns access token (valid for 1 hour) and refresh token (valid for 30 days)
3. Client stores tokens securely
4. Client includes access token in Authorization header for protected endpoints
5. When access token expires, use refresh token to get new access token
6. On logout, refresh tokens are revoked

## Endpoints

### Register User

Creates a new user account.

**Endpoint:** `POST /register`

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-01-01T12:00:00",
    "last_login": null,
    "is_active": true,
    "mfa_enabled": false
  }
}
```

**Error Responses:**
- `400 Bad Request`: Missing required fields or invalid data
- `409 Conflict`: Username or email already exists

---

### Login

Authenticates a user and returns JWT tokens.

**Endpoint:** `POST /login`

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123!",
  "mfa_code": "123456"  // Optional, required if MFA is enabled
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-01-01T12:00:00",
    "last_login": "2024-01-01T12:30:00",
    "is_active": true,
    "mfa_enabled": false
  }
}
```

**MFA Required Response (401 Unauthorized):**
```json
{
  "error": "MFA code required",
  "mfa_required": true
}
```

**Error Responses:**
- `400 Bad Request`: Missing username or password
- `401 Unauthorized`: Invalid credentials or MFA code
- `403 Forbidden`: Account is deactivated

---

### Refresh Token

Gets a new access token using a refresh token.

**Endpoint:** `POST /refresh`

**Headers:**
```
Authorization: Bearer {refresh_token}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired refresh token

---

### Logout

Logs out the user and revokes all refresh tokens.

**Endpoint:** `POST /logout`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

### Verify Token

Verifies the validity of an access token and returns user information.

**Endpoint:** `GET /verify`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "valid": true,
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-01-01T12:00:00",
    "last_login": "2024-01-01T12:30:00",
    "is_active": true,
    "mfa_enabled": false
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token
- `404 Not Found`: User not found

---

### Get Profile

Gets the current user's profile information.

**Endpoint:** `GET /profile`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2024-01-01T12:00:00",
  "last_login": "2024-01-01T12:30:00",
  "is_active": true,
  "mfa_enabled": false
}
```

---

### Update Profile

Updates the user's profile information (currently email only).

**Endpoint:** `PUT /profile`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "email": "newemail@example.com"
}
```

**Response (200 OK):**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "newemail@example.com",
    "created_at": "2024-01-01T12:00:00",
    "last_login": "2024-01-01T12:30:00",
    "is_active": true,
    "mfa_enabled": false
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid email format
- `409 Conflict`: Email already in use

---

### Change Password

Changes the user's password.

**Endpoint:** `POST /change-password`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "current_password": "SecurePass123!",
  "new_password": "NewSecurePass456!"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

**Error Responses:**
- `400 Bad Request`: Missing required fields or password doesn't meet requirements
- `401 Unauthorized`: Current password is incorrect

---

### Enable MFA

Enables multi-factor authentication for the user.

**Endpoint:** `POST /mfa/enable`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "message": "MFA enabled successfully",
  "secret": "JBSWY3DPEHPK3PXP"
}
```

**Note:** Save the secret in an authenticator app (Google Authenticator, Authy, etc.)

---

### Disable MFA

Disables multi-factor authentication for the user.

**Endpoint:** `POST /mfa/disable`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "message": "MFA disabled successfully"
}
```

**Error Responses:**
- `400 Bad Request`: Password required
- `401 Unauthorized`: Invalid password

---

## Password Requirements

Passwords must meet the following criteria:

- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one number (0-9)
- At least one special character (!@#$%^&*(),.?":{}|<>)

## Username Requirements

Usernames must meet the following criteria:

- 3-80 characters
- Alphanumeric characters, underscores, and hyphens only
- Pattern: `^[a-zA-Z0-9_-]+$`

## Security Best Practices

1. **Store Tokens Securely**: Use httpOnly cookies or secure localStorage
2. **HTTPS Only**: Always use HTTPS in production
3. **Token Rotation**: Refresh access tokens before expiration
4. **Logout on Password Change**: All sessions are invalidated when password is changed
5. **MFA Recommended**: Enable MFA for enhanced security
6. **Rate Limiting**: Implement rate limiting on authentication endpoints

## Error Handling

All error responses follow this format:

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

Common HTTP status codes:
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate username)
- `500 Internal Server Error`: Server error

## Examples

### Complete Authentication Flow

```javascript
// 1. Register
const registerResponse = await fetch('/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'johndoe',
    email: 'john@example.com',
    password: 'SecurePass123!'
  })
});

// 2. Login
const loginResponse = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'johndoe',
    password: 'SecurePass123!'
  })
});

const { access_token, refresh_token } = await loginResponse.json();

// 3. Make authenticated request
const profileResponse = await fetch('/api/auth/profile', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});

// 4. Refresh token when access token expires
const refreshResponse = await fetch('/api/auth/refresh', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${refresh_token}` }
});

const { access_token: newAccessToken } = await refreshResponse.json();

// 5. Logout
await fetch('/api/auth/logout', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${access_token}` }
});
```
