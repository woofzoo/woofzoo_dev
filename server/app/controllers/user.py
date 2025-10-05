"""
User controller for API layer.

Handles HTTP concerns for user read endpoints.
"""

from fastapi import HTTPException, status
from loguru import logger

from app.schemas.user import UserListResponse, UserResponse
from app.services.user import UserService


class UserController:
    """Controller for user read operations."""

    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def get_user(self, user_id: int) -> UserResponse:
        logger.info("Fetching user by ID", extra={"user_id": user_id})
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            logger.warning("User not found", extra={"user_id": user_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        logger.info("User retrieved successfully", extra={"user_id": user_id, "public_id": user.public_id})
        return UserResponse.model_validate(user)

    def get_user_by_public_id(self, public_id: str) -> UserResponse:
        logger.info("Fetching user by public ID", extra={"public_id": public_id})
        user = self.user_service.get_user_by_public_id(public_id)
        if not user:
            logger.warning("User not found by public ID", extra={"public_id": public_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with public_id {public_id} not found"
            )
        logger.info("User retrieved successfully by public ID", extra={"public_id": public_id, "user_id": user.id})
        return UserResponse.model_validate(user)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> UserListResponse:
        logger.info("Fetching all users", extra={"skip": skip, "limit": limit})
        users = self.user_service.get_all_users(skip=skip, limit=limit)
        total = self.user_service.count_users()
        user_responses = [UserResponse.model_validate(u) for u in users]
        logger.info("Users retrieved successfully", extra={"count": len(user_responses), "total": total})
        return UserListResponse(users=user_responses, total=total)

    def search_users(self, q: str, skip: int = 0, limit: int = 100) -> UserListResponse:
        logger.info("Searching users", extra={"query": q, "skip": skip, "limit": limit})
        users = self.user_service.search_users(q, skip=skip, limit=limit)
        user_responses = [UserResponse.model_validate(u) for u in users]
        logger.info("User search completed", extra={"query": q, "results_count": len(user_responses)})
        return UserListResponse(users=user_responses, total=len(user_responses))


