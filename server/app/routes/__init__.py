"""
Routes package for the application.

This package contains all API route modules.
"""

from app.routes.auth import router as auth_router
from app.routes.owner import router as owner_router
from app.routes.user import router as user_router
from app.routes.pet import router as pet_router
from app.routes.pet_types import router as pet_types_router
from app.routes.family import router as family_router
from app.routes.family_member import router as family_member_router
from app.routes.family_invitation import router as family_invitation_router
from app.routes.photo import router as photo_router
from app.routes.doctor_profile_routes import router as doctor_profile_router
from app.routes.clinic_profile_routes import router as clinic_profile_router
from app.routes.medical_record_routes import router as medical_record_router

__all__ = [
    "auth_router",
    "user_router",
    "owner_router",
    "pet_router",
    "pet_types_router",
    "family_router",
    "family_member_router",
    "family_invitation_router",
    "photo_router",
    "doctor_profile_router",
    "clinic_profile_router",
    "medical_record_router",
]
