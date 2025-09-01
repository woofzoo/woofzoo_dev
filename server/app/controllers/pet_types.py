"""
Pet types controller for API layer.

This module provides the PetTypesController class for handling HTTP requests
and responses related to pet types and breeds operations.
"""

from fastapi import HTTPException, status

from app.schemas.pet_types import PetTypesResponse, PetBreedsResponse
from app.services.pet_types import PetTypesService


class PetTypesController:
    """
    Pet types controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to pet types and breeds operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, pet_types_service: PetTypesService) -> None:
        """Initialize the pet types controller."""
        self.pet_types_service = pet_types_service
    
    def get_pet_types(self) -> PetTypesResponse:
        """Get all available pet types."""
        try:
            types = self.pet_types_service.get_pet_types()
            return PetTypesResponse(types=types)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve pet types"
            )
    
    def get_breeds_for_type(self, pet_type: str) -> PetBreedsResponse:
        """Get breeds for a specific pet type."""
        try:
            breeds = self.pet_types_service.get_breeds_for_type(pet_type)
            if not breeds:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No breeds found for pet type '{pet_type}'"
                )
            
            return PetBreedsResponse(pet_type=pet_type, breeds=breeds)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve breeds for pet type"
            )
    
    def validate_pet_type_and_breed(self, pet_type: str, breed: str) -> dict:
        """Validate if pet type and breed combination is valid."""
        try:
            is_valid = self.pet_types_service.validate_pet_type_and_breed(pet_type, breed)
            return {
                "pet_type": pet_type,
                "breed": breed,
                "is_valid": is_valid
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to validate pet type and breed"
            )
    
    def get_pet_type_info(self, pet_type: str) -> dict:
        """Get detailed information about a pet type."""
        try:
            info = self.pet_types_service.get_pet_type_info(pet_type)
            if not info["breeds"]:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Pet type '{pet_type}' not found"
                )
            
            return info
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve pet type information"
            )
    
    def search_breeds(self, search_term: str, pet_type: str = None) -> dict:
        """Search breeds by name, optionally filtered by pet type."""
        try:
            breeds = self.pet_types_service.search_breeds(search_term, pet_type)
            return {
                "search_term": search_term,
                "pet_type": pet_type,
                "breeds": breeds,
                "count": len(breeds)
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to search breeds"
            )
