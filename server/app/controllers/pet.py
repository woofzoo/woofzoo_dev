"""
Pet controller for API layer.

This module provides the PetController class for handling HTTP requests
and responses related to pet operations.
"""

from typing import List

from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.schemas.pet import PetCreate, PetListResponse, PetResponse, PetUpdate, PetLookupRequest, ClinicPetOnboardingRequest, ClinicPetOnboardingResponse
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
            logger.info("Creating new pet", extra={"pet_name": pet_data.name, "pet_type": pet_data.pet_type})
            pet = self.pet_service.create_pet(pet_data)
            logger.info("Pet created successfully", extra={"pet_id": pet.id, "pet_name": pet.name})
            return PetResponse.model_validate(pet)
        except ValueError as e:
            logger.warning("Pet creation failed - validation error", extra={"error": str(e), "pet_name": pet_data.name})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Pet creation failed - unexpected error", extra={
                "pet_name": pet_data.name,
                "pet_type": pet_data.pet_type
            })
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
            logger.exception("Failed to retrieve pets for owner", extra={
                "owner_id": owner_id,
                "error": str(e),
                "error_type": type(e).__name__
            })
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
    
    def onboard_pet_by_clinic(
        self, 
        onboarding_data: ClinicPetOnboardingRequest,
        current_user: User
    ) -> ClinicPetOnboardingResponse:
        """
        Onboard a pet via clinic.
        
        Note: Role validation (clinic_owner) is enforced at the route level.
        
        Args:
            onboarding_data: Clinic pet onboarding request data
            current_user: Current authenticated user (with clinic_owner role)
            
        Returns:
            ClinicPetOnboardingResponse: Response with pet details and onboarding status
            
        Raises:
            HTTPException: If onboarding fails
        """
        # Role check is handled by route dependency - no need to check again here
        try:
            logger.info(
                "Clinic pet onboarding initiated",
                extra={
                    "clinic_user_id": current_user.id,
                    "owner_email": onboarding_data.owner_email,
                    "pet_name": onboarding_data.pet_name
                }
            )
            
            # Call service to onboard pet
            pet, owner_user, is_new_user = self.pet_service.onboard_pet_by_clinic(
                onboarding_data=onboarding_data,
                clinic_user_id=current_user.public_id
            )
            
            # Build response message
            if is_new_user:
                message = "Pet onboarded successfully. A new account was created for the owner. Verification email sent."
            else:
                message = "Pet onboarded successfully. Pet has been added to existing owner account. Notification email sent."
            
            logger.info(
                "Clinic pet onboarding completed successfully",
                extra={
                    "clinic_user_id": current_user.id,
                    "pet_id": pet.pet_id,
                    "owner_user_id": str(owner_user.public_id),
                    "is_new_user": is_new_user
                }
            )
            
            # Return response
            return ClinicPetOnboardingResponse(
                pet=PetResponse.model_validate(pet),
                owner_created=is_new_user,
                message=message
            )
            
        except ValueError as e:
            logger.warning(
                "Clinic pet onboarding validation error",
                extra={
                    "clinic_user_id": current_user.id,
                    "error": str(e)
                }
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Clinic pet onboarding failed",
                extra={
                    "clinic_user_id": current_user.id,
                    "owner_email": onboarding_data.owner_email,
                    "pet_name": onboarding_data.pet_name
                }
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to onboard pet"
            )
