# API Development & Security Rules

## API Development

- Use role-based access control with FastAPI dependencies
- Always include proper error handling and logging
- Provide comprehensive docstrings
- Include request/response examples in schemas

---

## Role-Based Access Control (RBAC)

### Enforce RBAC at Route Level

Use FastAPI dependencies to enforce roles at the route level:

```python
@router.post("/clinic-only-endpoint")
def clinic_endpoint(
    request_data: RequestSchema,
    current_user: User = Depends(get_clinic_owner_user),  # Role check!
    controller: Controller = Depends(get_controller)
):
    """
    Endpoint accessible only by clinic_owner role.
    
    Authorization is enforced by the get_clinic_owner_user dependency.
    """
    return controller.handle_request(request_data, current_user)
```

### Available Role Dependencies

```python
# Use these convenience dependencies for common roles
get_clinic_owner_user = require_roles(["clinic_owner"])
get_pet_owner_user = require_roles(["pet_owner"])
get_doctor_user = require_roles(["doctor"])

# For multiple roles
get_clinic_or_doctor_user = require_roles(["clinic_owner", "doctor"])
```

### Custom Role Checks

```python
from app.dependencies import require_roles

# Create custom role dependency
get_admin_user = require_roles(["admin"])

@router.delete("/admin/delete-user/{user_id}")
def delete_user(
    user_id: uuid.UUID,
    current_user: User = Depends(get_admin_user)
):
    """Only admins can delete users."""
    # Role is already checked by dependency
```

---

## Input Validation

### Use Pydantic Schemas

```python
from pydantic import BaseModel, Field, field_validator

class CreatePetRequest(BaseModel):
    """Schema for creating a pet."""
    
    name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=50)
    weight: Optional[float] = Field(None, ge=0.1, le=500.0)
    pet_type: str = Field(..., description="Type of pet")
    
    @field_validator('pet_type')
    @classmethod
    def validate_pet_type(cls, v):
        """Validate pet type is uppercase."""
        return v.upper()
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate name is not empty."""
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
```

### Field Constraints

```python
from pydantic import EmailStr, constr, conint, confloat

class UserRegistration(BaseModel):
    email: EmailStr  # Validates email format
    password: constr(min_length=8, max_length=100)  # String constraints
    age: conint(ge=18, le=120)  # Integer constraints
    weight: confloat(ge=0.0, le=500.0)  # Float constraints
```

---

## Error Handling

### HTTP Exceptions

```python
from fastapi import HTTPException, status

@router.get("/pets/{pet_id}")
def get_pet(pet_id: uuid.UUID):
    try:
        pet = pet_service.get_pet(pet_id)
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pet not found"
            )
        return PetResponse.model_validate(pet)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.exception("Error getting pet", extra={"pet_id": str(pet_id)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

### Custom Exception Handlers

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
```

---

## Logging

### Log Security-Relevant Actions

```python
from app.logger import logger

@router.post("/clinic/onboard-pet")
def onboard_pet(
    request_data: OnboardingRequest,
    current_user: User = Depends(get_clinic_owner_user)
):
    logger.info(
        "Pet onboarding initiated",
        extra={
            "clinic_user_id": str(current_user.id),
            "owner_email": request_data.owner_email,
            "pet_name": request_data.pet_name
        }
    )
    
    try:
        result = controller.onboard_pet(request_data, current_user)
        
        logger.info(
            "Pet onboarding completed",
            extra={
                "clinic_user_id": str(current_user.id),
                "pet_id": result.pet.pet_id
            }
        )
        
        return result
    except Exception as e:
        logger.exception(
            "Pet onboarding failed",
            extra={
                "clinic_user_id": str(current_user.id),
                "error": str(e)
            }
        )
        raise
```

### What to Log

- ✅ Authentication attempts (success and failure)
- ✅ Authorization failures
- ✅ Data creation/modification/deletion
- ✅ Security-relevant actions
- ✅ Errors and exceptions
- ❌ Don't log sensitive data (passwords, tokens)
- ❌ Don't log PII without sanitization

