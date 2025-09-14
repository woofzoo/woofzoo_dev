"""
Family Member routes for API endpoints.

This module defines all family member-related API endpoints with proper
dependency injection and request/response handling.
"""

from fastapi import APIRouter, Depends, Query, status

from app.controllers.family_member import FamilyMemberController
from app.dependencies import get_family_member_controller
from app.schemas.family import FamilyMemberCreate, FamilyMemberListResponse, FamilyMemberResponse, FamilyMemberUpdate

# Create router
router = APIRouter(prefix="/family-members", tags=["family-members"])


# API Endpoints
@router.post(
    "/",
    response_model=FamilyMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a family member",
    description="Add a new member to a family"
)
def add_family_member(
    family_id: str = Query(..., description="Family's unique identifier"),
    member_data: FamilyMemberCreate = None,
    controller: FamilyMemberController = Depends(get_family_member_controller)
) -> FamilyMemberResponse:
    """Add a new family member."""
    return controller.add_family_member(family_id, member_data)


@router.get(
    "/",
    response_model=FamilyMemberListResponse,
    summary="Get family members",
    description="Retrieve members of a specific family with optional pagination"
)
def get_family_members(
    family_id: str = Query(..., description="Family's unique identifier"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: FamilyMemberController = Depends(get_family_member_controller)
) -> FamilyMemberListResponse:
    """Get family members by family ID with pagination."""
    return controller.get_family_members(family_id, skip=skip, limit=limit)


@router.get(
    "/user/{user_id}",
    response_model=FamilyMemberListResponse,
    summary="Get user's families",
    description="Retrieve all families that a user is a member of"
)
def get_user_families(
    user_id: str,
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: FamilyMemberController = Depends(get_family_member_controller)
) -> FamilyMemberListResponse:
    """Get user's family memberships with pagination."""
    return controller.get_user_families(user_id, skip=skip, limit=limit)


@router.get(
    "/{member_id}",
    response_model=FamilyMemberResponse,
    summary="Get a family member by ID",
    description="Retrieve a specific family member by its ID"
)
def get_family_member(
    member_id: str,
    controller: FamilyMemberController = Depends(get_family_member_controller)
) -> FamilyMemberResponse:
    """Get a family member by ID."""
    return controller.get_family_member(member_id)


@router.put(
    "/{member_id}",
    response_model=FamilyMemberResponse,
    summary="Update a family member",
    description="Update an existing family member's access level"
)
def update_family_member(
    member_id: str,
    member_data: FamilyMemberUpdate,
    controller: FamilyMemberController = Depends(get_family_member_controller)
) -> FamilyMemberResponse:
    """Update a family member."""
    return controller.update_family_member(member_id, member_data)


@router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a family member",
    description="Remove a family member by their ID"
)
def remove_family_member(
    member_id: str,
    controller: FamilyMemberController = Depends(get_family_member_controller)
) -> None:
    """Remove a family member."""
    controller.remove_family_member(member_id)


@router.delete(
    "/family/{family_id}/user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove user from family",
    description="Remove a specific user from a family"
)
def remove_user_from_family(
    family_id: str,
    user_id: str,
    controller: FamilyMemberController = Depends(get_family_member_controller)
) -> None:
    """Remove a user from a family."""
    controller.remove_user_from_family(family_id, user_id)
