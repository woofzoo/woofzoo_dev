# WoofZoo Authentication System

This document provides a comprehensive overview of the authentication system implemented for the WoofZoo application.

## Overview

The authentication system provides secure user registration, login, password reset, and email verification functionality using industry-standard practices:

- **JWT-based authentication** with access and refresh tokens
- **Secure password hashing** using bcrypt
- **Email verification** via Mailgun integration
- **Password reset** functionality with secure tokens
- **Role-based access control** with multiple user roles
- **Personalization settings** stored in JWT tokens

## User Roles

The system supports the following user roles:

- **pet_owner**: Primary pet owner with full access to pet management
- **family_member**: Family member of pet owner (invited or joined)
- **clinic_owner**: Owner of a veterinary clinic
- **doctor**: Veterinary doctor (can also be clinic owner)

Users can have multiple roles simultaneously (e.g., a doctor can also be a clinic owner).

## Architecture

The authentication system follows Clean Architecture principles with the following layers:

```
Routes → Controllers → Services → Repositories → Models
```

### Components

1. **Models** (`app/models/user.py`)
   - User model with all authentication fields
   - UserRole enum for role management

2. **Schemas** (`app/schemas/auth.py`)
   - Pydantic models for request/response validation
   - Password strength validation
   - Role validation

3. **Repositories** (`app/repositories/user.py`)
   - Database operations for user management
   - Token management operations

4. **Services** (`app/services/`)
   - `auth.py`: Core authentication business logic
   - `email.py`: Mailgun email service integration
   - `jwt.py`: JWT token generation and validation

5. **Controllers** (`app/controllers/auth.py`)
   - HTTP request/response handling
   - Error handling and status codes

6. **Routes** (`app/routes/auth.py`)
   - API endpoint definitions
   - Dependency injection

## API Endpoints

### Public Endpoints (No Authentication Required)

#### 1. User Registration
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "password": "SecurePass123!",
  "roles": ["pet_owner"]
}
```

**Response:**
```json
{
  "message": "User registered successfully"
}
```

#### 2. User Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "roles": ["pet_owner"],
    "is_active": true,
    "is_verified": false,
    "personalization": {},
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  },
  "tokens": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```

#### 3. Email Verification
```http
POST /api/auth/verify-email
Content-Type: application/json

{
  "token": "verification_token_here"
}
```

**Response:**
```json
{
  "message": "Email verified successfully"
}
```

#### 4. Password Reset Request
```http
POST /api/auth/request-password-reset
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "If an account with that email exists, a password reset link has been sent"
}
```

#### 5. Password Reset
```http
POST /api/auth/reset-password
Content-Type: application/json

{
  "token": "reset_token_here",
  "new_password": "NewSecurePass123!"
}
```

**Response:**
```json
{
  "message": "Password reset successfully"
}
```

