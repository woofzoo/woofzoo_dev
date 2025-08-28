"""
Schemas package for the application.

This package contains all Pydantic schemas for request/response validation.
"""

from app.schemas.auth import (
    UserSignup,
    UserLogin,
    UserResponse,
    TokenResponse,
    PasswordResetRequest,
    PasswordReset,
    EmailVerification,
    LoginResponse,
    MessageResponse,
    PersonalizationUpdate,
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
from app.schemas.family import (
    FamilyCreate,
    FamilyResponse,
    FamilyUpdate,
    FamilyListResponse,
    FamilyMemberCreate,
    FamilyMemberResponse,
    FamilyMemberUpdate,
    FamilyMemberListResponse,
    FamilyInvitationCreate,
    FamilyInvitationResponse,
    FamilyInvitationAccept,
    FamilyInvitationListResponse,
)

__all__ = [
    # Auth schemas
    "UserSignup",
    "UserLogin", 
    "UserResponse",
    "TokenResponse",
    "PasswordResetRequest",
    "PasswordReset",
    "EmailVerification",
    "LoginResponse",
    "MessageResponse",
    "PersonalizationUpdate",
    
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
    
    # Family schemas
    "FamilyCreate",
    "FamilyResponse",
    "FamilyUpdate",
    "FamilyListResponse",
    "FamilyMemberCreate",
    "FamilyMemberResponse",
    "FamilyMemberUpdate",
    "FamilyMemberListResponse",
    "FamilyInvitationCreate",
    "FamilyInvitationResponse",
    "FamilyInvitationAccept",
    "FamilyInvitationListResponse",
]
