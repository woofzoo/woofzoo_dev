"""
Pet types routes for API endpoints.

This module defines all pet types and breeds related API endpoints with proper
dependency injection and request/response handling.
"""

from fastapi import APIRouter, Depends, Query

from app.controllers.pet_types import PetTypesController
from app.dependencies import get_pet_types_controller
from app.schemas.pet_types import PetTypesResponse, PetBreedsResponse

# Create router
router = APIRouter(prefix="/pet-types", tags=["pet-types"])


# API Endpoints
@router.get(
    "/",
    response_model=PetTypesResponse,
    summary="Get available pet types",
    description="Retrieve list of all available pet types"
)
def get_pet_types(
    controller: PetTypesController = Depends(get_pet_types_controller)
) -> PetTypesResponse:
    """Get available pet types."""
    return controller.get_pet_types()


@router.get(
    "/search/breeds",
    summary="Search breeds",
    description="Search breeds by name, optionally filtered by pet type"
)
def search_breeds(
    q: str = Query(..., min_length=1, description="Search term"),
    pet_type: str = Query(None, description="Optional pet type filter"),
    controller: PetTypesController = Depends(get_pet_types_controller)
) -> dict:
    """Search breeds by name, optionally filtered by pet type."""
    return controller.search_breeds(search_term=q, pet_type=pet_type)


@router.get(
    "/{pet_type}/breeds",
    response_model=PetBreedsResponse,
    summary="Get breeds for pet type",
    description="Retrieve list of breeds for a specific pet type"
)
def get_pet_breeds(
    pet_type: str,
    controller: PetTypesController = Depends(get_pet_types_controller)
) -> PetBreedsResponse:
    """Get breeds for a specific pet type."""
    return controller.get_breeds_for_type(pet_type)


@router.get(
    "/{pet_type}/info",
    summary="Get pet type information",
    description="Retrieve detailed information about a specific pet type"
)
def get_pet_type_info(
    pet_type: str,
    controller: PetTypesController = Depends(get_pet_types_controller)
) -> dict:
    """Get detailed information about a pet type."""
    return controller.get_pet_type_info(pet_type)


@router.get(
    "/validate/{pet_type}/{breed}",
    summary="Validate pet type and breed",
    description="Validate if a pet type and breed combination is valid"
)
def validate_pet_type_and_breed(
    pet_type: str,
    breed: str,
    controller: PetTypesController = Depends(get_pet_types_controller)
) -> dict:
    """Validate if pet type and breed combination is valid."""
    return controller.validate_pet_type_and_breed(pet_type, breed)

