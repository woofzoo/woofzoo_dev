# User Management API Documentation

This document provides comprehensive curl commands for all user management endpoints in the WoofZoo API.

## Base URL
All endpoints are prefixed with `/api/users`

## Authentication
Most endpoints require authentication. Include the Bearer token in the Authorization header:
```bash
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## User Management Endpoints

### 1. Get Users

#### Get all users with pagination
```bash
curl -X GET "http://localhost:8000/api/users/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "email": "john.doe@example.com",
      "username": "johndoe",
      "first_name": "John",
      "last_name": "Doe",
      "is_active": true,
      "is_verified": true,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get user by ID
```bash
curl -X GET "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "is_verified": true,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get user by email
```bash
curl -X GET "http://localhost:8000/api/users/email/john.doe@example.com" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "is_verified": true,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get user by username
```bash
curl -X GET "http://localhost:8000/api/users/username/johndoe" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "is_verified": true,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### 2. Update User

#### Update user information
```bash
curl -X PATCH "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Johnny",
    "last_name": "Smith",
    "username": "johnnysmith"
  }'
```

**Response:**
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "username": "johnnysmith",
  "first_name": "Johnny",
  "last_name": "Smith",
  "is_active": true,
  "is_verified": true,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T13:00:00Z"
}
```

### 3. Delete User

#### Delete user
```bash
curl -X DELETE "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```
HTTP/1.1 204 No Content
```

### 4. Search Users

#### Search users by name or email
```bash
curl -X GET "http://localhost:8000/api/users/search/?q=john&skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "email": "john.doe@example.com",
      "username": "johndoe",
      "first_name": "John",
      "last_name": "Doe",
      "is_active": true,
      "is_verified": true,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

### 5. Get User Profile

#### Get current user profile
```bash
curl -X GET "http://localhost:8000/api/users/profile" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
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

### 6. Update User Profile

#### Update current user profile
```bash
curl -X PATCH "http://localhost:8000/api/users/profile" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Johnny",
    "last_name": "Smith",
    "personalization": {
      "theme": "dark",
      "language": "es",
      "notifications": {
        "email": true,
        "push": false,
        "sms": true
      }
    }
  }'
```

**Response:**
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "username": "johndoe",
  "first_name": "Johnny",
  "last_name": "Smith",
  "is_active": true,
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
  "updated_at": "2024-01-01T13:00:00Z"
}
```

### 7. Change Password

#### Change user password
```bash
curl -X POST "http://localhost:8000/api/users/change-password" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "oldpassword123",
    "new_password": "newpassword123"
  }'
```

**Response:**
```json
{
  "message": "Password changed successfully"
}
```

### 8. Deactivate User

#### Deactivate user account
```bash
curl -X POST "http://localhost:8000/api/users/1/deactivate" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "User deactivated successfully"
}
```

### 9. Activate User

#### Activate user account
```bash
curl -X POST "http://localhost:8000/api/users/1/activate" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "User activated successfully"
}
```

## Query Parameters

### Pagination
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 1000)

### Search
- `q`: Search term for user name, email, or username

## Request Body Examples

### Update User
```json
{
  "first_name": "Johnny",
  "last_name": "Smith",
  "username": "johnnysmith"
}
```

### Update User Profile
```json
{
  "first_name": "Johnny",
  "last_name": "Smith",
  "personalization": {
    "theme": "dark",
    "language": "es",
    "notifications": {
      "email": true,
      "push": false,
      "sms": true
    }
  }
}
```

### Change Password
```json
{
  "current_password": "oldpassword123",
  "new_password": "newpassword123"
}
```

## User Status

Available user statuses:
- `is_active`: User account is active and can access the system
- `is_verified`: User email has been verified

## Personalization Options

### Theme
- `light`: Light theme
- `dark`: Dark theme
- `auto`: Automatic theme based on system preference

### Language
- `en`: English
- `es`: Spanish
- `fr`: French
- `de`: German
- `it`: Italian
- `pt`: Portuguese

### Notifications
- `email`: Email notifications
- `push`: Push notifications
- `sms`: SMS notifications

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Username already exists"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
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
      "loc": ["body", "first_name"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "new_password"],
      "msg": "ensure this value has at least 8 characters",
      "type": "value_error.any_str.min_length"
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

## User Management Flow

1. **Retrieve** user information by ID, email, or username
2. **Update** user profile and personalization settings
3. **Search** for users by name, email, or username
4. **Change** user password securely
5. **Activate/Deactivate** user accounts
6. **Delete** user accounts when needed

## Data Validation Rules

### First Name
- Required field
- String value
- Minimum 1 character

### Last Name
- Required field
- String value
- Minimum 1 character

### Username
- Optional field
- String value
- Must be unique
- Alphanumeric characters only

### Email
- Required field
- Must be a valid email format
- Must be unique

### Password
- Required for password change
- Minimum 8 characters
- Must contain at least one uppercase letter, one lowercase letter, and one number

## Security Notes

- Most endpoints require authentication
- Users can only access their own profile information
- Admin users can access all user information
- Password changes require current password verification
- User operations are logged for audit purposes
- Sensitive information is not returned in responses

## Usage Examples

### Get Current User Profile
```bash
curl -X GET "http://localhost:8000/api/users/profile" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update Personalization Settings
```bash
curl -X PATCH "http://localhost:8000/api/users/profile" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "personalization": {
      "theme": "dark",
      "language": "es"
    }
  }'
```

### Search for Users
```bash
curl -X GET "http://localhost:8000/api/users/search/?q=john" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
