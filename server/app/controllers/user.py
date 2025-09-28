"""
User controller for API layer.

Handles HTTP concerns for user read endpoints.
"""

from fastapi import HTTPException, status

from app.schemas.user import UserListResponse, UserResponse
from app.services.user import UserService


class UserController:
    """Controller for user read operations."""

    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def get_user(self, user_id: int) -> UserResponse:
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return UserResponse.model_validate(user)

    def get_user_by_public_id(self, public_id: str) -> UserResponse:
        user = self.user_service.get_user_by_public_id(public_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with public_id {public_id} not found"
            )
        return UserResponse.model_validate(user)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> UserListResponse:
        users = self.user_service.get_all_users(skip=skip, limit=limit)
        total = self.user_service.count_users()
        user_responses = [UserResponse.model_validate(u) for u in users]
        return UserListResponse(users=user_responses, total=total)

    def search_users(self, q: str, skip: int = 0, limit: int = 100) -> UserListResponse:
        users = self.user_service.search_users(q, skip=skip, limit=limit)
        user_responses = [UserResponse.model_validate(u) for u in users]
        return UserListResponse(users=user_responses, total=len(user_responses))


