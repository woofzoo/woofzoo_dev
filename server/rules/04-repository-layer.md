# Repository Layer Rules

## Repository Responsibilities

- **ALL database access must happen in repositories**
- Repositories should extend `BaseRepository` for common operations
- Add domain-specific query methods to repositories
- Repositories handle all SQLAlchemy session operations
- Return model instances (not DTOs)

---

## BaseRepository Usage

### Available Methods

All repositories extend `BaseRepository` which provides:

```python
# Common CRUD operations
create(**kwargs) -> ModelType
get(id: uuid.UUID) -> Optional[ModelType]
get_by_id(id: str) -> Optional[ModelType]
get_all(skip: int = 0, limit: int = 100) -> List[ModelType]
update(id: str, **kwargs) -> Optional[ModelType]
delete(id: str) -> bool

# Entity operations
update_entity(entity: ModelType) -> ModelType
delete_entity(entity: ModelType) -> None
save(instance: ModelType) -> ModelType

# Transaction operations
commit() -> None
refresh(entity: ModelType) -> None

# Utility
count() -> int
```

### Usage Example

```python
class PetRepository(BaseRepository[Pet]):
    def __init__(self, session: Session):
        super().__init__(Pet, session)
    
    # Use inherited methods
    def create_pet(self, **pet_data):
        return self.create(**pet_data)
    
    def get_pet(self, pet_id: uuid.UUID):
        return self.get(pet_id)
    
    def update_pet(self, pet: Pet):
        return self.update_entity(pet)
```

---

## Domain-Specific Methods

Add custom query methods for domain needs:

### Simple Query Method

```python
class PetRepository(BaseRepository[Pet]):
    def get_by_owner_id(self, owner_id: uuid.UUID) -> List[Pet]:
        """Get all pets for an owner."""
        return self.session.query(Pet).filter(
            Pet.owner_id == owner_id,
            Pet.is_active == True
        ).all()
```

### Complex Query Method

```python
class PetClinicAccessRepository(BaseRepository[PetClinicAccess]):
    def get_todays_queue_for_doctor(
        self,
        doctor_id: uuid.UUID,
        start_date: datetime,
        end_date: datetime
    ) -> List[PetClinicAccess]:
        """Get all access records for a doctor's queue today."""
        return self.session.query(PetClinicAccess).filter(
            and_(
                PetClinicAccess.medical_record_id.isnot(None),
                PetClinicAccess.assigned_to_doctor_at >= start_date,
                PetClinicAccess.assigned_to_doctor_at < end_date,
                PetClinicAccess.queue_status.in_([
                    QueueStatus.WITH_DOCTOR,
                    QueueStatus.COMPLETED
                ])
            )
        ).join(
            MedicalRecord,
            PetClinicAccess.medical_record_id == MedicalRecord.id
        ).filter(
            MedicalRecord.doctor_id == doctor_id
        ).order_by(
            PetClinicAccess.queue_position
        ).all()
```

### Update Method with Business Logic

```python
class PetClinicAccessRepository(BaseRepository[PetClinicAccess]):
    def update_pre_check_vitals(
        self,
        access_record_id: uuid.UUID,
        weight: Optional[float],
        temperature: Optional[float],
        heart_rate: Optional[int],
        respiratory_rate: Optional[int],
        notes: Optional[str],
        completed_at: datetime,
        completed_by_user_id: uuid.UUID,
        new_queue_status: str
    ) -> PetClinicAccess:
        """Update pre-check vitals and queue status atomically."""
        access = self.get(access_record_id)
        if not access:
            raise ValueError("Access record not found")
        
        # Update all fields
        access.pre_check_weight = weight
        access.pre_check_temperature = temperature
        access.pre_check_heart_rate = heart_rate
        access.pre_check_respiratory_rate = respiratory_rate
        access.pre_check_notes = notes
        access.pre_check_completed_at = completed_at
        access.pre_check_by_user_id = completed_by_user_id
        access.queue_status = new_queue_status
        
        # Use BaseRepository method to commit
        return self.update_entity(access)
```

---

## Repository Patterns

### Read-Only Repository

```python
class ReportRepository(BaseRepository[Report]):
    """Repository for read-only reporting queries."""
    
    def get_monthly_stats(self, year: int, month: int) -> dict:
        """Get statistics for a given month."""
        # Complex read query
        return results
```

### Write-Heavy Repository

```python
class AuditLogRepository(BaseRepository[AuditLog]):
    """Repository for audit logging."""
    
    def log_action(self, user_id: uuid.UUID, action: str, details: dict):
        """Log an audit action."""
        return self.create(
            user_id=user_id,
            action=action,
            details=details,
            timestamp=datetime.now(timezone.utc)
        )
```

### Repository with Transactions

