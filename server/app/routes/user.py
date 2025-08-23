"""
User routes for API endpoints.

This module demonstrates how route files become much cleaner
when using centralized dependency injection.
"""

from fastapi import APIRouter, Depends, Query, status

from app.controllers.user import UserController
from app.dependencies import get_user_controller
from app.schemas.user import UserCreate, UserListResponse, UserResponse, UserUpdate

# Create router
router = APIRouter(prefix="/users", tags=["users"])


# API Endpoints
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided data"
)
async def create_user(
    user_data: UserCreate,
    controller: UserController = Depends(get_user_controller)
) -> UserResponse:
    """Create a new user."""
    return await controller.create_user(user_data)


@router.get(
    "/",
    response_model=UserListResponse,
    summary="Get all users",
    description="Retrieve all users with optional pagination"
)
async def get_users(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: UserController = Depends(get_user_controller)
) -> UserListResponse:
    """Get all users with pagination."""
    return await controller.get_all_users(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get a user by ID",
    description="Retrieve a specific user by their ID"
)
async def get_user(
    user_id: int,
    controller: UserController = Depends(get_user_controller)
) -> UserResponse:
    """Get a user by ID."""
    return await controller.get_user(user_id)


@router.get(
    "/{user_id}/with-tasks",
    summary="Get user with tasks",
    description="Retrieve a user with their associated tasks"
)
async def get_user_with_tasks(
    user_id: int,
    controller: UserController = Depends(get_user_controller)
) -> dict:
    """Get a user with their tasks."""
    return await controller.get_user_with_tasks(user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update a user",
    description="Update an existing user with the provided data"
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    controller: UserController = Depends(get_user_controller)
) -> UserResponse:
    """Update a user."""
    return await controller.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Delete a user by their ID"
)
async def delete_user(
    user_id: int,
    controller: UserController = Depends(get_user_controller)
) -> None:
    """Delete a user."""
    await controller.delete_user(user_id)
