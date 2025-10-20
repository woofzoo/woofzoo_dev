# Doctor Controller Refactoring Plan

**Date**: October 20, 2025  
**Status**: 📋 Planning  
**Priority**: High (Violates Clean Architecture)  
**Updated**: October 20, 2025

---

## Problems Identified

### Problem 1: Doctor Profile ID Resolution (TODO)
**Location**: `app/controllers/doctor_controller.py:59-61`

```python
# TODO: Get doctor_id from current_user's doctor profile
# For now, using user's public_id as placeholder
doctor_id = current_user.public_id  # ❌ WRONG
```

**Issue**: Using `user.public_id` instead of `doctor_profile.id`

**Impact**: 
- Queries will fail when joining on `doctor_id`
- Medical records expect `doctor_profile.id`, not `user_id`
- Data integrity issue

---

### Problem 2: Controller Accessing Database Directly
**Location**: `app/controllers/doctor_controller.py:74-125`

```python
# ❌ VIOLATES CLEAN ARCHITECTURE
db = next(get_db_session())  # Controller getting DB session!
try:
    pet_repo = PetRepository(db)  # Controller creating repositories!
    user_repo = UserRepository(db)
    mr_repo = MedicalRecordRepository(db)
    
    pet = pet_repo.get(access.pet_id)  # Controller querying data!
    owner = user_repo.get_by_public_id(pet.owner_id)
    medical_record = mr_repo.get(access.medical_record_id)
    # ... building response in controller
finally:
    db.close()
```

**Issues**:
- Controller knows about database sessions
- Controller creates repositories
- Controller performs data fetching
- Business logic in presentation layer
- Can't unit test controller without database
- Violates clean architecture principles

---

## Solution Strategy

### Two Approaches for Profile ID Resolution

#### Option 1: Middleware/Dependency Approach ⚠️
```python
# In middleware or dependency
def get_current_doctor_user(current_user: User = Depends(get_current_user)):
    """Resolve doctor profile and attach to user."""
    doctor_profile_repo = get_doctor_profile_repository()
    doctor_profile = doctor_profile_repo.get_by_user_id(current_user.public_id)
    if not doctor_profile:
        raise HTTPException(403, "Doctor profile not found")
    
    # Attach to user object
    current_user.doctor_profile_id = doctor_profile.id
    return current_user
```

**Pros**: 
- Profile ID available immediately in controller
- Single lookup per request

**Cons**:
- Middleware doing business logic (not lightweight)
- Tight coupling between auth and profiles
- Harder to test independently

#### Option 2: Service Layer Approach ✅ RECOMMENDED
```python
# In service
def get_doctor_profile_id(self, user_id: uuid.UUID) -> uuid.UUID:
    """Get doctor profile ID from user ID."""
    profile = self.doctor_profile_repository.get_by_user_id(user_id)
    if not profile:
        raise ValueError("Doctor profile not found")
    return profile.id
```

**Pros**:
- Keeps middleware lightweight
- Profile logic in appropriate layer
- More flexible and testable
- Can be reused across methods
- Follows clean architecture

**Cons**:
- Extra method call per request (minimal overhead)

**Decision**: ✅ Use **Option 2** (Service Layer) - **CONFIRMED**

**Rationale**:
- Keeps authentication/middleware lightweight
- Profile resolution is business logic, belongs in service layer
- More flexible and testable
- Can be reused across different service methods
- Follows clean architecture principles

---

## Detailed Implementation Plan

### Phase 0: Add get() Method to BaseRepository ⚠️ CRITICAL

**Problem Identified**: BaseRepository only has `get_by_id(id: str)` but services need `get(id: uuid.UUID)`

**File**: `app/repositories/base.py`

**Add this method after `get_by_id()`**:

```python
def get(self, id: uuid.UUID) -> Optional[ModelType]:
    """
    Get a record by UUID.
    
    Args:
        id: Record UUID
        
    Returns:
        Model instance or None if not found
    """
    return self.get_by_id(str(id))
```

**Why this is needed**:
- Current code in `doctor_queue_service.py` uses `.get(uuid)` which doesn't exist
- Services pass UUID objects, not strings
- This wrapper method provides convenience and type safety
- Internally delegates to `get_by_id(str(id))`

**Impact**: This fix is needed before the rest of the refactoring!

---

### Phase 1: Add Profile Repositories to Services

#### 1.1 Update DoctorQueueService Constructor

