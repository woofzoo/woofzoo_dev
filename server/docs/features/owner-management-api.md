# Owner Management API Documentation

This document provides comprehensive curl commands for all owner management endpoints in the WoofZoo API.

## Base URL
All endpoints are prefixed with `/api/owners`

## Authentication
Most endpoints require authentication. Include the Bearer token in the Authorization header:
```bash
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Owner Management Endpoints

### 1. Create Owner

#### Create a new owner profile
```bash
curl -X POST "http://localhost:8000/api/owners/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "address": "123 Main St, City, State 12345"
  }'
```

**Response:**
```json
{
  "id": 1,
  "phone_number": "+1234567890",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "address": "123 Main St, City, State 12345",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### 2. Get Owners

#### Get all owners with pagination
```bash
curl -X GET "http://localhost:8000/api/owners/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "owners": [
    {
      "id": 1,
      "phone_number": "+1234567890",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "address": "123 Main St, City, State 12345",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get owner by ID
```bash
curl -X GET "http://localhost:8000/api/owners/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "phone_number": "+1234567890",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "address": "123 Main St, City, State 12345",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get owner by phone number
```bash
curl -X GET "http://localhost:8000/api/owners/phone/+1234567890" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "phone_number": "+1234567890",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "address": "123 Main St, City, State 12345",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### 3. Update Owner

#### Update owner information
```bash
curl -X PATCH "http://localhost:8000/api/owners/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john.smith@example.com",
    "address": "456 Oak Ave, City, State 12345"
  }'
```

**Response:**
```json
{
  "id": 1,
  "phone_number": "+1234567890",
  "name": "John Smith",
  "email": "john.smith@example.com",
  "address": "456 Oak Ave, City, State 12345",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T13:00:00Z"
}
```

### 4. Delete Owner

#### Delete owner profile
```bash
curl -X DELETE "http://localhost:8000/api/owners/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```
HTTP/1.1 204 No Content
```

### 5. Search Owners

#### Search owners by name or phone number
```bash
curl -X GET "http://localhost:8000/api/owners/search/?q=John&skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "owners": [
    {
      "id": 1,
      "phone_number": "+1234567890",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "address": "123 Main St, City, State 12345",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    },
    {
      "id": 2,
      "phone_number": "+1234567891",
      "name": "John Smith",
      "email": "john.smith@example.com",
      "address": "456 Oak Ave, City, State 12345",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 2
}
```

## Query Parameters

### Pagination
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 1000)

### Search
- `q`: Search term for name or phone number

## Request Body Examples

### Create Owner
```json
{
  "phone_number": "+1234567890",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "address": "123 Main St, City, State 12345"
}
```

### Update Owner
```json
{
  "name": "John Smith",
  "email": "john.smith@example.com",
  "address": "456 Oak Ave, City, State 12345"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Phone number already exists"
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
  "detail": "Owner not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "phone_number"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
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

## Owner Management Flow

1. **Create** owner profile after user registration
2. **Retrieve** owner information by ID or phone number
3. **Update** owner information as needed
4. **Search** for owners by name or phone number
5. **Delete** owner profile when no longer needed

## Data Validation Rules

### Phone Number
- Must be in international format (e.g., +1234567890)
- Must be unique across all owners
- Required field

### Email
- Must be a valid email format
- Optional field
- Can be updated

### Name
- Required field
- String value
- Can be updated

### Address
- Optional field
- String value
- Can be updated

## Security Notes

- All endpoints require authentication
- Users can only access their own owner profiles
- Phone numbers must be unique
- Sensitive information is protected
- All operations are logged for audit purposes
