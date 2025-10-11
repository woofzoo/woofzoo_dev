# Role-Based Access Control (RBAC) in Routes

## ✅ Yes! You Can Enforce Roles at Route Level

FastAPI allows you to enforce role-based access control directly in the route definition using dependencies. This is the **recommended approach** as it's more declarative and visible.

## 🎯 Available Role Dependencies

The system provides pre-built role dependencies:

```python
from app.dependencies import (
    get_clinic_owner_user,  # Requires 'clinic_owner' role
    get_pet_owner_user,     # Requires 'pet_owner' role
    get_doctor_user         # Requires 'doctor' role
)
```

## 📝 Usage Examples

### Example 1: Clinic-Only Endpoint (Our Implementation)

```python
from fastapi import APIRouter, Depends
from app.dependencies import get_clinic_owner_user
from app.models.user import User

@router.post("/clinic-onboard")
def onboard_pet_by_clinic(
    data: SomeData,
    current_user: User = Depends(get_clinic_owner_user),  # ✅ Role check here!
    controller = Depends(get_controller)
):
    """Only clinic owners can access this endpoint."""
    return controller.do_something(data, current_user)
```

**Benefits:**
- ✅ Role requirement is **visible** in the route signature
- ✅ No need to check role again in controller
- ✅ FastAPI automatically returns **403 Forbidden** if user lacks role
- ✅ Appears in OpenAPI/Swagger docs

### Example 2: Pet Owner Endpoint

```python
@router.get("/my-pets")
def get_my_pets(
    current_user: User = Depends(get_pet_owner_user),  # Pet owners only
    controller = Depends(get_pet_controller)
):
    """Only pet owners can access this endpoint."""
    return controller.get_pets_by_owner(current_user.public_id)
```

### Example 3: Doctor Endpoint

```python
@router.post("/medical-records")
def create_medical_record(
    data: MedicalRecordCreate,
    current_user: User = Depends(get_doctor_user),  # Doctors only
    controller = Depends(get_medical_record_controller)
):
    """Only doctors can create medical records."""
    return controller.create_record(data, current_user)
```

### Example 4: Multiple Roles Allowed

```python
from app.dependencies import require_roles

# Allow both pet_owner and family_member
@router.get("/pets/{pet_id}")
def get_pet(
    pet_id: str,
    current_user: User = Depends(require_roles(["pet_owner", "family_member"])),
    controller = Depends(get_pet_controller)
):
    """Pet owners and family members can view pets."""
    return controller.get_pet(pet_id)
```

## 🔄 Before vs After Comparison

### ❌ Before (Role Check in Controller)

**Route:**
```python
@router.post("/clinic-onboard")
def onboard_pet(
    data: Data,
    current_user: User = Depends(get_current_user),  # Generic auth
    controller = Depends(get_controller)
):
    return controller.onboard(data, current_user)
```

**Controller:**
```python
def onboard(self, data, current_user):
    # ❌ Have to check role here
    if "clinic_owner" not in current_user.roles:
        raise HTTPException(403, "Insufficient permissions")
    
    # Actual logic...
```

**Problems:**
- Role requirement not visible in route
- Duplicate checks if multiple routes use same controller
- Not shown in API docs
- Easy to forget the check

### ✅ After (Role Check at Route Level)

**Route:**
```python
@router.post("/clinic-onboard")
def onboard_pet(
    data: Data,
    current_user: User = Depends(get_clinic_owner_user),  # ✅ Role enforced here!
    controller = Depends(get_controller)
):
    return controller.onboard(data, current_user)
```

**Controller:**
```python
def onboard(self, data, current_user):
    # ✅ No role check needed - guaranteed clinic_owner
    # Just business logic...
```

**Benefits:**
- ✅ Clear role requirement in route signature
- ✅ Automatic 403 response
- ✅ Shows in Swagger/OpenAPI docs
- ✅ DRY - no duplicate checks
- ✅ Impossible to forget

## 🛠️ How It Works

The `require_roles` function is a **dependency factory**:

```python
def require_roles(required_roles: list[str]):
    """Create a dependency that checks for specific roles."""
    def check_roles(current_user = Depends(get_current_user)):
        user_roles = set(current_user.roles)
        required_roles_set = set(required_roles)
        
        if not user_roles.intersection(required_roles_set):
            raise HTTPException(403, "Insufficient permissions")
        
        return current_user
    
    return check_roles
```

The convenience functions are just pre-configured instances:

```python
get_clinic_owner_user = require_roles(["clinic_owner"])
get_pet_owner_user = require_roles(["pet_owner"])
get_doctor_user = require_roles(["doctor"])
```

## 📊 Execution Flow

```
1. Request comes in → POST /api/pets/clinic-onboard
                      ↓
2. JWT Auth Middleware → Validates token
                      ↓
3. get_clinic_owner_user → Checks if user has 'clinic_owner' role
                      ↓
                   ✅ Success          ❌ Fail
                      ↓                  ↓
4. Route Handler          403 Forbidden Response
   (controller.onboard)
```

## 🎨 OpenAPI/Swagger Documentation

When you use role dependencies, FastAPI **automatically documents** them:

```yaml
/api/pets/clinic-onboard:
  post:
    summary: "Onboard a pet via clinic (clinic_owner only)"
    security:
      - Bearer: []
    responses:
      403:
        description: "Insufficient permissions"
```

## 🔒 Security Best Practices

### ✅ DO:
- Use role dependencies at route level
- Keep role checks consistent across endpoints
- Use the pre-built convenience functions
- Document role requirements in route docstrings

### ❌ DON'T:
- Check roles in controller when route already checks
- Use `get_current_user` when you need a specific role
- Forget to add role requirement to route summary

## 📚 Creating Custom Role Dependencies

If you need a custom role combination:

```python
# In app/dependencies.py
get_admin_user = require_roles(["admin"])
get_moderator_user = require_roles(["moderator", "admin"])
get_medical_staff = require_roles(["doctor", "nurse"])
```

Then use them in routes:

```python
from app.dependencies import get_admin_user

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_admin_user),  # Admin only
    controller = Depends(get_controller)
):
    return controller.delete_user(user_id)
```

## 🎯 Summary

| Approach | Visibility | Automatic 403 | In Docs | Reusable | Best Practice |
|----------|-----------|---------------|---------|----------|---------------|
| **Route Level** | ✅ High | ✅ Yes | ✅ Yes | ✅ Yes | ✅ **Recommended** |
| Controller Level | ❌ Hidden | ❌ Manual | ❌ No | ❌ Duplicated | ❌ Not recommended |

**✅ Use route-level role dependencies for cleaner, more maintainable code!**

## 🚀 Quick Reference

```python
# Import the role dependency
from app.dependencies import get_clinic_owner_user

# Use in route
@router.post("/some-endpoint")
def my_endpoint(
    current_user: User = Depends(get_clinic_owner_user)  # That's it!
):
    # current_user is guaranteed to have clinic_owner role
    pass
```

**That's all there is to it!** 🎉

