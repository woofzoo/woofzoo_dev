"""
Pet Journal controller for API layer.

This module provides the PetJournalController class for handling HTTP requests
and responses related to pet journal operations.
"""

from datetime import date
from typing import Optional
import uuid

from fastapi import HTTPException, status

from app.schemas.pet_journal import (
    PetJournalCreate,
    PetJournalUpdate,
    PetJournalResponse,
    PetJournalListResponse
)
from app.services.pet_journal_service import PetJournalService
from loguru import logger


class PetJournalController:
    """
    Pet Journal controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to pet journal operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, pet_journal_service: PetJournalService) -> None:
        """
        Initialize the pet journal controller.
        
        Args:
            pet_journal_service: Service for pet journal operations
        """
        self.pet_journal_service = pet_journal_service
    
    def create_journal_entry(
        self,
        journal_data: PetJournalCreate,
        user_id: int
    ) -> PetJournalResponse:
        """
        Create a new journal entry for a pet.
        
        Args:
            journal_data: Journal entry data
            user_id: ID of the authenticated user
            
        Returns:
            Created journal entry response
            
        Raises:
            HTTPException: If creation fails
        """
        try:
            logger.info(
                "Creating journal entry",
                extra={
                    "pet_id": journal_data.pet_id,
                    "entry_type": journal_data.entry_type,
                    "user_id": user_id
                }
            )
            entry = self.pet_journal_service.create_journal_entry(journal_data, user_id)
            logger.info(
                "Journal entry created successfully",
                extra={"entry_id": str(entry.id)}
            )
            return PetJournalResponse.model_validate(entry)
        except ValueError as e:
            logger.warning("Journal entry creation failed", extra={"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Unexpected error creating journal entry")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create journal entry"
            )
    
    def get_journal_entry(self, entry_id: str) -> PetJournalResponse:
        """
        Get a specific journal entry.
        
        Args:
            entry_id: Journal entry unique identifier
            
        Returns:
            Journal entry response
            
        Raises:
            HTTPException: If entry not found
        """
        try:
            entry_uuid = uuid.UUID(entry_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid entry_id format: {entry_id}"
            )
        
        entry = self.pet_journal_service.get_journal_entry_by_id(entry_uuid)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Journal entry with ID {entry_id} not found"
            )
        
        return PetJournalResponse.model_validate(entry)
    
    def get_journal_entries_by_pet(
        self,
        pet_id: str,
        skip: int = 0,
        limit: int = 100,
        entry_type: Optional[str] = None
    ) -> PetJournalListResponse:
        """
        Get journal entries for a pet with optional filtering.
        
        Args:
            pet_id: Pet's unique identifier
            skip: Number of records to skip
            limit: Maximum number of records to return
            entry_type: Optional filter by entry type
            
        Returns:
            List of journal entries
            
        Raises:
            HTTPException: If pet ID is invalid
        """
        try:
            pet_uuid = uuid.UUID(pet_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid pet_id format: {pet_id}"
            )
        
        try:
            entries = self.pet_journal_service.get_journal_entries_by_pet(
                pet_uuid, skip, limit, entry_type
            )
            total = self.pet_journal_service.count_journal_entries(pet_uuid)
            
            return PetJournalListResponse(
                entries=[PetJournalResponse.model_validate(e) for e in entries],
                total=total
            )
        except Exception as e:
            logger.exception("Error retrieving journal entries")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve journal entries"
            )
    
    def get_journal_entries_by_date_range(
        self,
        pet_id: str,
        start_date: date,
        end_date: date,
        entry_type: Optional[str] = None
    ) -> PetJournalListResponse:
        """
        Get journal entries within a date range.
        
        Args:
            pet_id: Pet's unique identifier
            start_date: Start date of range
            end_date: End date of range
            entry_type: Optional filter by entry type
            
        Returns:
            List of journal entries
            
        Raises:
            HTTPException: If pet ID is invalid
        """
        try:
            pet_uuid = uuid.UUID(pet_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid pet_id format: {pet_id}"
            )
        
        try:
            entries = self.pet_journal_service.get_journal_entries_by_date_range(
                pet_uuid, start_date, end_date, entry_type
            )
            
            return PetJournalListResponse(
                entries=[PetJournalResponse.model_validate(e) for e in entries],
                total=len(entries)
            )
        except Exception as e:
            logger.exception("Error retrieving journal entries by date range")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve journal entries"
            )
    
    def update_journal_entry(
        self,
        entry_id: str,
        update_data: PetJournalUpdate,
        user_id: int
    ) -> PetJournalResponse:
        """
        Update a journal entry.
        
        Args:
            entry_id: Journal entry unique identifier
            update_data: Update data
            user_id: ID of the authenticated user
            
        Returns:
            Updated journal entry response
            
        Raises:
            HTTPException: If update fails
        """
        try:
            entry_uuid = uuid.UUID(entry_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid entry_id format: {entry_id}"
            )
        
        try:
            updated_entry = self.pet_journal_service.update_journal_entry(
                entry_uuid, update_data, user_id
            )
            if not updated_entry:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Journal entry with ID {entry_id} not found"
                )
            
            logger.info("Journal entry updated", extra={"entry_id": entry_id})
            return PetJournalResponse.model_validate(updated_entry)
        except ValueError as e:
            logger.warning("Journal entry update failed", extra={"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Unexpected error updating journal entry")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update journal entry"
            )
    
    def delete_journal_entry(self, entry_id: str, user_id: int) -> dict:
        """
        Delete a journal entry.
        
        Args:
            entry_id: Journal entry unique identifier
            user_id: ID of the authenticated user
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If deletion fails
        """
        try:
            entry_uuid = uuid.UUID(entry_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid entry_id format: {entry_id}"
            )
        
        try:
            success = self.pet_journal_service.delete_journal_entry(entry_uuid, user_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Journal entry with ID {entry_id} not found"
                )
            
            logger.info("Journal entry deleted", extra={"entry_id": entry_id})
            return {"message": "Journal entry deleted successfully"}
        except ValueError as e:
            logger.warning("Journal entry deletion failed", extra={"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Unexpected error deleting journal entry")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete journal entry"
            )

