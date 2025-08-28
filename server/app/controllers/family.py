"""
Family controller for API layer.

This module provides the FamilyController class for handling HTTP requests
and responses related to family operations.
"""

from typing import List

from fastapi import HTTPException, status

from app.schemas.family import FamilyCreate, FamilyListResponse, FamilyResponse, FamilyUpdate
from app.services.family import FamilyService


class FamilyController:
    """
    Family controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to family operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, family_service: FamilyService) -> None:
        """Initialize the family controller."""
        self.family_service = family_service
    
    def create_family(self, family_data: FamilyCreate, owner_id: str) -> FamilyResponse:
        """Create a new family."""
        try:
            family = self.family_service.create_family(family_data, owner_id)
            return FamilyResponse.model_validate(family)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create family"
            )
    
    def get_family(self, family_id: str) -> FamilyResponse:
        """Get a family by ID."""
        family = self.family_service.get_family_by_id(family_id)
        if not family:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Family with ID {family_id} not found"
            )
        
        return FamilyResponse.model_validate(family)
    
    def get_families_by_owner(self, owner_id: str, skip: int = 0, limit: int = 100) -> FamilyListResponse:
        """Get families by owner ID with pagination."""
        try:
            families = self.family_service.get_families_by_owner(owner_id, skip=skip, limit=limit)
            total = self.family_service.get_family_count_by_owner(owner_id)
            
            family_responses = [FamilyResponse.model_validate(family) for family in families]
            return FamilyListResponse(families=family_responses, total=total)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve families"
            )
    
    def update_family(self, family_id: str, family_data: FamilyUpdate) -> FamilyResponse:
        """Update a family."""
        try:
            family = self.family_service.update_family(family_id, family_data)
            if not family:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Family with ID {family_id} not found"
                )
            
            return FamilyResponse.model_validate(family)
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update family"
            )
    
    def delete_family(self, family_id: str) -> dict:
        """Delete a family."""
        try:
            deleted = self.family_service.delete_family(family_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Family with ID {family_id} not found"
                )
            
            return {"message": f"Family with ID {family_id} deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete family"
            )
    
    def search_families(self, search_term: str, owner_id: str = None, skip: int = 0, limit: int = 100) -> FamilyListResponse:
        """Search families by name or description."""
        try:
            families = self.family_service.search_families(
                search_term=search_term,
                owner_id=owner_id,
                skip=skip,
                limit=limit
            )
            
            family_responses = [FamilyResponse.model_validate(family) for family in families]
            return FamilyListResponse(families=family_responses, total=len(family_responses))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to search families"
            )
