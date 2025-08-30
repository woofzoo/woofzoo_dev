# Pet Types API Documentation

This document provides comprehensive curl commands for all pet types endpoints in the WoofZoo API.

## Base URL
All endpoints are prefixed with `/api/pet-types`

## Authentication
Most endpoints require authentication. Include the Bearer token in the Authorization header:
```bash
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Pet Types Endpoints

### 1. Get Pet Types

#### Get all pet types
```bash
curl -X GET "http://localhost:8000/api/pet-types/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "pet_types": [
    {
      "id": 1,
      "name": "DOG",
      "display_name": "Dog",
      "description": "Domesticated canine companion",
      "icon": "🐕",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    },
    {
      "id": 2,
      "name": "CAT",
      "display_name": "Cat",
      "description": "Domesticated feline companion",
      "icon": "🐱",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    },
    {
      "id": 3,
      "name": "BIRD",
      "display_name": "Bird",
      "description": "Feathered companion",
      "icon": "🐦",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    },
    {
      "id": 4,
      "name": "FISH",
      "display_name": "Fish",
      "description": "Aquatic companion",
      "icon": "🐠",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    },
    {
      "id": 5,
      "name": "REPTILE",
      "display_name": "Reptile",
      "description": "Scaly companion",
      "icon": "🦎",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    },
    {
      "id": 6,
      "name": "SMALL_ANIMAL",
      "display_name": "Small Animal",
      "description": "Small companion animals",
      "icon": "🐹",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    },
    {
      "id": 7,
      "name": "OTHER",
      "display_name": "Other",
      "description": "Other types of pets",
      "icon": "🐾",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 7
}
```

#### Get pet type by ID
```bash
curl -X GET "http://localhost:8000/api/pet-types/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "name": "DOG",
  "display_name": "Dog",
  "description": "Domesticated canine companion",
  "icon": "🐕",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get pet type by name
```bash
curl -X GET "http://localhost:8000/api/pet-types/name/DOG" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "name": "DOG",
  "display_name": "Dog",
  "description": "Domesticated canine companion",
  "icon": "🐕",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### 2. Create Pet Type (Admin Only)

#### Create a new pet type
```bash
curl -X POST "http://localhost:8000/api/pet-types/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "HORSE",
    "display_name": "Horse",
    "description": "Large domesticated equine companion",
    "icon": "🐎"
  }'
```

**Response:**
```json
{
  "id": 8,
  "name": "HORSE",
  "display_name": "Horse",
  "description": "Large domesticated equine companion",
  "icon": "🐎",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### 3. Update Pet Type (Admin Only)

#### Update pet type information
```bash
curl -X PATCH "http://localhost:8000/api/pet-types/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "Canine Companion",
    "description": "Updated description for dogs"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "DOG",
  "display_name": "Canine Companion",
  "description": "Updated description for dogs",
  "icon": "🐕",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T13:00:00Z"
}
```

### 4. Delete Pet Type (Admin Only)

#### Delete pet type
```bash
curl -X DELETE "http://localhost:8000/api/pet-types/8" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```
HTTP/1.1 204 No Content
```

### 5. Search Pet Types

#### Search pet types by name
```bash
curl -X GET "http://localhost:8000/api/pet-types/search/?q=dog&skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "pet_types": [
    {
      "id": 1,
      "name": "DOG",
      "display_name": "Dog",
      "description": "Domesticated canine companion",
      "icon": "🐕",
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
- `q`: Search term for pet type name or display name

## Request Body Examples

### Create Pet Type
```json
{
  "name": "HORSE",
  "display_name": "Horse",
  "description": "Large domesticated equine companion",
  "icon": "🐎"
}
```

### Update Pet Type
```json
{
  "display_name": "Canine Companion",
  "description": "Updated description for dogs"
}
```

## Default Pet Types

The system comes with these default pet types:

| Name | Display Name | Description | Icon |
|------|--------------|-------------|------|
| DOG | Dog | Domesticated canine companion | 🐕 |
| CAT | Cat | Domesticated feline companion | 🐱 |
| BIRD | Bird | Feathered companion | 🐦 |
| FISH | Fish | Aquatic companion | 🐠 |
| REPTILE | Reptile | Scaly companion | 🦎 |
| SMALL_ANIMAL | Small Animal | Small companion animals | 🐹 |
| OTHER | Other | Other types of pets | 🐾 |

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Pet type name already exists"
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
  "detail": "Access denied - Admin privileges required"
}
```

### 404 Not Found
```json
{
  "detail": "Pet type not found"
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
    },
    {
      "loc": ["body", "display_name"],
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

## Pet Types Management Flow

1. **Retrieve** all available pet types
2. **Get** specific pet type by ID or name
3. **Search** for pet types by name or display name
4. **Create** new pet types (admin only)
5. **Update** pet type information (admin only)
6. **Delete** pet types (admin only)

## Data Validation Rules

### Name
- Required field
- String value
- Must be unique
- Should be in UPPER_CASE format

### Display Name
- Required field
- String value
- Human-readable name

### Description
- Optional field
- String value
- Detailed description of the pet type

### Icon
- Optional field
- String value
- Unicode emoji or icon representation

## Security Notes

- Read operations are available to all authenticated users
- Create, update, and delete operations require admin privileges
- Pet types are used as reference data for pet creation
- Deleting a pet type may affect existing pets
- Pet type operations are logged for audit purposes

## Usage Examples

### Get Pet Types for Dropdown
```bash
curl -X GET "http://localhost:8000/api/pet-types/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Validate Pet Type Before Creating Pet
```bash
curl -X GET "http://localhost:8000/api/pet-types/name/DOG" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Search for Pet Types
```bash
curl -X GET "http://localhost:8000/api/pet-types/search/?q=cat" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
