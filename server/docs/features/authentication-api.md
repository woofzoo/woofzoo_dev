# Authentication API Documentation

This document provides comprehensive curl commands for all authentication-related endpoints in the WoofZoo API.

## Base URL
All endpoints are prefixed with `/api/auth`

## Authentication Endpoints

### 1. User Registration

#### Register a new user
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "roles": ["pet_owner"]
  }'
```

**Response:**
```json
{
  "message": "User registered successfully. Please check your email for verification."
}
```

### 2. User Login

#### Login with email and password
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "roles": ["pet_owner"],
    "is_verified": false,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  }
}
```

### 3. Email Verification

#### Verify email via POST
```bash
curl -X POST "http://localhost:8000/api/auth/verify-email" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "verification_token_here"
  }'
```

#### Verify email via GET (for email links)
```bash
curl -X GET "http://localhost:8000/api/auth/verify-email?token=verification_token_here"
```

**Response:**
```json
{
  "message": "Email verified successfully"
}
```

### 4. Password Reset

#### Request password reset
```bash
curl -X POST "http://localhost:8000/api/auth/request-password-reset" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com"
  }'
```

**Response:**
```json
{
  "message": "Password reset email sent successfully"
}
```

#### Reset password
```bash
curl -X POST "http://localhost:8000/api/auth/reset-password" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "reset_token_here",
    "new_password": "NewSecurePass123!"
  }'
```

**Response:**
```json
{
  "message": "Password reset successfully"
}
```

#### Show password reset form (for email links)
```bash
curl -X GET "http://localhost:8000/api/auth/reset-password?token=reset_token_here"
```

### 5. Token Management

#### Refresh access token
```bash
curl -X POST "http://localhost:8000/api/auth/refresh?refresh_token=refresh_token_here"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Resend verification email
```bash
curl -X POST "http://localhost:8000/api/auth/resend-verification?email=user@example.com"
```

**Response:**
```json
{
  "message": "Verification email sent successfully"
}
```

### 6. Protected Endpoints (Require Authentication)

#### Get current user information
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "roles": ["pet_owner"],
  "is_verified": true,
  "personalization": {
    "theme": "light",
    "language": "en",
    "notifications": {
      "email": true,
      "push": true,
      "sms": false
    }
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Update personalization settings
```bash
curl -X PUT "http://localhost:8000/api/auth/me/personalization" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "dark",
    "language": "es",
    "notifications": {
      "email": true,
      "push": false,
      "sms": true
    }
  }'
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "roles": ["pet_owner"],
  "is_verified": true,
  "personalization": {
    "theme": "dark",
    "language": "es",
    "notifications": {
      "email": true,
      "push": false,
      "sms": true
    }
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Change password
```bash
curl -X POST "http://localhost:8000/api/auth/me/change-password?current_password=OldPass123!&new_password=NewSecurePass123!" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "Password changed successfully"
}
```

#### Logout user
```bash
curl -X POST "http://localhost:8000/api/auth/logout" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

### 7. Health Check

#### Check authentication service health
```bash
curl -X GET "http://localhost:8000/api/auth/health"
```

**Response:**
```json
{
  "message": "Authentication service is running"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid email format"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Authentication Flow

1. **Register** a new user account
2. **Verify** email address (check email for verification link)
3. **Login** with email and password
4. **Use access token** for authenticated requests
5. **Refresh token** when access token expires
6. **Logout** when done

## Security Notes

- Access tokens expire after 30 minutes
- Refresh tokens expire after 7 days
- Always use HTTPS in production
- Store tokens securely on the client side
- Never expose refresh tokens in client-side code
- Implement proper token rotation for security
