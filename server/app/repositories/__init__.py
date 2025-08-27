"""
Repositories package for data access layer.

This package contains all repository classes for database operations.
"""

from app.repositories.base import BaseRepository
from app.repositories.user import UserRepository

__all__ = ["BaseRepository", "UserRepository"]
