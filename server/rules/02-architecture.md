# Architecture & Code Organization

## Clean Architecture

Follow this layered architecture:

```
models → repositories → services → controllers → routes
```

Each layer has specific responsibilities and should not be bypassed.

---

## Layer Responsibilities

### Models (`app/models/`)

- Define database schema using SQLAlchemy
- Store enums as strings (see database rules)
- Include relationships between models
- **NO business logic**
- **NO database operations**

### Repositories (`app/repositories/`)

- **ALL database access happens here**
- Extend `BaseRepository` for common operations
- Add domain-specific query methods
- Handle SQLAlchemy session operations
- Return model instances (not DTOs)

### Services (`app/services/`)

- **Business logic ONLY**
- Call repositories for data access
- **NEVER inject `Session`**
- **NO direct database operations**
- Orchestrate multiple repository calls
- Apply business rules and validation

### Controllers (`app/controllers/`)

- **HTTP concerns ONLY**
- Parse requests
- Call services for business logic
- Format responses
- Handle HTTP exceptions
- **NO business logic**

### Routes (`app/routes/`)

- Define API endpoints
- Dependency injection setup
- Role-based access control (RBAC)
- OpenAPI documentation
- **NO business logic**

---

## General Principles

### Dependency Injection

- Use FastAPI's dependency injection system
- Inject dependencies at the route level
- Services receive repositories, not sessions
- Controllers receive services

### Separation of Concerns

- Keep business logic in services, not controllers
- Controllers should only handle HTTP concerns
- Don't bypass layers (e.g., controller → repository)

### Single Responsibility

- Each class should have one clear purpose
- Don't mix HTTP handling with business logic
- Don't mix business logic with data access

---

## Anti-Patterns to Avoid

❌ **Don't bypass layers**
```python
# WRONG: Controller calling repository directly
class MyController:
    def endpoint(self):
        entity = self.repository.get(id)  # Should call service!
```

❌ **Don't put business logic in controllers**
```python
# WRONG: Business logic in controller
class MyController:
    def endpoint(self):
        if entity.status == "active" and entity.age > 5:  # Business logic!
            # ... complex logic
```

❌ **Don't access database from services**
```python
# WRONG: Direct database access in service
class MyService:
    def __init__(self, db: Session):  # Never inject Session!
        self.db = db
```

✅ **Correct architecture**
```python
# Route → Controller → Service → Repository → Database
@router.get("/items/{id}")
def get_item(id: str, controller: Controller = Depends()):
    return controller.get_item(id)
```