**File**: `app/services/doctor_queue_service.py`

```python
# BEFORE
def __init__(
    self,
    pet_clinic_access_repository: PetClinicAccessRepository,
    medical_record_repository: MedicalRecordRepository,
    pet_repository: PetRepository,
    user_repository: UserRepository
):
    # ...

# AFTER
def __init__(
    self,
    pet_clinic_access_repository: PetClinicAccessRepository,
    medical_record_repository: MedicalRecordRepository,
    pet_repository: PetRepository,
    user_repository: UserRepository,
    doctor_profile_repository: DoctorProfileRepository  # ✅ Add
):
    # ...
    self.doctor_profile_repository = doctor_profile_repository
```

#### 1.2 Add Profile Resolution Method

```python
def get_doctor_profile_id(self, user_id: uuid.UUID) -> uuid.UUID:
    """
    Get doctor profile ID from user ID.
    
    Args:
        user_id: User's public ID
        
    Returns:
        Doctor profile ID
        
    Raises:
        ValueError: If doctor profile not found
    """
    profile = self.doctor_profile_repository.get_by_user_id(str(user_id))
    if not profile:
        raise ValueError(f"Doctor profile not found for user {user_id}")
    return profile.id
```

---

### Phase 2: Move Data Fetching to Service Layer

#### 2.1 Create Comprehensive Queue Method

**Problem**: Controller is fetching related data (pet, owner, medical_record)

**Solution**: Service should return complete data structures

```python
def get_todays_queue_with_details(
    self,
    user_id: uuid.UUID
) -> Tuple[List[dict], dict]:
    """
    Get today's queue with all related details.
    
    This method orchestrates data from multiple repositories to
    build a complete queue with pet, owner, and visit information.
    
    Args:
        user_id: Doctor user's public ID
        
    Returns:
        Tuple of (queue_items_with_details, statistics)
        
    Raises:
        ValueError: If doctor profile not found
    """
    # Step 1: Resolve doctor profile ID
    doctor_id = self.get_doctor_profile_id(user_id)
    
    # Step 2: Get queue items (existing method)
    queue_items, statistics = self.get_todays_queue(doctor_id)
    
    # Step 3: Fetch related data for each queue item
    queue_details = []
    for access in queue_items:
        # Fetch pet
        pet = self.pet_repository.get(access.pet_id)
        if not pet:
            logger.warning(f"Pet not found: {access.pet_id}")
            continue
        
        # Fetch owner
        owner = self.user_repository.get_by_public_id(pet.owner_id)
        if not owner:
            logger.warning(f"Owner not found: {pet.owner_id}")
            continue
        
        # Fetch medical record
        medical_record = self.medical_record_repository.get(access.medical_record_id)
        if not medical_record:
            logger.warning(f"Medical record not found: {access.medical_record_id}")
            continue
        
        # Build pre-checks dict
        pre_checks = None
        if access.pre_check_weight or access.pre_check_temperature:
            pre_checks = {
                "weight": access.pre_check_weight,
                "temperature": access.pre_check_temperature,
                "heart_rate": access.pre_check_heart_rate,
                "respiratory_rate": access.pre_check_respiratory_rate,
                "notes": access.pre_check_notes
            }
        
        # Build complete queue item
        queue_details.append({
            "queue_position": access.queue_position or 0,
            "pet": {
                "id": str(pet.id),
                "pet_id": pet.pet_id,
                "name": pet.name,
                "pet_type": pet.pet_type,
                "breed": pet.breed,
                "age": pet.age,
                "owner_name": owner.full_name
            },
            "visit_info": {
                "medical_record_id": str(medical_record.id),
                "visit_type": medical_record.visit_type or "GENERAL",
                "chief_complaint": medical_record.chief_complaint,
                "assigned_at": access.assigned_to_doctor_at,
                "pre_checks": pre_checks
            },
            "status": access.queue_status
        })
    
    return queue_details, statistics
```

---

### Phase 3: Refactor Controller

#### 3.1 Update get_todays_queue() Method

**File**: `app/controllers/doctor_controller.py`

