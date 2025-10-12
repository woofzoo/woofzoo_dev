# Service Layer Rules

## Critical Rules

### 🚫 NEVER Inject Session

- Services must **NEVER** receive `Session` as a dependency
- Services must **ONLY** call repository methods for data access
- Services must **NOT** use `session.commit()`, `session.refresh()`, or `session.query()`
- All database operations must go through repositories

---

## Examples

### ✅ CORRECT

```python
class MyService:
    def __init__(self, repo: Repository):
        self.repo = repo
    
    def update_item(self, item_id):
        item = self.repo.get(item_id)
        item.field = "new_value"
        return self.repo.update_entity(item)
```

### ❌ WRONG

```python
class MyService:
    def __init__(self, db: Session, repo: Repository):
        self.db = db  # ❌ Never inject Session!
    
    def update_item(self, item_id):
        item = self.repo.get(item_id)
        item.field = "new_value"
        self.db.commit()  # ❌ Never use session directly!
```

---

## Service Responsibilities

### What Services SHOULD Do

- ✅ Implement business logic
- ✅ Call repository methods for data access
- ✅ Orchestrate multiple repository calls
- ✅ Apply business rules and validation
- ✅ Transform data between layers
- ✅ Handle business exceptions

### What Services SHOULD NOT Do

- ❌ Access database directly
- ❌ Handle HTTP concerns (status codes, headers)
- ❌ Format HTTP responses
- ❌ Validate request syntax (use Pydantic)
- ❌ Know about FastAPI dependencies
- ❌ Import SQLAlchemy session

---

## Common Patterns

### Single Repository Service

```python
class PetService:
    def __init__(self, pet_repository: PetRepository):
        self.pet_repository = pet_repository
    
    def get_active_pets(self, owner_id: uuid.UUID) -> List[Pet]:
        pets = self.pet_repository.get_by_owner_id(owner_id)
        return [pet for pet in pets if pet.is_active]
```

### Multiple Repository Service

```python
class ClinicWorkflowService:
    def __init__(
        self,
        pet_repository: PetRepository,
        user_repository: UserRepository,
        access_repository: PetClinicAccessRepository
    ):
        self.pet_repository = pet_repository
        self.user_repository = user_repository
        self.access_repository = access_repository
    
    def grant_clinic_access(self, pet_id: uuid.UUID, clinic_id: uuid.UUID):
        # Orchestrate multiple repository calls
        pet = self.pet_repository.get(pet_id)
        clinic = self.user_repository.get(clinic_id)
        
        if not pet or not clinic:
            raise ValueError("Pet or clinic not found")
        
        return self.access_repository.grant_access(pet_id, clinic_id)
```

### Service with External Dependencies

```python
class NotificationService:
    def __init__(
        self,
        user_repository: UserRepository,
        email_service: EmailService
    ):
        self.user_repository = user_repository
        self.email_service = email_service
    
    def notify_owner(self, user_id: uuid.UUID, message: str):
        user = self.user_repository.get_by_public_id(user_id)
        if user:
            self.email_service.send_notification(user.email, message)
```

---

## Rationale

### Why No Session Injection?

1. **Testability**
   - Mock only repositories, not sessions
   - Easier to write unit tests
   - Clear dependencies

2. **Clean Architecture**
   - Services don't know about database
   - Can swap database implementations
   - Clear separation of concerns

3. **Maintainability**
   - Database logic in one place (repositories)
   - Easier to find and fix data access bugs
   - Consistent patterns across codebase

4. **Consistency**
   - All data access through repositories
   - No mixed patterns
   - Easier for new developers to understand

---

## Migration Guide

### If You Have Session Injection

1. **Remove Session from constructor**
   ```python
   # Before
   def __init__(self, db: Session, repo: Repository):
       self.db = db
   
   # After
   def __init__(self, repo: Repository):
       # No db!
   ```

2. **Replace direct session calls**
   ```python
   # Before
   self.db.commit()
   self.db.refresh(entity)
   
   # After
   return self.repo.update_entity(entity)
   ```

3. **Move queries to repositories**
   ```python
   # Before (in service)
   items = self.db.query(Item).filter(Item.status == "active").all()
   
   # After (in repository)
   # Add method to repository:
   def get_active_items(self) -> List[Item]:
       return self.session.query(Item).filter(Item.status == "active").all()
   
   # Then call from service:
   items = self.repo.get_active_items()
   ```

---

## Testing Services

### Unit Test Example

```python
from unittest.mock import Mock

def test_update_item():
    # Mock repository only
    mock_repo = Mock(spec=Repository)
    mock_repo.get.return_value = Mock(id=1, field="old")
    mock_repo.update_entity.return_value = Mock(id=1, field="new")
    
    service = MyService(repo=mock_repo)
    result = service.update_item(1)
    
    mock_repo.get.assert_called_once_with(1)
    mock_repo.update_entity.assert_called_once()
    assert result.field == "new"
```

No need to mock sessions! ✅