#### 6. Token Refresh
```http
POST /api/auth/refresh?refresh_token=refresh_token_here
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### 7. Resend Verification Email
```http
POST /api/auth/resend-verification?email=user@example.com
```

**Response:**
```json
{
  "message": "If an account with that email exists and is not verified, a verification email has been sent"
}
```

### Protected Endpoints (Authentication Required)

#### 1. Get Current User
```http
GET /api/auth/me
Authorization: Bearer access_token_here
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "roles": ["pet_owner"],
  "is_active": true,
  "is_verified": true,
  "personalization": {
    "theme": "light",
    "language": "en"
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### 2. Update Personalization
```http
PUT /api/auth/me/personalization
Authorization: Bearer access_token_here
Content-Type: application/json

{
  "personalization": {
    "theme": "dark",
    "language": "en",
    "notifications": {
      "email": true,
      "push": false
    }
  }
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "roles": ["pet_owner"],
  "is_active": true,
  "is_verified": true,
  "personalization": {
    "theme": "dark",
    "language": "en",
    "notifications": {
      "email": true,
      "push": false
    }
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### 3. Change Password
```http
POST /api/auth/me/change-password?current_password=oldpass&new_password=newpass
Authorization: Bearer access_token_here
```

**Response:**
```json
{
  "message": "Password changed successfully"
}
```

#### 4. Logout
```http
POST /api/auth/logout
Authorization: Bearer access_token_here
```

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

## Configuration

The authentication system is configured through environment variables:

### JWT Settings
```env
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256
```

### Email Settings (Mailgun)
```env
MAILGUN_API_KEY=dummy_api_key
MAILGUN_DOMAIN=sandbox25b3d4a0d8f64783982dd7f5770a0851.mailgun.org
MAILGUN_FROM_EMAIL=postmaster@sandbox25b3d4a0d8f64783982dd7f5770a0851.mailgun.org
MAILGUN_FROM_NAME=WoofZoo
```

### Token Expiration Settings
```env
EMAIL_VERIFICATION_EXPIRE_HOURS=24
PASSWORD_RESET_EXPIRE_HOURS=24
```

### Frontend URL
```env
FRONTEND_URL=http://localhost:3000
```

### Password Requirements
```env
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_LOWERCASE=true
PASSWORD_REQUIRE_DIGITS=true
PASSWORD_REQUIRE_SPECIAL=true
```

## Security Features

### Password Security
- **bcrypt hashing** with salt rounds
- **Strong password requirements**:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
  - At least one special character

### JWT Security
- **Access tokens** expire in 30 minutes
- **Refresh tokens** expire in 7 days
- **HS256 algorithm** for token signing
- **Token type validation** (access vs refresh)

### Email Security
- **Verification tokens** expire in 24 hours
- **Password reset tokens** expire in 24 hours
- **Secure token generation** using `secrets.token_urlsafe()`
- **Rate limiting** considerations (implemented at service level)

### API Security
- **CORS protection** with configurable origins
- **Trusted host middleware** for production
- **Input validation** using Pydantic schemas
- **SQL injection protection** via SQLAlchemy ORM

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    roles JSON NOT NULL DEFAULT '[]',
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_verified BOOLEAN NOT NULL DEFAULT false,
    email_verification_token VARCHAR(255),
    email_verification_expires TIMESTAMP WITH TIME ZONE,
    password_reset_token VARCHAR(255),
    password_reset_expires TIMESTAMP WITH TIME ZONE,
    personalization JSON NOT NULL DEFAULT '{}',
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX ix_users_email ON users(email);
CREATE INDEX ix_users_email_verification_token ON users(email_verification_token);
CREATE INDEX ix_users_password_reset_token ON users(password_reset_token);
```

## Email Templates

### Email Verification Template
- **Subject**: "Verify Your Email - WoofZoo"
- **Content**: HTML and plain text versions
- **Features**: Branded design, clear call-to-action, expiration notice

### Password Reset Template
- **Subject**: "Reset Your Password - WoofZoo"
- **Content**: HTML and plain text versions
- **Features**: Security warning, clear instructions, expiration notice

### Welcome Email Template
- **Subject**: "Welcome to WoofZoo! 🐾"
- **Content**: Feature overview, getting started guide

## Usage Examples

### Frontend Integration

#### 1. User Registration
```javascript
const registerUser = async (userData) => {
  const response = await fetch('/api/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });
  
  if (response.ok) {
    // Show success message and redirect to email verification
    const data = await response.json();
    showMessage(data.message);
  } else {
    // Handle validation errors
    const error = await response.json();
    showError(error.detail);
  }
};
```

#### 2. User Login
```javascript
const loginUser = async (credentials) => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });
  
  if (response.ok) {
    const data = await response.json();
    
    // Store tokens
    localStorage.setItem('access_token', data.tokens.access_token);
    localStorage.setItem('refresh_token', data.tokens.refresh_token);
    
    // Store user data
    localStorage.setItem('user', JSON.stringify(data.user));
    
    // Redirect to dashboard
    window.location.href = '/dashboard';
  } else {
    const error = await response.json();
    showError(error.detail);
  }
};
```

#### 3. Authenticated Requests
```javascript
const getCurrentUser = async () => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('/api/auth/me', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  if (response.ok) {
    const user = await response.json();
    return user;
  } else if (response.status === 401) {
    // Token expired, try to refresh
    await refreshToken();
    return getCurrentUser();
  }
};

const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  
  const response = await fetch(`/api/auth/refresh?refresh_token=${refreshToken}`);
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
  } else {
    // Refresh failed, redirect to login
    localStorage.clear();
    window.location.href = '/login';
  }
};
```

## Testing

The authentication system includes comprehensive tests:

```bash
# Run all tests
pytest

# Run only authentication tests
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/
```

### Test Coverage
- User registration (success, validation, duplicates)
- User login (success, invalid credentials)
- Email verification
- Password reset
- Token refresh
- Protected endpoints
- Personalization updates

## Deployment Considerations

### Production Checklist
- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Configure production database URL
- [ ] Set up production Mailgun domain
- [ ] Configure CORS origins for production
- [ ] Set up SSL/TLS certificates
- [ ] Configure trusted hosts
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy

### Security Best Practices
- [ ] Use environment variables for all secrets
- [ ] Implement rate limiting
- [ ] Set up monitoring for failed login attempts
- [ ] Regular security audits
- [ ] Keep dependencies updated
- [ ] Implement proper logging
- [ ] Set up intrusion detection

## Troubleshooting

### Common Issues

#### 1. Email Not Sending
- Check Mailgun API key and domain configuration
- Verify network connectivity
- Check email service logs

#### 2. Token Expiration Issues
- Verify token expiration settings
- Check system clock synchronization
- Review token refresh logic

#### 3. Database Connection Issues
- Verify database URL configuration
- Check database server status
- Review connection pool settings

#### 4. CORS Issues
- Verify CORS origins configuration
- Check frontend URL settings
- Review browser console for errors

### Debug Mode
Enable debug mode for development:
```env
DEBUG=true
DATABASE_ECHO=true
```

## Support

For issues and questions:
1. Check the logs for error messages
2. Review the test cases for usage examples
3. Verify configuration settings
4. Check the API documentation at `/docs`

## Future Enhancements

Potential improvements for the authentication system:
- [ ] Two-factor authentication (2FA)
- [ ] Social login integration
- [ ] Session management
- [ ] Account lockout after failed attempts
- [ ] Audit logging
- [ ] Multi-tenant support
- [ ] API rate limiting
- [ ] Webhook notifications