```python
# BEFORE (74 lines, violates clean architecture)
def get_todays_queue(self, current_user: User) -> DoctorQueueResponse:
    try:
        doctor_id = current_user.public_id  # ❌ Wrong
        
        # ❌ Controller accessing DB
        db = next(get_db_session())
        try:
            pet_repo = PetRepository(db)
            # ... 50+ lines of data fetching
        finally:
            db.close()
    except Exception as e:
        # error handling

# AFTER (clean and simple)
def get_todays_queue(self, current_user: User) -> DoctorQueueResponse:
    """
    Get today's queue for the logged-in doctor.
    
    Args:
        current_user: Current authenticated doctor user
        
    Returns:
        DoctorQueueResponse: Today's queue with statistics
        
    Raises:
        HTTPException: If fetching queue fails
    """
    try:
        logger.info(
            "Fetching today's queue",
            extra={"user_id": str(current_user.public_id)}
        )
        
        # ✅ Service handles everything
        queue_details, statistics = self.doctor_queue_service.get_todays_queue_with_details(
            user_id=current_user.public_id
        )
        
        # ✅ Controller just builds response from service data
        queue_list = [
            DoctorQueueItem(
                queue_position=item["queue_position"],
                pet=PetQueueInfo(**item["pet"]),
                visit_info=VisitInfo(**item["visit_info"]),
                status=item["status"]
            )
            for item in queue_details
        ]
        
        return DoctorQueueResponse(
            date=date.today(),
            queue=queue_list,
            **statistics
        )
    
    except ValueError as e:
        # Profile not found or data error
        logger.warning(
            "Failed to fetch queue",
            extra={"user_id": str(current_user.id), "error": str(e)}
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(
            "Failed to fetch today's queue",
            extra={"user_id": str(current_user.id)}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch today's queue"
        )
```

**Benefits**:
- ✅ 30 lines instead of 100+
- ✅ No database access
- ✅ No repository creation
- ✅ Single service call
- ✅ Simple response building
- ✅ Proper error handling

---

### Phase 4: Update Dependency Injection

#### 4.1 Add DoctorProfileRepository Dependency

**File**: `app/dependencies.py`

```python
def get_doctor_profile_repository(session: Session = Depends(get_db_session)):
    """
    Dependency to get doctor profile repository.
    
    Args:
        session: Database session
        
    Returns:
        DoctorProfileRepository instance
    """
    from app.repositories.doctor_profile import DoctorProfileRepository
    return DoctorProfileRepository(session)
```

#### 4.2 Update DoctorQueueService Dependency

```python
def get_doctor_queue_service(
    pet_clinic_access_repository: PetClinicAccessRepository = Depends(get_pet_clinic_access_repository),
    medical_record_repository: MedicalRecordRepository = Depends(get_medical_record_repository),
    pet_repository: PetRepository = Depends(get_pet_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    doctor_profile_repository = Depends(get_doctor_profile_repository)  # ✅ Add
) -> DoctorQueueService:
    """
    Dependency to get doctor queue service.
    
    Args:
        pet_clinic_access_repository: Pet clinic access repository
        medical_record_repository: Medical record repository
        pet_repository: Pet repository
        user_repository: User repository
        doctor_profile_repository: Doctor profile repository
        
    Returns:
        DoctorQueueService instance
    """
    return DoctorQueueService(
        pet_clinic_access_repository,
        medical_record_repository,
        pet_repository,
        user_repository,
        doctor_profile_repository  # ✅ Add
    )
```

---

## Architecture Comparison

### Before ❌

```
Route → Controller
         ├─ Get DB Session      # ❌ Wrong layer
         ├─ Create Repositories # ❌ Wrong layer
         ├─ Query Data         # ❌ Wrong layer
         └─ Build Response     # ✅ OK
```

**Problems**:
- Controller knows about database
- Controller knows about repositories
- Can't unit test without database
- Business logic in presentation layer

### After ✅

```
Route → Controller → Service
                      ├─ Resolve Profile ID
                      ├─ Get Queue Items
                      ├─ Fetch Pet Data
                      ├─ Fetch Owner Data
                      ├─ Fetch Medical Records
                      └─ Return Complete Data
        Controller ← Build Response
```

**Benefits**:
- Clean separation of concerns
- Controller only handles HTTP
- Service handles all business logic
- Easy to unit test
- Follows clean architecture

---

## Service Design Pattern

### Option A: Single Orchestration Method (RECOMMENDED)

```python
class DoctorQueueService:
    # Profile resolution
    def get_doctor_profile_id(user_id) -> uuid.UUID
    
    # Basic queue query
    def get_todays_queue(doctor_id) -> (items, stats)
    
    # Full orchestration (NEW)
    def get_todays_queue_with_details(user_id) -> (details, stats)
```

