"""
User service for read-only user operations.

Provides business logic for user read operations separate from auth flows.
"""

from typing import List, Optional

from app.models.user import User
from app.repositories.user import UserRepository


class UserService:
    """Service layer for user read operations."""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)

    def get_user_by_public_id(self, public_id: str) -> Optional[User]:
        return self.user_repository.get_by_field("public_id", public_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.get_by_email(email)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.user_repository.get_active_users(skip=skip, limit=limit)

    def search_users(self, search_term: str, skip: int = 0, limit: int = 100) -> List[User]:
        return self.user_repository.search_users(search_term, skip=skip, limit=limit)

    def count_users(self) -> int:
        return self.user_repository.count_active_users()


