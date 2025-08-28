"""
Pet routes for API endpoints.

This module defines all pet-related API endpoints with proper
dependency injection and request/response handling.
"""

from fastapi import APIRouter, Depends, Query, status

from app.controllers.pet import PetController
from app.dependencies import get_pet_controller
from app.schemas.pet import PetCreate, PetListResponse, PetResponse, PetUpdate, PetLookupRequest

# Create router
router = APIRouter(prefix="/pets", tags=["pets"])


# API Endpoints
@router.post(
    "/",
    response_model=PetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new pet",
    description="Create a new pet with the provided data"
)
def create_pet(
    pet_data: PetCreate,
    controller: PetController = Depends(get_pet_controller)
) -> PetResponse:
    """Create a new pet."""
    return controller.create_pet(pet_data)


@router.get(
    "/",
    response_model=PetListResponse,
    summary="Get all pets",
    description="Retrieve all pets with optional pagination"
)
def get_pets(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: PetController = Depends(get_pet_controller)
) -> PetListResponse:
    """Get all pets with pagination."""
    return controller.get_all_pets(skip=skip, limit=limit)


@router.get(
    "/{pet_id}",
    response_model=PetResponse,
    summary="Get a pet by ID",
    description="Retrieve a specific pet by their ID"
)
def get_pet(
    pet_id: str,
    controller: PetController = Depends(get_pet_controller)
) -> PetResponse:
    """Get a pet by ID."""
    return controller.get_pet(pet_id)


@router.get(
    "/pet-id/{pet_id}",
    response_model=PetResponse,
    summary="Get a pet by pet ID",
    description="Retrieve a specific pet by their pet ID"
)
def get_pet_by_pet_id(
    pet_id: str,
    controller: PetController = Depends(get_pet_controller)
) -> PetResponse:
    """Get a pet by pet ID."""
    return controller.get_pet_by_pet_id(pet_id)


@router.get(
    "/owner/{owner_id}",
    response_model=PetListResponse,
    summary="Get pets by owner",
    description="Retrieve all pets belonging to a specific owner"
)
def get_pets_by_owner(
    owner_id: str,
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: PetController = Depends(get_pet_controller)
) -> PetListResponse:
    """Get pets by owner."""
    return controller.get_pets_by_owner(owner_id=owner_id, skip=skip, limit=limit)


@router.patch(
    "/{pet_id}",
    response_model=PetResponse,
    summary="Update a pet",
    description="Update an existing pet with the provided data"
)
def update_pet(
    pet_id: str,
    pet_data: PetUpdate,
    controller: PetController = Depends(get_pet_controller)
) -> PetResponse:
    """Update a pet."""
    return controller.update_pet(pet_id, pet_data)


@router.delete(
    "/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a pet",
    description="Delete a pet by their ID"
)
def delete_pet(
    pet_id: str,
    controller: PetController = Depends(get_pet_controller)
) -> None:
    """Delete a pet."""
    controller.delete_pet(pet_id)


@router.get(
    "/search/",
    response_model=PetListResponse,
    summary="Search pets",
    description="Search pets by name or breed"
)
def search_pets(
    q: str = Query(..., min_length=1, description="Search term"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: PetController = Depends(get_pet_controller)
) -> PetListResponse:
    """Search pets by name or breed."""
    return controller.search_pets(search_term=q, skip=skip, limit=limit)


@router.get(
    "/type/{pet_type}",
    response_model=PetListResponse,
    summary="Get pets by type",
    description="Retrieve all pets of a specific type"
)
def get_pets_by_type(
    pet_type: str,
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: PetController = Depends(get_pet_controller)
) -> PetListResponse:
    """Get pets by type."""
    return controller.get_pets_by_type(pet_type=pet_type, skip=skip, limit=limit)


@router.get(
    "/breed/{breed}",
    response_model=PetListResponse,
    summary="Get pets by breed",
    description="Retrieve all pets of a specific breed"
)
def get_pets_by_breed(
    breed: str,
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: PetController = Depends(get_pet_controller)
) -> PetListResponse:
    """Get pets by breed."""
    return controller.get_pets_by_breed(breed=breed, skip=skip, limit=limit)


@router.post(
    "/lookup",
    response_model=PetResponse,
    summary="Lookup pet by pet ID",
    description="Lookup a pet by their unique pet ID"
)
def lookup_pet(
    lookup_data: PetLookupRequest,
    controller: PetController = Depends(get_pet_controller)
) -> PetResponse:
    """Lookup a pet by pet ID."""
    return controller.lookup_pet(lookup_data.pet_id)