**Pros**: 
- Single service
- Clear method names
- Easy to understand

**Cons**: 
- Service has multiple responsibilities
- Could get large over time

### Option B: Separate Services

```python
# Basic operations
class DoctorQueueService:
    def get_todays_queue(doctor_id) -> (items, stats)

# Orchestration
class DoctorQueueOrchestrationService:
    def __init__(
        self,
        queue_service: DoctorQueueService,
        pet_service: PetService,
        user_service: UserService
    ):
        # ...
    
    def get_todays_queue_with_details(user_id) -> (details, stats)
```

**Pros**:
- Single Responsibility Principle
- Services can be reused independently
- Clear separation

**Cons**:
- More files
- More dependencies
- Overhead for simple use case

**Decision**: Use **Option A** for now, refactor to Option B if services grow too large.

---

## Implementation Order

### Step 0: ⚠️ Add get() Method to BaseRepository (CRITICAL)
- Add `get(uuid.UUID)` wrapper method to BaseRepository
- This fixes existing broken code in doctor_queue_service
- **Must do first!**

### Step 1: ✅ Add DoctorProfileRepository Dependency
- Create `get_doctor_profile_repository()` in dependencies
- No breaking changes

### Step 2: ✅ Update DoctorQueueService
- Add `doctor_profile_repository` to constructor
- Add `get_doctor_profile_id()` method (using service layer approach ✅)
- Add `get_todays_queue_with_details()` method
- Update dependency injection

### Step 3: ✅ Refactor Controller
- Replace data fetching logic with service call
- Remove all DB/repository access (lines 74-125)
- Simplify from 100+ lines to ~30 lines

### Step 4: ✅ Test
- Unit test service methods (mock repositories only)
- Integration test endpoints
- Verify profile resolution works correctly
- Verify controller doesn't access DB

### Step 5: ✅ Apply Same Pattern to Other Methods
- `get_visit_details()`
- `update_visit_details()`
- `complete_visit()`

---

## Testing Strategy

### Unit Tests (Service)

```python
def test_get_doctor_profile_id():
    mock_profile_repo = Mock()
    mock_profile_repo.get_by_user_id.return_value = Mock(id="prof-123")
    
    service = DoctorQueueService(
        # ... other repos
        doctor_profile_repository=mock_profile_repo
    )
    
    profile_id = service.get_doctor_profile_id("user-123")
    assert profile_id == "prof-123"

def test_get_todays_queue_with_details():
    # Mock all repositories
    service = DoctorQueueService(...)
    
    details, stats = service.get_todays_queue_with_details("user-123")
    
    # Verify service orchestrated correctly
    assert len(details) > 0
    assert "pet" in details[0]
    assert "visit_info" in details[0]
```

### Integration Tests (API)

```bash
# Test endpoint still works
curl -X GET http://localhost:8000/api/doctor/queue/today \
  -H "Authorization: Bearer $DOCTOR_TOKEN"

# Should return:
# - 200 OK
# - Queue with pet/owner/visit details
# - Correct doctor profile used
```

---

## Benefits Summary

### Before ❌
- 100+ lines in controller
- Controller accessing database
- Can't unit test
- Violates clean architecture
- Profile ID issue (TODO)

### After ✅
- 30 lines in controller
- All logic in service layer
- Easy to unit test
- Follows clean architecture
- Profile ID properly resolved
- Reusable service methods

---

## Files to Modify

1. ✅ `app/services/doctor_queue_service.py`
   - Add `doctor_profile_repository` to constructor
   - Add `get_doctor_profile_id()` method
   - Add `get_todays_queue_with_details()` method

2. ✅ `app/controllers/doctor_controller.py`
   - Remove all DB/repository access
   - Simplify to call service method
   - Update error handling

3. ✅ `app/dependencies.py`
   - Add `get_doctor_profile_repository()` dependency
   - Update `get_doctor_queue_service()` to inject profile repo

4. ✅ Apply same pattern to other controller methods

---

## Risk Mitigation

- ✅ **Backward Compatible**: API interface unchanged
- ✅ **Incremental**: Can do one method at a time
- ✅ **Testable**: Each change can be tested independently
- ✅ **Documented**: Clear plan and examples

---

**Estimated Time**: 2-3 hours  
**Complexity**: Medium  
**Breaking Changes**: None (internal only)  
**Priority**: High (fixes architecture violation)

