# Family Management API Documentation

This document provides comprehensive curl commands for all family management endpoints in the WoofZoo API.

## Base URL
All endpoints are prefixed with `/api/families`

## Authentication
All endpoints require authentication. Include the Bearer token in the Authorization header:
```bash
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Family Management Endpoints

### 1. Create Family

#### Create a new family
```bash
curl -X POST "http://localhost:8000/api/families/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smith Family",
    "description": "Our loving family with pets",
    "owner_id": 1
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Smith Family",
  "description": "Our loving family with pets",
  "owner_id": 1,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### 2. Get Families

#### Get all families with pagination
```bash
curl -X GET "http://localhost:8000/api/families/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "families": [
    {
      "id": 1,
      "name": "Smith Family",
      "description": "Our loving family with pets",
      "owner_id": 1,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get family by ID
```bash
curl -X GET "http://localhost:8000/api/families/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "name": "Smith Family",
  "description": "Our loving family with pets",
  "owner_id": 1,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get families by owner
```bash
curl -X GET "http://localhost:8000/api/families/owner/1?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "families": [
    {
      "id": 1,
      "name": "Smith Family",
      "description": "Our loving family with pets",
      "owner_id": 1,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

### 3. Update Family

#### Update family information
```bash
curl -X PATCH "http://localhost:8000/api/families/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smith Family Updated",
    "description": "Updated family description"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Smith Family Updated",
  "description": "Updated family description",
  "owner_id": 1,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T13:00:00Z"
}
```

### 4. Delete Family

#### Delete family
```bash
curl -X DELETE "http://localhost:8000/api/families/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```
HTTP/1.1 204 No Content
```

### 5. Search Families

#### Search families by name
```bash
curl -X GET "http://localhost:8000/api/families/search/?q=Smith&skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "families": [
    {
      "id": 1,
      "name": "Smith Family",
      "description": "Our loving family with pets",
      "owner_id": 1,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

## Query Parameters

### Pagination
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 1000)

### Search
- `q`: Search term for family name

## Request Body Examples

### Create Family
```json
{
  "name": "Smith Family",
  "description": "Our loving family with pets",
  "owner_id": 1
}
```

### Update Family
```json
{
  "name": "Smith Family Updated",
  "description": "Updated family description"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Family name already exists for this owner"
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
  "detail": "Family not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
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

## Family Management Flow

1. **Create** family profile with owner information
2. **Retrieve** family information by ID or owner
3. **Update** family information as needed
4. **Search** for families by name
5. **Delete** family profile when no longer needed

## Data Validation Rules

### Name
- Required field
- String value
- Must be unique per owner

### Description
- Optional field
- String value

### Owner ID
- Required field
- Must reference a valid owner

## Security Notes

- All endpoints require authentication
- Users can only access families they own
- Family operations are logged for audit purposes