---

## Security Best Practices

### Never Expose Sensitive Data

```python
# WRONG: Exposing password hash
class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    password_hash: str  # ❌ Never expose!

# CORRECT: Only safe fields
class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    # No password_hash!
```

### Use Proper Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash passwords
hashed_password = pwd_context.hash(plain_password)

# Verify passwords
is_valid = pwd_context.verify(plain_password, hashed_password)
```

### Validate JWT Tokens

```python
from app.dependencies import get_current_user

@router.get("/protected")
def protected_endpoint(
    current_user: User = Depends(get_current_user)  # Validates JWT
):
    """This endpoint requires valid JWT."""
    return {"user_id": current_user.id}
```

### Rate Limiting

```python
# TODO: Implement rate limiting for sensitive endpoints
# - Login endpoints
# - Password reset
# - OTP generation
# - Account creation
```

---

## Response Formatting

### Success Responses

```python
from pydantic import BaseModel, ConfigDict

class PetResponse(BaseModel):
    """Schema for pet response."""
    
    id: uuid.UUID
    name: str
    pet_type: str
    breed: str
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Buddy",
                "pet_type": "DOG",
                "breed": "Golden Retriever"
            }
        }
    )
```

### Error Responses

```python
class ErrorResponse(BaseModel):
    """Standard error response."""
    
    detail: str
    error_code: Optional[str] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Pet not found",
                "error_code": "PET_NOT_FOUND"
            }
        }
    )
```

---

## API Documentation

### Document Endpoints

```python
@router.post(
    "/clinic-onboard",
    response_model=ClinicPetOnboardingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Onboard a pet via clinic",
    description="""
    Clinic owners can onboard a pet and create/link owner account.
    
    This endpoint:
    - Creates a new pet record
    - Creates owner account if email doesn't exist
    - Links pet to existing owner if email exists
    - Sends verification email to owner
    - Marks owner as admin of the pet
    
    **Authorization**: Requires `clinic_owner` role.
    """,
    responses={
        201: {"description": "Pet onboarded successfully"},
        400: {"description": "Invalid request data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized (wrong role)"},
        500: {"description": "Internal server error"}
    }
)
def onboard_pet(
    onboarding_data: ClinicPetOnboardingRequest,
    current_user: User = Depends(get_clinic_owner_user),
    controller: PetController = Depends(get_pet_controller)
):
    """Onboard a pet via clinic (clinic_owner role required)."""
    return controller.onboard_pet_by_clinic(onboarding_data, current_user)
```

### Include Request/Response Examples

All Pydantic schemas should include examples:

```python
model_config = ConfigDict(
    json_schema_extra={
        "example": {
            "field1": "value1",
            "field2": 42
        }
    }
)
```

---

## Testing APIs

### Integration Tests

```python
def test_create_pet(client, auth_headers):
    """Test creating a pet."""
    response = client.post(
        "/api/pets",
        json={
            "name": "Buddy",
            "pet_type": "DOG",
            "breed": "Golden Retriever",
            "age": 3
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Buddy"
    assert "id" in data
```

### Authorization Tests

```python
def test_clinic_endpoint_requires_role(client, pet_owner_headers):
    """Test that clinic endpoints reject pet owners."""
    response = client.post(
        "/api/clinic/onboard-pet",
        json={...},
        headers=pet_owner_headers  # Wrong role!
    )
    
    assert response.status_code == 403  # Forbidden
```

---

## Best Practices Summary

1. ✅ Enforce RBAC at route level with dependencies
2. ✅ Validate all input with Pydantic
3. ✅ Log security-relevant actions
4. ✅ Never expose sensitive data
5. ✅ Use proper password hashing
6. ✅ Provide comprehensive API documentation
7. ✅ Include request/response examples
8. ✅ Handle errors gracefully
9. ✅ Use appropriate HTTP status codes
10. ✅ Test authorization rules

