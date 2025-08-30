# Pet Management API Documentation

This document provides comprehensive curl commands for all pet management endpoints in the WoofZoo API.

## Base URL
All endpoints are prefixed with `/api/pets`

## Authentication
Most endpoints require authentication. Include the Bearer token in the Authorization header:
```bash
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Pet Management Endpoints

### 1. Create Pet

#### Create a new pet
```bash
curl -X POST "http://localhost:8000/api/pets/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Buddy",
    "pet_type": "DOG",
    "breed": "Golden Retriever",
    "age": 3,
    "gender": "MALE",
    "weight": 25.5,
    "owner_id": 1,
    "emergency_contacts": {
      "vet": {
        "name": "Dr. Smith",
        "phone": "+1234567890"
      },
      "owner": {
        "name": "John Doe",
        "phone": "+1234567890"
      }
    },
    "insurance_info": {
      "provider": "PetCare Insurance",
      "policy_number": "PC123456789"
    }
  }'
```

**Response:**
```json
{
  "id": 1,
  "pet_id": "PET_001",
  "name": "Buddy",
  "pet_type": "DOG",
  "breed": "Golden Retriever",
  "age": 3,
  "gender": "MALE",
  "weight": 25.5,
  "owner_id": 1,
  "emergency_contacts": {
    "vet": {
      "name": "Dr. Smith",
      "phone": "+1234567890"
    },
    "owner": {
      "name": "John Doe",
      "phone": "+1234567890"
    }
  },
  "insurance_info": {
    "provider": "PetCare Insurance",
    "policy_number": "PC123456789"
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### 2. Get Pets

#### Get all pets with pagination
```bash
curl -X GET "http://localhost:8000/api/pets/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "pets": [
    {
      "id": 1,
      "pet_id": "PET_001",
      "name": "Buddy",
      "pet_type": "DOG",
      "breed": "Golden Retriever",
      "age": 3,
      "gender": "MALE",
      "weight": 25.5,
      "owner_id": 1,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get pet by ID
```bash
curl -X GET "http://localhost:8000/api/pets/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "pet_id": "PET_001",
  "name": "Buddy",
  "pet_type": "DOG",
  "breed": "Golden Retriever",
  "age": 3,
  "gender": "MALE",
  "weight": 25.5,
  "owner_id": 1,
  "emergency_contacts": {
    "vet": {
      "name": "Dr. Smith",
      "phone": "+1234567890"
    },
    "owner": {
      "name": "John Doe",
      "phone": "+1234567890"
    }
  },
  "insurance_info": {
    "provider": "PetCare Insurance",
    "policy_number": "PC123456789"
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get pet by pet ID (public endpoint)
```bash
curl -X GET "http://localhost:8000/api/pets/pet-id/PET_001"
```

**Response:**
```json
{
  "id": 1,
  "pet_id": "PET_001",
  "name": "Buddy",
  "pet_type": "DOG",
  "breed": "Golden Retriever",
  "age": 3,
  "gender": "MALE",
  "weight": 25.5,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get pets by owner
```bash
curl -X GET "http://localhost:8000/api/pets/owner/1?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "pets": [
    {
      "id": 1,
      "pet_id": "PET_001",
      "name": "Buddy",
      "pet_type": "DOG",
      "breed": "Golden Retriever",
      "age": 3,
      "gender": "MALE",
      "weight": 25.5,
      "owner_id": 1,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

### 3. Update Pet

#### Update pet information
```bash
curl -X PATCH "http://localhost:8000/api/pets/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Buddy Jr",
    "age": 4,
    "weight": 26.0
  }'
```

**Response:**
```json
{
  "id": 1,
  "pet_id": "PET_001",
  "name": "Buddy Jr",
  "pet_type": "DOG",
  "breed": "Golden Retriever",
  "age": 4,
  "gender": "MALE",
  "weight": 26.0,
  "owner_id": 1,
  "emergency_contacts": {
    "vet": {
      "name": "Dr. Smith",
      "phone": "+1234567890"
    },
    "owner": {
      "name": "John Doe",
      "phone": "+1234567890"
    }
  },
  "insurance_info": {
    "provider": "PetCare Insurance",
    "policy_number": "PC123456789"
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T13:00:00Z"
}
```

### 4. Delete Pet

#### Delete pet
```bash
curl -X DELETE "http://localhost:8000/api/pets/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```
HTTP/1.1 204 No Content
```

### 5. Search Pets

#### Search pets by name
```bash
curl -X GET "http://localhost:8000/api/pets/search/?q=Buddy&skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "pets": [
    {
      "id": 1,
      "pet_id": "PET_001",
      "name": "Buddy",
      "pet_type": "DOG",
      "breed": "Golden Retriever",
      "age": 3,
      "gender": "MALE",
      "weight": 25.5,
      "owner_id": 1,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get pets by type
```bash
curl -X GET "http://localhost:8000/api/pets/type/DOG?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "pets": [
    {
      "id": 1,
      "pet_id": "PET_001",
      "name": "Buddy",
      "pet_type": "DOG",
      "breed": "Golden Retriever",
      "age": 3,
      "gender": "MALE",
      "weight": 25.5,
      "owner_id": 1,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get pets by breed
```bash
curl -X GET "http://localhost:8000/api/pets/breed/Golden%20Retriever?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "pets": [
    {
      "id": 1,
      "pet_id": "PET_001",
      "name": "Buddy",
      "pet_type": "DOG",
      "breed": "Golden Retriever",
      "age": 3,
      "gender": "MALE",
      "weight": 25.5,
      "owner_id": 1,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
```

### 6. Pet Lookup

#### Public pet lookup
```bash
curl -X POST "http://localhost:8000/api/pets/lookup" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "PET_001"
  }'
```

**Response:**
```json
{
  "id": 1,
  "pet_id": "PET_001",
  "name": "Buddy",
  "pet_type": "DOG",
  "breed": "Golden Retriever",
  "age": 3,
  "gender": "MALE",
  "weight": 25.5,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

## Query Parameters

### Pagination
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 1000)

### Search
- `q`: Search term for pet name

## Request Body Examples

### Create Pet
```json
{
  "name": "Buddy",
  "pet_type": "DOG",
  "breed": "Golden Retriever",
  "age": 3,
  "gender": "MALE",
  "weight": 25.5,
  "owner_id": 1,
  "emergency_contacts": {
    "vet": {
      "name": "Dr. Smith",
      "phone": "+1234567890"
    },
    "owner": {
      "name": "John Doe",
      "phone": "+1234567890"
    }
  },
  "insurance_info": {
    "provider": "PetCare Insurance",
    "policy_number": "PC123456789"
  }
}
```

### Update Pet
```json
{
  "name": "Buddy Jr",
  "age": 4,
  "weight": 26.0
}
```

### Pet Lookup
```json
{
  "pet_id": "PET_001"
}
```

## Pet Types

Available pet types:
- `DOG`
- `CAT`
- `BIRD`
- `FISH`
- `REPTILE`
- `SMALL_ANIMAL`
- `OTHER`

## Gender Options

Available gender options:
- `MALE`
- `FEMALE`
- `UNKNOWN`

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Pet name already exists for this owner"
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
  "detail": "Pet not found"
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
      "loc": ["body", "age"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
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

## Pet Management Flow

1. **Create** pet profile with owner information
2. **Retrieve** pet information by ID or pet ID
3. **Update** pet information as needed
4. **Search** for pets by name, type, or breed
5. **Delete** pet profile when no longer needed
6. **Public lookup** for sharing pet information

## Data Validation Rules

### Name
- Required field
- String value
- Must be unique per owner

### Pet Type
- Required field
- Must be one of the predefined types

### Breed
- Required field
- String value

### Age
- Required field
- Integer value
- Must be greater than 0

### Gender
- Required field
- Must be one of the predefined options

### Weight
- Optional field
- Float value
- Must be greater than 0

### Owner ID
- Required field
- Must reference a valid owner

## Security Notes

- Most endpoints require authentication
- Users can only access pets they own
- Public lookup endpoint is available for sharing
- Pet IDs are unique and auto-generated
- All operations are logged for audit purposes
