"""
Pet controller for API layer.

This module provides the PetController class for handling HTTP requests
and responses related to pet operations.
"""

from typing import List

from fastapi import HTTPException, status

from app.schemas.pet import PetCreate, PetListResponse, PetResponse, PetUpdate, PetLookupRequest
from app.services.pet import PetService
from loguru import logger


class PetController:
    """
    Pet controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to pet operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, pet_service: PetService) -> None:
        """Initialize the pet controller."""
        self.pet_service = pet_service
    
    def create_pet(self, pet_data: PetCreate) -> PetResponse:
        """Create a new pet."""
        try:
            pet = self.pet_service.create_pet(pet_data)
            return PetResponse.model_validate(pet)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Failed to create pet")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create pet"
            )
    
    def get_pet(self, pet_id: str) -> PetResponse:
        """Get a pet by ID."""
        pet = self.pet_service.get_pet_by_id(pet_id)
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pet with ID {pet_id} not found"
            )
        
        return PetResponse.model_validate(pet)
    
    def get_pet_by_pet_id(self, pet_id: str) -> PetResponse:
        """Get a pet by pet_id (unique identifier)."""
        pet = self.pet_service.get_pet_by_pet_id(pet_id)
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pet with pet_id {pet_id} not found"
            )
        
        return PetResponse.model_validate(pet)
    
    def get_pets_by_owner(self, owner_id: str, skip: int = 0, limit: int = 100) -> PetListResponse:
        """Get all pets for a specific owner."""
        try:
            pets = self.pet_service.get_pets_by_owner(owner_id, skip=skip, limit=limit)
            total = self.pet_service.count_pets_by_owner(owner_id)
            
            pet_responses = [PetResponse.model_validate(pet) for pet in pets]
            return PetListResponse(pets=pet_responses, total=total)
        except Exception as e:
            logger.exception("Failed to retrieve pets for owner_id={owner_id}", owner_id=owner_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve pets"
            )
    
    def update_pet(self, pet_id: str, pet_data: PetUpdate) -> PetResponse:
        """Update a pet."""
        try:
            pet = self.pet_service.update_pet(pet_id, pet_data)
            if not pet:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Pet with ID {pet_id} not found"
                )
            
            return PetResponse.model_validate(pet)
        except HTTPException as http_exc:
            logger.warning("Update pet failed: {detail}", detail=str(http_exc.detail))
            raise
        except Exception as e:
            logger.exception("Failed to update pet id={pet_id}", pet_id=pet_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update pet"
            )
    
    def delete_pet(self, pet_id: str) -> dict:
        """Delete a pet (soft delete)."""
        try:
            deleted = self.pet_service.delete_pet(pet_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Pet with ID {pet_id} not found"
                )
            
            return {"message": f"Pet with ID {pet_id} deleted successfully"}
        except HTTPException as http_exc:
            logger.warning("Delete pet failed: {detail}", detail=str(http_exc.detail))
            raise
        except Exception as e:
            logger.exception("Failed to delete pet id={pet_id}", pet_id=pet_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete pet"
            )
    
    def search_pets(self, search_term: str, skip: int = 0, limit: int = 100) -> PetListResponse:
        """Search pets by name, breed, or pet_type."""
        try:
            pets = self.pet_service.search_pets(
                search_term=search_term,
                skip=skip,
                limit=limit
            )
            
            pet_responses = [PetResponse.model_validate(pet) for pet in pets]
            return PetListResponse(pets=pet_responses, total=len(pet_responses))
        except Exception as e:
            logger.exception("Failed to search pets")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to search pets"
            )
    
    def get_pets_by_type(self, pet_type: str, skip: int = 0, limit: int = 100) -> PetListResponse:
        """Get all pets of a specific type."""
        try:
            pets = self.pet_service.get_pets_by_type(pet_type, skip=skip, limit=limit)
            
            pet_responses = [PetResponse.model_validate(pet) for pet in pets]
            return PetListResponse(pets=pet_responses, total=len(pet_responses))
        except Exception as e:
            logger.exception("Failed to retrieve pets by type {pet_type}", pet_type=pet_type)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve pets by type"
            )
    
    def get_pets_by_breed(self, breed: str, skip: int = 0, limit: int = 100) -> PetListResponse:
        """Get all pets of a specific breed."""
        try:
            pets = self.pet_service.get_pets_by_breed(breed, skip=skip, limit=limit)
            
            pet_responses = [PetResponse.model_validate(pet) for pet in pets]
            return PetListResponse(pets=pet_responses, total=len(pet_responses))
        except Exception as e:
            logger.exception("Failed to retrieve pets by breed {breed}", breed=breed)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve pets by breed"
            )
    
    def lookup_pet(self, pet_id: str) -> PetResponse:
        """Lookup pet by pet ID."""
        try:
            pet = self.pet_service.lookup_pet(pet_id)
            if not pet:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pet not found with the provided pet ID"
                )
            
            return PetResponse.model_validate(pet)
        except HTTPException as http_exc:
            logger.warning("Lookup pet failed: {detail}", detail=str(http_exc.detail))
            raise
        except Exception as e:
            logger.exception("Failed to lookup pet id={pet_id}", pet_id=pet_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to lookup pet"
            )
    
    def get_all_pets(self, skip: int = 0, limit: int = 100) -> PetListResponse:
        """Get all pets with pagination."""
        try:
            pets = self.pet_service.pet_repository.get_all(skip=skip, limit=limit)
            total = self.pet_service.count_active_pets()
            
            pet_responses = [PetResponse.model_validate(pet) for pet in pets]
            return PetListResponse(pets=pet_responses, total=total)
        except Exception as e:
            logger.exception("Failed to retrieve all pets")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve pets"
            )
