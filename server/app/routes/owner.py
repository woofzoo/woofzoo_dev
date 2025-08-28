"""
Owner routes for API endpoints.

This module defines all owner-related API endpoints with proper
dependency injection and request/response handling.
"""

from fastapi import APIRouter, Depends, Query, status

from app.controllers.owner import OwnerController
from app.dependencies import get_owner_controller
from app.schemas.owner import OwnerCreate, OwnerListResponse, OwnerResponse, OwnerUpdate

# Create router
router = APIRouter(prefix="/owners", tags=["owners"])


# API Endpoints
@router.post(
    "/",
    response_model=OwnerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new owner",
    description="Create a new owner with the provided data"
)
async def create_owner(
    owner_data: OwnerCreate,
    controller: OwnerController = Depends(get_owner_controller)
) -> OwnerResponse:
    """Create a new owner."""
    return controller.create_owner(owner_data)


@router.get(
    "/",
    response_model=OwnerListResponse,
    summary="Get all owners",
    description="Retrieve all owners with optional pagination"
)
async def get_owners(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: OwnerController = Depends(get_owner_controller)
) -> OwnerListResponse:
    """Get all owners with pagination."""
    return controller.get_all_owners(skip=skip, limit=limit)


@router.get(
    "/{owner_id}",
    response_model=OwnerResponse,
    summary="Get an owner by ID",
    description="Retrieve a specific owner by their ID"
)
async def get_owner(
    owner_id: str,
    controller: OwnerController = Depends(get_owner_controller)
) -> OwnerResponse:
    """Get an owner by ID."""
    return controller.get_owner(owner_id)


@router.get(
    "/phone/{phone_number}",
    response_model=OwnerResponse,
    summary="Get an owner by phone number",
    description="Retrieve a specific owner by their phone number"
)
async def get_owner_by_phone(
    phone_number: str,
    controller: OwnerController = Depends(get_owner_controller)
) -> OwnerResponse:
    """Get an owner by phone number."""
    return controller.get_owner_by_phone(phone_number)


@router.patch(
    "/{owner_id}",
    response_model=OwnerResponse,
    summary="Update an owner",
    description="Update an existing owner with the provided data"
)
async def update_owner(
    owner_id: str,
    owner_data: OwnerUpdate,
    controller: OwnerController = Depends(get_owner_controller)
) -> OwnerResponse:
    """Update an owner."""
    return controller.update_owner(owner_id, owner_data)


@router.delete(
    "/{owner_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an owner",
    description="Delete an owner by their ID"
)
async def delete_owner(
    owner_id: str,
    controller: OwnerController = Depends(get_owner_controller)
) -> None:
    """Delete an owner."""
    controller.delete_owner(owner_id)


@router.get(
    "/search/",
    response_model=OwnerListResponse,
    summary="Search owners",
    description="Search owners by name or phone number"
)
async def search_owners(
    q: str = Query(..., min_length=1, description="Search term"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: OwnerController = Depends(get_owner_controller)
) -> OwnerListResponse:
    """Search owners by name or phone number."""
    return controller.search_owners(search_term=q, skip=skip, limit=limit)