```python
class OrderRepository(BaseRepository[Order]):
    """Repository with transaction support."""
    
    def create_order_with_items(
        self,
        order_data: dict,
        items: List[dict]
    ) -> Order:
        """Create order and items in a transaction."""
        try:
            order = self.create(**order_data)
            for item_data in items:
                item_data['order_id'] = order.id
                self.session.add(OrderItem(**item_data))
            self.commit()
            self.refresh(order)
            return order
        except Exception:
            self.session.rollback()
            raise
```

---

## Anti-Patterns to Avoid

### ❌ Don't Put Business Logic in Repositories

```python
# WRONG: Business logic in repository
class PetRepository(BaseRepository[Pet]):
    def adopt_pet(self, pet_id: uuid.UUID, owner_id: uuid.UUID):
        pet = self.get(pet_id)
        if pet.age < 2:  # ❌ Business rule!
            raise ValueError("Pet too young")
        if not self.owner_has_space(owner_id):  # ❌ Business logic!
            raise ValueError("Owner has no space")
        pet.owner_id = owner_id
        return self.update_entity(pet)
```

✅ **Correct**: Business logic in service, data access in repository

```python
# Service handles business logic
class PetService:
    def adopt_pet(self, pet_id: uuid.UUID, owner_id: uuid.UUID):
        pet = self.pet_repository.get(pet_id)
        if pet.age < 2:  # ✅ Business logic in service
            raise ValueError("Pet too young")
        # ... more business logic
        return self.pet_repository.update_pet_owner(pet_id, owner_id)

# Repository handles data access
class PetRepository(BaseRepository[Pet]):
    def update_pet_owner(self, pet_id: uuid.UUID, owner_id: uuid.UUID):
        pet = self.get(pet_id)
        pet.owner_id = owner_id
        return self.update_entity(pet)
```

### ❌ Don't Return DTOs from Repositories

```python
# WRONG: Returning DTO
class PetRepository(BaseRepository[Pet]):
    def get_pet_dto(self, pet_id: uuid.UUID) -> PetResponse:
        pet = self.get(pet_id)
        return PetResponse.model_validate(pet)  # ❌ DTO in repository!
```

✅ **Correct**: Return model instances

```python
# Repository returns model
class PetRepository(BaseRepository[Pet]):
    def get_pet(self, pet_id: uuid.UUID) -> Pet:
        return self.get(pet_id)  # ✅ Return model

# Controller converts to DTO
class PetController:
    def get_pet(self, pet_id: uuid.UUID) -> PetResponse:
        pet = self.pet_service.get_pet(pet_id)
        return PetResponse.model_validate(pet)  # ✅ DTO in controller
```

### ❌ Don't Call Other Repositories

```python
# WRONG: Repository calling another repository
class PetRepository(BaseRepository[Pet]):
    def __init__(self, session: Session, owner_repo: OwnerRepository):
        super().__init__(Pet, session)
        self.owner_repo = owner_repo  # ❌
    
    def get_pet_with_owner(self, pet_id: uuid.UUID):
        pet = self.get(pet_id)
        owner = self.owner_repo.get(pet.owner_id)  # ❌ Calling another repo!
        return pet, owner
```

✅ **Correct**: Service orchestrates multiple repositories

```python
# Service orchestrates repositories
class PetService:
    def __init__(
        self,
        pet_repository: PetRepository,
        owner_repository: OwnerRepository
    ):
        self.pet_repository = pet_repository
        self.owner_repository = owner_repository
    
    def get_pet_with_owner(self, pet_id: uuid.UUID):
        pet = self.pet_repository.get(pet_id)
        owner = self.owner_repository.get(pet.owner_id)
        return pet, owner  # ✅ Service orchestrates
```

---

## Testing Repositories

### Integration Test Example

```python
def test_get_active_pets(db_session):
    """Test repository with real database."""
    repo = PetRepository(db_session)
    
    # Create test data
    repo.create(name="Rex", owner_id=owner_id, is_active=True)
    repo.create(name="Max", owner_id=owner_id, is_active=False)
    
    # Test query
    active_pets = repo.get_active_pets(owner_id)
    
    assert len(active_pets) == 1
    assert active_pets[0].name == "Rex"
```

### Unit Test (Mocking Session)

```python
from unittest.mock import Mock

def test_get_by_owner_id():
    """Test repository logic without database."""
    mock_session = Mock()
    mock_session.query.return_value.filter.return_value.all.return_value = [
        Mock(name="Rex"),
        Mock(name="Max")
    ]
    
    repo = PetRepository(mock_session)
    pets = repo.get_by_owner_id(owner_id)
    
    assert len(pets) == 2
    mock_session.query.assert_called_once()
```

---

## Best Practices

1. ✅ Keep repositories focused on data access
2. ✅ Add domain-specific query methods
3. ✅ Use BaseRepository methods for common operations
4. ✅ Handle database exceptions appropriately
5. ✅ Document complex queries
6. ✅ Return model instances, not DTOs
7. ✅ Keep transaction logic in repositories
8. ❌ Don't add business logic
9. ❌ Don't call other repositories
10. ❌ Don't format responses

