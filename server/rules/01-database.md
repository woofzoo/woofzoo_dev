# Database & Models Rules

## Enum Handling

- **NEVER create database ENUMs** (no PostgreSQL ENUM types)
- **Store enums as strings** in the database using `String(50)` or similar
- **Define Python enums** in code using `enum.Enum` for type safety

### Example

```python
# In model (CORRECT):
class Status(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

status: Optional[str] = Column(String(50), nullable=True)

# NOT this (WRONG):
status: Optional[str] = Column(Enum(Status), nullable=True)  # ❌ Don't use SQLAlchemy Enum()
```

### In Migrations

- Use `sa.String(50)`, never `sa.Enum()`
- Never use `sa.Enum().create(op.get_bind())`
- Never use `sa.Enum(name='...').drop()` in downgrades

### Reason

Database flexibility, easier migrations, no enum type management

---

## Migration Guidelines

- Always use string columns for enum-like fields
- Never use `sa.Enum().create(op.get_bind())`
- Never use `sa.Enum(name='...').drop()` in downgrades
- Test both upgrade and downgrade paths
- Document breaking changes in migration file docstrings

