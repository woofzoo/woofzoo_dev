# Family Invitation Management API Documentation

This document provides comprehensive curl commands for all family invitation management endpoints in the WoofZoo API.

## Base URL
All endpoints are prefixed with `/api/family-invitations`

## Authentication
All endpoints require authentication. Include the Bearer token in the Authorization header:
```bash
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Family Invitation Management Endpoints

### 1. Create Family Invitation

#### Send invitation to join family
```bash
curl -X POST "http://localhost:8000/api/family-invitations/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "family_id": 1,
    "invited_email": "john.doe@example.com",
    "invited_phone": "+1234567890",
    "role": "MEMBER",
    "permissions": {
      "can_view_pets": true,
      "can_edit_pets": false,
      "can_add_photos": true,
      "can_delete_photos": false
    },
    "message": "Please join our family to share pet photos!"
  }'
```

**Response:**
```json
{
  "id": 1,
  "family_id": 1,
  "invited_email": "john.doe@example.com",
  "invited_phone": "+1234567890",
  "role": "MEMBER",
  "permissions": {
    "can_view_pets": true,
    "can_edit_pets": false,
    "can_add_photos": true,
    "can_delete_photos": false
  },
  "message": "Please join our family to share pet photos!",
  "status": "PENDING",
  "expires_at": "2024-01-08T12:00:00Z",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### 2. Get Family Invitations

#### Get all invitations with pagination
```bash
curl -X GET "http://localhost:8000/api/family-invitations/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "invitations": [
    {
      "id": 1,
      "family_id": 1,
      "invited_email": "john.doe@example.com",
      "invited_phone": "+1234567890",
      "role": "MEMBER",
      "permissions": {
        "can_view_pets": true,
        "can_edit_pets": false,
        "can_add_photos": true,
        "can_delete_photos": false
      },
      "message": "Please join our family to share pet photos!",
      "status": "PENDING",
      "expires_at": "2024-01-08T12:00:00Z",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get invitation by ID
```bash
curl -X GET "http://localhost:8000/api/family-invitations/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "family_id": 1,
  "invited_email": "john.doe@example.com",
  "invited_phone": "+1234567890",
  "role": "MEMBER",
  "permissions": {
    "can_view_pets": true,
    "can_edit_pets": false,
    "can_add_photos": true,
    "can_delete_photos": false
  },
  "message": "Please join our family to share pet photos!",
  "status": "PENDING",
  "expires_at": "2024-01-08T12:00:00Z",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get invitations by family
```bash
curl -X GET "http://localhost:8000/api/family-invitations/family/1?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "invitations": [
    {
      "id": 1,
      "family_id": 1,
      "invited_email": "john.doe@example.com",
      "invited_phone": "+1234567890",
      "role": "MEMBER",
      "permissions": {
        "can_view_pets": true,
        "can_edit_pets": false,
        "can_add_photos": true,
        "can_delete_photos": false
      },
      "message": "Please join our family to share pet photos!",
      "status": "PENDING",
      "expires_at": "2024-01-08T12:00:00Z",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get invitations by email
```bash
curl -X GET "http://localhost:8000/api/family-invitations/email/john.doe@example.com?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "invitations": [
    {
      "id": 1,
      "family_id": 1,
      "invited_email": "john.doe@example.com",
      "invited_phone": "+1234567890",
      "role": "MEMBER",
      "permissions": {
        "can_view_pets": true,
        "can_edit_pets": false,
        "can_add_photos": true,
        "can_delete_photos": false
      },
      "message": "Please join our family to share pet photos!",
      "status": "PENDING",
      "expires_at": "2024-01-08T12:00:00Z",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

### 3. Accept Family Invitation

#### Accept invitation to join family
```bash
curl -X POST "http://localhost:8000/api/family-invitations/1/accept" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "Invitation accepted successfully",
  "family_member": {
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
}
```

### 4. Reject Family Invitation

#### Reject invitation to join family
```bash
curl -X POST "http://localhost:8000/api/family-invitations/1/reject" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "Invitation rejected successfully"
}
```

### 5. Resend Family Invitation

#### Resend expired invitation
```bash
curl -X POST "http://localhost:8000/api/family-invitations/1/resend" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "family_id": 1,
  "invited_email": "john.doe@example.com",
  "invited_phone": "+1234567890",
  "role": "MEMBER",
  "permissions": {
    "can_view_pets": true,
    "can_edit_pets": false,
    "can_add_photos": true,
    "can_delete_photos": false
  },
  "message": "Please join our family to share pet photos!",
  "status": "PENDING",
  "expires_at": "2024-01-08T12:00:00Z",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### 6. Cancel Family Invitation

#### Cancel pending invitation
```bash
curl -X DELETE "http://localhost:8000/api/family-invitations/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```
HTTP/1.1 204 No Content
```

### 7. Search Family Invitations

#### Search invitations by status
```bash
curl -X GET "http://localhost:8000/api/family-invitations/search/?status=PENDING&skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "invitations": [
    {
      "id": 1,
      "family_id": 1,
      "invited_email": "john.doe@example.com",
      "invited_phone": "+1234567890",
      "role": "MEMBER",
      "permissions": {
        "can_view_pets": true,
        "can_edit_pets": false,
        "can_add_photos": true,
        "can_delete_photos": false
      },
      "message": "Please join our family to share pet photos!",
      "status": "PENDING",
      "expires_at": "2024-01-08T12:00:00Z",
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
- `status`: Filter by invitation status (PENDING, ACCEPTED, REJECTED, EXPIRED)

## Request Body Examples

### Create Family Invitation
```json
{
  "family_id": 1,
  "invited_email": "john.doe@example.com",
  "invited_phone": "+1234567890",
  "role": "MEMBER",
  "permissions": {
    "can_view_pets": true,
    "can_edit_pets": false,
    "can_add_photos": true,
    "can_delete_photos": false
  },
  "message": "Please join our family to share pet photos!"
}
```

## Invitation Status

Available invitation statuses:
- `PENDING`: Invitation sent, waiting for response
- `ACCEPTED`: Invitation accepted, user joined family
- `REJECTED`: Invitation rejected by user
- `EXPIRED`: Invitation expired without response

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
  "detail": "Invitation already exists for this email and family"
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
  "detail": "Invitation not found"
}
```

### 409 Conflict
```json
{
  "detail": "Invitation has already been accepted"
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
      "loc": ["body", "invited_email"],
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

## Family Invitation Management Flow

1. **Create** invitation with role and permissions
2. **Retrieve** invitation information by ID, family, or email
3. **Accept** invitation to join family
4. **Reject** invitation to decline
5. **Resend** expired invitation
6. **Cancel** pending invitation
7. **Search** for invitations by status

## Data Validation Rules

### Family ID
- Required field
- Must reference a valid family

### Invited Email
- Required field
- Must be a valid email format
- Must be unique per family

### Invited Phone
- Optional field
- Must be a valid phone number format

### Role
- Required field
- Must be one of the predefined roles

### Permissions
- Optional field
- Object with boolean permission flags

### Message
- Optional field
- String value for invitation message

## Security Notes

- All endpoints require authentication
- Users can only access invitations for families they own
- Invitations expire after 7 days by default
- Invitation operations are logged for audit purposes
- Email notifications are sent for invitation events
