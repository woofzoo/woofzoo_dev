"""
Routes package for the application.

This package contains all API route modules.
"""

from app.routes.auth import router as auth_router
from app.routes.owner import router as owner_router
from app.routes.pet import router as pet_router
from app.routes.pet_types import router as pet_types_router

__all__ = [
    "auth_router",
    "owner_router",
    "pet_router",
    "pet_types_router",
]
