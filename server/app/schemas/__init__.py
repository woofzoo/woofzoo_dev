"""
Schemas package for the application.

This package contains all Pydantic schemas for request/response validation.
"""

from app.schemas.auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    EmailVerificationRequest,
)
from app.schemas.owner import (
    OwnerCreate,
    OwnerUpdate,
    OwnerResponse,
    OwnerListResponse,
)
from app.schemas.pet import (
    PetCreate,
    PetUpdate,
    PetResponse,
    PetListResponse,
    PetLookupRequest,
)
from app.schemas.pet_types import (
    PetTypesResponse,
    PetBreedsResponse,
)

__all__ = [
    # Auth schemas
    "UserCreate",
    "UserLogin", 
    "UserResponse",
    "TokenResponse",
    "RefreshTokenRequest",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "EmailVerificationRequest",
    
    # Owner schemas
    "OwnerCreate",
    "OwnerUpdate",
    "OwnerResponse",
    "OwnerListResponse",
    
    # Pet schemas
    "PetCreate",
    "PetUpdate",
    "PetResponse",
    "PetListResponse",
    "PetLookupRequest",
    
    # Pet types schemas
    "PetTypesResponse",
    "PetBreedsResponse",
]
