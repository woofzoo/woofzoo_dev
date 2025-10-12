# Enum Convention - Store as Strings, Not Database ENUMs

## ✅ Changes Applied

Per the project requirement, we **do not create database ENUMs**. Instead:
- ✅ Enums are defined in Python code
- ✅ Stored as simple strings in the database
- ✅ Cursor rule created in `.cursorrules`

---

## 📋 Why This Approach?

### Benefits
1. **Flexibility**: Easy to add new enum values without database migrations
2. **Portability**: Works across different database systems
3. **No Type Management**: No need to manage PostgreSQL ENUM types
4. **Easier Migrations**: Just string columns, no special enum handling
5. **Backwards Compatible**: Old values remain valid as strings

### Trade-offs
- No database-level constraint enforcement (validation happens in application)
- Slightly more storage (vs native enum)
- Need to validate enum values in application code (which we do via Pydantic)

---

## 🔧 Implementation Pattern

### ✅ CORRECT Way

```python
# Define Python enum
class QueueStatus(str, enum.Enum):
    """Queue status enumeration."""
    PENDING_PRECHECK = "pending_precheck"
    READY_FOR_DOCTOR = "ready_for_doctor"
    WITH_DOCTOR = "with_doctor"
    COMPLETED = "completed"

# Use String in SQLAlchemy model
queue_status: Optional[str] = Column(
    String(50),  # ✅ String, not Enum()
    nullable=True,
    index=True
)
```

### ❌ WRONG Way

```python
# Don't do this:
queue_status: Optional[str] = Column(
    Enum(QueueStatus),  # ❌ Creates database ENUM
    nullable=True
)
```

### ✅ CORRECT Migration

```python
def upgrade() -> None:
    # Use String column
    op.add_column('table_name', sa.Column('status', sa.String(50), nullable=True))
    # No enum creation!

def downgrade() -> None:
    op.drop_column('table_name', 'status')
    # No enum dropping!
```

### ❌ WRONG Migration

```python
def upgrade() -> None:
    # Don't do this:
    status_enum = sa.Enum('value1', 'value2', name='statustype')
    status_enum.create(op.get_bind())  # ❌
    op.add_column('table_name', sa.Column('status', status_enum))

def downgrade() -> None:
    sa.Enum(name='statustype').drop(op.get_bind())  # ❌
```

---

## 📁 Files Changed

### Migration Fixed
- `alembic/versions/bc9dd895956d_add_queue_and_precheck_fields_to_pet_.py`
  - Removed `sa.Enum()` creation
  - Changed to `sa.String(50)`
  - Removed enum drop in downgrade

### Model Updated
- `app/models/pet_clinic_access.py`
  - Changed `Enum(AccessStatus)` → `String(50)`
  - Changed `Enum(QueueStatus)` → `String(50)`
  - Removed `Enum` import from SQLAlchemy
  - Updated default values to use `.value` (e.g., `AccessStatus.ACTIVE.value`)

### Cursor Rule Created
- `.cursorrules`
  - Added "Enum Handling" section
  - Clear examples of correct vs incorrect patterns
  - Explains reasoning and best practices

---

## 🔍 Current Enum Fields in Database

All stored as `String(50)`:

### PetClinicAccess Model
1. **status** (AccessStatus enum)
   - Values: `"active"`, `"expired"`, `"revoked"`
   - Type in DB: `String(50)`
   - Default: `"active"`

2. **queue_status** (QueueStatus enum)
   - Values: `"pending_precheck"`, `"ready_for_doctor"`, `"with_doctor"`, `"completed"`
   - Type in DB: `String(50)`
   - No default (nullable)

---

## ✅ Verification

### Test Results
```
✅ Application starts successfully
✅ Models import correctly
✅ Enums defined in Python (not database)
✅ Stored as strings in database
✅ Migration applied successfully
```

### Enum Values
```python
QueueStatus.PENDING_PRECHECK = "pending_precheck"
QueueStatus.READY_FOR_DOCTOR = "ready_for_doctor"
QueueStatus.WITH_DOCTOR = "with_doctor"
QueueStatus.COMPLETED = "completed"

AccessStatus.ACTIVE = "active"
AccessStatus.EXPIRED = "expired"
AccessStatus.REVOKED = "revoked"
```

All working as expected! ✅

---

## 📝 Future Guidelines

### When Adding New Enums

1. **Define Python Enum**:
   ```python
   class MyStatus(str, enum.Enum):
       VALUE1 = "value1"
       VALUE2 = "value2"
   ```

2. **Use String in Model**:
   ```python
   my_status: Optional[str] = Column(String(50), nullable=True)
   ```

3. **Create String Column in Migration**:
   ```python
   op.add_column('table', sa.Column('my_status', sa.String(50), nullable=True))
   ```

4. **Validate in Pydantic Schema**:
   ```python
   my_status: MyStatus  # Pydantic will validate against enum values
   ```

### When Modifying Existing Enums

1. Just add new value to Python enum class
2. No database migration needed (it's just a string!)
3. Update Pydantic schemas if needed
4. Deploy and enjoy ✨

---

## 🎓 Benefits Recap

✅ **Flexibility**: Add enum values without migrations  
✅ **Portability**: Works with any database  
✅ **Simplicity**: No special enum type management  
✅ **Speed**: Faster migrations, no type recreation  
✅ **Safety**: Application-level validation via Pydantic  

---

**Status**: ✅ **CONVENTION ESTABLISHED & APPLIED**

All future code should follow this pattern as documented in `.cursorrules`.

