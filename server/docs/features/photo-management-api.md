# Photo Management API Documentation

This document provides comprehensive curl commands for all photo management endpoints in the WoofZoo API.

## Base URL
All endpoints are prefixed with `/api/photos`

## Authentication
Most endpoints require authentication. Include the Bearer token in the Authorization header:
```bash
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Photo Management Endpoints

### 1. Create Upload Request

#### Request pre-signed URL for photo upload
```bash
curl -X POST "http://localhost:8000/api/photos/upload-request" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "file_name": "buddy_photo.jpg",
    "file_size": 2048576,
    "content_type": "image/jpeg",
    "description": "Buddy playing in the park"
  }'
```

**Response:**
```json
{
  "upload_request_id": "req_123456",
  "upload_url": "https://storage.example.com/upload?token=abc123",
  "file_name": "buddy_photo.jpg",
  "expires_at": "2024-01-01T13:00:00Z"
}
```

### 2. Create Photo

#### Create photo record after successful upload
```bash
curl -X POST "http://localhost:8000/api/photos/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "uploader_id": 1,
    "file_name": "buddy_photo.jpg",
    "file_size": 2048576,
    "content_type": "image/jpeg",
    "description": "Buddy playing in the park",
    "upload_request_id": "req_123456",
    "metadata": {
      "location": "Central Park",
      "tags": ["playful", "outdoor"]
    }
  }'
