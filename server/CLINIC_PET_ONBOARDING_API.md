# Clinic Pet Onboarding API

## Overview

The Clinic Pet Onboarding API allows clinic owners to register pets and automatically create or link pet owner accounts. This streamlines the onboarding process when a pet visits a clinic for the first time.

## Endpoint

**POST** `/api/pets/clinic-onboard`

**Authentication Required:** Yes (JWT token with `clinic_owner` role)

## How It Works

1. **Clinic submits pet and owner information**
2. **System checks if owner email exists:**
   - If **YES**: Links pet to existing user account
   - If **NO**: Creates new user account with random password and `pet_owner` role
3. **Pet is created** with unique `pet_id`
4. **Owner is marked as admin** of the pet (via `pet.owner_id`)
5. **Email is sent** to owner:
   - New users: Receives verification email to activate account
   - Existing users: Receives notification that pet was registered

## Request Body

```json
{
  "owner_email": "john.doe@example.com",  // Required
  "owner_phone": "+1234567890",           // Optional
  "owner_name": "John Doe",               // Optional
  "pet_name": "Buddy",                    // Required
  "pet_type": "DOG",                      // Required
  "breed": "Golden Retriever",            // Required
  "age": 3,                               // Optional
  "gender": "MALE",                       // Optional
  "weight": 25.5,                         // Optional
  "emergency_contacts": {                 // Optional
    "vet": {
      "name": "Dr. Smith",
      "phone": "+1234567890"
    }
  },
  "insurance_info": {                     // Optional
    "provider": "PetCare Insurance",
    "policy_number": "PC123456789"
  }
}
```

## Response

**Success (201 Created):**

```json
{
  "pet": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "pet_id": "DOG-GOLDEN-RETRIEVER-000001",
    "owner_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Buddy",
    "pet_type": "DOG",
    "breed": "Golden Retriever",
    "age": 3,
    "gender": "MALE",
    "weight": 25.5,
    "photos": [],
    "emergency_contacts": {},
    "insurance_info": {},
    "is_active": true,
    "created_at": "2025-01-01T12:00:00Z",
    "updated_at": "2025-01-01T12:00:00Z"
  },
  "owner_created": true,
  "message": "Pet onboarded successfully. A new account was created for the owner. Verification email sent."
}
```

**Error Responses:**

- **400 Bad Request**: Invalid data or validation error
- **403 Forbidden**: User doesn't have `clinic_owner` role
- **500 Internal Server Error**: Server-side error

## Usage Example (cURL)

```bash
curl -X POST "http://localhost:8000/api/pets/clinic-onboard" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "owner_email": "john.doe@example.com",
    "owner_name": "John Doe",
    "owner_phone": "+1234567890",
    "pet_name": "Buddy",
    "pet_type": "DOG",
    "breed": "Golden Retriever",
    "age": 3,
    "gender": "MALE",
    "weight": 25.5
  }'
```

## Usage Example (Python)

```python
import requests

# Get your JWT token first (from login)
token = "your_jwt_token_here"

# Prepare the request
url = "http://localhost:8000/api/pets/clinic-onboard"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
data = {
    "owner_email": "john.doe@example.com",
    "owner_name": "John Doe",
    "owner_phone": "+1234567890",
    "pet_name": "Buddy",
    "pet_type": "DOG",
    "breed": "Golden Retriever",
    "age": 3,
    "gender": "MALE",
    "weight": 25.5,
    "emergency_contacts": {
        "vet": {"name": "Dr. Smith", "phone": "+1234567890"}
    }
}

# Make the request
response = requests.post(url, headers=headers, json=data)

# Check response
if response.status_code == 201:
    result = response.json()
    print(f"Pet onboarded successfully!")
    print(f"Pet ID: {result['pet']['pet_id']}")
    print(f"New user created: {result['owner_created']}")
    print(f"Message: {result['message']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

## Email Notifications

### New User Email

When a new owner account is created, they receive an email with:
- Pet registration details (name, type, breed, registered by clinic)
- Account creation notice
- **Email verification link** (must verify within 24 hours by default)
- Instructions on accessing their account

### Existing User Email

When the owner already has an account, they receive:
- Pet registration details
- Notification that the pet was added to their account
- No verification needed (already verified)

## Important Notes

1. **Owner Table Status**: The `owners` table is **DEPRECATED**. All pet owners are now entries in the `users` table with the `pet_owner` role.

2. **Pet Ownership**: The `pet.owner_id` field references `users.public_id`, making that user the admin/owner of the pet.

3. **Password Generation**: For new users, a random secure password is generated automatically. Users should use the "forgot password" flow to set their own password after verifying their email.

4. **Email Validation**: The `owner_email` field must be a valid email address format.

5. **Pet Type/Breed**: Must match the valid pet types and breeds defined in the system.

6. **Gender**: Must be either "MALE" or "FEMALE" (case-insensitive, will be converted to uppercase).

## Testing

To test the API:

1. **Create a clinic owner user** (with `clinic_owner` role)
2. **Login** to get a JWT token
3. **Call the endpoint** with pet and owner information
4. **Check the response** for success
5. **Verify the email** was sent (check logs in debug mode)
6. **Check the database** to confirm:
   - User was created (if new) in `users` table
   - Pet was created in `pets` table
   - Pet's `owner_id` matches user's `public_id`

## Security

- Only users with `clinic_owner` role can access this endpoint
- JWT authentication is required
- Email verification is enforced for new accounts
- Passwords are securely hashed using bcrypt

## Future Enhancements

- Add clinic name to email notifications (currently shows "Clinic" as placeholder)
- Support bulk pet onboarding
- Add option to skip email sending
- Add audit logging for onboarding events

