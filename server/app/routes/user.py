"""
User routes for read-only endpoints.

These endpoints are not tied to auth flows.
"""

from fastapi import APIRouter, Depends, Query

from app.controllers.user import UserController
from app.dependencies import get_user_controller
from app.schemas.user import UserListResponse, UserResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=UserListResponse,
    summary="Get users",
    description="Retrieve users with pagination"
)
async def get_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    controller: UserController = Depends(get_user_controller)
) -> UserListResponse:
    return controller.get_all_users(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID"
)
async def get_user_by_id(
    user_id: int,
    controller: UserController = Depends(get_user_controller)
) -> UserResponse:
    return controller.get_user(user_id)


@router.get(
    "/public/{public_id}",
    response_model=UserResponse,
    summary="Get user by public_id"
)
async def get_user_by_public_id(
    public_id: str,
    controller: UserController = Depends(get_user_controller)
) -> UserResponse:
    return controller.get_user_by_public_id(public_id)


@router.get(
    "/search/",
    response_model=UserListResponse,
    summary="Search users"
)
async def search_users(
    q: str = Query(..., min_length=1),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    controller: UserController = Depends(get_user_controller)
) -> UserListResponse:
    return controller.search_users(q=q, skip=skip, limit=limit)