```

**Response:**
```json
{
  "id": 1,
  "pet_id": 1,
  "uploader_id": 1,
  "file_name": "buddy_photo.jpg",
  "file_size": 2048576,
  "content_type": "image/jpeg",
  "description": "Buddy playing in the park",
  "is_primary": false,
  "metadata": {
    "location": "Central Park",
    "tags": ["playful", "outdoor"]
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### 3. Get Photos

#### Get all photos with pagination
```bash
curl -X GET "http://localhost:8000/api/photos/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "photos": [
    {
      "id": 1,
      "pet_id": 1,
      "uploader_id": 1,
      "file_name": "buddy_photo.jpg",
      "file_size": 2048576,
      "content_type": "image/jpeg",
      "description": "Buddy playing in the park",
      "is_primary": false,
      "metadata": {
        "location": "Central Park",
        "tags": ["playful", "outdoor"]
      },
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get photo by ID
```bash
curl -X GET "http://localhost:8000/api/photos/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "pet_id": 1,
  "uploader_id": 1,
  "file_name": "buddy_photo.jpg",
  "file_size": 2048576,
  "content_type": "image/jpeg",
  "description": "Buddy playing in the park",
  "is_primary": false,
  "metadata": {
    "location": "Central Park",
    "tags": ["playful", "outdoor"]
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get photos by pet
```bash
curl -X GET "http://localhost:8000/api/photos/pet/1?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "photos": [
    {
      "id": 1,
      "pet_id": 1,
      "uploader_id": 1,
      "file_name": "buddy_photo.jpg",
      "file_size": 2048576,
      "content_type": "image/jpeg",
      "description": "Buddy playing in the park",
      "is_primary": false,
      "metadata": {
        "location": "Central Park",
        "tags": ["playful", "outdoor"]
      },
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get primary photo by pet
```bash
curl -X GET "http://localhost:8000/api/photos/pet/1/primary" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "pet_id": 1,
  "uploader_id": 1,
  "file_name": "buddy_photo.jpg",
  "file_size": 2048576,
  "content_type": "image/jpeg",
  "description": "Buddy playing in the park",
  "is_primary": true,
  "metadata": {
    "location": "Central Park",
    "tags": ["playful", "outdoor"]
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get photos by uploader
```bash
curl -X GET "http://localhost:8000/api/photos/uploader/1?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "photos": [
    {
      "id": 1,
      "pet_id": 1,
      "uploader_id": 1,
      "file_name": "buddy_photo.jpg",
      "file_size": 2048576,
      "content_type": "image/jpeg",
      "description": "Buddy playing in the park",
      "is_primary": false,
      "metadata": {
        "location": "Central Park",
        "tags": ["playful", "outdoor"]
      },
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

### 4. Get Download URL

#### Get download URL for photo
```bash
curl -X GET "http://localhost:8000/api/photos/1/download" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "download_url": "https://storage.example.com/photos/buddy_photo.jpg?token=xyz789",
  "expires_at": "2024-01-01T13:00:00Z"
}
```

### 5. Update Photo

#### Update photo information
```bash
curl -X PATCH "http://localhost:8000/api/photos/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description",
    "metadata": {
      "location": "Updated Location",
      "tags": ["updated", "tags"]
    }
  }'
```

**Response:**
```json
{
  "id": 1,
  "pet_id": 1,
  "uploader_id": 1,
  "file_name": "buddy_photo.jpg",
  "file_size": 2048576,
  "content_type": "image/jpeg",
  "description": "Updated description",
  "is_primary": false,
  "metadata": {
    "location": "Updated Location",
    "tags": ["updated", "tags"]
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T13:00:00Z"
}
```

### 6. Set Primary Photo

#### Set photo as primary for pet
```bash
curl -X POST "http://localhost:8000/api/photos/1/set-primary" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "pet_id": 1,
  "uploader_id": 1,
  "file_name": "buddy_photo.jpg",
  "file_size": 2048576,
  "content_type": "image/jpeg",
  "description": "Buddy playing in the park",
  "is_primary": true,
  "metadata": {
    "location": "Central Park",
    "tags": ["playful", "outdoor"]
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T13:00:00Z"
}
```

### 7. Delete Photo

#### Soft delete photo
```bash
curl -X DELETE "http://localhost:8000/api/photos/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```
HTTP/1.1 204 No Content
```

#### Hard delete photo
```bash
curl -X DELETE "http://localhost:8000/api/photos/1?hard_delete=true" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```
HTTP/1.1 204 No Content
```

### 8. Search Photos

#### Search photos by description
```bash
curl -X GET "http://localhost:8000/api/photos/search/?q=park&skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "photos": [
    {
      "id": 1,
      "pet_id": 1,
      "uploader_id": 1,
      "file_name": "buddy_photo.jpg",
      "file_size": 2048576,
      "content_type": "image/jpeg",
      "description": "Buddy playing in the park",
      "is_primary": false,
      "metadata": {
        "location": "Central Park",
        "tags": ["playful", "outdoor"]
      },
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
- `q`: Search term for photo description

### Delete
- `hard_delete`: Set to `true` for permanent deletion (default: false)

## Request Body Examples

### Create Upload Request
```json
{
  "pet_id": 1,
  "file_name": "buddy_photo.jpg",
  "file_size": 2048576,
  "content_type": "image/jpeg",
  "description": "Buddy playing in the park"
}
```

### Create Photo
```json
{
  "pet_id": 1,
  "uploader_id": 1,
  "file_name": "buddy_photo.jpg",
  "file_size": 2048576,
  "content_type": "image/jpeg",
  "description": "Buddy playing in the park",
  "upload_request_id": "req_123456",
  "metadata": {
    "location": "Central Park",
    "tags": ["playful", "outdoor"]
  }
}
```

### Update Photo
```json
{
  "description": "Updated description",
  "metadata": {
    "location": "Updated Location",
    "tags": ["updated", "tags"]
  }
}
```

## Supported File Types

Supported content types:
- `image/jpeg`
- `image/png`
- `image/gif`
- `image/webp`

## File Size Limits

- Maximum file size: 10MB
- Recommended file size: 2MB or less

## Error Responses

### 400 Bad Request
```json
{
  "detail": "File size exceeds maximum limit"
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
  "detail": "Photo not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "pet_id"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "file_name"],
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

## Photo Management Flow

1. **Request** pre-signed upload URL
2. **Upload** photo to storage using the URL
3. **Create** photo record after successful upload
4. **Retrieve** photo information by ID, pet, or uploader
5. **Update** photo description and metadata
6. **Set** primary photo for pet
7. **Get** download URL for viewing
8. **Delete** photo (soft or hard delete)
9. **Search** for photos by description

## Data Validation Rules

### Pet ID
- Required field
- Must reference a valid pet

### Uploader ID
- Required field
- Must reference a valid user

### File Name
- Required field
- String value
- Must be unique per pet

### File Size
- Required field
- Integer value
- Must be within size limits

### Content Type
- Required field
- Must be a supported image type

### Description
- Optional field
- String value

### Metadata
- Optional field
- JSON object with custom data

## Security Notes

- Most endpoints require authentication
- Users can only access photos of pets they own or have access to
- Upload URLs expire after 1 hour
- Download URLs expire after 24 hours
- Soft delete is used by default for data recovery
- Photo operations are logged for audit purposes
