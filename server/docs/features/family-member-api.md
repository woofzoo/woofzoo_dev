# Family Member Management API Documentation

This document provides comprehensive curl commands for all family member management endpoints in the WoofZoo API.

## Base URL
All endpoints are prefixed with `/api/family-members`

## Authentication
All endpoints require authentication. Include the Bearer token in the Authorization header:
```bash
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Family Member Management Endpoints

### 1. Create Family Member

#### Create a new family member
```bash
curl -X POST "http://localhost:8000/api/family-members/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "family_id": 1,
    "user_id": 2,
    "role": "MEMBER",
    "permissions": {
      "can_view_pets": true,
      "can_edit_pets": false,
      "can_add_photos": true,
      "can_delete_photos": false
    }
  }'
```

**Response:**
```json
{
  "id": 1,
  "family_id": 1,
  "user_id": 2,
  "role": "MEMBER",
  "permissions": {
    "can_view_pets": true,
    "can_edit_pets": false,
    "can_add_photos": true,
    "can_delete_photos": false
  },
  "joined_at": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### 2. Get Family Members

#### Get all family members with pagination
```bash
curl -X GET "http://localhost:8000/api/family-members/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "family_members": [
    {
      "id": 1,
      "family_id": 1,
      "user_id": 2,
      "role": "MEMBER",
      "permissions": {
        "can_view_pets": true,
        "can_edit_pets": false,
        "can_add_photos": true,
        "can_delete_photos": false
      },
      "joined_at": "2024-01-01T12:00:00Z",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get family member by ID
```bash
curl -X GET "http://localhost:8000/api/family-members/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "family_id": 1,
  "user_id": 2,
  "role": "MEMBER",
  "permissions": {
    "can_view_pets": true,
    "can_edit_pets": false,
    "can_add_photos": true,
    "can_delete_photos": false
  },
  "joined_at": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get family members by family
```bash
curl -X GET "http://localhost:8000/api/family-members/family/1?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "family_members": [
    {
      "id": 1,
      "family_id": 1,
      "user_id": 2,
      "role": "MEMBER",
      "permissions": {
        "can_view_pets": true,
        "can_edit_pets": false,
        "can_add_photos": true,
        "can_delete_photos": false
      },
      "joined_at": "2024-01-01T12:00:00Z",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get family members by user
```bash
curl -X GET "http://localhost:8000/api/family-members/user/2?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "family_members": [
    {
      "id": 1,
      "family_id": 1,
      "user_id": 2,
      "role": "MEMBER",
      "permissions": {
        "can_view_pets": true,
        "can_edit_pets": false,
        "can_add_photos": true,
        "can_delete_photos": false
      },
      "joined_at": "2024-01-01T12:00:00Z",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

### 3. Update Family Member

#### Update family member information
```bash
curl -X PATCH "http://localhost:8000/api/family-members/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "ADMIN",
    "permissions": {
      "can_view_pets": true,
      "can_edit_pets": true,
      "can_add_photos": true,
      "can_delete_photos": true
    }
  }'
```

**Response:**
```json
{
  "id": 1,
  "family_id": 1,
  "user_id": 2,
  "role": "ADMIN",
  "permissions": {
    "can_view_pets": true,
    "can_edit_pets": true,
    "can_add_photos": true,
    "can_delete_photos": true
  },
  "joined_at": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T13:00:00Z"
}
```

### 4. Delete Family Member

#### Remove family member
```bash
curl -X DELETE "http://localhost:8000/api/family-members/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```
HTTP/1.1 204 No Content
```

### 5. Search Family Members

#### Search family members by role
```bash
curl -X GET "http://localhost:8000/api/family-members/search/?role=MEMBER&skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "family_members": [
    {
      "id": 1,
      "family_id": 1,
      "user_id": 2,
      "role": "MEMBER",
      "permissions": {
        "can_view_pets": true,
        "can_edit_pets": false,
        "can_add_photos": true,
        "can_delete_photos": false
      },
      "joined_at": "2024-01-01T12:00:00Z",
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
- `role`: Filter by member role (OWNER, ADMIN, MEMBER)

## Request Body Examples

### Create Family Member
```json
{
  "family_id": 1,
  "user_id": 2,
  "role": "MEMBER",
  "permissions": {
    "can_view_pets": true,
    "can_edit_pets": false,
    "can_add_photos": true,
    "can_delete_photos": false
  }
}
```

### Update Family Member
```json
{
  "role": "ADMIN",
  "permissions": {
    "can_view_pets": true,
    "can_edit_pets": true,
    "can_add_photos": true,
    "can_delete_photos": true
  }
}
```

## Member Roles

Available member roles:
- `OWNER`: Full access to family and pets
- `ADMIN`: Administrative access to family and pets
- `MEMBER`: Limited access based on permissions

## Permission Options

Available permissions:
- `can_view_pets`: Can view pet information
- `can_edit_pets`: Can edit pet information
- `can_add_photos`: Can add photos to pets
- `can_delete_photos`: Can delete photos from pets

## Error Responses

### 400 Bad Request
```json
{
  "detail": "User is already a member of this family"
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
  "detail": "Family member not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "family_id"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "user_id"],
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

## Family Member Management Flow

1. **Create** family member with role and permissions
2. **Retrieve** family member information by ID, family, or user
3. **Update** family member role and permissions
4. **Search** for family members by role
5. **Remove** family member when no longer needed

## Data Validation Rules

### Family ID
- Required field
- Must reference a valid family

### User ID
- Required field
- Must reference a valid user

### Role
- Required field
- Must be one of the predefined roles

### Permissions
- Optional field
- Object with boolean permission flags

## Security Notes

- All endpoints require authentication
- Users can only access family members of families they belong to
- Role-based access control is enforced
- Family member operations are logged for audit purposes
