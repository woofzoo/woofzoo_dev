# Code Documentation Standards

## Function Documentation

Every function must have a docstring with:
- Brief description
- Args (with types)
- Returns (with type)
- Raises (exceptions, if any)

---

## Docstring Format

### Standard Function

```python
def get_pet_by_id(self, pet_id: uuid.UUID) -> Optional[Pet]:
    """
    Get a pet by ID.
    
    Args:
        pet_id: UUID of the pet to retrieve
        
    Returns:
        Pet instance or None if not found
        
    Raises:
        ValueError: If pet_id is invalid format
    """
    # Implementation
```

### Function with Multiple Parameters

```python
def update_pre_check_vitals(
    self,
    access_record_id: uuid.UUID,
    weight: Optional[float],
    temperature: Optional[float],
    heart_rate: Optional[int],
    notes: Optional[str]
) -> PetClinicAccess:
    """
    Update pre-check vitals for a pet visit.
    
    This method updates all vital signs recorded during pre-check
    and marks the pre-check as completed.
    
    Args:
        access_record_id: UUID of the access record to update
        weight: Weight in kilograms (optional)
        temperature: Temperature in Celsius (optional)
        heart_rate: Heart rate in beats per minute (optional)
        notes: Additional observations (optional)
        
    Returns:
        Updated PetClinicAccess instance with new vitals
        
    Raises:
        ValueError: If access_record_id not found
        ValueError: If access record is not in correct status
    """
    # Implementation
```

### Service Method with Business Logic

```python
def onboard_pet_by_clinic(
    self, 
    onboarding_data: ClinicPetOnboardingRequest,
    clinic_user_id: uuid.UUID
) -> Tuple[Pet, User, bool]:
    """
    Onboard a pet via clinic with automatic owner account creation.
    
    This method handles the complete pet onboarding workflow:
    1. Check if owner exists by email
    2. Create new owner account if needed (with verification email)
    3. Generate unique pet_id
    4. Create pet record linked to owner
    5. Send notification email to owner
    
    Args:
        onboarding_data: Pet and owner information for onboarding
        clinic_user_id: UUID of the clinic user performing onboarding
        
    Returns:
        Tuple of (created_pet, owner_user, is_new_user)
        - created_pet: The newly created Pet instance
        - owner_user: The User instance (new or existing)
        - is_new_user: True if new account was created
        
    Raises:
        ValueError: If user repository not available
        ValueError: If email service not available
        ValueError: If pet creation fails
    """
    # Implementation
```

---

## Class Documentation

### Document Classes

```python
class PetService:
    """
    Service for pet-related business logic.
    
    This service handles all pet operations including CRUD operations,
    pet onboarding, and pet ownership management.
    
    Attributes:
        pet_repository: Repository for pet data access
        user_repository: Repository for user data access
        email_service: Service for sending emails
    """
    
    def __init__(
        self,
        pet_repository: PetRepository,
        user_repository: UserRepository,
        email_service: EmailService
    ):
        """
        Initialize the pet service.
        
        Args:
            pet_repository: Repository for pet data access
            user_repository: Repository for user data access
            email_service: Service for sending emails
        """
        self.pet_repository = pet_repository
        self.user_repository = user_repository
        self.email_service = email_service
```

---

## Schema Documentation

### Pydantic Schema with Examples

```python
from pydantic import BaseModel, Field, ConfigDict

class CreatePetRequest(BaseModel):
    """
    Schema for creating a new pet.
    
    This schema validates all required and optional fields for
    pet creation, including owner information.
    """
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the pet"
    )
    
    pet_type: str = Field(
        ...,
        description="Type of pet (e.g., DOG, CAT, BIRD)"
    )
    
    breed: str = Field(
        ...,
        description="Breed of the pet"
    )
    
    age: Optional[int] = Field(
        None,
        ge=0,
        le=50,
        description="Age of the pet in years"
    )
    
    weight: Optional[float] = Field(
        None,
        ge=0.1,
        le=500.0,
        description="Weight of the pet in kilograms"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Buddy",
                "pet_type": "DOG",
                "breed": "Golden Retriever",
                "age": 3,
                "weight": 25.5
            }
        }
    )
```

### Response Schema Documentation

```python
class PetResponse(BaseModel):
    """
    Schema for pet response data.
    
    This schema represents the pet data returned to clients,
    excluding sensitive internal fields.
    """
    
    id: uuid.UUID = Field(description="Unique pet identifier")
    pet_id: str = Field(description="Human-readable pet ID")
    name: str = Field(description="Pet name")
    pet_type: str = Field(description="Type of pet")
    breed: str = Field(description="Breed of pet")
    owner_id: uuid.UUID = Field(description="Owner's user ID")
    is_active: bool = Field(description="Whether pet record is active")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "pet_id": "DOG-GOLDEN-RETRIEVER-000001",
                "name": "Buddy",
                "pet_type": "DOG",
                "breed": "Golden Retriever",
                "owner_id": "660e8400-e29b-41d4-a716-446655440000",
                "is_active": True
            }
        }
    )
```

---

## Inline Comments

### When to Use Inline Comments

Use inline comments for:
- Complex logic that isn't obvious
- Business rules and constraints
- Workarounds or temporary solutions
- References to external documentation

