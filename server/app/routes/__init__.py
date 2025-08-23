"""
Routes package for API endpoints.

This package contains all route modules for API endpoints.
"""

from app.routes.task import router as task_router
from app.routes.auth import router as auth_router

__all__ = ["task_router", "auth_router"]
