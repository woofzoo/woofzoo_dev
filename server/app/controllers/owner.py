"""
Owner controller for API layer.

This module provides the OwnerController class for handling HTTP requests
and responses related to owner operations.
"""

from typing import List

from fastapi import HTTPException, status

from app.schemas.owner import OwnerCreate, OwnerListResponse, OwnerResponse, OwnerUpdate
from app.services.owner import OwnerService
from loguru import logger


class OwnerController:
    """
    Owner controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to owner operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, owner_service: OwnerService) -> None:
        """Initialize the owner controller."""
        self.owner_service = owner_service
    
    def create_owner(self, owner_data: OwnerCreate) -> OwnerResponse:
        """Create a new owner."""
        try:
            owner = self.owner_service.create_owner(owner_data)
            return OwnerResponse.model_validate(owner)
        except ValueError as e:
            logger.warning("Create owner failed: {message}", message=str(e))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Unexpected error creating owner")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create owner"
            )
    
    def get_owner(self, owner_id: str) -> OwnerResponse:
        """Get an owner by ID."""
        owner = self.owner_service.get_owner_by_id(owner_id)
        if not owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Owner with ID {owner_id} not found"
            )
        
        return OwnerResponse.model_validate(owner)
    
    def get_owner_by_phone(self, phone_number: str) -> OwnerResponse:
        """Get an owner by phone number."""
        owner = self.owner_service.get_owner_by_phone(phone_number)
        if not owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Owner with phone number {phone_number} not found"
            )
        
        return OwnerResponse.model_validate(owner)
    
    def get_all_owners(self, skip: int = 0, limit: int = 100) -> OwnerListResponse:
        """Get all owners with pagination."""
        try:
            owners = self.owner_service.get_all_owners(skip=skip, limit=limit)
            total = self.owner_service.count_owners()
            
            owner_responses = [OwnerResponse.model_validate(owner) for owner in owners]
            return OwnerListResponse(owners=owner_responses, total=total)
        except Exception as e:
            logger.exception("Unexpected error retrieving owners")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve owners"
            )
    
    def update_owner(self, owner_id: str, owner_data: OwnerUpdate) -> OwnerResponse:
        """Update an owner."""
        try:
            owner = self.owner_service.update_owner(owner_id, owner_data)
            if not owner:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Owner with ID {owner_id} not found"
                )
            
            return OwnerResponse.model_validate(owner)
        except HTTPException:
            logger.error("Update owner failed: not found")
            raise
        except Exception as e:
            logger.exception("Unexpected error updating owner")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update owner"
            )
    
    def delete_owner(self, owner_id: str) -> dict:
        """Delete an owner (soft delete)."""
        try:
            deleted = self.owner_service.delete_owner(owner_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Owner with ID {owner_id} not found"
                )
            
            return {"message": f"Owner with ID {owner_id} deleted successfully"}
        except HTTPException:
            logger.error("Delete owner failed: not found")
            raise
        except Exception as e:
            logger.exception("Unexpected error deleting owner")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete owner"
            )
    
    def search_owners(self, search_term: str, skip: int = 0, limit: int = 100) -> OwnerListResponse:
        """Search owners by name or phone number."""
        try:
            owners = self.owner_service.search_owners(
                search_term=search_term,
                skip=skip,
                limit=limit
            )
            
            owner_responses = [OwnerResponse.model_validate(owner) for owner in owners]
            return OwnerListResponse(owners=owner_responses, total=len(owner_responses))
        except Exception as e:
            logger.exception("Unexpected error searching owners")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to search owners"
            )