```python
def calculate_queue_position(self, doctor_id: uuid.UUID) -> int:
    """Calculate the next position in the doctor's queue."""
    
    # Count only active pets assigned to this doctor today
    # This ensures queue positions are sequential and current
    today = datetime.now(timezone.utc).date()
    tomorrow = today + timedelta(days=1)
    
    active_count = self.pet_clinic_access_repository.count_active_in_queue(
        queue_status=QueueStatus.WITH_DOCTOR.value,
        assigned_before=datetime.combine(tomorrow, datetime.min.time())
    )
    
    # Queue position starts at 1, not 0
    # This matches the UI's 1-based display
    return active_count + 1
```

### Document Design Decisions

```python
def generate_pet_id(self, pet_type: str, breed: str) -> str:
    """
    Generate a unique, human-readable pet ID.
    
    Format: {PET_TYPE}-{BREED}-{SEQUENCE}
    Example: DOG-GOLDEN-RETRIEVER-000001
    
    Design Decision: We use a sequential counter per pet-type/breed
    combination to ensure IDs are predictable and sortable, rather
    than using UUIDs which are less user-friendly.
    """
    # Implementation
```

### Explain Non-Obvious Code

```python
def verify_otp(self, otp_code: str, phone: str) -> bool:
    """Verify OTP code for a phone number."""
    
    otp = self.otp_repository.get_by_code_and_phone(otp_code, phone)
    
    if not otp:
        return False
    
    # OTP must not be used and not expired
    # Note: We check is_used first for performance (indexed field)
    if otp.is_used:
        return False
    
    # Timezone-aware comparison required for accurate expiration check
    now = datetime.now(timezone.utc)
    if otp.expires_at < now:
        return False
    
    return True
```

---

## API Route Documentation

### Complete Route Documentation

```python
@router.post(
    "/clinic-onboard",
    response_model=ClinicPetOnboardingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Onboard a pet via clinic",
    description="""
    Clinic owners can onboard a pet and automatically create or link owner account.
    
    **Workflow:**
    1. Clinic enters pet and owner information
    2. System checks if owner email exists
    3. If new email: Creates user account and sends verification email
    4. If existing email: Links pet to existing user
    5. Creates pet record with unique pet_id
    6. Sends notification email to owner
    7. Returns pet details and account creation status
    
    **Authorization:**
    Requires `clinic_owner` role. This is enforced at the route level
    by the `get_clinic_owner_user` dependency.
    
    **Email Notifications:**
    - New users: Receive verification email + pet onboarding notification
    - Existing users: Receive pet onboarding notification only
    
    **Owner Permissions:**
    The owner is automatically marked as the admin of the pet.
    """,
    responses={
        201: {
            "description": "Pet onboarded successfully",
            "model": ClinicPetOnboardingResponse
        },
        400: {
            "description": "Invalid request data",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid email format"}
                }
            }
        },
        401: {
            "description": "Not authenticated"
        },
        403: {
            "description": "Not authorized (requires clinic_owner role)"
        },
        500: {
            "description": "Internal server error"
        }
    },
    tags=["Clinic Operations"]
)
def onboard_pet_by_clinic(
    onboarding_data: ClinicPetOnboardingRequest,
    current_user: User = Depends(get_clinic_owner_user),
    controller: PetController = Depends(get_pet_controller)
) -> ClinicPetOnboardingResponse:
    """
    Onboard a pet via clinic (clinic_owner role required).
    
    See endpoint description for complete workflow details.
    """
    return controller.onboard_pet_by_clinic(onboarding_data, current_user)
```

---

## Module-Level Documentation

### Module Docstring

```python
"""
Pet Service Module

This module provides the PetService class which handles all pet-related
business logic including:
- Pet CRUD operations
- Pet onboarding by clinics
- Pet ownership management
- Pet ID generation
- Pet activation/deactivation

The service follows clean architecture principles:
- Only calls repository methods for data access
- Never injects database Session
- Contains all pet-related business rules
"""

from typing import Optional, List, Tuple
# ... imports
```

---

## TODO Comments

### Use TODO for Future Work

```python
def send_notification(self, user_id: uuid.UUID, message: str):
    """Send notification to user."""
    
    # TODO: Implement push notifications
    # Currently only sends email, should also support:
    # - SMS notifications
    # - In-app notifications
    # - Push notifications for mobile app
    
    self.email_service.send_notification(user.email, message)
```

### Use FIXME for Known Issues

```python
def calculate_age(self, birth_date: date) -> int:
    """Calculate age from birth date."""
    
    # FIXME: This doesn't account for leap years correctly
    # Should use more robust date calculation
    # See issue #123
    
    today = date.today()
    return today.year - birth_date.year
```

---

## Best Practices

### DO

- ✅ Document all public functions and methods
- ✅ Include types in docstrings
- ✅ Provide examples in schemas
- ✅ Explain complex business logic
- ✅ Document design decisions
- ✅ Keep documentation up to date

### DON'T

- ❌ Don't document obvious code
- ❌ Don't repeat parameter names without adding value
- ❌ Don't write outdated documentation
- ❌ Don't use vague descriptions like "does stuff"
- ❌ Don't document implementation details that may change

---

## Documentation Maintenance

### When to Update Documentation

- ✅ When adding new functions or classes
- ✅ When changing function signatures
- ✅ When modifying behavior or business logic
- ✅ When fixing bugs that weren't documented
- ✅ When deprecating functionality

### Documentation Review Checklist

Before committing:
- [ ] All new functions have docstrings
- [ ] All parameters are documented
- [ ] Return types are documented
- [ ] Exceptions are documented
- [ ] Examples are included in schemas
- [ ] Complex logic has inline comments
- [ ] API routes are fully documented

