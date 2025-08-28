"""
Family routes for API endpoints.

This module defines all family-related API endpoints with proper
dependency injection and request/response handling.
"""

from fastapi import APIRouter, Depends, Query, status

from app.controllers.family import FamilyController
from app.dependencies import get_family_controller
from app.schemas.family import FamilyCreate, FamilyListResponse, FamilyResponse, FamilyUpdate

# Create router
router = APIRouter(prefix="/families", tags=["families"])


# API Endpoints
@router.post(
    "/",
    response_model=FamilyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new family",
    description="Create a new family with the provided data"
)
def create_family(
    family_data: FamilyCreate,
    owner_id: str = Query(..., description="Owner's unique identifier"),
    controller: FamilyController = Depends(get_family_controller)
) -> FamilyResponse:
    """Create a new family."""
    return controller.create_family(family_data, owner_id)


@router.get(
    "/",
    response_model=FamilyListResponse,
    summary="Get families by owner",
    description="Retrieve families for a specific owner with optional pagination"
)
def get_families_by_owner(
    owner_id: str = Query(..., description="Owner's unique identifier"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: FamilyController = Depends(get_family_controller)
) -> FamilyListResponse:
    """Get families by owner ID with pagination."""
    return controller.get_families_by_owner(owner_id, skip=skip, limit=limit)


@router.get(
    "/{family_id}",
    response_model=FamilyResponse,
    summary="Get a family by ID",
    description="Retrieve a specific family by its ID"
)
def get_family(
    family_id: str,
    controller: FamilyController = Depends(get_family_controller)
) -> FamilyResponse:
    """Get a family by ID."""
    return controller.get_family(family_id)


@router.put(
    "/{family_id}",
    response_model=FamilyResponse,
    summary="Update a family",
    description="Update an existing family with the provided data"
)
def update_family(
    family_id: str,
    family_data: FamilyUpdate,
    controller: FamilyController = Depends(get_family_controller)
) -> FamilyResponse:
    """Update a family."""
    return controller.update_family(family_id, family_data)


@router.delete(
    "/{family_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a family",
    description="Delete a family by its ID"
)
def delete_family(
    family_id: str,
    controller: FamilyController = Depends(get_family_controller)
) -> None:
    """Delete a family."""
    controller.delete_family(family_id)


@router.get(
    "/search/",
    response_model=FamilyListResponse,
    summary="Search families",
    description="Search families by name or description"
)
def search_families(
    q: str = Query(..., min_length=1, description="Search term"),
    owner_id: str = Query(None, description="Optional owner ID filter"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: FamilyController = Depends(get_family_controller)
) -> FamilyListResponse:
    """Search families by name or description."""
    return controller.search_families(search_term=q, owner_id=owner_id, skip=skip, limit=limit)
